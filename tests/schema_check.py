#!/usr/bin/env python3
import requests, sys, json
from extruct import extract
from tqdm import tqdm

urls_file = "tests/urls.txt"

def validate_jsonld(data, url):
	try:
		if "json-ld" not in data:
			print(f"[SKIP] No JSON-LD found on {url}")
			return False
		else:
			print(f"[OK] {len(data['json-ld'])} JSON-LD blocks found on {url}")
			return True
	except Exception as e:
		print(f"[ERROR] {url} => {e}")
		return False

def main():
	with open(urls_file, "r", encoding="utf-8") as f:
		urls = [line.strip() for line in f if line.strip()]

	errors = 0
	for url in tqdm(urls, desc="Checking schema.org JSON-LD"):
		try:
			html = requests.get(url, timeout=15).text
			data = extract(html, syntaxes=["json-ld"])
			if not validate_jsonld(data, url):
				errors += 1
		except Exception as e:
			print(f"[FAIL] {url} => {e}")
			errors += 1

	print(f"\n✅ Completed. {len(urls)} URLs checked, {errors} errors.\n")
	if errors > 0:
		sys.exit(1)

if __name__ == "__main__":
	main()
