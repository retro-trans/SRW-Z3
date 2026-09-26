"""Original Japanese voice cast, romanized consistently for Library ACTR fields."""
import json
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / 'translation/library_voice_actors.json'


def load_catalog():
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate voice actor: ' + key)
            if not value or not value.isascii() or value.strip() != value:
                raise ValueError('Invalid romanized voice actor: ' + repr(value))
            result[key] = value
        return result
    return json.loads(CATALOG.read_text(encoding='utf-8'), object_pairs_hook=unique)


def romanize(text, catalog):
    # Fail closed: new/changed cast credits must be reviewed, not guessed.
    if text not in catalog:
        raise ValueError('Unmapped Library voice actor: ' + repr(text))
    return catalog[text]
