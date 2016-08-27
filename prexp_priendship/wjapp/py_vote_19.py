import urllib.request
import urllib.parse
import json
from wjapp.models import Vote19, VoteVector
import firstexp.models as fem
import firstexp.py_submit_log_analyzer as fsla
import math

def int_vectorize():
	vote_db = Vote19.objects.all()
	my_p_list = fem.Politician.objects.all()
	
	vote_vector_db = VoteVector.objects.all()
	for v in vote_vector_db:
		v.delete()

	for vote in vote_db:
		for p in my_p_list:
			# only intersection of mine and 19's
			if vote.name == p.name:
				v_list = vote.vote.split(",")
				vectorized_list = []
				for v_word in v_list:
					if v_word == "찬성":
						vectorized_list.append("1")
					elif v_word == "반대":
						vectorized_list.append("-1")
					else:
						# abstention, absence, etc.
						vectorized_list.append("0")
				new_vv = VoteVector(name=vote.name, party=vote.party, vote=",".join(vectorized_list))
				new_vv.save()

def get_eud(vv1, vv2):
	"""
	:param vv1, vv2: VoteVector.vote 1,0,-1,1, ... ,
	:return: Euclidean distance of vv1 and vv2
	"""
	vv1_list = [int(v) for v in vv1.split(",")]
	vv2_list = [int(v) for v in vv2.split(",")]

	if len(vv1_list) != len(vv2_list):
		raise(Exception("VectorLengthDifferentError"))

	eud = math.sqrt(sum([(e1 - e2)**2 for (e1, e2) in zip(vv1_list, vv2_list)]))
	return eud

def create_vote_network(piv_w_value=0.15):
	"""
	:return: dict {(pid_x, pid_y): "weight"}
	"""
	vv_list = VoteVector.objects.all()
	p_hash = fsla.create_p_hash()
	pid_hash = dict((y, x) for (x, y) in p_hash.items())
	
	v_network = {}
	vvlen = len(vv_list)
	for idx in range(vvlen):
		for jdx in range(idx+1, vvlen):
			vv1 = vv_list[idx]
			vv2 = vv_list[jdx]
			pid_pair = tuple(sorted([pid_hash[vv1.name], pid_hash[vv2.name]]))
			v_network[pid_pair] = 1/(1+get_eud(vv1.vote, vv2.vote))
	
	rv_network = {}
	v_piv_ascend = get_piv(v_network.values(), piv_w_value, option="ascend")
	for k, v in v_network.items():
		if v > v_piv_ascend:
			rv_network[k] = v

	return rv_network

def create_visjs_network_from_raw(p_network, p_hash, option=0):
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
			edge["color"] = {"color": "grey", "highlight": "green"}
			edge["value"] = abs(weight)
			edge_list.append(edge)

	return (node_list, edge_list)

def create_visjs_vote_network():
	v_network = create_vote_network()
	p_hash = fsla.create_p_hash()
	return create_visjs_network_from_raw(v_network, p_hash)

def get_avg(l):
	return sum(l)/len(l)

def get_med(l):
	sl = sorted([x for x in l])
	length = len(l)
	midx = int(length/2)
	if length%2 == 1:
		return sl[midx]
	else:
		return get_avg([sl[midx-1], sl[midx]])

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

# max num = 293
def crawl(num):
	vote_db = Vote19.objects.all()
	
	# start from previous index
	for num in range(len(vote_db)+1, num):
		base_url = "http://read-data.codenamu.org/congress-report/api/congress_people/"
		base_url += str(num) + ".json"
		request = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
		response = urllib.request.urlopen(request)
		js = json.loads(response.read().decode("utf-8"))

		name = js["congress_person"]["name_kr"]
		party = js["congress_person"]["party"]
		vote_list = js["congress_person"]["bill_votes"]
		vote_hash = {}
		for vote in vote_list:
			vote_hash[vote["bill_id"]] = vote["vote"]

		new_vote_list = []
		for i in range(1, 2571):
			try:
				new_vote_list.append(vote_hash[i])
			except:
				new_vote_list.append("없음")
	
		vote_line = ",".join(new_vote_list)
		new_model = Vote19(name=name, party=party, vote=vote_line)
		new_model.save()
