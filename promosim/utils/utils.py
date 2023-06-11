import numpy as np
import pm4py

from pm4py.objects.log.obj import EventLog
from pm4py.objects.petri_net.obj import PetriNet, Marking


def extract_traces_as_strings(play_out_log):
    traces = set([''.join(t) for t in pm4py.project_on_event_attribute(play_out_log, "concept:name")])
    return traces


def extract_traces_as_sequences(play_out_log):
    traces = set([t for t in pm4py.project_on_event_attribute(play_out_log, "concept:name")])
    return traces


def playout_traces(net, im, fm, transform_traces=extract_traces_as_sequences):
    play_out_log = pm4py.play_out(net, im, fm,
                                  parameters={"add_only_if_fm_is_reached": True,
                                              "fm_leq_accepted": False,
                                              "maxTraceLength": 10})
    traces = transform_traces(play_out_log)
    return traces


def build_cost_matrix(collection1, collection2, pair_cost_func):
    count_collection1 = len(collection1)
    count_collection2 = len(collection2)
    cost_matrix = np.zeros((count_collection1, count_collection2))
    for i, el1 in zip(range(count_collection1), collection1):
        for j, el2 in zip(range(count_collection2), collection2):
            cost_matrix[i][j] = pair_cost_func(el1, el2)

    return cost_matrix


def extract_efg_from_net(net: PetriNet, im: Marking, fm: Marking):
    log = pm4py.play_out((net, im, fm))
    return extract_efg_from_log(log)


def extract_efg_from_log(log: EventLog):
    return set([item[0] for item in pm4py.discover_eventually_follows_graph(log).items()])


def extract_efg_from_trace_set(traces):
    efg = set()
    for trace in traces:
        for i in range(len(trace) - 1):
            for j in range(i+1, len(trace)):
                efg.add((trace[i], trace[j]))
    return efg
