#!/usr/bin/env python3

import requests
import json
from pprint import pprint

def main():
  pprint(json.loads(requests.get("http://127.0.0.1:53075/players/").content.decode()))
  pprint(json.loads(requests.get("http://127.0.0.1:53075/teams/").content.decode()))
  pprint(json.loads(requests.get("http://127.0.0.1:53075/fixtures/").content.decode()))


if __name__ == "__main__":
  main()