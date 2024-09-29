from elasticsearch import Elasticsearch


es = Elasticsearch(
    cloud_id="hackumbc204:dXMtZWFzdDQuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJDliYzU5ZGM5NTZmOTQ2YWRiY2E2Mjk5OWY2MDgzNWU3JDg4MWJmODc0OWY1MjQwYWE4YzYyMTFmYjAyNzlkMWRm",
    api_key="T0JTMFBKSUJHSk9vRERQemM3MFo6M2tvOUV1SWFUMWVIc3lsc0Y0ZkhRdw==   "
    
)

doc_count = es.count(index="profs")['count']
print(f"Total documents indexed: {doc_count}")
input()

ingest_pipeline = es.ingest.get_pipeline(id="elser-ingest-pipeline")
print(ingest_pipeline)
input()

indexed_doc = es.get(index="profs", id=1)
print(indexed_doc)
input()

response = es.search(
    index="profs",
    size=1,
    query={
        "text_expansion": {
            "plot_embedding": {
                "model_id": ".elser_model_2",
                "model_text": "visual",
            }
        }
    },
)
print(response)