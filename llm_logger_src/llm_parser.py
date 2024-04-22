""" Parser for graph produced by logger.

Expected graph structure:

graph
    ├── node_for_adding : str/NodeID
    ├── nodes
    │   └── data
    │   │   └── content
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

:raises ValueError: _description_
:raises ValueError: _description_
:return: _description_
"""

import networkx as nx
import pandas as pd
from plotly import graph_objects as go
from typing import Tuple, Dict, Any, Union, List


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
    from utils.ids import NodeID, ChapterID, EdgeID, _NODE, \
        _CHAPTER, _EDGE, valid_node_id, valid_chapter_id, edge_id_to_vertex_ids
    from utils.chapters import get_chapter_ids_with_node_ids
    from assets.styles import LAYOUT_DEFAULT_STYLE, \
        XAXES_DEFAULT_STYLE, YAXES_DEFAULT_STYLE, NODE_DEFAULT_STYLES, \
        CHAPTER_DEFAULT_STYLES
    from assets.sizing import DEFAULT_SIZING
    from utils.graphics import _get_node_trace, \
        _get_chapter_trace, _get_edge_trace
except ImportError:
    from llm_logger_src.utils.ids import NodeID, ChapterID, EdgeID, _NODE, \
        _CHAPTER, _EDGE, valid_node_id, valid_chapter_id, edge_id_to_vertex_ids
    from llm_logger_src.utils.chapters import get_chapter_ids_with_node_ids
    from llm_logger_src.assets.styles import LAYOUT_DEFAULT_STYLE, \
        XAXES_DEFAULT_STYLE, YAXES_DEFAULT_STYLE, NODE_DEFAULT_STYLES, \
        CHAPTER_DEFAULT_STYLES
    from llm_logger_src.assets.sizing import DEFAULT_SIZING
    from llm_logger_src.utils.graphics import _get_node_trace, \
        _get_chapter_trace, _get_edge_trace
    
_EXTRA_COLUMN = "__extra__"

