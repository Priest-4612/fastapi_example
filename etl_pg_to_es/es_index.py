import json

ES_SETTINGS = {
    'index': {
        'refresh_interval': '1s',
        'number_of_shards': '1',
        'provided_name': 'movies',
        'creation_date': '1645717374283',
        'analysis': {
            'filter': {
                'russian_stemmer': {
                    'type': 'stemmer',
                    'language': 'russian',
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
                    'type': 'stop',
                    'stopwords': '_russian_',
                },
                'english_stop': {
                    'type': 'stop',
                    'stopwords': '_english_',
                },
            },
            'analyzer': {
                'ru_en': {
                    'filter': [
                        'lowercase',
                        'english_stop',
                        'english_stemmer',
                        'english_possessive_stemmer',
                        'russian_stop',
                        'russian_stemmer',
                    ],
                    'tokenizer': 'standard',
                },
            },
        },
        'number_of_replicas': '1',
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

ES_PROPERTIES_NESTED = {
    'type': 'nested',
    'dynamic': 'strict',
    'properties': {
        'id': ES_PROPERTIES_KEYWORD,
        'name': ES_PROPERTIES_TEXT_RU_EN,
    },
}

INDEX_MOVIES_SETTINGS_ELASTIC = {
    'settings': ES_SETTINGS,
    'index': 'movies',
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
            'genres': ES_PROPERTIES_NESTED,
            'actors': ES_PROPERTIES_NESTED,
            'directors': ES_PROPERTIES_NESTED,
            'writers': ES_PROPERTIES_NESTED,
        },
    },
}

INDEX_PERSONS_SETTINGS_ELASTIC = {
    'settings': ES_SETTINGS,
    'index': 'persons',
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'id': ES_PROPERTIES_KEYWORD,
            'full_name': {
                **ES_PROPERTIES_TEXT_RU_EN,
                **ES_PROPERTIES_RAW,
            },
            'role': ES_PROPERTIES_KEYWORD,
            'film_ids': ES_PROPERTIES_KEYWORD,
        },
    },
}

INDEX_GENRES_SETTINGS_ELASTIC = {
    'settings': ES_SETTINGS,
    'index': 'genres',
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
    'FILM_INDEX': {
        'name': 'movies',
        'json': json.dumps(INDEX_MOVIES_SETTINGS_ELASTIC),
    },
    'GENRE_INDEX': {
        'name': 'genres',
        'json': json.dumps(INDEX_GENRES_SETTINGS_ELASTIC),
    },
    'PERSON_INDEX': {
        'name': 'persons',
        'json': json.dumps(INDEX_PERSONS_SETTINGS_ELASTIC),
    },
}


CINEMA_INDEX_BODY = """
{
  "settings": {
    "index": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "refresh_interval": "1s",
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
        },
        "english_stemmer": {
          "type": "stemmer",
          "language": "english"
        },
        "english_possessive_stemmer": {
          "type": "stemmer",
          "language": "possessive_english"
        },
        "russian_stop": {
          "type":       "stop",
          "stopwords":  "_russian_"
        },
        "russian_stemmer": {
          "type": "stemmer",
          "language": "russian"
        }
      },
      "analyzer": {
        "ru_en": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "english_stop",
            "english_stemmer",
            "english_possessive_stemmer",
            "russian_stop",
            "russian_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "id": {
        "type": "keyword"
      },
      "imdb_rating": {
        "type": "float"
      },
      "imdb_tconst": {
        "type": "keyword"
      },
      "filmtype": {
        "type": "keyword"
      },
      "genre": {
        "type": "keyword"
      },
      "title": {
        "type": "text",
        "analyzer": "ru_en",
        "fields": {
          "raw": {
            "type":  "keyword"
          }
        }
      },
      "description": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "directors_names": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "actors_names": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "writers_names": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "directors": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      },
      "actors": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      },
      "writers": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      }
    }
  }
}
"""
