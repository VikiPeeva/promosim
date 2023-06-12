from scipy.optimize import linear_sum_assignment

from pm4py.objects.petri_net.obj import PetriNet

import pylev
from promosim.utils.utils import build_gain_matrix


def place_matching_gain(place1: PetriNet.Place, place2: PetriNet.Place):
    in_tr1 = set([arc.source.label for arc in place1.in_arcs])
    out_tr1 = set([arc.target.label for arc in place1.out_arcs])
    in_tr2 = set([arc.source.label for arc in place2.in_arcs])
    out_tr2 = set([arc.target.label for arc in place2.out_arcs])

    return ((2 * len(in_tr1.intersection(in_tr2))) / (len(in_tr1) + len(in_tr2))) / 2 + \
        ((2 * len(out_tr1.intersection(out_tr2))) / (len(out_tr1) + len(out_tr2))) / 2


def trace_matching_gain(trace1, trace2):
    return 1 - pylev.levenshtein(trace1, trace2) / max(len(trace1), len(trace2))


def calculate_optimal_place_matching(net1: PetriNet, net2: PetriNet):
    gain_matrix = build_gain_matrix(net1.places, net2.places, place_matching_gain)
    return gain_matrix, linear_sum_assignment(gain_matrix, maximize=True)


def calculate_optimal_trace_matching(traces1, traces2):
    gain_matrix = build_gain_matrix(traces1, traces2, trace_matching_gain)
    return gain_matrix, linear_sum_assignment(gain_matrix, maximize=True)
