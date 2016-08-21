# -*- coding: utf-8 -*-
from secondexp.models import Politician, SubmitLog


def create_p_hash(option=0):
	"""
	:param option: {model(default):0, local:1}
	:return: dict {"pid":"name"}
	"""
	p_hash = {}
    
	# source from model
	if option == 0:
		p_list = Politician.objects.all()
		for p in p_list:
			p_hash[str(p.pid)] = p.name
    # source from local file
	else:
		for line in open("mod_ansi_unified_assembly_50.txt", "r"):
			line = line.strip()
			ll = line.split("\t")
			p_hash[ll[7].split("/")[-1].split(".")[0]] = ll[0]
	return p_hash


def create_pair_list(p_hash):
	"""
	:param p_hash: dict {"pid":"name"}
	:return: set that consists of combination ("pid_x", "pid_y")
	"""
	return set([tuple(sorted([x, y])) for x in p_hash.keys() for y in p_hash.keys()])


def create_network_from_logs(pair_list, option=0):
	"""
	:param pair_list: set that consists of combination ("pid_x", "pid_y")
	:param option: {model(default):0, local:1}
	:return: dict {"(pid_x, pid_y)": "weight"}
	"""
	# (x, (0, 0)) = (pair, (sum, count))
	p_network = dict([(x, (0, 0)) for x in pair_list])
	
	# source from model
	if option == 0:
		sl_list = SubmitLog.objects.all()
		for sl in sl_list:
			shown_tuple = tuple(sorted(sl.shown_list.split(",")))
			affinity_score = sl.affinity_score
			if affinity_score != "donot-know":
				(s, c) = p_network[shown_tuple]
				p_network[shown_tuple] = (s+int(affinity_score), c+1)
		for pair in p_network.keys():
			(s, c) = p_network[pair]
			if c != 0:
				p_network[pair] = s/(1.0*c)
			else:
				p_network[pair] = 0

	# source from local file
	else:
		# no need to implement
		pass

	return p_network

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
			int_weight = int(p_network[(x, y)])
			
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
			if int_weight > 0:
				# familiar relation: pos weight
				edge["color"] = {"color": "green", "highlight": "green"}
			else:
				# unfaimilar relation: neg weight
				edge["color"] = {"color":"red", "highlight": "red"}

			edge["value"] = abs(int_weight)
			edge_list.append(edge)

	return (node_list, edge_list)


def create_visjs_with_whole_process(option=0):
	p_hash = create_p_hash(option)
	pair_list = create_pair_list(p_hash)
	p_network = create_network_from_logs(pair_list, option)
	visjs_network = create_visjs_network_from_raw(p_network, p_hash)
	return visjs_network


if __name__ == "__main__":
	visjs = create_visjs_with_whole_process(1)
	print(visjs[0])
	print(visjs[1])
