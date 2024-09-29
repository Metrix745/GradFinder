from elasticsearch import Elasticsearch, helpers, exceptions
from urllib.request import urlopen
from getpass import getpass
import json
import time
import os


es = Elasticsearch(
    cloud_id="8bea67a8bbf24d56ac04d03a52055394:dXMtZWFzdDQuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJGU5NmRhMDc2OWEzNTRmMmE4MjI3MGQ4YWE0MmZlZGQxJDViNDdhYWQ5NDBiNDRiMjliNWMwMWYxYTBkMDJmMjZh",
    api_key="Z2dwcFBKSUJkcE5vX0NmS3Bfc2w6d196TF85b1lSQmFfSFRPTV9zUjNyZw=="
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
                    {"input_field": "desc0", "output_field": "plot_embedding"}
                ],
            }
        }
    ],
)

mappings = {
        "properties": {
            "id" : {"type":"text"}}
}
mappings["plot_embedding"] = {"type": "sparse_vector"}
mappings["descs"] = {"type":"text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},}


es.indices.delete(index="profs", ignore_unavailable=True)
try:
    es.indices.create(index="profs",settings={"index": {"default_pipeline": "elser-ingest-pipeline"}}, mappings=mappings)
except exceptions.BadRequestError:
    # proceed
    print()

dir = "prof_jsons"
for file in os.listdir(dir):
    print("hi")
    with open(os.path.join(dir,file)) as f:
        data = json.load(f)
        es.index(index="profs",id=1,document=data)

response = es.search(
    index="profs",
    size=1,
    query={
        "text_expansion": {
            "plot_embedding": {
                "model_id": ".elser_model_2",
                "model_text": "computer vision",
            }
        }
    },
)

print(response.body)
