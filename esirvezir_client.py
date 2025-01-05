# Encrypted Secure Remote Virtual System (ESRVS) (Esir Vezir)
# Client Code

import random
import requests
import json

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
class ESRVS:
	def __init__(self):
		self.target = "http://esirvezir_machine.net/secret/root/run"
		self.method = "ESRVS"
		self.key = "key"
		self.keyengine = ShieldKEY()
	def run_command(self, command, input=""):
		content = {"key": self.key, "target": command, "input": input}
		content = json.dumps(content)
		content = self.keyengine.encrypt(content, self.key)
		content = self.keyengine.encode(content)
		data = {"command": "command", "content": content}
		response = requests.request(self.method, self.target, json=data)
		try:
			text = response.text
			text = self.keyengine.decode(text)
			text = self.keyengine.decrypt(text, self.key)
			return text
		except:
			return response.text
	def run_python(self, code):
		content = {"key": self.key, "target": code}
		content = json.dumps(content)
		content = self.keyengine.encrypt(content, self.key)
		content = self.keyengine.encode(content)
		data = {"command": "python", "content": content}
		response = requests.request(self.method, self.target, json=data)
		try:
			text = response.text
			text = self.keyengine.decode(text)
			text = self.keyengine.decrypt(text, self.key)
			return text
		except:
			return response.text