################################################################################
##                                 llm_parser                                 ##
################################################################################
class llm_parser:
    """ LLM_PARSER
        Should keep internal track of traces in the figure, then it is a 
        matter of indexing to change style of a trace. 
        
        Internal tracks can be a DataFrame. For nodes, it will preserve:
            x - center
            y - center
            stack - bool
            style - str (name of the style)
    
    """
    
    def __init__(self, 
                graph:nx.Graph,
                layout_style:Dict[str, Dict[str, Any]] = None,
                xaxes_style:Dict[str, Dict[str, Any]] = None,
                yaxes_style:Dict[str, Dict[str, Any]] = None,
                node_styles:Dict[str, Dict[str, Any]] = None,
                chapter_styles:Dict[str, Dict[str, Any]] = None,
                **kwargs,
            ):
        # internal variable
        self.graph = graph
        # adjust graph
        self._add_start_end_chapter(start_title="START", end_title="END")
        
        # default/custom style
        self.layout_style = LAYOUT_DEFAULT_STYLE if isinstance(layout_style, type(None)) else layout_style
        self.xaxes_style = XAXES_DEFAULT_STYLE if isinstance(xaxes_style, type(None)) else xaxes_style
        self.yaxes_style = YAXES_DEFAULT_STYLE if isinstance(yaxes_style, type(None)) else yaxes_style
        self.node_styles = NODE_DEFAULT_STYLES if isinstance(node_styles, type(None)) else node_styles
        self.chapter_styles = CHAPTER_DEFAULT_STYLES if isinstance(chapter_styles, type(None)) else chapter_styles

        # provided sizing variables
        self.chapter_height = kwargs.get('chapter_height', DEFAULT_SIZING['chapter_height'])
        self.node_height = kwargs.get('node_height', DEFAULT_SIZING['node_height'])
        self.node_step = kwargs.get('node_step', DEFAULT_SIZING['node_step'])
        self.chapter_step = kwargs.get('chapter_step', DEFAULT_SIZING['chapter_step'])
        self.margin_rel_col = kwargs.get('margin_rel_col', DEFAULT_SIZING['margin_rel_col'])
        self.node_width_rel_col = kwargs.get('node_width_rel_col', DEFAULT_SIZING['node_width_rel_col'])
        self.chapter_width_rel_fig = kwargs.get('chapter_width_rel_fig', DEFAULT_SIZING['chapter_width_rel_fig'])
        self.window_height = kwargs.get('window_heigh', DEFAULT_SIZING['window_height'])
        
        # private variables
        self._initialize_private_variables(requested_column_order=None, raise_error=True)
        # self.__x = 0
        # self.__y = 0
        # self.__stack = False
        # self.__stack_hop = False
        # self.__column = ''
        # self.__column_order = \
        #     self._set_column_order(requested_column_order=None)
        # self.__column_positions, self.max_column_width = \
        #     self._assign_column_position()
        # self.__vertex_positions = \
        #     self._assign_vertex_positions()     
        # self.__partitioned_vertices, self.__partitions = \
        #     self._assign_vertex_partitions( 
        #         vertical_window = self.window_height,
        #         include_connected_edges=True,
        #     )
        # self.__partitioned_edges = \
        #     self._assign_edge_partitions(
        #         partitioned_vertices=self.__partitioned_vertices,
        #     )
        # self.__partitioned_traces = \
        #     self._get_partitioned_traces(
        #         partitioned_edges=self.__partitioned_edges,
        #         partitioned_vertices=self.__partitioned_vertices,
        #     )
        
        # # derived variables
        # self.node_width = self.max_column_width * self.node_width_rel_col     
        
        
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
        # # reset internal state
        # self.__x = 0
        # self.__y = 0
        # self.__stack = False
        # self.__stack_hop = False
        # self.__column = ''
        # # re-assign column order, columns positions, vertex positions,
        # # vertex partitioning and edge partitioning
        # self.__column_order = self._set_column_order(
        #     requested_column_order=requested_column_order,
        #     raise_error=False,
        #     )
        # self.__column_positions, self.max_column_width = \
        #     self._assign_column_position()
        # self.__vertex_positions =  self._assign_vertex_positions()     
        # self.__partitioned_vertices, self.__partitions = \
        #     self._assign_vertex_partitions( 
        #         vertical_window = self.window_height,
        #         include_connected_edges=True,
        #     )
        # self.__partitioned_edges = \
        #     self._assign_edge_partitions(
        #         partitioned_vertices=self.__partitioned_vertices,
        #     )
        # self.__partitioned_traces = self._get_partitioned_traces(
        #         partitioned_edges=self.__partitioned_edges,
        #         partitioned_vertices=self.__partitioned_vertices,
        #     )    
            
        # self.node_width = self.max_column_width * self.node_width_rel_col
        
    ##------------------------------------------------------------------------##
    ##                                  report                                ##
    ##------------------------------------------------------------------------##
    def report(self):
        # __column_order
        print(f"->   column order: ===========================================")
        column_order = "->      "
        for column in self.__column_order:
            column_order = column_order + f"{column:<10}"
        print(column_order)
        print(f"->")
        print(f"->   column positions: =======================================")
        print(f"->      column    center    width")
        for column, position in self.__column_positions.items():
            print(f"->       {column:<9} {position['center']:<9.2f} {position['width']:<9.2f}")
        print(f"->")
        print(f"->   vertex positions: =======================================")
        str_vertex_position = "->      "\
            +self.__vertex_positions.to_string().replace('\n', '\n->      ')
        print(str_vertex_position)
        print(f"->")
        print(f"->   partitioned vertices: ===================================")
        str_partitioned_vertices = "->      "\
            +self.__partitioned_vertices.to_string().replace('\n', '\n->      ')
        print(str_partitioned_vertices)
        print(f"->   partitioned edges: ======================================")
        str_partitioned_edges = "->      "\
            +self.__partitioned_edges.to_string().replace('\n', '\n->      ')
        print(str_partitioned_edges)
        print(f"->")
        print(f"->   partitioned traces: =====================================")
        str_partitioned_traces = "->      "\
            +self.__partitioned_traces.to_string().replace('\n', '\n->      ')
        print(str_partitioned_traces)
        print(f"->")
        print(f"->   partitions: =============================================")
        str_partitions = "->      "\
            +self.__partitions.to_string().replace('\n', '\n->      ')
        print(str_partitions)
            
    
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
    def get_columns(self) -> List[str]:
        """ Get a list of columns present in the graph.

        :return: List of columns present in the graph.
        """
        columns = list()
        for _, node_data in self.graph.nodes(data=True):
            if node_data['metadata']['type'] == _NODE:
                columns.append(node_data['metadata']['column'])
        return list(set(columns))
    
    
    ##------------------------------------------------------------------------##
    ##                             get_chapter_ids                            ##
    ##------------------------------------------------------------------------##
    def get_chapter_ids(self) -> List[ChapterID]:
        """ Collects all chapter_ids within graph.

        :return: _description_
        """
        chapter_ids_with_node_ids = get_chapter_ids_with_node_ids(self.graph)
        chapter_ids = list(chapter_ids_with_node_ids.keys())
        chapter_ids.sort()
        
        return chapter_ids
    
    
    ##------------------------------------------------------------------------##
    ##                              get_node_data                             ##
    ##------------------------------------------------------------------------##
    def get_node_data(self, node_id:NodeID) \
            -> Tuple[Dict[str, Any], Dict[str, Any]]:
        node_data = self.graph.nodes(data=True)[node_id]
        return node_data['data'], node_data['metadata']
    
    
    ##------------------------------------------------------------------------##
    ##                             get_chapter_data                           ##
    ##------------------------------------------------------------------------##
    def get_chapter_data(self, chapter_id:ChapterID) \
            -> Tuple[Dict[str, Any], Dict[str, Any]]:
        chapter_data = self.graph.nodes(data=True)[chapter_id]
        return chapter_data['data'], chapter_data['metadata']
    
    
    ##------------------------------------------------------------------------##
    ##                              get_vertex_data                           ##
    ##------------------------------------------------------------------------##
    def get_vertex_data(self, vertex_id:Union[NodeID, ChapterID]) \
            -> Tuple[Dict[str, Any], Dict[str, Any]]:
        vertex_data = self.graph.nodes(data=True)[vertex_id]
        return vertex_data['data'], vertex_data['metadata']
    
    
    ##------------------------------------------------------------------------##
    ##                             get_node_column                            ##
    ##------------------------------------------------------------------------##
    def get_node_column(self, node_id:NodeID) -> str:
        _, node_data = self.graph.nodes[node_id]
        return node_data['metadata']['column']

    
    # def render_graph(self, partition_name:str=None):
    #     """ Render the vertices (nodes & chapters) connected with edges. 
    #         Only single partition can be specified.
    #     """
        
        
        
    
    
    ############################################################################
    ##                                 PRIVATE                                ##
    ############################################################################
    ##------------------------------------------------------------------------##
    ##                            _set_column_order                           ##
    ##------------------------------------------------------------------------##
    def _add_start_end_chapter(self, 
                               start_title:str="START", 
                               end_title:str="END", 
                               raise_error:bool=True):
        
        # check whether start & end chapters are already included
        chapter_ids = self.get_chapter_ids()
        
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
        columns = self.get_columns()
        
        if isinstance(requested_column_order, type(None)):
            # default order (alphabetically sorted)
            columns.sort()
            ordered_columns = columns
        else:
                    
            # for column in columns:
            #     if column in requested_column_order:
            #         ordered_columns.append(requested_column_order)
            #     else:
            #         extra_column_required = True
                
            # if extra_column_required:
            #     ordered_columns.append(_EXTRA_COLUMN)
                
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
                _, metadata = self.get_node_data(node_id)
                
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
            
        self.node_width = self.max_column_width * self.node_width_rel_col


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
            
        _partitioned_edges = partitioned_edges.copy()
        
        
        
        _partitioned_edges['id'] = _partitioned_edges.apply( \
            lambda row: EdgeID(row['id_0'], row['id_1']), 
            axis=1,
        )
        
        # _partitioned_edges['id'] = \
        #     list(tuple(sorted(item)) for item in \
        #         zip(partitioned_edges['id_0'], partitioned_edges['id_1']))
        _partitioned_edges.drop(columns=['id_0', 'id_1'], inplace=True)
        _partitioned_edges['type'] = _EDGE
        
        _partitioned_vertices = partitioned_vertices.copy()
        _partitioned_vertices['type'] = None
        
        
        mask_node = _partitioned_vertices['id'].apply(valid_node_id)
        _partitioned_vertices.loc[mask_node,'type'] = _NODE
        mask_chapter = _partitioned_vertices['id'].apply(valid_chapter_id)
        _partitioned_vertices.loc[mask_chapter,'type'] = _CHAPTER

        partitioned_traces = pd.concat([_partitioned_edges, _partitioned_vertices])
        
        return partitioned_traces

    ##------------------------------------------------------------------------##
    ##                               _draw_edge                               ##
    ##------------------------------------------------------------------------##
    # def _draw_edge_trace(edge_id:x_start:float, y_start:float, x_end:float, y_end:float, 
    #                 width:float, style:Dict[str, Any], raise_error:bool=True,
    #                 )


    ##------------------------------------------------------------------------##
    ##                              _render_edge                              ##
    ##------------------------------------------------------------------------##
    def _render_edge():
        pass


    ##------------------------------------------------------------------------##
    ##                             _render_vertex                             ##
    ##------------------------------------------------------------------------##
    def _render_vertex(self, vertex_id:Union[NodeID, str]) -> go.Scatter:
        """ Generates a trace

        :param data: DataFrame assigning every vertex 
            into a partition (partitions overlap)
        :return: DataFrame assigning every edge 
            into a partition (partitions overlap)
        """
        data, metadata = self.get_vertex_data(vertex_id=vertex_id)
        x = self.__vertex_positions.at[vertex_id, 'x']
        y = self.__vertex_positions.at[vertex_id, 'y']
        
        if self.__vertex_positions.at[vertex_id, 'type'] == _NODE:
            trace = _get_node_trace(
                x=x,
                y=y,
                width=parser.node_width,
                height=parser.node_height,
                style=NODE_DEFAULT_STYLES[metadata['style']],
            )
        elif self.__vertex_positions.at[vertex_id, 'type'] == _CHAPTER:
            trace = _get_chapter_trace(
                x=x,
                y=y,
                width=parser.node_width,
                height=parser.node_height,
                style=NODE_DEFAULT_STYLES[metadata['style']],
            )
        else:
            raise ValueError(
                f"vertex_id='{vertex_id}' is of unknown vertex type!")
            
        return trace

    
    ##------------------------------------------------------------------------##
    ##                              _render_graph                             ##
    ##------------------------------------------------------------------------##    
    def _render_graph():
        pass
    
    
    
    # ##------------------------------------------------------------------------##
    # ##                               _draw_chapter                               ##
    # ##------------------------------------------------------------------------##
    # def _render_node_trace(self, node_id:Union[NodeID, str]) -> go.Scatter:
    #     """ Generates a trace

    #     :param data: DataFrame assigning every vertex 
    #         into a partition (partitions overlap)
    #     :return: DataFrame assigning every edge 
    #         into a partition (partitions overlap)
    #     """
    #     data, metadata = self.get_node_data(node_id=node_id)
    #     x = self.__vertex_positions.at[node_id, 'x']
    #     y = self.__vertex_positions.at[node_id, 'y']
        
    #     trace = _get_node_trace(
    #         x=x,
    #         y=y,
    #         width=parser.node_width,
    #         height=parser.node_height,
    #         style=NODE_DEFAULT_STYLES[metadata['style']],
    #     )
        
    #     return trace


