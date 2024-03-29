import os
import shutil
import urllib.request
import json
from . import terminal as term

path_lib = os.path.dirname(os.path.abspath(__file__))
path_data = path_lib+"/data"
path_config = path_data+'/config.json'
path_devices = path_data+"/devices.json"


def running():
	return os.path.dirname(os.path.abspath(__file__))


def clean():
	if input('delete all local data? [y/n]') == 'y':
		shutil.rmtree(path_data)
		print("deleted", path_data)


def removeConfig():
	if input('delete config? [y/n]') == 'y':
		os.remove(path_config)
		print("removed", path_config)


def removeDeviceList():
	os.remove(path_devices)
	print("removed", path_devices)


def ls(l):
	if isinstance(l, dict):
		l = l.values()

	for i in l:
		print(i)


def request(url, headers, data=None, debug=False):

	if debug:
		print(term.mod('debugging request', [term.color('yellow')]))
		print('-'*40)
		print('url :', url)
		print('headers :', headers)
		print('data :', data)
		print('-'*40)
		return False

	req = urllib.request.Request(url, json.dumps(data).encode() if data else None, headers)
	try:
		with urllib.request.urlopen(req) as response:
			body = json.loads(response.read())
			if body["message"] == "success":
				return body["body"] if body["body"] else True
			else:
				print(term.mod('ERROR', [term.color('red')]))
				print("request data:", data)
				print("response message:", body["message"])
				print("response body", body["body"])

	except urllib.error.URLError as e:
		print("URLError", e)


def write(file, string):
	try:
		open(file, "w").write(string)
		print("saved", file)
	except:
		print("failed to save", file)


def toOptions(ls):
	s = "[ "
	for i in range(len(ls)):
		s += str(i) + " " + str(ls[i])
		if i < len(ls)-1:
			s += " | "

	return s + " ]"

def setOption(v, ls):
	if v in ls:
		return ls.index(v)

	# when v is int
	if isinstance(v, int) and 0<=v and v<len(ls):
		return v

	# when v is 'n'
	if v in [str(i) for i in range(len(ls))]:
		return int(v)

	v = input("choose option " + toOptions(ls) + " >>")
	return setOption(int(v) if v.isdigit() else v, ls)


executable = {
	'clean':clean,
	'removeConfig':removeConfig,
	'removeDeviceList': removeDeviceList,
	'running': running
}