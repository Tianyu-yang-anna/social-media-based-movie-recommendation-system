import json

di = {
    
}

with open("./credentials/credentials.json", "w") as f:
    json.dump(di, f)