################################################################################
##                                    TESTS                                   ##
################################################################################
if __name__ == "__main__":
    
    import pathlib as pl
    
    try:
        from llm_logger import llm_logger
    except ImportError:
        from llm_logger_src.llm_logger import llm_logger
        
    logger = llm_logger(
        path=pl.Path('./'),
        file='test_log.json',
    )
    
    logger.new_chapter(title = "A")
    
    first_node_id = logger.log(
        column="other", 
        style="default", 
        stack=True,
        content="This is content.", 
        relates_to_node_id=None, 
        relation_content=None,
    )
    
    last_node_id = logger.log(
        column="other", 
        style="default", 
        stack=True,
        content="This is content.", 
        relates_to_node_id=None, 
        relation_content=None,
    )
    
    last_node_id = logger.log(
        column="other", 
        style="default", 
        stack=True,
        content="This is content.", 
        relates_to_node_id=last_node_id, 
        relation_content=None,
    )
    logger.new_chapter(title = "B")
    last_node_id = logger.log(
        column="C", 
        style="default", 
        stack=True,
        content="This is content.", 
        relates_to_node_id=None, 
        relation_content=None,
    )    
    
    last_node_id = logger.log(
        column="A", 
        style="default", 
        stack=False,
        content="This is content.", 
        relates_to_node_id=last_node_id, 
        relation_content=f"Relation to '{last_node_id}'",
    )
    logger.new_chapter(title = "C")
    last_node_id = logger.log(
        column="B", 
        style="default", 
        stack=False,
        content="This is content.", 
        relates_to_node_id=first_node_id, 
        relation_content=f"Relation to '{last_node_id}'",
    )
    logger.new_chapter(title = "D")
    
    
    parser = llm_parser(graph=logger.graph)
    
    parser.report()
    
    # parser.update_column_order(requested_column_order=['A', 'B', 'C', 'other'])
    
    # import plotly.graph_objects as go 
    # fig = go.Figure() 
    # column_positions, max_column_width = parser._assign_column_position()
    
    # for column, position in column_positions.items():
    #     fig.add_vrect(
    #         x0=position['center'] - position['width']/2, #position['start'],
    #         x1=position['center'] + position['width']/2,
    #         fillcolor='green',
    #         opacity=0.1,
    #         line_width=0,
    #     )


    # # get sorted IDs (IDs are always assigned in incremental manner)
    # chapter_ids_with_node_ids = get_chapter_ids_with_node_ids(parser.graph)
    # chapter_ids = list(chapter_ids_with_node_ids.keys())
    # chapter_ids.sort()
            
    # vertex_positions =  parser._assign_vertex_positions( 
    #         chapter_ids=chapter_ids,
    #         node_ids_per_chapter=chapter_ids_with_node_ids,
    #     )

    # partitioned_vertices, partitions = parser._assign_partitions(
    #         vertical_window=1, 
    #         include_connected_edges=True,
    #     )
    


    
    
    # parser.report()
    
    # print(f"+++++++++++++++++++++++++ df_vertices ++++++++++++++++++++++++++++")
    # print(partitioned_vertices)

    # print(f"++++++++++++++++++++++++ df_partitions +++++++++++++++++++++++++++")
    # print(partitions)

    # print(vertex_positions)

    # # for id, position in vertex_positions.items():
    # for row in vertex_positions.itertuples():
    #     fig.add_trace(
    #         _get_node_trace(
    #             x=row.x,
    #             y=row.y,
    #             width=parser.node_width,
    #             height=parser.node_height,
    #             style=NODE_DEFAULT_STYLES['decision'],
    #         )
    #     )


    # fig.update_layout(
    #     yaxis = dict(autorange="reversed"),
    #     **parser.layout_style,
    # )
    # fig.update_xaxes(**parser.xaxes_style)
    # fig.update_yaxes(**parser.yaxes_style)
    # fig.show()
    
    # print(parser.graph.nodes())