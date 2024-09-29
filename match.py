from elasticsearch import Elasticsearch
import json



es = Elasticsearch("http://localhost:9200")

mappings = {
        "properties": {
            "id" : {"type":"text"}}
}
for i in range(20):
    currstring = f"desc{i}"
    mappings["properties"][currstring] = {"type":"text","analyzer":"english"}

es.indices.create(index="profs", mappings=mappings)


with open("./profjsons/i3uLKmkAAAAJ.json") as file:
    data = json.load(file)
    es.index(index="profs",id=1,document=data)


resp = es.search(
    index="profs",
    query={
            "bool": {
                "must": {
                    "match_phrase": {
                        "description": "Universal Declaration of the Rights of Wetlands",
                    }
                },
            },
        },
)

print(resp.body)