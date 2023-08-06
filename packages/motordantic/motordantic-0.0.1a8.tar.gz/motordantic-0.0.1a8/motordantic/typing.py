from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Dict,
    List,
    Mapping,
    Set,
    Type,
    Union,
)

__all__ = (
    'MongoModelType',
    'DictStrList',
    'DictStrAny',
    'DictAny',
    'SetStr',
    'ListStr',
    'IntStr',
    'AbstractSetIntStr',
    'DictIntStrAny',
)

if TYPE_CHECKING:
    from .models import MongoModel

IntStr = Union[int, str]
DictIntStrAny = Dict[IntStr, Any]
MappingIntStrAny = Mapping[IntStr, Any]
MongoModelType = Type['MongoModel']
DictStrList = Dict[str, List]
DictStrAny = Dict[str, Any]
DictAny = Dict[Any, Any]
SetStr = Set[str]
ListStr = List[str]
AbstractSetIntStr = AbstractSet[IntStr]
ExcludeInclude = Union[AbstractSetIntStr, MappingIntStrAny, Any]
