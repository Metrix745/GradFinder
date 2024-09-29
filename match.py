from elasticsearch import Elasticsearch, helpers, exceptions
from urllib.request import urlopen
from getpass import getpass
import json
import time
import os


es = Elasticsearch(
    cloud_id="hackumbc204:dXMtZWFzdDQuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJDliYzU5ZGM5NTZmOTQ2YWRiY2E2Mjk5OWY2MDgzNWU3JDg4MWJmODc0OWY1MjQwYWE4YzYyMTFmYjAyNzlkMWRm",
    api_key="T0JTMFBKSUJHSk9vRERQemM3MFo6M2tvOUV1SWFUMWVIc3lsc0Y0ZkhRdw==   "
    
)
print(es.info())

try:
    es.ml.delete_trained_model(model_id=".elser_model_2", force=True)
    print("Model deleted successfully, We will proceed with creating one")
except exceptions.NotFoundError:
    print("Model doesn't exist, but We will proceed with creating one")

# Creates the ELSER model configuration. Automatically downloads the model if it doesn't exist.
es.ml.put_trained_model(model_id=".elser_model_2", input={"field_names": ["text_field"]})

while True:
    status = es.ml.get_trained_models(
        model_id=".elser_model_2", include="definition_status",
    )

    if status["trained_model_configs"][0]["fully_defined"]:
        print("ELSER Model is downloaded and ready to be deployed.")
        break
    else:
        print("ELSER Model is downloaded but not ready to be deployed.")
    time.sleep(5)


# Start trained model deployment if not already deployed
es.ml.start_trained_model_deployment(
    model_id=".elser_model_2", number_of_allocations=1, wait_for="starting"
)

while True:
    status = es.ml.get_trained_models_stats(
        model_id=".elser_model_2",
    )
    if status["trained_model_stats"][0]["deployment_stats"]["state"] == "started":
        print("ELSER Model has been successfully deployed.")
        break
    else:
        print("ELSER Model is currently being deployed.")
    time.sleep(5)

es.ingest.put_pipeline(
    id="elser-ingest-pipeline",
    description="Ingest pipeline for ELSER",
    processors=[
        {
            "inference": {
                "model_id": ".elser_model_2",
                "input_output": [
                    {"input_field": "description", "output_field": "description_embedding"}
                ],
            }
        }
    ],
)

mappings = {
        "properties": {
            "id" : {"type":"text"}}
}
mappings["properties"]["description_embedding"] = {"type": "sparse_vector"}
mappings["properties"]["description"] = {"type":"text"}


es.indices.delete(index="profs", ignore_unavailable=True)
try:
    es.indices.create(index="profs",settings={"index": {"default_pipeline": "elser-ingest-pipeline"}}, mappings=mappings)
except exceptions.BadRequestError:
    # proceed
    print()

dir = "prof_jsons"

i = 0
for file in os.listdir(dir):
    print("hi")
    with open(os.path.join(dir,file)) as f:
        data = json.load(f)
        data["description"] = str(data["description"])
        es.index(index="profs",id=i,document=data)
    i = i+1

response = es.search(
    index="profs",
    size=1,
    query={
        "text_expansion": {
            "description_embedding": {
                "model_id": ".elser_model_2",
                "model_text": "computer vision",
            }
        }
    },
)

print(response.body)
