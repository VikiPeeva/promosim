from pm4py.objects.petri_net.obj import PetriNet

from promosim.utils.matching import calculate_optimal_place_matching


def transition_label_similarity(net1: PetriNet, net2: PetriNet):
    labels1 = set([transition.label for transition in net1.transitions])
    labels2 = set([transition.label for transition in net2.transitions])
    labels_intersection = labels1.intersection(labels2)
    return 2 * len(labels_intersection) / (len(labels1) + len(labels2))


def node_similarity(net1: PetriNet, net2: PetriNet):
    place_matching_cost_matrix, place_matching_assignment = calculate_optimal_place_matching(net1, net2)
    labels1 = set([transition.label for transition in net1.transitions])
    labels2 = set([transition.label for transition in net2.transitions])
    labels_intersection = labels1.intersection(labels2)

    return (2 * len(labels_intersection) + 2 * place_matching_cost_matrix[place_matching_assignment].sum())\
        / (len(labels1) + len(labels2) + len(net1.places) + len(net2.places))
