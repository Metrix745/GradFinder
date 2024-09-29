import json
import os

dir = "prof_jsons"
for file in os.listdir(dir):
    print("hi")
    with open(os.path.join(dir,file)) as f:
        data = json.load(f)
        print(data)