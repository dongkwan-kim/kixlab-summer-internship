import urllib.request
import urllib.parse
from wjapp.models import CoBill20, CoBillNetwork
import firstexp.py_submit_log_analyzer as fsla

def create_cb_network(piv_w_value=0.3):
	"""
	:return: dict {(pid_x, pid_y): "weight"}
	"""
	p_hash = fsla.create_p_hash()
	pid_hash = dict((y, x) for (x, y) in p_hash.items())
	CB = CoBillNetwork.objects.all()
	
	cb_network = {}
	for obj_cb in CB:
		pair = [obj_cb.p1, obj_cb.p2]
		pid_pair = tuple(sorted([pid_hash[p] for p in pair]))
		cb_network[pid_pair] = obj_cb.weight
	
	rcb_network = {}
	v_piv_ascend = get_piv(cb_network.values(), piv_w_value, option="ascend")
	for k, v in cb_network.items():
		if v > v_piv_ascend:
			rcb_network[k] = v

	return rcb_network

def create_visjs_network_from_raw(p_network, p_hash):
	"""
	:param p_network: dict {"(pid_x, pid_y)": "weight"}
	:param p_hash: dict {"pid":"p_name"}
	:return: tuple (node_list, edge_list)
	"""
	node_list = []
	edge_list = []
	node_color = {"background": "white", "border": "#455a64"}

	for x, y in sorted(p_network, key=p_network.get, reverse=True):
		if p_network[(x, y)] != 0:
			px = str(p_hash[x])
			py = str(p_hash[y])
			weight = p_network[(x, y)]

			# only save node which has edges
			node_x = {}
			node_x["id"] = x
			node_x["label"] = px
			node_x["color"] = node_color
			node_y = {}
			node_y["id"] = y
			node_y["label"] = py
			node_y["color"] = node_color
			if node_x not in node_list:
				node_list.append(node_x)
			if node_y not in node_list:
				node_list.append(node_y)

			edge = {}
			edge["from"] = x
			edge["to"] = y
			edge["color"] = {"color": "grey", "highlight": "orange"}
			edge["value"] = abs(weight)
			edge_list.append(edge)

	return (node_list, edge_list)

def create_visjs_cb_network():
	cb_network = create_cb_network()
	p_hash = fsla.create_p_hash()
	return create_visjs_network_from_raw(cb_network, p_hash)

def get_piv(l, c, option="ascend"):
	if option == "ascend":
		sl = list(reversed(sorted([x for x in l])))
	else:
		sl = list(sorted([x for x in l]))
	length = len(l)

	if c != 1:
		pidx = int(c*length)
		return sl[pidx]
	else:
		return sl[-1] - 1


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
				name = p_line.split("(")[0]
				if name in ["김성태", "최경환"]:
					cname = p_line.split("/")[1][:-1]
					p_list.append(name+"_"+cname)
					print(p_list[-1])
				else:
					p_list.append(name)

			cb_20 = CoBill20(bill_no=bill_no, p_list=p_list)
			cb_20.save()
			break

def crawl_all_bill():
	old_cb = CoBill20.objects.all()
	start_no = old_cb[len(old_cb)-1].bill_no+1
	for no in range(start_no, 2001745):
		crawl_bill(no)

def del_db():
	old_cb = CoBill20.objects.all()
	for ocb in old_cb:
		ocb.delete()

# test
if __name__ == "__main__":
	crawl_bill(2000159)
