import urllib.request
import urllib.parse
from wjapp.models import CoBill20

def crawl_bill(bill_no):
	"""
	:param bill_no: idx of bill, 2000001<=bill_no<=2001744 (2016.08.28)
	:crawl bill of specific bill_no
	"""
	base_url = "http://watch.peoplepower21.org/?mid=LawInfo&bill_no="+str(bill_no)
	request = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urllib.request.urlopen(request)

	for line in response:
		line = line.decode("utf-8")
		if "<br>" in line:
			line_arr = line.split("<br>")
			line_arr = [l.strip() for l in line_arr if len(l.strip()) != 0]
			p_list = []			
			for p_line in line_arr:
				# p_line = "kname(party/cname)"
				# token = "kname(party"
				# name_party = "kname_party"
				token = p_line.split("/")[0]
				name_party = token.replace("(", "_")
				p_list.append(name_party)
			cb_20 = CoBill20(bill_no=bill_no, p_list=p_list)
			cb_20.save()
			break

# test
if __name__ == "__main__":
	crawl_bill(2001744)
