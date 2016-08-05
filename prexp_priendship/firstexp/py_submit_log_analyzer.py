# -*- coding: utf-8 -*-
from firstexp.models import Politician, SubmitLog


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
	p_network = dict([(x, 0) for x in pair_list])

	# source from model
	if option == 0:
		q_hash = {"친하": "green", "안 친하": "red"}
		sl_list = SubmitLog.objects.all()
		for sl in sl_list:
			select_tuple = tuple(sorted(sl.select_list.split(",")))
			q_kind = q_hash[sl.q_kind]
			print(q_kind)
			if len(select_tuple) == 2:
				if q_kind == "red":
					p_network[select_tuple] -= 1
				else:
					p_network[select_tuple] += 1
	# source from local file
	else:
		for line in open("submit_logs_first_iterations.txt", "r"):
			line = line.strip()
			ll = line.split("\t")

			select_tuple = tuple(sorted(ll[3].split(",")))
			q_kind = ll[1]

			if len(select_tuple) == 2:
				if q_kind == "red":
					p_network[select_tuple] -= 1
				else:
					p_network[select_tuple] += 1
	return p_network

def create_visjs_network_from_raw(p_network, p_hash, option=0):
	"""
	:param p_network: dict {"(pid_x, pid_y)": "weight"}
	:param p_hash: dict {"pid":"p_name"}
	:return: tuple (node_list, edge_list)
	"""
	node_list = []
	edge_list = []

	for x, y in sorted(p_network, key=p_network.get, reverse=True):
		if p_network[(x, y)] != 0:
			px = str(p_hash[x])
			py = str(p_hash[y])
			int_weight = int(p_network[(x, y)])

			# only save node which has edges
			node_x = {}
			node_x["id"] = x
			node_x["label"] = px
			node_y = {}
			node_y["id"] = y
			node_y["label"] = py
			if node_x not in node_list:
				node_list.append(node_x)
			if node_y not in node_list:
				node_list.append(node_y)

			edge = {}
			edge["from"] = x
			edge["to"] = y
			if int_weight > 0:
				# familiar relation: pos weight
				edge["color"] = {"color":"green"}
			else:
				# unfaimilar relation: neg weight
				edge["color"] = {"color":"red"}
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
