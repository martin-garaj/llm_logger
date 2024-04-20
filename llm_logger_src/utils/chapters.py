
from collections import defaultdict
import networkx as nx
from typing import Dict

try:
    from .ids import NodeID, ChapterID, _NODE, _CHAPTER
except ImportError:
    from llm_logger_src.utils.ids import NodeID, ChapterID, _NODE, _CHAPTER
    
    
    

def get_chapter_ids_with_node_ids(graph:nx.DiGraph) -> Dict[ChapterID, NodeID]:
    """ Collapses the graph into chapters. Every chapter contains 
        a list of nodes within that chapter. 

    :return: _description_
    """
    chapters = defaultdict(list)
    for node_id, data in graph.nodes(data=True):
        if data['metadata']['type'] == _NODE:
            chapters[data['metadata']['chapter_id']].append(node_id)
        elif data['metadata']['type'] == _CHAPTER:
            if node_id not in chapters.keys():
                chapters[node_id] = list()
            
    
    return chapters

