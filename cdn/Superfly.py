#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import base64
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from binascii import hexlify as hx, unhexlify as uhx
from hashlib import sha256
from struct import pack as pk, unpack as upk
from io import TextIOWrapper
from nut import Titles
import requests
import unidecode
import urllib3
from nut import Print
from nut import Status
from nut import Config
import os
import hashlib
from nut import Title
import cdn


def makeRequest(method, url, hdArgs={}):

	reqHd = {
		'X-Nintendo-DenebEdgeToken': Config.edgeToken.token,
		'User-Agent': 'NintendoSDK Firmware/%s (platform:NX; eid:%s)' % (Config.cdn.firmware, Config.cdn.environment),
		'Accept-Encoding': 'gzip, deflate',
		'Accept': '*/*',
		'Connection': 'keep-alive'
	}

	reqHd.update(hdArgs)

	r = requests.request(method, url, cert=Config.paths.NXclientCert, headers=reqHd, verify=False, stream=True)

	if r.status_code == 403:
		raise IOError('Request rejected by server! Check your cert ' + r.text)

	return r

def makeJsonRequest(method, url, hdArgs={}, key = None, force = False):

	os.makedirs('cache/superfly/', exist_ok=True)
	cacheFileName = 'cache/superfly/' + hashlib.md5(url.encode()).hexdigest()
	#print(url)

	if key:
		key = 'cache/superfly/' + Config.cdn.environment + '/' + key

	j = None

	if cdn.isValidCache(cacheFileName) and not force:
		if not key:
			with open(cacheFileName, encoding="utf-8-sig") as f:
				j = json.loads(f.read())
		else:
			os.makedirs(os.path.dirname(key), exist_ok=True)
			os.rename(cacheFileName, key)

	if key:
		cacheFileName = key
		if cdn.isValidCache(cacheFileName) and not force:
			with open(key, encoding="utf-8-sig") as f:
				j = json.loads(f.read())

	if not j:
		r = makeRequest(method, url, hdArgs)

		os.makedirs(os.path.dirname(cacheFileName), exist_ok=True)

		with open(cacheFileName, 'wb') as f:
			f.write(r.text.encode('utf-8'))

		j = r.json()

	try:
		if j['error']:
			print('error: ' + url)
			return None
	except Exception as e:
		pass

	return j

def getAddOns(titleId, shop_id=3):
	url = 'https://superfly.hac.%s.d4c.nintendo.net/v1/a/%s/dv' % (Config.cdn.environment, titleId)
	j = makeJsonRequest('GET', url, {}, '%d/a/%s/dv.json' % (shop_id, titleId), force = False)
	lst = []

	if not j:
		return lst

	for i in j:
		id = i['title_id'].upper()

		if not Titles.contains(id):
			Print.info('New DLC found: ' + id)

		title = Titles.get(id, None, None)
		title.setVersion(int(i['version']))


		lst.append(id)

	return lst
