import json

def parse_to_json(data):
    response = []
    for row in data:
        record = {}
        for key in row.keys():
            if row.__getitem__(key):
                if key in ['title', 'gutenberg_id', 'genre', 'language', 'subjects', 'bookshelves']:
                    record[key] = row.__getitem__(key)
                elif key == 'auth':
                    record[key] = json.loads(row.__getitem__(key))
                    continue
                elif isinstance(row.__getitem__(key), list):
                    sublist = []
                    for elem in row.__getitem__(key):
                        sublist.append(json.loads(elem))
                    record[key] = sublist
                else:
                    record[key] = row.__getitem__(key)
            else:
                record[key] = row.__getitem__(key)
        response.append(record)
    return response
