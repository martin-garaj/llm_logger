""" Parser for graph produced by logger.

Expected graph structure:

    graph
        ├── node_for_adding : str/NodeID
        ├── nodes
        │   └── data
        │   │   └── content : Any
        │   └── metadata
        |       └── time : datetime
        |       └── type : str
        |       └── column : str
        |       └── category : str
        |       └── stack : bool
        |       └── chapter_id : str/ChapterID
        └── edges
            └── u_of_edge : str/NodeID
            └── v_of_edge : str/NodeID
            └── data
                └── content
"""
if __name__ == "__main__":
    import sys
    import os
    import pathlib as pl
    file_path = pl.Path(__file__).parent
    try:
        sys.path.index(file_path)
    except ValueError:
        sys.path.append(file_path)
    project_root_in_sys = sys.path[sys.path.index(file_path)]
    print(f"TESTING: add '{project_root_in_sys}' to PYTHONPATH")

################################################################################
##                                  CONSTANTS                                 ##
################################################################################
_EXTRA_COLUMN = "__extra__"


################################################################################
##                                   IMPORTS                                  ##
################################################################################
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


import networkx as nx
import pandas as pd
from plotly import graph_objects as go
from typing import Tuple, Dict, Any, Union, List
import copy

# try:
from utils.ids import NodeID, ChapterID, EdgeID, _NODE, \
    _CHAPTER, _EDGE, valid_node_id, valid_chapter_id, edge_id_to_vertex_ids
from utils.chapters import get_chapter_ids_with_node_ids
from assets.styles import LAYOUT_STYLES, COLUMN_STYLES, \
    XAXES_STYLES, YAXES_STYLES, NODE_STYLES, CHAPTER_STYLES, EDGE_STYLES, \
    NODE_ANNOTATIONS, CHAPTER_ANNOTATIONS
from assets.sizing import DEFAULT_SIZING
from utils.traces import \
    _get_node_trace, _get_edge_trace, _get_chapter_trace, \
    _set_node_datastruct, _set_chapter_datastruct, _set_edge_datastruct, \
    _set_node_metadata, _set_edge_metadata, _get_annotation
from utils.graph import get_columns, get_chapter_ids, \
    get_node_data, get_vertex_data, get_edge_data
from utils.customdata import print_customdata
# except ImportError:
#     from llm_logger_src.utils.ids import NodeID, ChapterID, EdgeID, _NODE, \
#         _CHAPTER, _EDGE, valid_node_id, valid_chapter_id, edge_id_to_vertex_ids
#     from llm_logger_src.utils.chapters import get_chapter_ids_with_node_ids
#     from llm_logger_src.assets.styles import LAYOUT_STYLES, COLUMN_STYLES, \
#         XAXES_STYLES, YAXES_STYLES, NODE_STYLES, CHAPTER_STYLES, EDGE_STYLES, \
#         NODE_ANNOTATIONS, CHAPTER_ANNOTATIONS
#     from llm_logger_src.assets.sizing import DEFAULT_SIZING
#     from llm_logger_src.utils.traces import \
#         _get_node_trace, _get_edge_trace, _get_chapter_trace, \
#         _set_node_datastruct, _set_chapter_datastruct, _set_edge_datastruct, \
#         _set_node_metadata, _set_edge_metadata, _get_annotation
#     from llm_logger_src.utils.graph import get_columns, get_chapter_ids, \
#         get_node_data, get_vertex_data, get_edge_data
#     from llm_logger_src.utils.customdata import print_customdata


