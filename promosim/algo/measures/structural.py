from pm4py.objects.petri_net.obj import PetriNet

from promosim.utils.matching import place_matching_gain
from promosim.utils.lpms import get_graph_from_petri_net

import networkx as nx


def ged_distance(net1: PetriNet, net2: PetriNet, include_nodes=True, include_edges=True, timeout=None):
    g1 = get_graph_from_petri_net(net1)
    g2 = get_graph_from_petri_net(net2)
    graph_dist = ged_distance_graphs(g1, g2, include_nodes, include_edges, timeout=timeout)
    return graph_dist / (ged_distance_graphs(g1, nx.empty_graph(), include_nodes, include_edges, timeout=timeout) +
                         ged_distance_graphs(g2, nx.empty_graph(), include_nodes, include_edges, timeout=timeout))


def ged_distance_graphs(g1: nx.DiGraph, g2: nx.DiGraph, include_nodes=True, include_edges=True,
                        pmg=place_matching_gain, timeout=None):
    """"""
    node_subst_cost_matrix = calculate_node_subst_cost(g1, g2, pmg)
    edge_subst_cost_matrix = calculate_edge_subst_cost(g1, g2, pmg)
    if include_nodes and include_edges:
        return nx.graph_edit_distance(g1, g2,
                                      node_subst_cost=lambda n1, n2: node_subst_cost_matrix[n1["id"]][n2["id"]],
                                      edge_subst_cost=lambda e1, e2: edge_subst_cost_matrix[e1["id"]][e2["id"]],
                                      timeout=timeout)
    elif include_nodes:
        return nx.graph_edit_distance(g1, g2,
                                      node_subst_cost=lambda n1, n2: node_subst_cost_matrix[n1["id"]][n2["id"]],
                                      timeout=timeout)
    return nx.graph_edit_distance(g1, g2, timeout=timeout)


def calculate_node_subst_cost(g1: nx.DiGraph, g2: nx.DiGraph, pmg=place_matching_gain):
    dists = {}
    for n1 in g1.nodes:
        dists[n1] = {}
        for n2 in g2.nodes:
            node1 = g1.nodes[n1]
            node2 = g2.nodes[n2]
            dists[n1][n2] = node_subst_cost(node1, node2, pmg)
    return dists


def calculate_edge_subst_cost(g1: nx.DiGraph, g2: nx.DiGraph, pmg=place_matching_gain):
    dists = {}
    for e1 in g1.edges:
        dists[e1] = {}
        for e2 in g2.edges:
            edge1 = g1.edges[e1]
            edge2 = g2.edges[e2]
            dists[e1][e2] = edge_subst_cost(edge1, edge2, pmg)
    return dists


def node_subst_cost(n1, n2, pmg=place_matching_gain):
    if n1["type"] != n2["type"]:
        return 1
    elif n1["type"] == "place":
        return 1 - pmg(n1["place"], n2["place"])
    else:
        return (n1["label"] != n2["label"]) * 1


def edge_subst_cost(e1, e2, pmg=place_matching_gain):
    if e1["etype"] != e2["etype"]:
        return 1
    cost = 0
    if e1["transition"] != e2["transition"]:
        cost = cost + 1
    cost = cost + (1 - pmg(e1["place"], e2["place"]))
    return cost / 2
