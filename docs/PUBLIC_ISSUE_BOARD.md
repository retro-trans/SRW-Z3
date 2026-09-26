# Public issue board sample

## Issue-list labels (2026-09-06)

Version 7 shows label badges under each issue title, with workflow state kept
separate. Data comes directly from the fixed Linear project; only label names
are public. Label pagination validates project membership, rejects cursor loops
and fails closed instead of serving a partial label set. Badges wrap, use 14px
text, and render as escaped React text. No labels or issue statuses were mutated.
Regression tests and production build passed; public API verified 43 issues,
23 with labels, and an existing screenshot still loads. User approved public
publishing; audience and secret revision 1 unchanged.

- Source: `8a24239f0dcbdfcbc3ce0602b6bc80ea281fa261`.
- Version: `appgprj_6a9ccf15d0d481918083784303671c92~appgver_49762eb12eb08191a00ac0f4ca27cf0c`.
- Deployment: `appgdep_6a9d1f73109c81918f828ef3b13ab6cc`, succeeded.

## Screenshot import completed (2026-09-06)

After the user signed into GitHub, retrieved fresh image links from each rendered
issue page, uploaded all 37 original screenshot files into Linear, and verified
uploaded bytes against the originals. Replaced pending notes and source links
with actual image Markdown in report descriptions. Linear normalizes ordinary
links to `(<url>)`; importer now accepts that form and only embeds byte-verified
upload destinations. All 40 images in Linear pass the audit: 37 report images,
two imported comment images and the existing test comment image. No remaining
GitHub screenshot links or pending notes. Original issue text/status/comments
preserved. No website rebuild, GitHub mutation or game change.

`work/linear-import/verify.mjs` now additionally checks each report screenshot is
an embed and public `imageCount` matches the Linear description, so a mere link
cannot pass. `image-audit.json` records all 40 URLs returning HTTP 200.
Final verification passed for all 43 public issue pages, nine comments and 40
public image responses, with zero pending images. RET-16 was also visually
checked in the browser: the original Get Result screenshot is displayed in the
report's Screenshots section.
The partial-import notes below are historical; the GitHub-access blocker is resolved.

## All GitHub issues imported (2026-09-06)