################################################################################
##                                 llm_parser                                 ##
################################################################################
class LLMLogParser:
    """ LLM_PARSER
        Should keep internal track of traces in the figure, then it is a 
        matter of indexing to change style of a trace. 
        
        Internal tracks can be a DataFrame. For nodes, it will preserve:
            x - center
            y - center
            stack - bool
            style - str (name of the style)
    
    Internal variables (can be checked via parser.report())
    
    Expected graph structure:

        graph
            ├── node_for_adding : str/NodeID
            ├── nodes
            │   └── data
            │   │   └── content : Any
            │   └── metadata
            |       └── time : str(Timestamp)
            |       └── type : str
            |       └── column : str
            |       └── category : str
            |       └── stack : bool
            |       └── chapter_id : str/ChapterID
            └── edges
                └── u_of_edge : str/NodeID
                └── v_of_edge : str/NodeID
                └── data
                    └── content    
    """
    
    def __init__(self, 
                graph:nx.Graph,
                layout_styles:Dict[str, Dict[str, Any]] = None,
                column_styles:Dict[str, Dict[str, Any]] = None,
                xaxes_styles:Dict[str, Dict[str, Any]] = None,
                yaxes_styles:Dict[str, Dict[str, Any]] = None,
                node_styles:Dict[str, Dict[str, Any]] = None,
                chapter_styles:Dict[str, Dict[str, Any]] = None,
                edge_styles:Dict[str, Dict[str, Any]] = None,
                node_annotations:Dict[str, Dict[str, Any]] = None,
                chapter_annotations:Dict[str, Dict[str, Any]] = None,
                **kwargs,
            ):
        # internal variable
        self.graph = graph
        # adjust graph
        self._add_start_end_chapter(start_title="START", end_title="END")
        
        # default/custom style
        self.layout_styles  = LAYOUT_STYLES \
            if isinstance(layout_styles, type(None)) else layout_styles
        self.column_styles  = COLUMN_STYLES \
            if isinstance(column_styles, type(None)) else column_styles
        self.xaxes_style    = XAXES_STYLES \
            if isinstance(xaxes_styles, type(None)) else xaxes_styles
        self.yaxes_style    = YAXES_STYLES \
            if isinstance(yaxes_styles, type(None)) else yaxes_styles
        # self.node_styles    = NODE_STYLES \
        #     if isinstance(node_styles, type(None)) else node_styles
        # self.chapter_styles = CHAPTER_STYLES \
        #     if isinstance(chapter_styles, type(None)) else chapter_styles
        # self.edge_styles    = EDGE_STYLES \
        #     if isinstance(edge_styles, type(None)) else edge_styles
        self.__node_styles = dict()
        self.__chapter_styles = dict()
        self.__edge_styles = dict()
        self._set_styles( 
                node_styles=node_styles, 
                chapter_styles=chapter_styles, 
                edge_styles=edge_styles, 
                required_styles=["__default__", "__default_selected__"], 
                alt_styles=["selected"],
            )
        self.node_annotations = NODE_ANNOTATIONS \
            if isinstance(node_annotations, type(None)) else node_annotations
        self.chapter_annotations = CHAPTER_ANNOTATIONS \
            if isinstance(chapter_annotations, type(None)) else chapter_annotations
        
        # provided sizing variables
        self.chapter_height = kwargs.get('chapter_height', 
                                    DEFAULT_SIZING['chapter_height'])
        self.node_height = kwargs.get('node_height', 
                                    DEFAULT_SIZING['node_height'])
        self.node_step = kwargs.get('node_step', 
                                    DEFAULT_SIZING['node_step'])
        self.chapter_step = kwargs.get('chapter_step', 
                                    DEFAULT_SIZING['chapter_step'])
        self.edge_width = kwargs.get('edge_width', 
                                    DEFAULT_SIZING['edge_width'])
        self.margin_rel_col = kwargs.get('margin_rel_col', 
                                    DEFAULT_SIZING['margin_rel_col'])
        self.node_width_rel_col = kwargs.get('node_width_rel_col', 
                                    DEFAULT_SIZING['node_width_rel_col'])
        self.chapter_width_rel_fig = kwargs.get('chapter_width_rel_fig', 
                                    DEFAULT_SIZING['chapter_width_rel_fig'])
        self.window_height = kwargs.get('window_heigh', 
                                    DEFAULT_SIZING['window_height'])
        
        # default values of private variables
        self.__partitions = None
        # private variables
        self._initialize_private_variables(
            requested_column_order=None, 
            raise_error=True,
            )
        self.figure = None
    
    ############################################################################
    ##                               ATTRIBUTES                               ##
    ############################################################################
    @property
    def chapters(self):
        if isinstance(self.__vertex_positions, type(None)):
            raise RuntimeError(f"LLMLogParser is not initialized!")
        mask = (self.__vertex_positions["type"] == _CHAPTER)
        chapters = self.__vertex_positions.loc[mask]
        chapters = chapters.drop(columns=['type'])
        titles = list()
        for chapter in chapters.itertuples():
            titles.append(self.graph.nodes[chapter.id]["data"]["title"])
        chapters = chapters.assign(title = titles)
        chapters.reset_index(drop=True, inplace=True)
        return chapters
    
    @property
    def aspect_ratio(self):
        if isinstance(self.__vertex_positions, type(None)):
            raise RuntimeError(f"LLMLogParser is not initialized!")
        return self.__y
    
    @property
    def related_traces(self):
        if isinstance(self.__partitioned_traces, type(None)):
            raise RuntimeError(f"LLMLogParser is not initialized!")

        return copy.deepcopy(self.__related_traces)
    
    @property
    def node_styles(self):
        return copy.deepcopy(self.__node_styles)
    
    @property
    def chapter_styles(self):
        return copy.deepcopy(self.__chapter_styles)    
    
    @property
    def edge_styles(self):
        return copy.deepcopy(self.__edge_styles)
    

    ############################################################################
    ##                                 PUBLIC                                 ##
    ############################################################################
    def update_column_order(self, requested_column_order:List[str]):
        """ Update column order.
        
        NOTICE: Updating the columns order can change the length of the graph 
            (e.g. merging multiple columns into _EXTRA_COLUMN). 
            Thus reordering triggers vertex positioning, which triggers 
            partition assignment.
        
        :param requested_column_order: List of columns in requested order,
            defaults to None
        """
        self._initialize_private_variables( \
                requested_column_order=requested_column_order,
                raise_error=False,
            )

    ##------------------------------------------------------------------------##
    ##                                  report                                ##
    ##------------------------------------------------------------------------##
    def report(self, 
            column_order:bool=True, 
            column_positions:bool=True, 
            vertex_positions:bool=True, 
            partitioned_vertices:bool=True,
            partitioned_edges:bool=True,
            partitioned_traces:bool=True,
            partitions:bool=True,
            related_traces:bool=True,
            chapters:bool=True,
            figure:bool=True):
        print(f"->   LLMLogParser.report() ===================================")
        print(f"->")
        # __column_order
        if column_order:
            print(f"->   LLMLogParser.__column_order =============================")
            column_order = "->      "
            for column in self.__column_order:
                column_order = column_order + f"{column:<10}"
            print(column_order)
            print(f"->")
        if column_positions:
            print(f"->   LLMLogParser.__column_positions =========================")
            print(f"->      column    center    width")
            for column, position in self.__column_positions.items():
                print(
                    f"->       {column:<9} {position['center']:<9.2f} "\
                    f"{position['width']:<9.2f}")
            print(f"->")
        if vertex_positions:
            print(f"->   LLMLogParser.__vertex_positions =========================")
            str_vertex_position = "->      "\
                +self.__vertex_positions.to_string().replace('\n', '\n->      ')
            print(str_vertex_position)
            print(f"->")
        if partitioned_vertices:
            print(f"->   LLMLogParser.__partitioned_vertices =====================")
            str_partitioned_vertices = "->      "\
                +self.__partitioned_vertices.to_string().replace('\n', '\n->      ')
            print(str_partitioned_vertices)
            print(f"->")
        if partitioned_edges:
            print(f"->   LLMLogParser.__partitioned_edges ========================")
            str_partitioned_edges = "->      "\
                +self.__partitioned_edges.to_string().replace('\n', '\n->      ')
            print(str_partitioned_edges)
            print(f"->")
        if partitioned_traces:
            print(f"->   LLMLogParser.__partitioned_traces =======================")
            str_partitioned_traces = "->      "\
                +self.__partitioned_traces.to_string().replace('\n', '\n->      ')
            print(str_partitioned_traces)
            print(f"->")
        if partitions:
            print(f"->   LLMLogParser.__partitions ===============================")
            str_partitions = "->      "\
                +self.__partitions.to_string().replace('\n', '\n->      ')
            print(str_partitions)
            print(f"->")
        if related_traces:
            print(f"->   LLMLogParser.__related_traces ===========================")
            str_related_edges = ""
            max_len = len(str(len(self.__related_traces)))
            for trace_index, related_indices in self.__related_traces.items():
                str_related_edges = str_related_edges \
                    + f"->      {str(trace_index).rjust(max_len)} : "\
                    f"[{', '.join([str(index).rjust(max_len) for index in related_indices])}]\n"
            str_related_edges = str_related_edges[0:-1]
            print(str_related_edges)
            
        if chapters:
            print(f"->   LLMLogParser.chapters ===================================")
            str_chapters = "->      "\
                +self.chapters.to_string().replace('\n', '\n->      ')
            print(str_chapters)
            print(f"->")
        if figure:
            print(f"->   LLMLogParser.figure =====================================")
            if not isinstance(self.figure, type(None)):
                skipped = False
                for idx, trace in enumerate(self.figure["data"]):
                    if idx < 3 or idx > len(self.figure["data"])-4:
                        print_customdata(trace)
                    else:
                        if not skipped:
                            print(f"->      ")
                            print(f"->      ...")
                            print(f"->      ")
                            skipped=True
            else:
                print(f"->      Figure not rendered yet!")
    
    ############################################################################
    ##                                 PRIVATE                                ##
    ############################################################################
    ##------------------------------------------------------------------------##
    ##                               _set_styles                              ##
    ##------------------------------------------------------------------------##
    def _set_styles(self, 
                node_styles:dict=None, 
                chapter_styles:dict=None, 
                edge_styles:dict=None, 
                required_styles:list=["__default__", "__default_selected__"], 
                alt_styles:list=["selected"],
            ):
        
        # set styles
        self.__node_styles    = NODE_STYLES \
            if isinstance(node_styles, type(None)) else node_styles
        self.__chapter_styles = CHAPTER_STYLES \
            if isinstance(chapter_styles, type(None)) else chapter_styles
        self.__edge_styles    = EDGE_STYLES \
            if isinstance(edge_styles, type(None)) else edge_styles
    
        _styles = dict(
            node_styles = self.__node_styles,
            chapter_styles = self.__chapter_styles,
            edge_styles = self.__edge_styles,
            
        )
        # check required fields
        for name, styles in _styles.items():
            for required_style in required_styles:
                if required_style not in styles.keys():
                    raise RuntimeError(
                        f"Provided '{name}' do not include "\
                        f"'{required_style}'! Assure all required styles "\
                        f"{required_styles} are defined!")
        
        # TODO: find a better way to check this
        # assign missing alternative styles
        temp_node_styles = copy.deepcopy(self.__node_styles)
        for style_name in temp_node_styles.keys():
            # skip required styles, as they are already present
            if style_name in required_styles:
                continue
            # check every alternative style
            for alt_style in alt_styles:
                # get alternative and default-alternative style names
                alt_style_name = f"{style_name}_{alt_style}"
                default_style_name = f"__default_{alt_style}__"
                
                # current 'style_name' is not alternative style
                style_name_not_alt = (alt_style not in style_name and "__" not in style_name)
                # alternative style is not defined
                alt_style_not_defined = \
                    (alt_style_name not in temp_node_styles.keys())
                # both conditions are TRUE
                if style_name_not_alt and alt_style_not_defined:
                    # add alternative style as a default style
                    self.__node_styles[alt_style_name] = \
                        self.__node_styles[default_style_name]
                        
        # assign missing alternative styles
        temp_chapter_styles = copy.deepcopy(self.__chapter_styles)
        for style_name in temp_chapter_styles.keys():
            # skip required styles, as they are already present
            if style_name in required_styles:
                continue
            # check every alternative style
            for alt_style in alt_styles:
                # get alternative and default-alternative style names
                alt_style_name = f"{style_name}_{alt_style}"
                default_style_name = f"__default_{alt_style}__"
                
                # current 'style_name' is not alternative style
                style_name_not_alt = (alt_style not in style_name and "__" not in style_name)
                # alternative style is not defined
                alt_style_not_defined = \
                    (alt_style_name not in temp_chapter_styles.keys())
                # both conditions are TRUE
                if style_name_not_alt and alt_style_not_defined:
                    # add alternative style as a default style
                    self.__chapter_styles[alt_style_name] = \
                        self.__chapter_styles[default_style_name]
                    
                        
        # assign missing alternative styles
        temp_edge_styles = copy.deepcopy(self.__edge_styles)
        for style_name in temp_edge_styles.keys():
            # skip required styles, as they are already present
            if style_name in required_styles:
                continue
            # check every alternative style
            for alt_style in alt_styles:
                # get alternative and default-alternative style names
                alt_style_name = f"{style_name}_{alt_style}"
                default_style_name = f"__default_{alt_style}__"
                
                # current 'style_name' is not alternative style
                style_name_not_alt = (alt_style not in style_name and "__" not in style_name)
                # alternative style is not defined
                alt_style_not_defined = \
                    (alt_style_name not in temp_edge_styles.keys())
                # both conditions are TRUE
                if style_name_not_alt and alt_style_not_defined:
                    # add alternative style as a default style
                    self.__edge_styles[alt_style_name] = \
                        self.__edge_styles[default_style_name]
                    
            
        
    ##------------------------------------------------------------------------##
    ##                            _set_column_order                           ##
    ##------------------------------------------------------------------------##
    def _add_start_end_chapter(self, 
                               start_title:str="START", 
                               end_title:str="END", 
                               raise_error:bool=True):
        
        # check whether start & end chapters are already included
        chapter_ids = get_chapter_ids(graph=self.graph)
        
        # add start node
        if ChapterID(0) not in chapter_ids:
            self.graph.add_node(
                node_for_adding = ChapterID(0),
                data=dict(
                    title=start_title),
                metadata=dict(
                    type=_CHAPTER,
                    style = "__start__",
                    ),
                )
        elif raise_error:
            raise RuntimeError(
                f"graph already includes ID for dedicated starting "\
                f"chapter '{ChapterID(0)}'")
            
        # add start node
        if ChapterID(0, last=True) not in chapter_ids:
            self.graph.add_node(
                node_for_adding = ChapterID(0, last=True),
                data=dict(
                    title=end_title),
                metadata=dict(
                    type=_CHAPTER,
                    style = "__end__",
                    ),
                )
        elif raise_error:
            raise RuntimeError(
                f"graph already includes ID for dedicated ending "\
                f"chapter '{ChapterID(0, last=True)}'")


    ##------------------------------------------------------------------------##
    ##                            _set_column_order                           ##
    ##------------------------------------------------------------------------##
    def _set_column_order(self, requested_column_order:List[str]=None, 
                         raise_error:bool=True) -> List[str]:
        """ Obtain ordered columns.

        :param requested_column_order: List of columns in requested order, 
            defaults to None
        :param raise_error: Disrupt execution on error, defaults to True
        :raises ValueError: If requested column is not found within the 
            columns present in the graph.
        :return: List of ordered columns, extra column is added in case one or 
            more requested columns are not present and raise_error=False.
        """
        # output variable
        ordered_columns = list()
        
        # columns present in the graph
        columns = get_columns(graph=self.graph)
        
        if isinstance(requested_column_order, type(None)):
            # default order (alphabetically sorted)
            columns.sort()
            ordered_columns = columns
        else:
            for requested_column in requested_column_order:
                # assure the columns names with leading & trailing '_' 
                # are reserved # for internal purpose only
                requested_column = requested_column.strip('_')
                if requested_column in columns:
                    ordered_columns.append(requested_column)
                else:
                    # requested column is not present in the graph
                    if raise_error:
                        raise ValueError(
                            f"Requested column '{requested_column}' is not "\
                            f"present in the graph columns = "\
                            f"[{', '.join(columns)}]")

            # at least one requested column was not found
            if set(ordered_columns) != set(columns):
                ordered_columns.append(_EXTRA_COLUMN)
        
        return ordered_columns    
    
    
    ##------------------------------------------------------------------------##
    ##                         _assign_column_position                        ##
    ##------------------------------------------------------------------------##
    def _assign_column_position(self) -> Dict[str, Dict[str, float]]:
        """ Assign relative position (between 0.0 and 1.0) to columns.

        :return: Dictionary of relative start and end of a column on X-axis. 
        """

        total_columns = len(self.__column_order)
        max_column_width = 1.0/total_columns
        margin = max_column_width*self.margin_rel_col
            
        column_positions = dict()
        for column_idx, column in enumerate(self.__column_order):
            center = (max_column_width/2) + (max_column_width*column_idx)
            column_positions[column] = dict(
                center = center,
                width = max_column_width - margin,
            )
            
        return column_positions, max_column_width
            
    
    ##------------------------------------------------------------------------##
    ##                        _assign_chapter_position                        ##
    ##------------------------------------------------------------------------##
    def _assign_chapter_position(self) -> None:
        self.__x = 0.5
        self.__y = self.__y + self.chapter_step
            
        # reset associated state variables
        self.__stack_hop = False
        self.__stack = False
        
        
    ##------------------------------------------------------------------------##
    ##                         _assign_node_position                          ##
    ##------------------------------------------------------------------------##
    def _assign_node_position(self, column:str, stack:bool):
        
        # check (and re-assign) column column
        if column not in self.__column_positions.keys():
            column = _EXTRA_COLUMN
        # get column center
        x_column_center = self.__column_positions[column]['center']
        
        # consecutive nodes with stacking
        if column == self.__column and self.__stack and stack:
            # hop value
            _hop_value = self.max_column_width * self.margin_rel_col
            # assign x
            if self.__stack_hop:
                self.__x = x_column_center + _hop_value
                self.__stack_hop = False
            else:
                self.__x = x_column_center - _hop_value
                self.__stack_hop = True
            # assign y (stacking means small steps)
            self.__y = self.__y + _hop_value 
        # regular nodes (no stacking)
        else:
            self.__x = x_column_center
            self.__y = self.__y + self.node_step
            
        # update internal state
        self.__stack = stack
        self.__column = column
            
        return self.__x, self.__y
        
    
    ##------------------------------------------------------------------------##
    ##                       _assign_vertex_positions                         ##
    ##------------------------------------------------------------------------##
    def _assign_vertex_positions(self, 
            chapter_ids:List[ChapterID] = None,
            node_ids_per_chapter:List[NodeID] = None,
            ) -> pd.DataFrame:
    
        # by default assign positions to all vertices in the graph
        if isinstance(chapter_ids, type(None)) and isinstance(node_ids_per_chapter, type(None)): 
            node_ids_per_chapter = get_chapter_ids_with_node_ids(self.graph)
            chapter_ids = list(node_ids_per_chapter.keys())
            chapter_ids.sort()
    
        # output structure - vertex (nodes & chapter) positions
        vertex_positions = pd.DataFrame(columns=['id', 'x', 'y'])
        
        # iterate over chapters
        for chapter_id in chapter_ids:
            self._assign_chapter_position()
            vertex_position = dict(id=[chapter_id], type=[_CHAPTER], x=[self.__x], y=[self.__y])
            vertex_positions = pd.concat(
                    [vertex_positions, pd.DataFrame(vertex_position)],
                )
            # iterate over nodes 
            for node_id in node_ids_per_chapter[chapter_id]:
                _, metadata = get_node_data(graph=self.graph, node_id=node_id)
                
                self._assign_node_position(
                    column=metadata['column'], stack=metadata['stack'])
                vertex_position = dict(id=[node_id], type=[_NODE], x=[self.__x], y=[self.__y])
                vertex_positions = pd.concat(
                        [vertex_positions, pd.DataFrame(vertex_position)],
                    )
        vertex_positions.reset_index(drop=True, inplace=True)
        return vertex_positions        


    ##------------------------------------------------------------------------##
    ##                       _assign_vertex_partitions                        ##
    ##------------------------------------------------------------------------##
    def _assign_vertex_partitions(self, 
                           vertical_window:float,
                           include_connected_edges:bool=True,
                           ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        figure        |------------------------|
        
        nodes         . ...   . .  . . ...   . .
        
        window        |-----x-----| 
                            |-----x-----|
                                  |-----x-----|
                                        |-----x-----|
                                              |-----x-----| -> may contain 
                                              nodes, but may never be activated, 
                                              because the nodes are fully 
                                              overlapped by previous window
                                              
        active area   |________| -> on purpose covers more      
                               |_____|
                                     |_____|
                                           |_____|
                                                 |_____|

        * figure - total figure length in figure units
        * window - window length in figure units, covering the whole figure in 
            overlapping manner
        * active area - every window has exactly 1 active area, active area is 
            aligned in non-overlapping manner, covering the whole figure

        :param vertical_window: Length of sliding window in figure units.
        :param include_connected_edges: Option to include nodes within 
            a partition, that are outside of the partition (by distance), 
            but are connected to the nodes within the partition.
        :return: Returns 2 pd.DataFrames:
            partitioned_vertices
                - assigns every vertex into a partition (partitions overlap)
                columns:
                    - 'id' - (ChapterID/NodeID/str) - vertex id
                    - 'partition_<counter>' (bool) - True if node with 'id' 
                        belongs to the partition, else False
            active_areas
                - describes the areas, where the respective partitions are active
                columns:
                    - 'partition' (str) - partition name 'partition_<counter>'
                    - start (float) - start on Y-axis
                    - end (float) - end on Y-axis
        
        """
        # allocate outputs
        partitioned_vertices = pd.DataFrame(
            columns=['id'], data=self.__vertex_positions['id'],
            )
        partitioned_vertices.reset_index(drop=True, inplace=True)
        active_areas = pd.DataFrame(columns=['partition', 'start', 'end'])
        
        
        last_vertex_y = self.__vertex_positions['y'].max()
        
        # internal variables
        partition_counter = 0 # counts partitions
        window_center = 0.0 # shifts with every partition

        # repeat until all nodes are assigned a partition
        while True:
            # position the window and the active area
            window_start        = window_center - vertical_window/2
            window_end          = window_center + vertical_window/2
            active_area_start   = window_start \
                if partition_counter == 0 else window_center - vertical_window/4
            active_area_end     = window_center + vertical_window/4
            
            # STOP CONDITION
            if window_start > last_vertex_y:
                # window is beyond the last vertex
                break
            
            # re-center window
            window_center = window_center + vertical_window/2
            
            # add new partition
            partition_name = f"partition_{partition_counter}"
            partition_counter = partition_counter + 1
            partitioned_vertices[partition_name] = False
            
            # add all nodes within current window to the partition
            mask = (self.__vertex_positions['y'] > window_start) \
                 & (self.__vertex_positions['y'] <= window_end)
            partitioned_vertices.loc[mask, partition_name] = True
            
            # add all nodes that are connecting from other partitions
            if include_connected_edges:
                vertex_ids = partitioned_vertices[mask]['id'].tolist()
                # print(vertex_ids)
                for vertex_id in vertex_ids:
                    # only valid nodes have edges
                    if not valid_node_id(vertex_id):
                        continue
                    for edge in self.graph.edges(vertex_id):
                        if edge[0] == vertex_id:
                            mask = (partitioned_vertices['id']==edge[1])
                        elif edge[1] == vertex_id:
                            mask = (partitioned_vertices['id']==edge[0])
                        else:
                            raise RuntimeError(
                                f"found incorrectly connected "\
                                f"edge=['{edge[0]} -> '{edge[1]}']")
                        partitioned_vertices.loc[mask,partition_name] = True
                    # for edge in self.graph.out_edges(vertex_id):
                    #     mask = (partitioned_vertices['id']==edge[1])
                    #     partitioned_vertices.loc[mask,partition_name] = True

            # append partition
            active_area = dict(
                partition=[partition_name],
                start=[active_area_start],
                end=[active_area_end])
            active_areas = pd.concat(
                [active_areas, pd.DataFrame(active_area)],
                )
        active_areas.reset_index(drop=True, inplace=True)

        return partitioned_vertices, active_areas


    ##------------------------------------------------------------------------##
    ##                        _assign_edge_partitions                         ##
    ##------------------------------------------------------------------------##
    def _assign_edge_partitions(self, 
                           partitioned_vertices:pd.DataFrame,
                           ) -> pd.DataFrame:
        """ Assigns partitions to edges according to partitioned vertices.
        

        :param partitioned_vertices: DataFrame assigning every vertex 
            into a partition (partitions overlap)
        :return: DataFrame assigning every edge into a partition 
            (partitions overlap)
        """       
        # sanity check
        if partitioned_vertices.duplicated(subset=['id']).sum() > 0:
            raise RuntimeError(
                f"partitioned_vertices have following duplicates = "\
                f"{partitioned_vertices['id'].duplicates()}")
        
        # get all columns related to partitions 'partition_<counter>'
        partition_columns = list()
        for column in partitioned_vertices.columns:
            if "partition_" in column:
                partition_columns.append(column)

        # allocate output
        partitioned_edges = \
            pd.DataFrame(columns=['id_0', 'id_1', *partition_columns])
        
        # loop though all edges 
        #    NOTICE: in_edges and out_edges give the same information, 
        #            just in reversed order)
        for edge in self.graph.edges():
            idx_0 = (partitioned_vertices['id'] == edge[0])
            idx_1 = (partitioned_vertices['id'] == edge[1])
            partitioned_node_0 = partitioned_vertices.loc[idx_0,partition_columns]
            partitioned_node_1 = partitioned_vertices.loc[idx_1,partition_columns]
            
            # partitioning is logical OR, thus the edge belongs to any 
            # partition that the underlying edge belongs to
            partitioning = \
                (partitioned_node_0.values | partitioned_node_1.values)\
                    .squeeze().tolist()
            
            # append result as a line to the output dataframe
            keys = ['id_0', 'id_1'] + partition_columns
            values = [edge[0], edge[1]] + partitioning
            values = [ [value] for value in values ]
            partitioned_edge = dict(
                zip(keys, values)
            )
            partitioned_edges = \
                pd.concat([partitioned_edges, pd.DataFrame(partitioned_edge)])
        
        partitioned_edges.reset_index(drop=True, inplace=True)

        return partitioned_edges


    ##------------------------------------------------------------------------##
    ##                      _initialize_private_variables                     ##
    ##------------------------------------------------------------------------##
    def _initialize_private_variables(self, \
            requested_column_order:List[str]=None, raise_error:bool=True,
        ):
        """ Update column order.
        
        NOTICE: Updating the columns order can change the length of the graph 
            (e.g. merging multiple columns into _EXTRA_COLUMN). 
            Thus reordering triggers vertex positioning, which triggers 
            partition assignment.
        
        :param requested_column_order: List of columns in requested order,
            defaults to None
        """
        # reset internal state
        self.__x = 0
        self.__y = 0
        self.__stack = False
        self.__stack_hop = False
        self.__column = ''
        # re-assign column order, columns positions, vertex positions,
        # vertex partitioning and edge partitioning
        self.__column_order = self._set_column_order(
            requested_column_order=requested_column_order,
            raise_error=raise_error,
            )
        self.__column_positions, self.max_column_width = \
            self._assign_column_position()
        self.__vertex_positions =  self._assign_vertex_positions()     
        self.__partitioned_vertices, self.__partitions = \
            self._assign_vertex_partitions( 
                vertical_window = self.window_height,
                include_connected_edges=True,
            )
        self.__partitioned_edges = \
            self._assign_edge_partitions(
                partitioned_vertices=self.__partitioned_vertices,
            )
        self.__partitioned_traces = self._get_partitioned_traces(
                partitioned_edges=self.__partitioned_edges,
                partitioned_vertices=self.__partitioned_vertices,
            )    
        self.__related_traces = self._get_related_traces(
            self.__partitioned_traces,
            )
        self.node_width = self.max_column_width * self.node_width_rel_col
        self.chapter_width = 1.0 * self.chapter_width_rel_fig


    ##------------------------------------------------------------------------##
    ##                        _get_partitioned_traces                         ##
    ##------------------------------------------------------------------------##
    def _get_partitioned_traces(self,
            partitioned_edges:pd.DataFrame,
            partitioned_vertices:pd.DataFrame,
            ) -> pd.DataFrame:
        
        # sanity check
        if partitioned_edges.duplicated(subset=['id_0', 'id_1']).sum() > 0:
            mask = partitioned_edges.duplicated(subset=['id_0', 'id_1'])
            raise RuntimeError(
                f"partitioned_vertices have following duplicates = "\
                f"{partitioned_edges[mask]['id_0', 'id_1']}")
        if partitioned_vertices.duplicated(subset=['id']).sum() > 0:
            mask = partitioned_vertices.duplicated(subset=['id'])
            raise RuntimeError(
                f"partitioned_vertices have following duplicates = "\
                f"{partitioned_vertices[mask]['id']}")
        
        # partition edges
        _partitioned_edges = partitioned_edges.copy()
        _partitioned_edges['id'] = _partitioned_edges.apply( \
            lambda row: EdgeID(row['id_0'], row['id_1']), 
            axis=1,
        )
        _partitioned_edges.drop(columns=['id_0', 'id_1'], inplace=True)
        _partitioned_edges['type'] = _EDGE
        
        # partition vertices
        _partitioned_vertices = partitioned_vertices.copy()
        _partitioned_vertices['type'] = None
        mask_node = _partitioned_vertices['id'].apply(valid_node_id)
        _partitioned_vertices.loc[mask_node,'type'] = _NODE
        mask_chapter = _partitioned_vertices['id'].apply(valid_chapter_id)
        _partitioned_vertices.loc[mask_chapter,'type'] = _CHAPTER

        # determine rendering order
        partitioned_traces = pd.concat([_partitioned_edges, _partitioned_vertices])
        partitioned_traces.reset_index(drop=True, inplace=True)
        
        return partitioned_traces


    ##------------------------------------------------------------------------##
    ##                          _get_related_traces                           ##
    ##------------------------------------------------------------------------##
    # TODO: check this as it seems the trace_index is incorrectly assigned or 
    # related_traces are incorrectly determined.
    def _get_related_traces(self, partitioned_traces:pd.DataFrame) -> Dict[int, List[int]]:
        
        related_traces = dict()

        def __get_node_ids_related_to_edge_id(id:EdgeID):
            node_id_0, node_id_1 = edge_id_to_vertex_ids(id=id)
            node_0_trace_index = partitioned_traces.query("id == @node_id_0").index[0]
            node_1_trace_index = partitioned_traces.query("id == @node_id_1").index[0]
            return int(node_0_trace_index), int(node_1_trace_index)
        
        for row in partitioned_traces.itertuples():
            trace_index = int(row.Index)
            related_traces[trace_index] = list()
            
            if row.type == _NODE:
                edge_ids = list(self.graph.edges(row.id))
                for edge_id in self.graph.edges(row.id):
                    # get EdgeID
                    _edge_id = EdgeID(vertex_id_0=edge_id[0], vertex_id_1=edge_id[1])
                    # get edge index
                    edge_trace_index = \
                        int(partitioned_traces.query("id == @_edge_id").index[0])
                    # get node ids of nodes connected to the EdgeID
                    node_0_trace_index, node_1_trace_index = \
                        __get_node_ids_related_to_edge_id(id=_edge_id)
                    # if edge index not in related_traces, then add
                    if edge_trace_index not in related_traces[trace_index]:
                        related_traces[trace_index].append(edge_trace_index)
                    # if node index not in related_traces and is not clicked node index, then add
                    if int(row.Index) != node_0_trace_index \
                        and node_0_trace_index not in related_traces[trace_index]:
                        related_traces[trace_index].append(node_0_trace_index)
                    if int(row.Index) != node_1_trace_index \
                        and node_1_trace_index not in related_traces[trace_index]:
                        related_traces[trace_index].append(node_1_trace_index)
            elif row.type == _EDGE:
                node_0_trace_index, node_1_trace_index = \
                    __get_node_ids_related_to_edge_id(id=row.id)
                related_traces[trace_index].append(node_0_trace_index)
                related_traces[trace_index].append(node_1_trace_index)
            else:
                continue
                
        return related_traces

    ##------------------------------------------------------------------------##
    ##                              _render_edge                              ##
    ##------------------------------------------------------------------------##
    def _render_edge(self, id:Union[EdgeID, str], trace_index:int) -> go.Scatter:
        
        # edge data
        edge_data, edge_metadata = get_edge_data(graph=self.graph, edge_id=id)
        # vertex positions
        node_id_0, node_id_1 = edge_id_to_vertex_ids(id)
        
        node_0_index = self.__vertex_positions.query("id == @node_id_0").index[0]
        node_1_index = self.__vertex_positions.query("id == @node_id_1").index[0]

        x_start = self.__vertex_positions.at[node_0_index, 'x']
        y_start = self.__vertex_positions.at[node_0_index, 'y']
        x_end = self.__vertex_positions.at[node_1_index, 'x']
        y_end = self.__vertex_positions.at[node_1_index, 'y']        
        
        # trace 
        trace_style_name = edge_metadata['style'] \
            if edge_metadata['style'] in self.chapter_styles.keys() else "__default__"
        trace = _get_edge_trace(
            x_start=x_start, 
            y_start=y_start, 
            x_end=x_end, 
            y_end=y_end, 
            width=self.edge_width, 
            style=self.edge_styles[trace_style_name],
            raise_error=True,
            )
        trace = _set_edge_datastruct(
                    trace=trace, 
                    trace_index=trace_index,
                    trace_style=trace_style_name,
                    data=edge_data, 
                    )

        return trace


    ##------------------------------------------------------------------------##
    ##                             _render_vertex                             ##
    ##------------------------------------------------------------------------##
    def _render_vertex(self, vertex_id:Union[NodeID, str], trace_index:int) -> go.Scatter:
        """ Generates a trace

        :param data: DataFrame assigning every vertex 
            into a partition (partitions overlap)
        :return: DataFrame assigning every edge 
            into a partition (partitions overlap)
        """
        data, metadata = get_vertex_data(graph=self.graph, vertex_id=vertex_id)
        
        vertex_index = int(self.__vertex_positions.query("id == @vertex_id").index[0])
        
        x = self.__vertex_positions.at[vertex_index, 'x']
        y = self.__vertex_positions.at[vertex_index, 'y']
        
        if self.__vertex_positions.at[vertex_index, 'type'] == _NODE:
            trace_style_name = metadata['style'] \
                if metadata['style'] in self.node_styles.keys() else "__default__"
            trace = _get_node_trace(
                x=x,
                y=y,
                width=self.node_width,
                height=self.node_height,
                style=self.node_styles[trace_style_name],
            )
            trace = _set_node_datastruct(
                    trace=trace, 
                    trace_index=trace_index,
                    trace_style=trace_style_name,
                    data=data, 
                    metadata=metadata,
                    excerpt_len=200,
                ) 
            annotation = _get_annotation(
                x=x,
                y=y,
                text=metadata["column"],\
                style=self.node_annotations.get(metadata['style'], self.node_annotations["__default__"]),
            )
        elif self.__vertex_positions.at[vertex_index, 'type'] == _CHAPTER:
            trace_style_name = metadata['style'] \
                if metadata['style'] in self.chapter_styles.keys() else "__default__"
            trace = _get_chapter_trace(
                x=x,
                y=y,
                width=self.chapter_width,
                height=self.chapter_height,
                style=self.chapter_styles[trace_style_name],
            )
            trace = _set_chapter_datastruct(
                    trace=trace, 
                    trace_index=trace_index,
                    trace_style=trace_style_name,
                    data=data,
                )
            annotation = _get_annotation(
                x=x,
                y=y,
                text=data["title"],
                style=self.chapter_annotations.get(metadata['style'], self.chapter_annotations["__default__"]),
            )
        else:
            raise ValueError(
                f"vertex_id='{vertex_id}' is of unknown vertex type!")
        
        return trace, annotation

    
    ##------------------------------------------------------------------------##
    ##                              _render_graph                             ##
    ##------------------------------------------------------------------------##    
    def _render_graph(self, 
                      layout_style:str="__default__", 
                      column_style:str="__default__", 
                      xaxis_style:str="__default__", 
                      yaxis_style:str="__default__",
                      ):
        
        figure_data = list()
        annotations = list()
        
        print(f"llm_parser._render_graph() -> ")
        for row in self.__partitioned_traces.itertuples():
            print(f"->   {row}")
            if row.type == _EDGE:
                trace = self._render_edge(id=row.id, trace_index=int(row.Index))
            elif row.type in [_NODE, _CHAPTER]:
                trace, annotation = self._render_vertex(vertex_id=row.id, trace_index=int(row.Index))
                annotations.append(annotation)
            else: 
                raise RuntimeError(f"unknown type='{row.type}'!")
            
            
            figure_data.append(trace)
            
        # figure object
        figure=go.Figure(
            data=figure_data, #+ annotations,
            layout=go.Layout(
                # constant settings
                showlegend=False,
                )
            )
        
        for annotation in annotations:
            figure.add_annotation(**annotation)
        
        # add additional graphics
        if not isinstance(column_style, type(None)) or column_style == "none":
            for column, position in self.__column_positions.items():
                figure.add_vrect(
                    x0=position['center'] - position['width']/2,
                    x1=position['center'] + position['width']/2,
                    **self.column_styles[column_style],
                )

        print(f"updating layout")
        figure.update_layout(
            **self.layout_styles[layout_style],
        )
        
        print(f"updating xaxes")
        # self.xaxes_style[xaxis_style]["range"] = [0, 1]
        figure.update_xaxes(
            **self.xaxes_style[xaxis_style],
        )
        
        print(f"updating yaxes")
        # self.yaxes_style[yaxis_style]["range"] = [0, self.__y]
        # print(self.yaxes_style[yaxis_style])
        figure.update_yaxes(
            **self.yaxes_style[yaxis_style],
        )

        # assign figure
        self.figure = copy.deepcopy(figure)


        # # set layout
        # self.update_figure_layout(
        #     **self.layout_styles[layout_style],
        #     xaxis=self.xaxes_style[xaxis_style],
        #     yaxis=self.yaxes_style[yaxis_style],
        # )


    ##------------------------------------------------------------------------##
    ##                           update_figure_layout                         ##
    ##------------------------------------------------------------------------##
    def update_figure_layout(self, **kwargs):
        print("update_figure_layout()=========================================")
        for key, value in kwargs.items():
            print(f"{key} : {value}")
        # print(kwargs["xaxis"])
        # print(kwargs["yaxis"])
        self.figure.update_layout(
            **kwargs,
        )


    ##------------------------------------------------------------------------##
    ##                             render_figure                              ##
    ##------------------------------------------------------------------------##
    def render_figure(self, 
                      layout_style:str="__default__", 
                      column_style:str="__default__", 
                      xaxis_style:str="__default__", 
                      yaxis_style:str="__default__",
                      ) -> go.Figure:
        self._render_graph(  
            layout_style=layout_style, 
            column_style=column_style, 
            xaxis_style=xaxis_style, 
            yaxis_style=yaxis_style,
        )
        return self.figure



################################################################################
##                                    TESTS                                   ##
################################################################################
if __name__ == "__main__":
    
    import pathlib as pl
    
    try:
        from llm_logger import LLMLogger
    except ImportError:
        from llm_logger_src.llm_logger import LLMLogger
        
    logger = LLMLogger()
    
    

    graph = nx.read_gml(
        path='/home/gartin/Documents/AlphaPrompt/Fairy_tales/Projects/__data/test_graph_log.gml')

    graph = logger.load(
        path='/home/gartin/Documents/AlphaPrompt/Fairy_tales/Projects/__data/test_graph_log.gml')

    parser = LLMLogParser(graph=graph)
    # parser = LLMLogParser(graph=logger._test(num_nodes=6, num_chapters=2, connectivity=0.9, num_columns=2))
    
    print(parser.chapters)
    
    figure = parser.render_figure()
    parser.report()
    figure.show()
