# -*- coding: utf-8 -*-

import firstexp.models as fem
import secondexp.models as sem


class Network():
    def __init__(self, v_list, e_dict):
        """
        :param v_list: list of vertex
        :param e_dict: dict {key: tuple(v1, v2), value: weight}
        """
        self.v_list = v_list
        self.e_dict = e_dict

    def get_neighbors(self, v):
        """
        :param v: one specific vertex
        :return: dict {key: neighbor_v, value: weight of e(v, neighber_v)}
        """
        if v not in self.v_list:
            raise(Exception("WrongVertexError"))

        rv_dict = {}
        for vt in self.e_dict.keys():
            if v in vt:
                change = dict([(vt[0], vt[1]), (vt[1], vt[0])])
                rv_dict[change[v]] = e_dict[vt]

        return rv_dict


class GED():
    def __init__(self, g1, g2):
        self.g1 = g1
        self.g2 = g2
        self.e_mark = {}
        e_list = list(set(g1.e_dict.keys()+g2.e_dict.keys()))
        for e in e_list:
            self.e_mark[e] = True

        # in this program, g1 and g2 are isomorphic
        if not self.is_isomorphic(g1, g2):
            raise(Exception("NotIsomorphicError"))

    def is_isomorphic(self, g1, g2):
        # not implemented
        return True

    def cost(self, v):
        """
        :param v: vertex from network
        :return: integer cost
        """
        nbr1_dict = self.g1.get_neighbors(v)
        nbr2_dict = self.g2.get_neighbors(v)
        union_keys = list(set(nbr1_dict.keys()+nbr2.keys()))
        union_dict = {}
        # not implemented

        cost = 1
        return cost

    def get_ged(self):
        """
        :return: graph edit distance
        """
        # GED(g1, g2)
        # = min_{(e1,...,e_{k} IN P(g1, g2))} SUM_{1<=i<=k} c(e_{i})
        # where P(g1, g2) denotes the set of edit paths transforming g1 into g2
        # and c(e) >=0 is the cost of each graph edit operation e
        # graph edit operation includes (v, e) X (insert, delete, substiute)

        # not implemented
        ged = None
        for v in self.g1.v_list:
            c = self.cost(v)

        return ged

def moderate_lwj():
    pass

def moderate_mine():
    pass
