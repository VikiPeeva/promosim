from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils
import pm4py
from copy import deepcopy
import uuid


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
    initial_places = set(net.places)

    for trans in net.transitions:
        if trans.label is not None:
            # limits the execution to 1
            new_place = PetriNet.Place(str(uuid.uuid4()))
            net.places.add(new_place)
            petri_utils.add_arc_from_to(new_place, trans, net)
            im[new_place] = 1

    for place in initial_places:
        inverse_place = PetriNet.Place(str(uuid.uuid4()))
        im[inverse_place] = 1
        net.places.add(inverse_place)
        in_arcs = [arc for arc in net.arcs if arc.target == place]
        for arc in in_arcs:
            petri_utils.add_arc_from_to(inverse_place, arc.source, net)

    return net, im, fm
