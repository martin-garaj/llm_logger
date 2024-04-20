from typing import Union

################################################################################
##                                  CONSTANTS                                 ##
################################################################################
_ID_LENGTH = 6
_NODE = "NODE_"
_CHAPTER = "CHAP_"

################################################################################
##                                   NodeID                                   ##
################################################################################
class NodeID(str):
    def __new__(cls, counter):
        if not isinstance(counter, int):
            ValueError(f"type(counter)='{type(counter)}' but 'int' is expected!")
        if counter < 0:
            ValueError(f"counter='{counter}', but counter>=0 is is expected!")
        id = _NODE + str(counter).zfill(_ID_LENGTH)
        return super(NodeID, cls).__new__(cls, id)


################################################################################
##                                  ChapterID                                 ##
################################################################################
class ChapterID(str):
    def __new__(cls, counter, last:bool=False):
        if not isinstance(counter, int):
            ValueError(f"type(counter)='{type(counter)}' but 'int' is expected!")
        if counter < 0:
            ValueError(f"counter='{counter}', but counter>=0 is is expected!")
        if last:
            id = _CHAPTER + ("9"*_ID_LENGTH)
        else:
            id = _CHAPTER + str(counter).zfill(_ID_LENGTH)
        return super(ChapterID, cls).__new__(cls, id)


################################################################################
##                                valid_node_id                               ##
################################################################################
def valid_node_id(id:Union[NodeID, str]) -> bool:
    """ Check validity of node ID.

    :param id: Node id.
    :raises TypeError: type(id) != ChapterID
    :return: True, if the id is valid, False, if the id is invalid 
        (wrong type or wrong length)
    """
    # sanity check
    if not isinstance(id, (NodeID, str)):
        raise TypeError(
            f"type(id)='{type(id)}', "\
            f"but valid values are [NodeID, str]!")
    
    return id[0:len(_NODE)] == _NODE \
                   and len(id) == (len(_NODE)+_ID_LENGTH)


################################################################################
##                              valid_chapter_id                              ##
################################################################################
def valid_chapter_id(id:Union[ChapterID, str]) -> bool:
    """ Check validity of chapter ID.

    :param id: Chapter id.
    :raises TypeError: type(id) != ChapterID
    :return: True, if the id is valid, False, if the id is invalid 
        (wrong type or wrong length)
    """
    # sanity check
    if not isinstance(id, (ChapterID, str)):
        raise TypeError(
            f"type(id)='{type(id)}', "\
            f"but valid value is ChapterID or str!")
    
    return id[0:len(_CHAPTER)] == _CHAPTER \
                   and len(id) == (len(_CHAPTER)+_ID_LENGTH)


################################################################################
##                                    TESTS                                   ##
################################################################################
if __name__ == "__main__":
    
    node_id = NodeID(counter=0)
    
    print(f"NodeID class tests:")
    print(f"type(node_id)                     = '{type(node_id)}'")
    print(f"isinstance(node_id, NodeID)       = {isinstance(node_id, NodeID)}")
    print(f"isinstance(node_id, str)          = {isinstance(node_id, str)}")
    print(f"valid_node_id(node_id)            = {valid_node_id(node_id)}")
    print(f"valid_node_id(str(node_id))       = {valid_node_id(str(node_id))}")
    print(f"valid_chapter_id(str(node_id))    = {valid_chapter_id(str(node_id))}")
    
    chapter_id = ChapterID(counter=0)
    
    print(f"ChapterID class tests:")
    print(f"type(chapter_id)                  = '{type(chapter_id)}'")
    print(f"isinstance(chapter_id, ChapterID) = {isinstance(chapter_id, ChapterID)}")
    print(f"isinstance(chapter_id, str)       = {isinstance(chapter_id, str)}")
    print(f"valid_chapter_id(chapter_id)      = {valid_chapter_id(chapter_id)}")
    print(f"valid_chapter_id(str(chapter_id)) = {valid_chapter_id(str(chapter_id))}")
    print(f"valid_node_id(str(chapter_id))    = {valid_node_id(str(chapter_id))}")
    
    
# ################################################################################
# ##                                 get_node_id                                ##
# ################################################################################
# def get_node_id(counter:int) -> str:
#     """ Generate node id based on counter.

#     :param counter: Unique counter value.
#     :return: String representing node id.
#     """
#     return __NODE_ID + str(counter).zfill(__ID_LENGTH)


# ################################################################################
# ##                               get_chapter_id                               ##
# ################################################################################
# def get_chapter_id(counter:int) -> str:
#     """ Generate chapter id based on counter.

#     :param counter: Unique counter value.
#     :return: String representing chapter id.
#     """
#     return __CHAP_ID + str(counter).zfill(__ID_LENGTH)


# ################################################################################
# ##                                  valid_id                                  ##
# ################################################################################
# def valid_id(id:str, type:Literal["chapter", "node"]) -> bool:
#     """ Check validity of the ID.

#     :param id: node id or chapter id.
#     :param type: Type of the id to be checked.
#     :raises ValueError: If wrong 'type' value.
#     :return: True, if the id is valid, False, if the id is invalid 
#         (wrong type or wrong length)
#     """
#     # sanity check
#     if not type in ["chapter", "node"]:
#         raise ValueError(
#             f"type='{type}' is invalid value, "\
#             f"valid values = ['chapter', 'node']")
    
#     # id validation
#     if not isinstance(id, str):
#         return False
#     if type == "node":
#         return id[0:len(__NODE_ID)] == __NODE_ID \
#                         and len(id) == (len(__NODE_ID)+__ID_LENGTH)
#     if type == "chapter":
#         return id[0:len(__CHAP_ID)] == __CHAP_ID \
#                         and len(id) == (len(__CHAP_ID)+__ID_LENGTH)
#     return False
    