from typing import List, Dict, Tuple, Any, Union
import networkx as nx

try:
    from utils.ids import NodeID, ChapterID, EdgeID, _NODE, \
        _CHAPTER, _EDGE, valid_node_id, valid_chapter_id, edge_id_to_vertex_ids
    from utils.chapters import get_chapter_ids_with_node_ids
except ImportError:
    from llm_logger_src.utils.ids import NodeID, ChapterID, EdgeID, _NODE, \
        _CHAPTER, _EDGE, valid_node_id, valid_chapter_id, edge_id_to_vertex_ids
    from llm_logger_src.utils.chapters import get_chapter_ids_with_node_ids
        
        

##------------------------------------------------------------------------##
##                               valid_graph                              ##
##------------------------------------------------------------------------##
def valid_graph() -> bool:
    """ Validate graph consistency

    :return: _description_
    """
    pass        


##------------------------------------------------------------------------##
##                               get_columns                              ##
##------------------------------------------------------------------------##
def get_columns(graph:nx.Graph) -> List[str]:
    """ Get a list of columns present in the graph.

    :return: List of columns present in the graph.
    """
    columns = list()
    for _, node_data in graph.nodes(data=True):
        if node_data['metadata']['type'] == _NODE:
            columns.append(node_data['metadata']['column'])
    return list(set(columns))


##------------------------------------------------------------------------##
##                             get_chapter_ids                            ##
##------------------------------------------------------------------------##
def get_chapter_ids(graph:nx.Graph) -> List[ChapterID]:
    """ Collects all chapter_ids within graph.

    :return: _description_
    """
    chapter_ids_with_node_ids = get_chapter_ids_with_node_ids(graph)
    chapter_ids = list(chapter_ids_with_node_ids.keys())
    chapter_ids.sort()
    
    return chapter_ids


##------------------------------------------------------------------------##
##                              get_node_data                             ##
##------------------------------------------------------------------------##
def get_node_data(graph:nx.Graph, node_id:NodeID) \
        -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if not valid_node_id(node_id):
        raise ValueError(f"node_id='{node_id}' is not valid!")
    node_data = graph.nodes(data=True)[node_id]
    return node_data['data'], node_data['metadata']


##------------------------------------------------------------------------##
##                             get_chapter_data                           ##
##------------------------------------------------------------------------##
def get_chapter_data(graph:nx.Graph, chapter_id:ChapterID) \
        -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if not valid_chapter_id(chapter_id):
        raise ValueError(f"chapter_id='{chapter_id}' is not valid!")
    chapter_data = graph.nodes(data=True)[chapter_id]
    return chapter_data['data'], chapter_data['metadata']


##------------------------------------------------------------------------##
##                              get_vertex_data                           ##
##------------------------------------------------------------------------##
def get_vertex_data(graph:nx.Graph, vertex_id:Union[NodeID, ChapterID]) \
        -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if not (valid_chapter_id(vertex_id) or valid_node_id(vertex_id)):
        raise ValueError(f"vertex_id='{vertex_id}' is not valid!")
    vertex_data = graph.nodes(data=True)[vertex_id]
    return vertex_data['data'], vertex_data['metadata']

##------------------------------------------------------------------------##
##                               get_edge_data                            ##
##------------------------------------------------------------------------##
def get_edge_data(graph:nx.Graph, edge_id:Union[EdgeID, str]) \
        -> Tuple[Dict[str, Any], Dict[str, Any]]:
    node_id_0, node_id_1 = edge_id_to_vertex_ids(id=edge_id)
    edge_data = graph.get_edge_data(
        u=node_id_0, 
        v=node_id_1, 
        default=graph.get_edge_data(
            u=node_id_1, 
            v=node_id_0, 
            default=None),
        )
    if isinstance(edge_data, type(None)):
        raise ValueError(f"edge_id='{edge_id}' doesn't exist!")
    return edge_data['data'], edge_data['metadata']


##------------------------------------------------------------------------##
##                             get_node_column                            ##
##------------------------------------------------------------------------##
def get_node_column(graph:nx.Graph, node_id:NodeID) -> str:
    if not valid_node_id(node_id):
        raise ValueError(f"node_id='{node_id}' is not valid!")
    _, node_data = graph.nodes[node_id]
    return node_data['metadata']['column']
