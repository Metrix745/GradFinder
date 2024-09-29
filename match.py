from elasticsearch import Elasticsearch
import pandas as pd



es = Elasticsearch("http://localhost:9200")
es.info().body


mappings = {
        "properties": {
            "name": {"type": "text", "analyzer": "english"},
            "department": {"type": "text", "analyzer": "standard"},
            "director": {"type": "text", "analyzer": "standard"},
            "cast": {"type": "text", "analyzer": "standard"},
            "genre": {"type": "text", "analyzer": "standard"},
            "plot": {"type": "text", "analyzer": "english"},
            "year": {"type": "integer"},
            "scholar_page": {"type": "keyword"}
    }
}

es.indices.create(index="movies", mappings=mappings)