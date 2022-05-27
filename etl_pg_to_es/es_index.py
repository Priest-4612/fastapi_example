ES_SETTINGS = {
    'index': {
        'number_of_shards': 1,
        'number_of_replicas': 0,
    },
    'refresh_interval': '1s',
    'analysis': {
        'filter': {
            'english_stop': {
                'type':       'stop',
                'stopwords':  '_english_',
            },
            'english_stemmer': {
                'type': 'stemmer',
                'language': 'english',
            },
            'english_possessive_stemmer': {
                'type': 'stemmer',
                'language': 'possessive_english',
            },
            'russian_stop': {
                'type':       'stop',
                'stopwords':  '_russian_',
            },
            'russian_stemmer': {
                'type': 'stemmer',
                'language': 'russian',
            },
        },
        'analyzer': {
            'ru_en': {
                'tokenizer': 'standard',
                'filter': [
                    'lowercase',
                    'english_stop',
                    'english_stemmer',
                    'english_possessive_stemmer',
                    'russian_stop',
                    'russian_stemmer',
                ],
            },
        },
    },
}

ES_PROPERTIES_KEYWORD = {
    'type': 'keyword',
}

ES_PROPERTIES_RAW = {
    'fields': {
        'raw': ES_PROPERTIES_KEYWORD,
    },
}

ES_PROPERTIES_TEXT_RU_EN = {
    'type': 'text',
    'analyzer': 'ru_en',
}

ES_PROPERTIES_NESTED_PERSON = {
    'type': 'nested',
    'dynamic': 'strict',
    'properties': {
        'id': ES_PROPERTIES_KEYWORD,
        'name': ES_PROPERTIES_TEXT_RU_EN,
    },
}

ES_PROPERTIES_NESTED_GENRE = {
    'type': 'nested',
    'dynamic': 'strict',
    'properties': {
        'id': ES_PROPERTIES_KEYWORD,
        'name': ES_PROPERTIES_KEYWORD,
        'description': ES_PROPERTIES_TEXT_RU_EN,
    },
}

INDEX_MOVIES_SETTINGS_ELASTIC = {
    'settings': ES_SETTINGS,
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': ES_PROPERTIES_KEYWORD,
            'title': {
                **ES_PROPERTIES_TEXT_RU_EN,
                **ES_PROPERTIES_RAW,
            },
            'description': ES_PROPERTIES_TEXT_RU_EN,
            'imdb_rating': {'type': 'float'},
            'type': ES_PROPERTIES_TEXT_RU_EN,
            'genres_names': ES_PROPERTIES_TEXT_RU_EN,
            'actors_names': ES_PROPERTIES_TEXT_RU_EN,
            'directors_names': ES_PROPERTIES_TEXT_RU_EN,
            'writers_names': ES_PROPERTIES_TEXT_RU_EN,
            'genres': ES_PROPERTIES_NESTED_GENRE,
            'actors': ES_PROPERTIES_NESTED_PERSON,
            'directors': ES_PROPERTIES_NESTED_PERSON,
            'writers': ES_PROPERTIES_NESTED_PERSON,
        },
    },
}

INDEX_PERSONS_SETTINGS_ELASTIC = {
    'settings': ES_SETTINGS,
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': ES_PROPERTIES_KEYWORD,
            'name': {
                **ES_PROPERTIES_TEXT_RU_EN,
                **ES_PROPERTIES_RAW,
            },
            'role': ES_PROPERTIES_TEXT_RU_EN,
            'film_ids': ES_PROPERTIES_KEYWORD,
            'actor_film_ids': ES_PROPERTIES_KEYWORD,
            'director_film_ids': ES_PROPERTIES_KEYWORD,
            'writer_film_ids': ES_PROPERTIES_KEYWORD,
        },
    },
}

INDEX_GENRES_SETTINGS_ELASTIC = {
    'settings': ES_SETTINGS,
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': ES_PROPERTIES_KEYWORD,
            'name': ES_PROPERTIES_KEYWORD,
            'description': ES_PROPERTIES_TEXT_RU_EN,
        },
    },
}

ELASTIC_INDEX = {
    'movies': INDEX_MOVIES_SETTINGS_ELASTIC,
    'genres': INDEX_GENRES_SETTINGS_ELASTIC,
    'persons': INDEX_PERSONS_SETTINGS_ELASTIC,
}
