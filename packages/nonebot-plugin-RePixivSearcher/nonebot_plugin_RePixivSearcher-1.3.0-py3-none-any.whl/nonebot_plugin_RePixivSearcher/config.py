import json

def write(json_data: dict, json_name: str):
    with open(f'data/PixivSearcher/{json_name}.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def read(json_name: str):
    with open(f'data/PixivSearcher/{json_name}.json', 'r', encoding='utf-8') as f:
        return json.load(f)
