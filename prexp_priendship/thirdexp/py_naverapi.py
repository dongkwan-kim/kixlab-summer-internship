# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET


class NaverAPIXML():

	def __init__(self, query, kind):
		self.query = query
		self.kind = kind
		(self.client_id, self.client_secret) = self.get_proper_client(kind)

	def __str__(self):
		return "NaverAPIXML | query={0} | kind={1}".format(self.query, self.kind)

	def get_proper_client(self, kind):
		if kind == "news":
			return ("c0p5z3dxRD1qnH6wc7I3", "Q2vDiQF2NA")
		elif kind == "image":
			return ("f6fUGpCglJ_3fnfOw4ft", "uNbO46NQhJ")
		else:
			return (None, None)

	def get_response(self, sort="sim", display=10):
		base_url = "https://openapi.naver.com/v1/search/{0}.xml".format(self.kind)
		base_url += "?query="+urllib.parse.quote(str(self.query))
		base_url += "&sort="+str(sort)
		base_url += "&display="+str(display)

		request = urllib.request.Request(base_url)
		request.add_header("X-Naver-Client-Id", self.client_id)
		request.add_header("X-Naver-Client-Secret", self.client_secret)
		
		# this must be decoded to utf-8
		return urllib.request.urlopen(request)

	def get_items(self):
		res = self.get_response()
		xml = res.read().decode("utf-8")
		root = ET.fromstring(xml)
		if self.kind == "news":
			return self.get_news_items(root)
		elif self.kind == "image":
			return self.get_image_items(root)
		else:
			return None

	def get_news_items(self, root):
		r_list = []
		for it in root.iter("item"):
			_title = it.findtext("title")
			_link = it.findtext("link")
			_description = it.findtext("description")
			_pub_date = it.findtext("pubDate")
			r_list.append(NaverNewsItem(_title, _link, _description, _pub_date))
		return r_list
	
	def get_image_items(self, root):
		r_list = []
		for it in root.iter("item"):
			_title = it.findtext("title")
			_link = it.findtext("link")
			_thumbnail = it.findtext("thumbnail")
			r_list.append(NaverImageItem(_title, _link, _thumbnail))
		return r_list


class NaverNewsItem():
	
	def __init__(self, title, link, description, pub_date):
		self.title = title
		self.link = link
		self.description = description
		self.pub_date = pub_date
	
	def __str__(self):
		return "title={0} | description={1} | pubDate={2}".format(self.title, self.description, self.pub_date)


class NaverImageItem():
	
	def __init__(self, title, link, thumbnail):
		self.title = title
		self.link = link
		self.thumbnail = thumbnail

	def __str__(self):
		return "title={0} | link={1} | thumbnail={2}".format(self.title, self.link, self.thumbnail)


if __name__ == "__main__":
	nn = NaverAPIXML("박근혜 유승민", "news")
	for it in nn.get_items():
		print(it)
	ni = NaverAPIXML("박근혜 유승민", "image")
	for it in ni.get_items():
		print(it)
