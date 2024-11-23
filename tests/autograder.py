import requests
import json
import sys

def load_standard(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def test_api(test):
    url = test["url"]
    method = test["method"]
    headers = test.get("headers", {})
    payload = test.get("body", {})
    query_params = test.get("query_params", {})
    weight = test.get("weight", 0)

    if method.upper() == "GET":
        response = requests.get(url, headers=headers, params=query_params)
    elif method.upper() == "POST":
        response = requests.post(url, json=payload, headers=headers, params=query_params)
    elif method.upper() == "PUT":
        response = requests.put(url, json=payload, headers=headers, params=query_params)
    elif method.upper() == "DELETE":
        response = requests.delete(url, json=payload, headers=headers, params=query_params)
    else:
        print(f"Unsupported HTTP method: {method}")
        return 0

    # status
    expected_status = test["response"]["status"]
    if response.status_code != expected_status:
        print(f"Score: 0\nReason: Expected status code {expected_status}, but got {response.status_code}")
        return 0

    # is JSON?
    try:
        data = response.json()
    except ValueError:
        print("Score: 0\nReason: Response is not a valid JSON")
        return 0

    # check response
    expected_body = test["response"]["body"]
    for key, value in expected_body.items():
        if key not in data or data[key] != value:
            print(f"Score: 0\nReason: Expected '{key}' to be '{value}', but got '{data.get(key)}'")
            return 0

    return weight

if __name__ == "__main__":
   
    standard = load_standard("./tests/standard.json")
    total_score = 0
    max_score = 0
    for test in standard["tests"]:
        max_score += test.get("weight", 0)
        total_score += test_api(test)

    print(f"Total Score: {total_score}/{max_score}")