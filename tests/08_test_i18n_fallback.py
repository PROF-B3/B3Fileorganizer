import unittest
import sys
import os
import json
from pathlib import Path
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestI18nFallback(unittest.TestCase):
    def test_missing_key_adds_placeholder(self):
        from b3fileorganizer.utils import i18n
        test_key = 'test_missing_prompt_key'
        # Remove key if it exists
        lang_file = Path('b3fileorganizer/i18n/en.json')
        with open(lang_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if test_key in data:
            del data[test_key]
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        # Call tr to trigger fallback
        result = i18n.tr(test_key)
        self.assertIn('[MISSING:', result)
        # Wait briefly to ensure file system flush
        time.sleep(0.1)
        # Reload the language to ensure the in-memory cache is in sync
        i18n.load_language('en')
        with open(lang_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertIn(test_key, data)
        self.assertIn('[MISSING:', data[test_key])

if __name__ == '__main__':
    unittest.main() 