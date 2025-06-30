import requests

def run():
    res = requests.post("http://localhost:8000/agents/sales", json={"n": 1})
    print(res.json())

if __name__ == "__main__":
    run()