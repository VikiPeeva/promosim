import numpy as np
from scipy.optimize import linear_sum_assignment

from pm4py.objects.petri_net.obj import PetriNet


def transition_label_matching(net1: PetriNet, net2: PetriNet):
    labels1 = set([transition.label for transition in net1.transitions])
    labels2 = set([transition.label for transition in net2.transitions])
    labels_intersection = labels1.intersection(labels2)
    return 2 * len(labels_intersection) / (len(labels1) + len(labels2))


def node_matching(net1: PetriNet, net2: PetriNet):
    place_matching_cost_matrix, place_matching_assignment = find_optimal_place_matching(net1, net2)
    labels1 = set([transition.label for transition in net1.transitions])
    labels2 = set([transition.label for transition in net2.transitions])
    labels_intersection = labels1.intersection(labels2)

    return (2 * len(labels_intersection) + 2 * place_matching_cost_matrix[place_matching_assignment].sum())\
        / (len(labels1) + len(labels2) + len(net1.places) + len(net2.places))


def place_matching_cost(place1: PetriNet.Place, place2: PetriNet.Place):
    in_tr1 = set([arc.source.label for arc in place1.in_arcs])
    out_tr1 = set([arc.target.label for arc in place1.out_arcs])
    in_tr2 = set([arc.source.label for arc in place2.in_arcs])
    out_tr2 = set([arc.target.label for arc in place2.out_arcs])

    return ((2 * len(in_tr1.intersection(in_tr2))) / (len(in_tr1) + len(in_tr2))) / 2 + \
        ((2 * len(out_tr1.intersection(out_tr2))) / (len(out_tr1) + len(out_tr2))) / 2


def find_optimal_place_matching(net1: PetriNet, net2: PetriNet):
    count_places_net1 = len(net1.places)
    count_places_net2 = len(net2.places)
    cost_matrix = np.zeros((count_places_net1, count_places_net2))
    for i, place1 in zip(range(count_places_net1), net1.places):
        for j, place2 in zip(range(count_places_net2), net2.places):
            cost_matrix[i][j] = place_matching_cost(place1, place2)

    return cost_matrix, linear_sum_assignment(cost_matrix, maximize=True)
