import aiohttp
import asyncio
import json
import sys

def load_standard(filename):
    with open(filename, 'r') as f:
        return json.load(f)

async def make_request(session, test):
    url = test["url"]
    method = test["method"].upper()
    headers = test.get("headers", {})
    payload = test.get("body", {})
    query_params = test.get("query_params", {})
    weight = test.get("weight", 0)

    async with session.request(method, url, headers=headers, json=payload, params=query_params) as response:
        expected_status = test["response"]["status"]
        if response.status != expected_status:
            print(f"Score: 0\nReason: Expected status code {expected_status}, but got {response.status}")
            return 0

        try:
            data = await response.json()
        except aiohttp.ContentTypeError:
            print("Score: 0\nReason: Response is not a valid JSON")
            return 0

        expected_body = test["response"]["body"]
        for key, value in expected_body.items():
            if data.get(key) != value:
                print(f"Score: 0\nReason: Expected '{key}' to be '{value}', but got '{data.get(key)}'")
                return 0

        return weight

async def test_api(test):
    count = test.get("count", 1)
    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, test) for _ in range(count)]
        results = await asyncio.gather(*tasks)
    return sum(results)/count

async def main():
    if len(sys.argv) != 2:
        print("Usage: api_test.py <standard.json>")
        sys.exit(1)

    standard_file = sys.argv[1]
    standard = load_standard(standard_file)
    total_score = 0
    max_score = 0

    for test in standard["tests"]:
        max_score += test.get("weight", 0)
        total_score += await test_api(test)

    print(f"Total Score: {total_score}/{max_score}")

if __name__ == "__main__":
    asyncio.run(main())