from elasticsearch import Elasticsearch



es = Elasticsearch("http://localhost:9200")


resp = es.search(
    index="profs",
    query={
            "bool": {
                "must": {
                    "match_phrase": {
                        "description": "Global Lakes and Wetlands Database",
                    }
                },
            },
        },
)
print(resp.body)
