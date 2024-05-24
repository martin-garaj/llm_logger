from typing import Union, List, Any

# try:
#     from .ids import NodeID, ChapterID, EdgeID
# except ImportError:
#     from llm_logger_src.utils.ids import NodeID, ChapterID, EdgeID


_UNSELECTED = 0
_SELECTED = 1
_HIDDEN = 2

_VALID_STATES = {
    _UNSELECTED : f"_UNSELECTED", 
    _SELECTED : f"_SELECTED", 
    _HIDDEN : f"_HIDDEN",
}



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                              CustomDataStruct                              ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
class CustomDataStruct:
    
    def __init__(
        self,
        index:str, #Union[NodeID, ChapterID, EdgeID],
        related_indices:List=list(), #[Union[NodeID, ChapterID, EdgeID]],
        state:int=_UNSELECTED,
        content:Any=list(),
    ):
        self.metadata = self._MetaData(
            index = index,
            related_indices = related_indices,
            state = state,
        )
        self.data = self._Data(
            content=content
        )
        
    def __str__(self):
        string = \
            f"CustomDataStruct\n"\
            f"   ├── metadadata:\n"\
            f"   |  ├── index  :           {self.metadata.index}\n"\
            f"   |  ├── related_indices  : {self.metadata.related_indices} \n" \
            f"   |  └── state  :           {self.metadata.state} \n" \
            f"   └── data : '{str(self.data.content)[0:15]}'"
        return string
            
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    ##                               __MetaData                               ##
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    class _MetaData:
        def __init__(
            self,
            index:int,
            related_indices:List[int],
            state:int=_UNSELECTED,
        ):
            
            self._index = index
            
            self._check_related_indices(related_indices)
            self._related_indices = related_indices
            
            self._check_state(state)
            self._state = state
        
        
        
        ############################## IMMUTABLE ###############################
        @property
        def index(self):
            return self._index

        ############################### MUTABLE ################################
        @property
        def state(self):
            return self._state
        @state.setter
        def state(self, value):
            self._check_state(value)
            self._state = value
            
        @property
        def related_indices(self):
            return self._related_indices
        @related_indices.setter
        def related_indices(self, value):
            self._check_related_indices()
            self._related_indices = value


        ############################## FUNCTIONS ###############################
        def _check_state(self, value):
            if value not in _VALID_STATES.keys():
                raise ValueError(\
                    f"Valid 'state' values = {list(_VALID_STATES.values())}, "\
                    f"but '{value}' was provided!")
                
        def _check_related_indices(self, value):
            if not isinstance(value, list):
                raise TypeError(
                    f"related_indices requires type {type(list)} but "\
                    f"{type(value)} was provided!")
            for _value in value:
                if not isinstance(_value, int):
                    raise TypeError(
                        f"related_indices must include type {type(int)} only "\
                        f"but value={_value} {type(_value)} was provided!")
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    ##                                 __Data                                 ##
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    class _Data:
        def __init__(
            self,
            content:Any=list(),
        ):
            self._content = content
        ############################## IMMUTABLE ###############################
        @property
        def content(self):
            return self._content    
    


################################################################################
##                                    TEST                                    ##
################################################################################
if __name__ == "__main__":
    
    import json
    print(_VALID_STATES)
    
    customdata = CustomDataStruct(
        index = 1, 
        related_indices = [2, 3, 4],
        state=_UNSELECTED,
        # content=[[['some text here']]],
        )
    
    
    print(json.dumps(customdata))
    
    print(customdata)