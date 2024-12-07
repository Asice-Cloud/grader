import aiohttp
import asyncio
import json
import sys
from colorama import init,Fore,Style

init(autoreset=True)

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
            print(f"{Fore.RED}WRONG:Reason: Expected status code {expected_status}, but got {response.status}")
            return 0

        try:
            data = await response.json()
        except aiohttp.ContentTypeError:
            print(f"{Fore.RED}WRONG:Reason: Response is not a valid JSON")
            return 0

        expected_body = test["response"]["body"]
        if not compare_json(data, expected_body):
            print(f"{Fore.RED}WRONG:Reason: Response JSON does not match expected JSON")
            return 0

        return weight

def compare_json(actual,expected):
    if isinstance(expected, dict):
        for key, value in expected.items():
            if key not in actual or not compare_json(actual[key], value):
                return False
    elif isinstance(expected, list):
        if len(actual) != len(expected):
            return False
        for item_actual, item_expected in zip(actual, expected):
            if not compare_json(item_actual, item_expected):
                return False
    else:
        return actual == expected
    return True

async def test_api(test):
    print(f"{Fore.LIGHTGREEN_EX}Now testing",f"{Fore.LIGHTWHITE_EX}"+test["url"])
    count = test.get("count", 1)
    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, test) for _ in range(count)]
        results = await asyncio.gather(*tasks)
    re = sum(results)/count
    print(f"{Fore.LIGHTYELLOW_EX}Score: {re}\n")
    return re

async def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: api_test.py <standard.json>")
        sys.exit(1)

    standard_file = sys.argv[1]
    standard = load_standard(standard_file)
    total_score = 0
    max_score = 0
    

    for test in standard["tests"]:
        max_score += test.get("weight", 0)
        total_score += await test_api(test)

    print(f"\n{Fore.LIGHTMAGENTA_EX}Total Score: {total_score}/{max_score}")

    pe = total_score/max_score *100
    if pe<=50:
        print(f"{Fore.LIGHTBLUE_EX}percentage_value: "+f"{Fore.LIGHTRED_EX}{pe}")
    elif pe<=80:
        print(f"{Fore.LIGHTBLUE_EX}percentage_value: "+f"{Fore.LIGHTGREEN_EX}{pe}")
    else:
        print(f"{Fore.LIGHTBLUE_EX}percentage_value: "+f"{Fore.LIGHTMAGENTA_EX}{pe}")
if __name__ == "__main__":
    asyncio.run(main())