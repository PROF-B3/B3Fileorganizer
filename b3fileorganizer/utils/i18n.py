import json
import os
from pathlib import Path

I18N_DIR = Path(__file__).parent.parent / "i18n"
DEFAULT_LANG = "en"
_current_lang = DEFAULT_LANG
_translations = {}


def load_language(lang):
    global _translations, _current_lang
    lang_file = I18N_DIR / f"{lang}.json"
    if not lang_file.exists():
        lang_file = I18N_DIR / f"{DEFAULT_LANG}.json"
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            _translations = json.load(f)
        _current_lang = lang
    except Exception:
        _translations = {}
        _current_lang = DEFAULT_LANG


def tr(key):
    # Try current language, then fallback to English
    if key in _translations:
        return _translations[key]
    # Log missing key
    lang_file = I18N_DIR / f"{_current_lang}.json"
    try:
        # Load current translations
        with open(lang_file, 'r', encoding='utf-8') as f:
            lang_trans = json.load(f)
    except Exception:
        lang_trans = {}
    if key not in lang_trans:
        placeholder = f"[MISSING: {key}]"
        lang_trans[key] = placeholder
        _translations[key] = placeholder  # Update in-memory cache
        try:
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(lang_trans, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
        return placeholder
    if _current_lang != DEFAULT_LANG:
        try:
            with open(I18N_DIR / f"{DEFAULT_LANG}.json", 'r', encoding='utf-8') as f:
                en_trans = json.load(f)
            return en_trans.get(key, key)
        except Exception:
            return key
    return key


def set_language(lang):
    load_language(lang)


def get_current_language():
    return _current_lang

# Load default language at import
default_loaded = False
if not default_loaded:
    load_language(DEFAULT_LANG)
    default_loaded = True 