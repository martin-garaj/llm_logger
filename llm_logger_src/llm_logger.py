
import pathlib as pl
from typing import Any, Literal
import networkx as nx
import datetime as dt
import numpy as np
import copy
import io

if __name__ == "__main__":
    import sys
    import os
    import pathlib as pl
    project_root = pl.Path(os.getcwd()).absolute()
    try:
        sys.path.index(project_root)
    except ValueError:
        sys.path.append(project_root)
    project_root_in_sys = sys.path[sys.path.index(project_root)]
    print(f"TESTING: add '{project_root_in_sys}' to PYTHONPATH")

try:
    from utils.ids import NodeID, ChapterID, _NODE, _CHAPTER, \
        _EDGE
    from utils.chapters import get_chapter_ids_with_node_ids
except ImportError:
    from llm_logger_src.utils.ids import NodeID, ChapterID, _NODE, _CHAPTER, \
        _EDGE
    from llm_logger_src.utils.chapters import get_chapter_ids_with_node_ids


################################################################################
##                                 llm_logger                                 ##
################################################################################
class LLMLogger:
    
    def __init__(self,
        path:pl.Path=None,
        filename:str=None,
        **kwargs:Literal["create_path"],
        ):
        
        # sanity check
        if not isinstance(path, type(None)):
            path = pl.Path(path).resolve()
            if kwargs.get("create_path", False):
                os.makedirs(path, exist_ok=True)
            if not path.exists():
                raise RuntimeError(
                    f"path='{str(path)}', does not exist! use "\
                    f"kwargs['create_path']=True to create folder structure.")
        else:
            path = None

        self.path = path
        self.file = filename
        
        # state variables
        self._graph = nx.Graph(
            metadata=dict(time=str(self._get_timestamp())),
            )
        self.__chapter_counter = 0
        self.__node_counter = 0
        
    ############################################################################
    ##                               ATTRIBUTES                               ##
    ############################################################################        
    
    @property
    def graph(self):
        return copy.deepcopy(self._graph)
    
    ############################################################################
    ##                                 PUBLIC                                 ##
    ############################################################################
    ##------------------------------------------------------------------------##
    ##                                   log                                  ##
    ##------------------------------------------------------------------------##
    def log(self, 
            column:str="other", 
            style:str="default", 
            stack:bool=False,
            content:Any=None, 
            relates_to_node_id:NodeID=None, 
            relation_content:Any=None,
            relation_style:str="default") -> NodeID:
        """ Create a node in the log-graph, returns the nodes ID. 
            The node may be connected to previously logged node using 
            'relate_to' given the previous node ID (self-loops thus do not exists). 

        :param column: Column of the log-graph, defaults to "other"
        :param style: Category relates to the visual style of the node, 
            defaults to "default"
        :param content: Content to be displayed in the llm_logger_app, 
            defaults to None
        :param relates_to: Previous node ID to create edge between nodes, 
            defaults to None
        :param relation_content: Edge content displayed in llm_logger_app, 
            defaults to None
        :param stack: Stack successive nodes with the same column, 
            defaults to False
        :return: Unique Node ID.
        """
        
        # assure the columns names with leading & trailing '_' 
        # are reserved for internal purpose only
        column = column.strip('_')
        
        # get new node id
        self.__node_counter = self.__node_counter + 1
        node_id = NodeID(self.__node_counter)
        
        # add node
        self._graph.add_node(
            node_for_adding = node_id,
            data=dict(
                title="",
                content=content),
            metadata=dict(
                time=str(self._get_timestamp()),
                type=_NODE,
                column = column.strip('_'),
                style = style.strip('_'),
                stack = stack,
                chapter_id = ChapterID(self.__chapter_counter),
                ),
            )
        
        # add edge
        if isinstance(relates_to_node_id, NodeID):
            self._graph.add_edge(
                u_of_edge=node_id,
                v_of_edge=relates_to_node_id,
                data=dict(
                    title="",
                    content=relation_content,
                    ),
                metadata=dict(
                    time=str(self._get_timestamp()),
                    type=_EDGE,
                    style=relation_style.strip('_'),
                    ),
                )
        
        return node_id
    

    ##------------------------------------------------------------------------##
    ##                               new_chapter                              ##
    ##------------------------------------------------------------------------##
    def new_chapter(self, 
                    title:str,
                    style:str="default", 
                    content:Any=None) -> None:
        """ Create new chapter, thus partitioning the log-graph in 
            vertical manner.

        :param title: Title of the chapter displayed in ll_logger_app.
        :param content: Content to be displayed in the llm_logger_app, 
            defaults to None
        """
        # get new node id
        self.__chapter_counter = self.__chapter_counter + 1
        chapter_id = ChapterID(self.__chapter_counter)
        
        # add node
        self._graph.add_node(
            node_for_adding = chapter_id,
            data=dict(
                title=title,
                content=content),
            metadata=dict(
                time=str(self._get_timestamp()),
                type=_CHAPTER,
                style = style.strip('_'),
                ),
            )
    
    
    ##------------------------------------------------------------------------##
    ##                                  report                                ##
    ##------------------------------------------------------------------------##
    def report(self):
        chapter_ids_with_node_ids = \
            get_chapter_ids_with_node_ids(graph=self._graph)
        
        for chapter_id, node_ids in chapter_ids_with_node_ids.items():
            print(f"ChapterID = '{chapter_id}'")
            for node_id in node_ids:
                print(f"   NodeID = '{node_id}'")
        

    ##------------------------------------------------------------------------##
    ##                                   save                                 ##
    ##------------------------------------------------------------------------##
    def save(self, 
            path:str=None, 
            filename:str=None, 
            format="gml", 
            **kwargs,
        ) -> None:
        
        # parh
        if isinstance(path, type(None)):
            if isinstance(self.path, type(None)):
                raise RuntimeError(
                    f"'path' parameter is required if not provided when "\
                    f"LLMLogger is created!")
            else:
                path = self.path
        else:
            path = pl.Path(path).resolve()
            if kwargs.get("create_path", False):
                os.makedirs(path, exist_ok=True)
            if not path.exists():
                raise RuntimeError(
                    f"path='{str(path)}', does not exist! use "\
                    f"kwargs['create_path']=True to create folder structure.")
        # filename
        if isinstance(filename, type(None)):
            if isinstance(self.filename, type(None)):
                raise RuntimeError(
                    f"'filename' parameter is required if not provided when "\
                    f"LLMLogger is created!")
            else:
                filename = self.filename
        
        def default_stringizer(value:Any) -> str:
            import re
            if isinstance(value, type(None)):
                return ""
            if isinstance(value, NodeID):
                return str(value)
            if isinstance(value, ChapterID):
                return str(value)
            if isinstance(value, list):
                return str(value)
            if isinstance(value, str):
                return value
            raise ValueError(
                f"default_stringizer undefined conversion for "\
                f"type(value)='{type(value)}'!")
            
        # save
        if str(format).lower() == "gml":
            nx.write_gml(
                G=self._graph, 
                path=pl.Path(path, str(filename)+".gml"),
                stringizer=kwargs.get("stringizer", default_stringizer),
            )
        elif str(format).lower() == "dot":
            nx.write_dot(
                G=self._graph, 
                path=pl.Path(path, str(filename)+".dot"),
            )
        else:
            nx.write_gml(
                G=self._graph, 
                path=pl.Path(path, str(filename)+".gml"),
                stringizer=kwargs.get("stringizer", default_stringizer),
            )
            raise TypeError(
                f"Format='{format}', but valid formats=['gml', 'dot']! The graph "\
                f"was saved as {str(pl.Path(path, str(filename)+'.gml'))} "\
                f"to prevent data-loss.")


    ##------------------------------------------------------------------------##
    ##                                   load                                 ##
    ##------------------------------------------------------------------------##
    def load(self,
             path_or_buffer:Any,
             filename:str=None,
             **kwargs,
        ) -> nx.Graph: 

        # path or buffer
        suffix = ""
        if isinstance(path_or_buffer, io.BytesIO):
            path = path_or_buffer
            if not isinstance(filename, type(None)):
                suffix = str(pl.Path(filename).suffix).replace(".", "").lower()
        else:
            path = pl.Path(path_or_buffer)
            suffix = str(path.suffix).replace(".", "").lower()
        # default format
        if suffix == "":
            suffix = "gml"
                
        # read
        if suffix == "gml":
            graph = nx.read_gml(
                path = path,
                destringizer=kwargs.get("destringizer", None),
            )
        elif suffix == "dot":
            nx.read_dot(
                path = path,
            )
        else:
            graph = nx.read_gml(
                path = path,
                destringizer=kwargs.get("destringizer", None),
            )
        
        return graph
    

    ############################################################################
    ##                                PRIVATE                                 ##
    ############################################################################
    def _test(self, 
            num_nodes:int=10, 
            num_chapters:int=5, 
            num_columns:int=3, 
            connectivity:float=0.333) -> nx.Graph:
        
        with open(__file__, "r") as this_file:
            text = this_file.read()
        len_text = len(text)
        
        rng = np.random.default_rng(num_nodes+num_chapters+num_columns)
        letters = list(map(chr, range(65, 90)))
        styles=["default", "decision", "success", "failure", "error"]
        
        def rnd_elem(array, max:int=None) -> int:
            if len(array) == 0:
                return None
            if max is None:
                idx = rng.integers(low=0, high=len(array), size=1)[0]
                return array[idx]
            else:
                if max > len(array):
                    print(array)
                    raise ValueError(f"max={max}, but maximum is {len(array)}!")
                idx = rng.integers(low=0, high=max, size=1)[0]
                return array[idx]
            
            
        if num_columns > len(letters):
            raise ValueError(
                f"Max. supported num_columns={len(letters)}, "\
                f"but {num_columns} are required!")

        count_nodes = 0
        count_chapters = 0
        node_ids = list()
    
        for chapter_idx in range(num_chapters):
            count_chapters = count_chapters + 1
            chapter_title = f"{chapter_idx+1}." + rnd_elem(letters)
            self.new_chapter(title = chapter_title)
            
            # last chapter
            if chapter_idx == num_chapters-1:
                new_nodes = num_nodes - count_nodes
            else:
                max_new_nodes = int((num_nodes - count_nodes - count_chapters) / 2)
                max_new_nodes = max_new_nodes if max_new_nodes > 0 else 0
                new_nodes = rng.integers(low=0, high=max_new_nodes+1, size=1)[0]
                
            for node_idx in range(new_nodes):
                node_id = self.log(
                    column=rnd_elem(letters, max=num_columns), 
                    style=rnd_elem(styles), 
                    stack=rnd_elem([True, False]),
                    content=text[0:rng.integers(low=1, high=len_text, size=1)[0]], 
                    relates_to_node_id=rnd_elem(node_ids) if rng.random() < connectivity else None, 
                    relation_content=None,
                )
                node_ids.append(node_id)
                count_nodes = count_nodes + 1
    
        return self._graph

    def _get_timestamp(self) -> dt.datetime.timestamp:
        return dt.datetime.timestamp(dt.datetime.now())

################################################################################
##                                    TESTS                                   ##
################################################################################
if __name__ == "__main__":
    
    logger = LLMLogger()
    
    logger._test(num_nodes=20, num_chapters=3, num_columns=4, connectivity=0.5)
    logger.report()
    logger.save(path='/home/gartin/Documents/Projects/AlphaPrompt/Fairy_tales/Projects/llm_logger/__data', 
                filename='test_graph_log', 
                format='gml',
                )
    