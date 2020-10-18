#!/usr/bin/env python3

import requests

def main():
  print(requests.get("http://127.0.0.1:53075"))

if __name__ == "__main__":
  main()