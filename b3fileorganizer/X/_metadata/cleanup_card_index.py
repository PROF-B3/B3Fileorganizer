import json
from pathlib import Path

CARD_INDEX_PATH = Path(__file__).parent / "card_index.json"

with open(CARD_INDEX_PATH, 'r', encoding='utf-8') as f:
    card_index = json.load(f)

changed = False
for card_id, card in card_index.items():
    if 'tags' not in card or not isinstance(card['tags'], list):
        card['tags'] = []
        changed = True
    if 'cross_references' not in card or not isinstance(card['cross_references'], list):
        card['cross_references'] = []
        changed = True

if changed:
    with open(CARD_INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(card_index, f, indent=2, ensure_ascii=False)
    print("✅ card_index.json cleaned: all cards have 'tags' and 'cross_references' as lists.")
else:
    print("No changes needed: all cards already have 'tags' and 'cross_references' as lists.") 