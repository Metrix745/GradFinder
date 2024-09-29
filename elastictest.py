from elasticsearch import Elasticsearch


es = Elasticsearch(
    cloud_id="XXX",
    api_key="XXX"
    
)

response = es.search(
    index="profs",
    size=5,
    query={
        "text_expansion": {
            "description_embedding": {
                "model_id": ".elser_model_2",
                "model_text": "Theoretical Computer Science",
            }
        }
    },
)

# print(response["hits"]["hits"][0]['_source']['scholar_id'])
for hit in response['hits']['hits']:
    print(hit['_source']['scholar_id'])
    # print()
    
    