import firstexp.py_submit_log_analyzer as fsla
from wjapp.models import LWJNetwork

def create_lwj_network():
	"""
	:return: dict {(pid_x, pid_y): "weight"}
	"""
	p_hash = fsla.create_p_hash()
	pid_hash = dict((y, x) for (x, y) in p_hash.items())
	LWJ = LWJNetwork.objects.all()
	
	p_network = {}
	for obj_lwj in LWJ:
		pair = [obj_lwj.p1, obj_lwj.p2]
		pid_pair = tuple(sorted([pid_hash[p] for p in pair]))
		p_network[pid_pair] = obj_lwj.weight
	
	return p_network

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
			edge["color"] = {"color": "grey", "highlight": "green"}
			edge["value"] = abs(weight)
			edge_list.append(edge)

	return (node_list, edge_list)

def create_visjs_lwj_network():
	lwj_network = create_lwj_network()
	p_hash = fsla.create_p_hash()
	return create_visjs_network_from_raw(v_network, p_hash)
