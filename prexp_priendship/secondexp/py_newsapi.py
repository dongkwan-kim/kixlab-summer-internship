import urllib.request


class NaverNews():
	
	def __init__(self, query):
		self.client_id = "c0p5z3dxRD1qnH6wc7I3"
		self.client_secret = "Q2vDiQF2NA"
		self.query = query

	def get_response(sort=""):
		base_url = "https://openapi.naver.com/v1/search/news.xml"
		base_url += "?query="+str(self.query)
		if sort != "":
			base_url += "&sort="+str(sort)
		
		request = urllib.request.Request(base_url)
		request.add_header("X-Naver-Client-Id", self.client_id)
		request.add_header("X-Naver-Client-Secret", self.client_secret)
	
		return urllib.request.urlopen(request)		
