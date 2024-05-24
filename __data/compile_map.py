""" The purpose of this function script/function is to compile information 
    into a proper graph, such that latter processing can be unified for all 
    other map-like objects.
"""
from ft import DBinterface

from ft import Characters, Relations, Places, Paths
import networkx as nx
import numpy as np
import plotly.graph_objects as go

from typing import List
from datetime import datetime
################################################################################
##                                   INPUTS                                   ##
################################################################################
plot_map = True
save_path = "/home/gartin/Documents/Fairy_tales/UI/FT_writer/dash_v5"
save_filename = "test_map.json"

################################################################################
##                                    UTILS                                   ##
################################################################################
import json
import pprint
from pathlib import Path


def network_to_json(network):
    json_data = nx.node_link_data(network)
    json_formatted_str = json.dumps(json_data, indent=2)
    return json_formatted_str
    
def print_network(network):
    pprint.pprint(dict(network.nodes(data=True)))

def save_json(path, filename, json_text):
    if '.json' in filename:
        _path = Path(path, filename)
    else:
        _path = Path(path, filename, '.json')
    with open(_path, 'w') as file:
        file.write(json_text)


################################################################################
##                           COMPILE CHARACTER MAP                            ##
################################################################################

def compile_map(
    db_interface, 
    list_of_node_ids:List[str], 
    list_of_edge_ids:List[str],
    map_type:int,
    ) -> nx.DiGraph:
    """ Produces a JSON file with unified structure shared among all maps. 
    The JSON representing the network contains:
        "nodes"
            "_id" - node id (the same as ID in the database)
            "info" - dictionary with keys:
                "text" - content shown when the node is hovered/clicked
                "metainfo" - additional info (empty string at the moment)
        "links"
            "source" - source ID (one of the "node" IDs)
            "target" - target ID (one of the "node" IDs)
            "info" - dictionary with keys:
                "text" - content shown when the node is hovered/clicked
                "metainfo" - additional info (empty string at the moment)
        "directed"
            True
        "multigraph"
            False
        "graph"
            "version" - version of the "compile_character_map" function
            "date" - data creation date
            "graph_data"
                "list_of_character_ids" - 'list_of_character_ids' provided to this function
                "list_of_relation_ids" - 'list_of_relation_ids' provided to this function

    :param db_interface: Initialized DBinterface object.
    :param list_of_node_ids: Set of IDs requested to be shown by default.
    :param list_of_edge_ids: Set of IDs requested to be shown by default.
    :param map_type: Select different maps, valid values ["characters", "places"].
    :return: Returns a NetworkX graph.
    """
    
    if map_type not in ["characters", "places"]:
        raise ValueError(
            f"'map_type' expected to be from ['characters', 'places'], "\
            f"but is '{map_type}' instead!")
    
    # prepare network
    network = nx.DiGraph(
        version=f"v{0.1}",
        date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        graph_data={
            "list_of_node_ids":list_of_node_ids, 
            "list_of_edge_ids":list_of_edge_ids,
        }
    )

    # sort the keys here, so that network already includes sorted keys


    # assign nodes
    for node_id in list_of_node_ids:
        if map_type == "characters":
            node_entry = db_interface.get_characters(includes_any={'_id':[node_id]})[0]
            text=db_interface.get_stext_characters(includes_any={'_id':[node_id]})
        elif map_type == "places":
            node_entry = db_interface.get_places(includes_any={'_id':[node_id]})[0]
            text=db_interface.get_stext_places(includes_any={'_id':[node_id]})
            
        network.add_node(
            node_for_adding=node_id,
            # name = node_entry["name"],
            # _id = node_entry["_id"],
            **node_entry,
            _text = text,
            _metainfo = "",
            )
        
    # assign relations
    for edge_id in list_of_edge_ids:
        if map_type == "characters":
            edge_entry = db_interface.get_relations(includes_any={'_id':[edge_id]})[0]
            text = db_interface.get_stext_relations(includes_any={'_id':[edge_id]})
        elif map_type == "places":
            edge_entry = db_interface.get_paths(includes_any={'_id':[edge_id]})[0]
            text = db_interface.get_stext_paths(includes_any={'_id':[edge_id]})
        
        network.add_edge(
            u_of_edge=edge_entry["source"], 
            v_of_edge=edge_entry["target"], 
            # _id = edge_entry["_id"],
            **edge_entry,
            _text = text,
            _metainfo = "",
            )

    # return general network structure
    return network


################################################################################
##                                    MAIN                                    ##
################################################################################
if __name__ == "__main__":
        
    path = '/home/gartin/Documents/Fairy_tales/version_2/db/chars/'
    consistency_file = '/home/gartin/Documents/Fairy_tales/version_2/db/consistency_checks/CHAR_entry.json'
    chars = Characters(folder_path=path, consistency_file=consistency_file)
    path = '/home/gartin/Documents/Fairy_tales/version_2/db/relations/'
    consistency_file = '/home/gartin/Documents/Fairy_tales/version_2/db/consistency_checks/Relation_entry.json'
    relations = Relations(folder_path=path, consistency_file=consistency_file)

    db = DBinterface(character_table=chars, 
                    relations_table=relations,
                    )


    path = '/home/gartin/Documents/Fairy_tales/version_2/db/places/'
    consistency_file = '/home/gartin/Documents/Fairy_tales/version_2/db/consistency_checks/PLACE_entry.json'
    places = Places(folder_path=path, consistency_file=consistency_file)
    path = '/home/gartin/Documents/Fairy_tales/version_2/db/paths/'
    consistency_file = '/home/gartin/Documents/Fairy_tales/version_2/db/consistency_checks/Path_entry.json'
    paths = Paths(folder_path=path, consistency_file=consistency_file)
    db = DBinterface(character_table=chars, 
                    relations_table=relations,
                    places_table=places,
                    paths_table=paths,
                    )


    # prepare character network
    char_graph = compile_map(
        db_interface=db, 
        list_of_node_ids = chars.list_ids(), 
        list_of_edge_ids = relations.list_ids(),
        map_type="characters",
        )

    # save the output
    if not isinstance(save_path, type(None)):
        json_text = network_to_json(char_graph)
        save_json(path=save_path, filename='TEST_char_map.json', json_text=json_text)
    
    # prepare character network
    place_graph = compile_map(
        db_interface=db, 
        list_of_node_ids = places.list_ids(), 
        list_of_edge_ids = paths.list_ids(),
        map_type="places",
        )

    # save the output
    if not isinstance(save_path, type(None)):
        json_text = network_to_json(place_graph)
        save_json(path=save_path, filename='TEST_place_map.json', json_text=json_text)

# ################################################################################
# ##                                  PLOT MAP                                  ##
# ################################################################################

#     if plot_map:

#         fig = go.Figure()
#         for node_id, node in graph.nodes(data=True):
#             fig.add_trace(go.Scatter(x=[node['pos'][0]], y=[node['pos'][1]],
#                                 mode='markers',
#                                 name='markers'))
            
#         fig.update_xaxes(range=[-1.5, 1.5])
#         fig.update_yaxes(range=[-1.5, 1.5])
#         fig.update_yaxes(
#             scaleanchor = "x",
#             scaleratio = 1,
#         )

#         fig.show()
        
    print("FINISHED")
    
    
