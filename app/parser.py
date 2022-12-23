import json
from functools import lru_cache

from .logger import get_logger
from .config import Settings


@lru_cache()
def get_settings():
    return Settings()

logger = get_logger(__name__, get_settings())


def parse_to_json(data):
    response = []
    logger.info("Parsing output from dictionary {0}".format(data))
    for row in data:
        logger.info("Itering row {0}".format(row))
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
        logger.info("Appending row in response model. Record - {0}".format(record))
        response.append(record)
    return response
