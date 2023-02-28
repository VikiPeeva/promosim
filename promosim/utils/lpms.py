from copy import deepcopy
import uuid

from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.obj import PetriNet


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
