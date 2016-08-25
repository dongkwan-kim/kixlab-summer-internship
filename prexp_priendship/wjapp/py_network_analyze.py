# -*- coding: utf-8 -*-

import firstexp.models as fem
import secondexp.models as sem


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
	    # no need to implement
        pass
    return p_hash



