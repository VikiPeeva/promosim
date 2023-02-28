import pm4py
from pm4py.objects.petri_net.obj import PetriNet, Marking

from promosim.utils.lpms import limit_lpm
from promosim.utils.utils import extract_traces_as_strings
from promosim.utils.matching import calculate_optimal_trace_matching


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


def full_lang_distance(net1: PetriNet, im1: Marking, fm1: Marking, net2: PetriNet, im2: Marking, fm2: Marking):
    traces1 = extract_traces_as_strings(net1, im1, fm1)
    traces2 = extract_traces_as_strings(net2, im2, fm2)
    cost_matrix, assignment = calculate_optimal_trace_matching(traces1, traces2)
    return 2 * cost_matrix[assignment].sum() / (len(traces1) + len(traces2))
