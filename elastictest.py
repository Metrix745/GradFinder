from elasticsearch import Elasticsearch


es = Elasticsearch(
    cloud_id="hackumbc204:dXMtZWFzdDQuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJDliYzU5ZGM5NTZmOTQ2YWRiY2E2Mjk5OWY2MDgzNWU3JDg4MWJmODc0OWY1MjQwYWE4YzYyMTFmYjAyNzlkMWRm",
    api_key="T0JTMFBKSUJHSk9vRERQemM3MFo6M2tvOUV1SWFUMWVIc3lsc0Y0ZkhRdw==   "
    
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
    
    