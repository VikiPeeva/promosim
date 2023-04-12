from copy import deepcopy
import uuid

from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.obj import PetriNet

import networkx as nx


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


def get_petri_net_place_short_string(place: PetriNet.Place):
    in_tr = [arc.source.label for arc in place.in_arcs]
    in_tr.sort()
    out_tr = [arc.target.label for arc in place.out_arcs]
    out_tr.sort()

    return "({in_trl} | {out_trl})".format(in_trl=" ".join(in_tr), out_trl=" ".join(out_tr))


def get_graph_from_petri_net(net):
    g = nx.DiGraph()
    g.add_nodes_from([(t.name, {"id": t.name, "type": "transition", "label": t.label})
                      for t in net.transitions])
    g.add_nodes_from([(p.name, {"id": p.name, "in_tr": set([x.source.label for x in p.in_arcs]),
                                "out_tr": set([x.target.label for x in p.out_arcs]),
                                "place": p,
                                "type": "place"})
                      for p in net.places])
    for arc in net.arcs:
        if isinstance(arc.source, PetriNet.Place):
            g.add_edge(arc.source.name, arc.target.name, id=(arc.source.name, arc.target.name), etype="pt",
                       place=arc.source, transition=arc.target.label)
        else:
            g.add_edge(arc.source.name, arc.target.name, id=(arc.source.name, arc.target.name), etype="tp",
                       transition=arc.source.label, place=arc.target)
    return g
