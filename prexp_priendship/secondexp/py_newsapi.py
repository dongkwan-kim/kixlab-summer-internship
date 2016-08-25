# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

class NaverNewsXML():

	def __init__(self, query, display=10):
		self.client_id = "c0p5z3dxRD1qnH6wc7I3"
		self.client_secret = "Q2vDiQF2NA"
		self.query = query
		self.display = display

	def get_response(self, sort="sim"):
		base_url = "https://openapi.naver.com/v1/search/news.xml"
		base_url += "?query="+urllib.parse.quote(str(self.query))
		base_url += "&sort="+str(sort)
		base_url += "&display="+str(self.display)

		request = urllib.request.Request(base_url)
		request.add_header("X-Naver-Client-Id", self.client_id)
		request.add_header("X-Naver-Client-Secret", self.client_secret)

		# this must be decoded to utf-8
		return urllib.request.urlopen(request)

	def get_news_items(self):
		res = self.get_response()
		xml = res.read().decode("utf-8")
		root = ET.fromstring(xml)
		r_list = []
		for it in root.iter("item"):
			_title = it.findtext("title")
			_link = it.findtext("link")
			_description = it.findtext("description")
			_pub_date = it.findtext("pubDate")
			r_list.append(NaverNewsItem(_title, _link, _description, _pub_date))
		return r_list

class NaverNewsItem():

	def __init__(self, title, link, description, pub_date):
		self.title = title
		self.link = link
		self.description = description
		self.pub_date = pub_date

if __name__ == "__main__":
	nn = NaverNewsXML("박근혜 유승민")
	for it in nn.get_news_items():
		print(it.title)
