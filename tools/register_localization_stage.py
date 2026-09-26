"""Add a stage translated AFTER the migration to the shared catalog.

    python tools/register_localization_stage.py work/tr/STG0075/review/stage0075_03.json [..] [--write]

The 2026-09-14 migration imported all 475 legacy files in one pass and must
not be rerun -- rerunning it renumbers the catalog. Every stage translated
from now on still needs the four rows that migration would have written:

    localization/messages/<group>.json          IDs, Japanese source, context
    localization/locales/en/<group>.json        the English wording
    localization/manifest.json                  the group, in stage order
    platforms/ps3/localization/legacy.json      the compatibility template

and then the generated view `translation/<group>.json` plus its receipt in
`localization/compatibility.json`, which is exactly what `localization.py
sync` writes for a group that already exists. It cannot write a view for a
group that does not, because it reads the old file before rendering the new
one, so a first registration writes that pair here instead.

Input is a MERGED, CHECKED stage file -- the temporary review output of
merge_stage.py, never a canonical file. IDs are minted the way the migration
minted them (sha256 of the record's JSON pointer, not of its wording), so a
later edit to the English keeps the ID.

Additive only. An existing group, message file, locale file, binding, view or
receipt is an error, not an update: changing shipped English is an edit to
`localization/locales/en/<group>.json` by ID, not a re-registration.
"""
import argparse
import difflib
import hashlib
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import localization


def read(path):
    with io.open(path, encoding="utf-8") as stream:
        return json.load(stream)


def write_text(path, value):
    """Rewrite a control file without touching anybody else's line endings.

    These files are hand-edited by more than one person and at least one of
    them writes LF into a CRLF file, so a whole-file rewrite turns a
    three-line addition into a diff that also claims eight lines nobody
    touched. Unchanged lines keep the ending they had; an inserted line
    copies the ending of the line it follows, the same rule register_stage.py
    uses on the four stage tables.
    """
    wanted = localization.dump(value).splitlines(True)
    before = []
    if os.path.exists(path):       # a first registration writes new files too
        with io.open(path, "rb") as stream:
            before = stream.read().decode("utf-8").splitlines(True)
    ending = lambda line: line[len(line.rstrip("\r\n")):] or "\n"
    out, previous = [], "\r\n" if any(l.endswith("\r\n") for l in before) else os.linesep
    matcher = difflib.SequenceMatcher(
        None, [l.rstrip("\r\n") for l in before], [l.rstrip("\r\n") for l in wanted])
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        for offset, line in enumerate(wanted[j1:j2]):
            body = line.rstrip("\r\n")
            if tag == "equal":
                previous = ending(before[i1 + offset])
            out.append(body + previous)
    with io.open(path, "wb") as stream:
        stream.write("".join(out).encode("utf-8"))


def mid_of(group, index):
    identity = "/LINES/%d/en" % index
    return group + ":r_" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]


def plan(path):
    group = os.path.basename(path)[:-len(".json")]
    record = read(path)
    definitions, locale, lines = {}, {}, []
    for index, row in enumerate(record["LINES"]):
        english = row["en"]
        if not english:
            raise SystemExit("%s: record %d has no English" % (group, index))
        mid = mid_of(group, index)
        if mid in definitions:
            raise SystemExit("ID collision: " + mid)
        definitions[mid] = dict(
            source=row["jp"], kind="dialogue",
            context={key: row[key] for key in ("event", "n", "pid") if key in row},
            source_status="available",
            tokens=localization.TOKEN.findall(english),
            links=english.count("《"), link_closes=english.count("》"))
        # New wording, not copied from an earlier source: 'imported' would
        # claim these came over unchanged from the pre-migration files.
        locale[mid] = dict(text=english, status="translated")
        lines.append(dict(row, en={"$message": mid}))
    return group, record, definitions, locale, dict(record, LINES=lines)


def register(paths, write=False):
    manifest_path = os.path.join(ROOT, "localization", "manifest.json")
    legacy_path = os.path.join(ROOT, "platforms", "ps3", "localization", "legacy.json")
    receipt_path = os.path.join(ROOT, "localization", "compatibility.json")
    manifest, legacy, receipt = read(manifest_path), read(legacy_path), read(receipt_path)

    # Proof that rewriting these three does not reformat anybody else's rows.
    for path, value in ((manifest_path, manifest), (legacy_path, legacy),
                        (receipt_path, receipt)):
        # Read with newline translation, since write_text puts them back.
        with io.open(path, encoding="utf-8") as stream:
            if stream.read() != localization.dump(value):
                raise SystemExit("would reformat " + os.path.basename(path))

    pending = []
    for path in paths:
        group, record, definitions, locale, template = plan(path)
        view = "translation/%s.json" % group
        for existing, what in (
                (group in manifest["groups"], "group in manifest"),
                (view in legacy["documents"], "legacy binding"),
                (view in receipt["files"], "compatibility receipt"),
                (os.path.exists(os.path.join(ROOT, view)), view),
                (os.path.exists(os.path.join(ROOT, "localization", "messages", group + ".json")), "messages file"),
                (os.path.exists(os.path.join(ROOT, "localization", "locales", "en", group + ".json")), "locale file")):
            if existing:
                raise SystemExit("%s already registered (%s); edit by ID instead" % (group, what))

        # Round trip before anything is written: the view this group will
        # generate has to be the file that was checked, character for
        # character, or the English on screen is not the English approved.
        rendered = {"LINES": [dict(line, en=locale[line["en"]["$message"]]["text"])
                              for line in template["LINES"]]}
        if rendered != record:
            raise SystemExit(group + ": template does not round trip")

        # The group list is not globally sorted (the ui.* rows lead it), but
        # its stage block is. Keep that block in order and leave every other
        # row exactly where it is.
        groups = list(manifest["groups"])
        after = [i for i, name in enumerate(groups) if name.startswith("stage") and name < group]
        groups.insert(after[-1] + 1 if after else len(groups), group)
        manifest["groups"] = groups
        legacy["documents"][view] = dict(format="json", template=template)
        pending.append((group, view, definitions, locale, template))
        print("%-16s %5d records  %s" % (group, len(record["LINES"]), view))

    if not write:
        print("DRY RUN: %d groups would be registered" % len(pending))
        return 0

    written = []
    try:
        for group, view, definitions, locale, template in pending:
            for relative, value in (
                    ("localization/messages/%s.json" % group, {"schema": 1, "messages": definitions}),
                    ("localization/locales/en/%s.json" % group,
                     {"schema": 1, "language": "en", "messages": locale})):
                target = os.path.join(ROOT, relative)
                write_text(target, value)
                written.append(target)
            target = os.path.join(ROOT, view)
            # Byte-for-byte what sync would write on a later edit, so the
            # first change to this stage is a one-line diff and not a reflow.
            body = localization.dump({"LINES": [dict(line, en=locale[line["en"]["$message"]]["text"])
                                                for line in template["LINES"]]}).encode("utf-8")
            with io.open(target, "wb") as stream:
                stream.write(body)
            written.append(target)
            receipt["files"][view] = localization.sha(body)
        for path, value in ((manifest_path, manifest), (legacy_path, legacy),
                            (receipt_path, receipt)):
            write_text(path, value)
    except Exception:
        for target in written:
            os.remove(target)
        raise
    print("registered %d groups" % len(pending))
    return len(pending)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    register(args.files, args.write)


if __name__ == "__main__":
    main()
