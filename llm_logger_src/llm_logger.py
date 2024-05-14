
import pathlib as pl
from typing import Any, Literal
import networkx as nx
import datetime as dt
import numpy as np

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
        path:pl.Path,
        file:str,
        **kwargs:Literal["create_path", "file_rewrite", "time_format"],
        ):
        
        # sanity check
        if not path.resolve().exists() and kwargs.get("create_path", False):
            raise RuntimeError(
                f"path='{path.resolve()}', does not exists! use "\
                f"kwargs['create_path']=True to create folder structure.")
        
        # store inputs
        self.path = path.resolve()
        self.file = file
        self.file_rewrite = kwargs.get("file_rewrite", False)
        self.__time_format = kwargs.get("time_format", dt.timezone.utc)
        
        # state variables
        self.graph = nx.Graph(
            metadata=dict(time=dt.datetime.now(self.__time_format).isoformat()),
            )
        self.chapter_counter = 0
        self.node_counter = 0
        
        # # include start chapter by default
        # self.__start_chapter_included = False
        # self._start_chapter()
        
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
        self.node_counter = self.node_counter + 1
        node_id = NodeID(self.node_counter)
        
        # add node
        self.graph.add_node(
            node_for_adding = node_id,
            data=dict(
                title="",
                content=content),
            metadata=dict(
                time=dt.datetime.now(self.__time_format).isoformat(),
                type=_NODE,
                column = column.strip('_'),
                style = style.strip('_'),
                stack = stack,
                chapter_id = ChapterID(self.chapter_counter),
                ),
            )
        
        # add edge
        if isinstance(relates_to_node_id, NodeID):
            self.graph.add_edge(
                u_of_edge=node_id,
                v_of_edge=relates_to_node_id,
                data=dict(
                    title="",
                    content=relation_content,
                    ),
                metadata=dict(
                    time=dt.datetime.now(self.__time_format).isoformat(),
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
        self.chapter_counter = self.chapter_counter + 1
        chapter_id = ChapterID(self.chapter_counter)
        
        # add node
        self.graph.add_node(
            node_for_adding = chapter_id,
            data=dict(
                title=title,
                content=content),
            metadata=dict(
                time=dt.datetime.now(self.__time_format).isoformat(),
                type=_CHAPTER,
                style = style.strip('_'),
                ),
            )
    
    
    ##------------------------------------------------------------------------##
    ##                                  report                                ##
    ##------------------------------------------------------------------------##
    def report(self):
        chapter_ids_with_node_ids = \
            get_chapter_ids_with_node_ids(graph=self.graph)
        
        for chapter_id, node_ids in chapter_ids_with_node_ids.items():
            print(f"ChapterID = '{chapter_id}'")
            for node_id in node_ids:
                print(f"   NodeID = '{node_id}'")
        
        
    ############################################################################
    ##                                PRIVATE                                 ##
    ############################################################################
    def _test(self, num_nodes:int=10, num_chapters:int=5, num_columns:int=3, connectivity:float=0.333):
        
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
        
        # print(__file__)
        
        # self.new_chapter(title = "A")
        
        # first_node_id = self.log(
        #     column="other", 
        #     style="default", 
        #     stack=True,
        #     content="This is content.", 
        #     relates_to_node_id=None, 
        #     relation_content=None,
        # )
        
        # last_node_id = self.log(
        #     column="other", 
        #     style="default", 
        #     stack=True,
        #     content="This is content.", 
        #     relates_to_node_id=None, 
        #     relation_content=None,
        # )
        
        # last_node_id = self.log(
        #     column="other", 
        #     style="default", 
        #     stack=True,
        #     content="This is content.", 
        #     relates_to_node_id=last_node_id, 
        #     relation_content=None,
        # )
        # self.new_chapter(title = "B")
        # last_node_id = self.log(
        #     column="C", 
        #     style="default", 
        #     stack=True,
        #     content="This is content.", 
        #     relates_to_node_id=None, 
        #     relation_content=None,
        # )    
        
        # last_node_id = self.log(
        #     column="A", 
        #     style="default", 
        #     stack=False,
        #     content="This is content.", 
        #     relates_to_node_id=last_node_id, 
        #     relation_content=f"Relation to '{last_node_id}'",
        # )
        # self.new_chapter(title = "C")
        # last_node_id = self.log(
        #     column="B", 
        #     style="default", 
        #     stack=False,
        #     content="This is content.", 
        #     relates_to_node_id=first_node_id, 
        #     relation_content=f"Relation to '{last_node_id}'",
        # )
        
        # last_node_id = self.log(
        #     column="A", 
        #     style="default", 
        #     stack=False,
        #     content="This is content.", 
        #     relates_to_node_id=last_node_id, 
        #     relation_content=f"Relation to '{last_node_id}'",
        # )
        
        # last_node_id = self.log(
        #     column="A", 
        #     style="default", 
        #     stack=False,
        #     content="This is content.", 
        #     relates_to_node_id=last_node_id, 
        #     relation_content=f"Relation to '{last_node_id}'",
        # )
        
        # last_node_id = self.log(
        #     column="A", 
        #     style="default", 
        #     stack=False,
        #     content="This is content.", 
        #     relates_to_node_id=last_node_id, 
        #     relation_content=f"Relation to '{last_node_id}'",
        # )
        
        # last_node_id = self.log(
        #     column="C", 
        #     style="default", 
        #     stack=False,
        #     content="This is content.", 
        #     relates_to_node_id=last_node_id, 
        #     relation_content=f"Relation to '{last_node_id}'",
        # )

        return self.graph
        
################################################################################
##                                    TESTS                                   ##
################################################################################
if __name__ == "__main__":
    
    logger = LLMLogger(
        path=pl.Path('./'),
        file='test_log.json',
    )
    
    # logger.new_chapter(title = "A")
    
    # last_node_id = logger.log(
    #     column="other", 
    #     style="default", 
    #     stack=False,
    #     content="This is content.", 
    #     relates_to_node_id=None, 
    #     relation_content=None,
    # )
    
    # last_node_id = logger.log(
    #     column="other", 
    #     style="default", 
    #     stack=False,
    #     content="This is content.", 
    #     relates_to_node_id=last_node_id, 
    #     relation_content=f"Relation to '{last_node_id}'",
    # )
    
    # logger.report()
    
    
    logger._test(num_nodes=100, num_chapters=10, num_columns=10, connectivity=0.2)
    
    logger.report()