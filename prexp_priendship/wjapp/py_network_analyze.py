# -*- coding: utf-8 -*-

import firstexp.models as fem
import secondexp.models as sem


def create_node_list(option=0):
	"""
	:param option: {model(default):0, local:1}
	:return: dict {"pid":"name"}
	"""
	p_hash = {}

	# source from model
	if option == 0:
		p_list = Politician.objects.all()
		for p in p_list:
			p_hash[p.name] = str(p.pid)
    # source from local file
	else:
	    # no need to implement
        pass
    return p_hash

def cost_function(n1, n2):
	"""
	:param n1: node from network 1
	:param n2: node from network 2
	:return: integer cost
	"""
	return cost

def ged(g1, g2):
	# in this program, g1 and g2 are isomorphic
	"""
	:param g1: network graph 1
	:param g2: network graph 2
	:return: graph edit distance
	"""
	# GED(g1, g2)
	# = min_{(e1,...,e_{k} IN P(g1, g2))} SUM_{1<=i<=k} c(e_{i})
	# where P(g1, g2) denotes the set of edit paths transforming g1 into g2
	# and c(e) >=0 is the cost of each graph edit operation e
	# graph edit operation includes (v, e) X (insert, delete, substiute)
	return ged

def moderate_lwj():
	pass

def moderate_mine():
	pass