User authorized importing all reports and repairing images in Linear. Source
repository `retro-trans/SRW-Z3` has 41 issues (#2–#42). Forty new Linear issues
were created (RET-8–RET-47); GitHub #39 reuses RET-5. RET-6 and RET-7 test issues
were preserved. Public board lists 43 issues. All 8 GitHub comments were copied
with original dates; existing RET-5 test comment remains (9 total).
Open GitHub reports remain Backlog. Closed/not-planned #2–#5 map to Canceled;
#38 maps to Done. #8's comment says duplicate but no target is given, so it maps
to Canceled with that explanation in the description (Linear rejects creation
in Duplicate state without the relationship). Source needs-verification and
help wanted labels retained. No GitHub changes, game fixes or extra imports.

Tooling and private snapshots: `work/linear-import/`. Importer defaults to
read-only dry-run, uses stable UUIDs and exact source-number matching (not URL
prefixes: #3 must not match #39), and retains a migration checkpoint.
Comment images on GitHub #35/#36 were manually uploaded to Linear using signed
source URLs from GitHub rendered comments and byte-verified. Together with the
existing test image, three images work. **37 original report images remain
blocked by private GitHub access.** Linear automatically rewrote their Markdown
URLs into uploads.linear.app URLs but did not fetch the underlying bytes; all
37 returned 404. They are marked pending with original source links preserved,
instead of leaving broken image embeds. RET-5's description is no longer called
a single sample import; its triage and user comment are preserved.

Next: ask the user to sign in to GitHub in the existing in-app tab or supply the
37 originals. Retrieve each original image, upload via fileUpload + PUT, verify
bytes from uploads.linear.app, then replace the pending note/source link with
actual Markdown image. Do not trust URL rewriting as proof that a file exists.
No site rebuild is required for Linear content updates; reload after the
60-second cache expires. `verify.mjs` requires every image to work and currently
fails appropriately; `image-audit.json` records exactly which images failed.

## Project issue-list update (2026-09-06)

The user requested an all-issues page. Public scope now covers the configured
SRW Z3 Linear project, not the rest of the workspace. Homepage `/` lists titles,
identifiers, statuses and update dates, sorted newest-updated first. `/issue?issue=RET-5`
is the report view with existing comments/screenshots and a back-to-list link.
`/api/issues` reads every project issue page, including archived issues. Each
detail/image request must match a member of this fixed project's issue list;
the detail query rechecks project membership before returning any data.
No arbitrary GraphQL, upstream URLs, author account fields or mutations.

Both issue-list and bounded per-issue caches expire after 60 seconds. Reload to
fetch new issues. Linear currently contains only RET-5 in this project; no extra
issues were invented or imported. Build and tests passed for multiple issue
pages, multiple detail routes, cross-project rejection, independent caches,
empty/error states, comment pagination and image proxying. Actual local list
matched Linear; original comment and image remain available.

- Source: `857dc590fa7fe426c197024377c76929b15c8ffe`.
- Version 6: `appgprj_6a9ccf15d0d481918083784303671c92~appgver_3b2c82bad85c8191add19799601e92a3`.
- Deployment: `appgdep_6a9cf197be2481918d122e827f46588c`, succeeded with environment revision 1.
- Anonymous production checks passed: list and detail pages/API HTTP 200;
  actual list matched RET-5's title; comment/screenshot retained; unrelated
  issue identifier returned HTTP 404. Public audience unchanged.

## All comments update (2026-09-06)

User explicitly approved all comments on RET-5 for public display. The Worker
now reads every comments page, checks issue/project on each response, and fails
safely instead of returning a partial list on pagination failure. Comments are
oldest-first, with body, created/edited dates and Linear-hosted screenshots.
No author account fields or internal comment IDs are exposed. Comment text is
rendered as escaped plain text; attached Linear image Markdown becomes a proxied
image. Other Markdown remains plain text. No new public write endpoint.

Local API verified the real comment "Hello, 1234, test image" and its 686425-byte
PNG attachment. Build, secret scan, multi-page/empty-comment/scope/image/failure
tests passed. Cache remains 60 seconds; reload is needed to fetch new comments.
No automatic polling, Discord integration, extra issues, or Linear mutations.

- Source: `2b9739b10cd0577975caeb512d9b4fb474a6fc81`.
- Version 5: `appgprj_6a9ccf15d0d481918083784303671c92~appgver_7b4a50b22fe8819189a32dce72f246a0`.
- Deployment: `appgdep_6a9cee18103c819184698d2e64165935`, succeeded with secret environment revision 1.
- Anonymous production verification: page/API HTTP 200; actual comment body/date
  matched Linear; screenshot HTTP 200, image/png, 686425 bytes. No credential
  exposed in response. Existing public audience unchanged.

## Live connection update (2026-09-06)

The user supplied `Linear_API.txt`; verified the credential with a read-only
Linear GraphQL query. Stored it as the Sites secret `LINEAR_API_KEY` (environment
revision 1). Added the local filename to the game repository's .gitignore; it
was not tracked and remains on disk. Do not print or commit its contents.

Version 2 replaces manually authored content with /api/issue and a custom
dependency-free Worker. Only issue UUID `f3c22e93-ff29-4887-b778-a500759c4639`
(RET-5) from project UUID `dd1aed47-a0c8-4751-80cd-65559f1255f8` can be queried.
No mutations. Site remains public. Cache is 60 seconds; reload to get updates.
Title/status/description come from Linear. Public description excludes private
links and reporter identifiers. The no-fix suggestions already in Linear remain
visible verbatim; the page adds no proposed wording of its own.

Removed earlier substitute screenshot from site copy. RET-5 currently has only a
private GitHub link; imageCount is 0. Image endpoint permits only raster images
linked in this issue's Markdown on uploads.linear.app, with server-only auth and
no redirects. No generic URL proxy or client-selected issue IDs are accepted.

Build and mocked security/scope/failure tests pass. Local API verified against
actual Linear data; no API secret present in any build artifact. Generated
Vinext server intermediates are removed from the output: only static frontend
and the dependency-free custom Worker are deployed. No server actions.

- Source: `0d00e37259f53715d6c0056132793c0b614f7916`.
- Version 2: `appgprj_6a9ccf15d0d481918083784303671c92~appgver_3a5faf8edf8081919547161cd4d71856`.
- Deployment: `appgdep_6a9ce686fbac81919492ffc53dc53e88`.

Version 2 deployed but the public API returned 503 (local API succeeded).
Version 3 removes the dispatch Cache API dependency, using a 60-second ephemeral
per-isolate cache, and adds safe failure-class logging. Source
`b5589eda9ce62d72b567285f0bd5b9f759765126`; version
`appgprj_6a9ccf15d0d481918083784303671c92~appgver_456495da9824819193115310d38ca784`;
deployment `appgdep_6a9ce7ad12308191b7d3d2a8c76900dd`.

**Verified live fix, version 4:** Cloudflare Worker fetch required manual
redirect handling instead of `redirect: error`. Manual redirects are not
followed; non-200 upstream responses are rejected. V4 anonymous /api/issue
returned HTTP 200 with RET-5's actual title, Backlog status, imageCount 0.
Deployment succeeded with secret environment revision 1. Source
`561d352ad1119c9fa7eac509ad4a23c42b03f818`; version
`appgprj_6a9ccf15d0d481918083784303671c92~appgver_96ecf68f13588191b9ec755d6252be97`;
deployment `appgdep_6a9ce89146b08191971e167670415e09`.

## Version 1 history (superseded)

The user approved a separate read-only public page, not a public Linear link.
Only one report is in scope: RET-5, copied from GitHub issue #39. Status remains
Backlog; terminology not approved and no game fix applied. GitHub unchanged.

- Site checkout: `work/public-issue-board` (isolated Git repository).
- Sites project: `appgprj_6a9ccf15d0d481918083784303671c92`.
- Live URL: https://srw-z3-issue-board.binhlt0402.chatgpt.site
- Deployment succeeded. Anonymous Node fetch (no cookies/auth) returned HTTP 200
  for the actual report HTML and image/png screenshot. Public access revision 2.
- Source commit: `494d22de0bbbadd5f1ef7ee0c05336cbdf3d58f9`.
- Version 1: `appgprj_6a9ccf15d0d481918083784303671c92~appgver_1c9db05a83e481919cd40e9483f647ad`.
- Deployment: `appgdep_6a9cd2a228888191b0c285750c4ae70b`.

The screenshot is a local user-supplied earlier Japanese attack menu, clearly
captioned, not the inaccessible original GitHub attachment. No public Discord
IDs, private links, credentials or game binaries are included. User explicitly
said to omit the Discord link for now. No live synchronization, Discord bot,
public comments, or editing exists. Broader migration is not authorized yet.

Build passed with npm run build; the wrapper allows successful native worker
shutdown on Windows rather than Vinext's abrupt process.exit(0), which crashed.
Package using the Sites helper with MSYS /e/... paths, not E:/... archive paths.
Only static dist/client is published. Full starter lint has pre-existing errors
in unused vendored components; app also has the no-img-element optimization
warning (intentional full-size local screenshot, no server image optimization).
Pinned build/server dependency audit advisories are documented in site README;
no vulnerable server endpoints or development server are deployed.

Reuse this project and its manifest for future work. Never create a duplicate.
Read Sites skills before building or hosting. Obtain a fresh short-lived source
write credential when necessary; never store tokens in files or Git config.
