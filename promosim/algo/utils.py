import numpy as np
import pm4py


def extract_traces_as_strings(net, im, fm):
    play_out_log = pm4py.play_out((net, im, fm),
                                  parameters={"add_only_if_fm_is_reached": True, "fm_leq_accepted": False})
    traces = set([''.join(t) for t in pm4py.project_on_event_attribute(play_out_log, "concept:name")])
    return traces


def build_cost_matrix(collection1, collection2, pair_cost_func):
    count_collection1 = len(collection1)
    count_collection2 = len(collection2)
    cost_matrix = np.zeros((count_collection1, count_collection2))
    for i, el1 in zip(range(count_collection1), collection1):
        for j, el2 in zip(range(count_collection2), collection2):
            cost_matrix[i][j] = pair_cost_func(el1, el2)

    return cost_matrix

