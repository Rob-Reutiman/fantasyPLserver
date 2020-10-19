#!/usr/bin/env python3

import requests
import json
from pprint import pprint

def main():

  # Login to user that doesn't exist
  r = json.loads(requests.post("http://127.0.0.1:53075/auth/", data = json.dumps({"username": "pat", "password": "bald"})).content.decode())
  assert(r["result"] == "error")

  # Create user and login with wrong, right password
  r = json.loads(requests.post("http://127.0.0.1:53075/create/", data = json.dumps({"username": "robo", "password": "jeems"})).content.decode())
  assert(r["result"] == "success")
  r = json.loads(requests.post("http://127.0.0.1:53075/auth/", data = json.dumps({"username": "robo", "password": "bald"})).content.decode())
  assert(r["result"] == "error")
  r = json.loads(requests.post("http://127.0.0.1:53075/auth/", data = json.dumps({"username": "robo", "password": "jeems"})).content.decode())
  assert(r["result"] == "success")

  # Test data retrieval
  r = json.loads(requests.post("http://127.0.0.1:53075/players/", data = json.dumps({"username": "robo", "password": "jeems"})).content.decode())
  assert(r["result"] == "success")
  r = json.loads(requests.post("http://127.0.0.1:53075/teams/", data = json.dumps({"username": "robo", "password": "jeems"})).content.decode())
  assert(r["result"] == "success")
  r = json.loads(requests.post("http://127.0.0.1:53075/fixtures/", data = json.dumps({"username": "robo", "password": "jeems"})).content.decode())
  assert(r["result"] == "success")

if __name__ == "__main__":
  main()
