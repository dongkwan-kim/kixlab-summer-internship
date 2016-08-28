import urllib.request
import urllib.parse
from wjapp.models import CoBill20

def crawl_bill(bill_no):
	"""
	:param bill_no: idx of bill, 2,000,001<=bill_no<=2,001,744 (2016.08.28)
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
			if len(line_arr) <= 1:
				print("wrong: " + str(bill_no))
				break
			
			p_list = []			
			for p_line in line_arr:
				# p_line = "kname(party/cname)"
				# token = "kname(party"
				token = p_line.split("/")[0]
				[n, p] = token.split("(")
				p_list.append(n+"_"+p[0])
			cb_20 = CoBill20(bill_no=bill_no, p_list=p_list)
			cb_20.save()
			break

def crawl_all_bill():
	old_cb = CoBill20.objects.all()
	start_no = old_cb[len(old_cb)-1].bill_no+1
	for no in range(start_no, 2001745):
		crawl_bill(no)
# test
if __name__ == "__main__":
	crawl_bill(2000159)
