from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils
import pm4py
from copy import deepcopy
import uuid
from promosim.algo.utils import extract_traces_as_strings, build_cost_matrix
from promosim.algo.similarity_metrics.matching import trace_matching_cost
from scipy.optimize import linear_sum_assignment


def partial_order(net1: PetriNet, net2: PetriNet):
    tnet1, im1, fm1 = limit_lpm(net1, Marking(), Marking())
    tnet2, im2, fm2 = limit_lpm(net2, Marking(), Marking())

    log1 = pm4py.play_out(tnet1, im1, fm1)
    log2 = pm4py.play_out(tnet2, im2, fm2)

    po1 = set([item for item in pm4py.discover_eventually_follows_graph(log1).items()])
    po2 = set([item for item in pm4py.discover_eventually_follows_graph(log2).items()])

    if po1 == 0 and po2 == 0:
        pm4py.view_petri_net(tnet1, im1, fm1)
        pm4py.view_petri_net(tnet2, im2, fm2)
        return 0
    po_intersection = po1.intersection(po2)
    return 2 * len(po_intersection) / (len(po1) + len(po2))


def limit_lpm(net0, im0, fm0):
    [net, im, fm] = deepcopy([net0, im0, fm0])
    initial_tr = net.transitions - set([arc.target for arc in net.arcs if isinstance(arc.target, PetriNet.Transition)])
    initial_places = set([arc.target for arc in net.arcs if arc.source in initial_tr])

    for place in initial_places:
        inverse_place = PetriNet.Place(str(uuid.uuid4()))
        im[inverse_place] = 1
        net.places.add(inverse_place)
        in_arcs = [arc for arc in net.arcs if arc.target == place]  # and arc.source in initial_tr]
        for arc in in_arcs:
            petri_utils.add_arc_from_to(inverse_place, arc.source, net)

    return net, im, fm


def optimal_trace_matching(traces1, traces2):
    cost_matrix = build_cost_matrix(traces1, traces2, trace_matching_cost)
    return cost_matrix, linear_sum_assignment(cost_matrix, maximize=True)


def full_lang_distance(net1: PetriNet, im1: Marking, fm1: Marking, net2: PetriNet, im2: Marking, fm2: Marking):
    traces1 = extract_traces_as_strings(net1, im1, fm1)
    traces2 = extract_traces_as_strings(net2, im2, fm2)
    cost_matrix, assignment = optimal_trace_matching(traces1, traces2)
    return 2 * cost_matrix[assignment].sum() / (len(traces1) + len(traces2))
