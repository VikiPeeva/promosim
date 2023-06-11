import pm4py
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.log.obj import EventLog

from promosim.utils.lpms import limit_lpm
from promosim.utils.utils import playout_traces_as_strings, extract_efg_from_trace_set, extract_efg_from_log
from promosim.utils.matching import calculate_optimal_trace_matching
from promosim.utils.utils import extract_traces_as_sequences


def efg_distance_nets(net1: PetriNet, net2: PetriNet):
    tnet1, im1, fm1 = limit_lpm(net1, Marking(), Marking())
    tnet2, im2, fm2 = limit_lpm(net2, Marking(), Marking())

    log1 = pm4py.play_out(tnet1, im1, fm1)
    log2 = pm4py.play_out(tnet2, im2, fm2)

    return efg_similarity_logs(log1, log2)


def efg_similarity_logs(log1: EventLog, log2: EventLog):
    efg1 = extract_efg_from_log(log1)
    efg2 = extract_efg_from_log(log2)
    return efg_similarity(efg1, efg2)


def efg_similarity_traces(traces1, traces2):
    efg1 = extract_efg_from_trace_set(traces1)
    efg2 = extract_efg_from_trace_set(traces2)
    return efg_similarity(efg1, efg2)


def efg_similarity(efg1, efg2):
    if len(efg1) == 0 and len(efg2) == 0:
        return 0
    efg_intersection = efg1.intersection(efg2)
    return 2 * len(efg_intersection) / (len(efg1) + len(efg2))


def full_lang_similarity(net1: PetriNet, im1: Marking, fm1: Marking,
                         net2: PetriNet, im2: Marking, fm2: Marking,
                         transform_traces=extract_traces_as_sequences):
    traces1 = playout_traces_as_strings(net1, im1, fm1, transform_traces=transform_traces)
    traces2 = playout_traces_as_strings(net2, im2, fm2, transform_traces=transform_traces)
    gain_matrix, assignment = calculate_optimal_trace_matching(traces1, traces2)
    return 2 * gain_matrix[assignment].sum() / (len(traces1) + len(traces2))
