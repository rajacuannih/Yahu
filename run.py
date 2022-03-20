#!/usr/bin/env python

import os, uuid, pause, json, sys
from subprocess import call
from faker import Faker

def gen_uname(full_name):
	a = full_name.split()
	b = str(uuid.uuid4()).split("-")[-1].join([v for v in a])
	return b

if __name__=="__main__":
	fake = Faker()
	a = open('n.txt').read().splitlines()
	i = 0
	for b in a:
		try:
			i+=1
			fake_name = fake.name()
			fname = fake_name.split()[0]
			lname = fake_name.split()[1]
			full_name = fname + " " + lname
			username = gen_uname(full_name)

			data = {
				"first_name":fname,
				"last_name":lname,
				"phone_number":b,
				"username":username
			}
			with open("data.json", "a+") as f:
				f.write(json.dumps(data, indent=4) + "\n")
				f.close()

			pause.seconds(5)
			ARGUMENT = f"{data['first_name']},{data['last_name']},{username},{data['phone_number']}"
			call(f"start cmd /c python main.py {ARGUMENT}", cwd=r'C:\\Users\\botpo\\john-doe\\python\\Yahoo', shell=True)
			if i%2==0:
				x= input("Press any key to the next 2 numbers..")
		except KeyboardInterrupt:
			x=input("Press any key to continue..")
			if "y" in x:
				continue
			else:
				sys.exit(0)
		except Exception as e:
			continue
