from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Type, cast

from pydantic.fields import Field as PydanticField
from pydantic.fields import FieldInfo as PydanticFieldInfo
from pydantic.fields import ModelField, Representation, Undefined

__all__ = (
    'Field',
    'FieldInfo',
    'ComputedField',
    'computed_field',
)

if TYPE_CHECKING:
    from typing import Callable, Union

    from pydantic import BaseConfig, BaseModel
    from pydantic.class_validators import Validator
    from pydantic.fields import ModelField


class FieldInfo:
    __slots__ = ("pydantic_field_info", "db_field_name", "default")

    def __init__(
        self,
        *,
        pydantic_field_info: PydanticFieldInfo,
        db_field_name: Optional[str],
    ):
        self.pydantic_field_info = pydantic_field_info
        self.db_field_name = db_field_name


def Field(
    default: Any = Undefined,
    *,
    db_field_name: Optional[str] = None,
    default_factory: Optional[Callable[[], Any]] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    **extra: Any,
) -> Any:
    pydantic_field = PydanticField(
        default,
        default_factory=default_factory,
        # alias=db_field_name,
        title=cast(str, title),
        description=cast(str, description),
        const=cast(bool, const),
        gt=cast(float, gt),
        ge=cast(float, ge),
        lt=cast(float, lt),
        le=cast(float, le),
        multiple_of=cast(float, multiple_of),
        min_items=cast(int, min_items),
        max_items=cast(int, max_items),
        min_length=cast(int, min_length),
        max_length=cast(int, max_length),
        regex=cast(str, regex),
        **extra,
    )
    return FieldInfo(pydantic_field_info=pydantic_field, db_field_name=db_field_name)


def computed_field(
    func: Optional[Any] = None,
    *,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> 'Union[Callable[[Any], ComputedField], ComputedField]':
    import inspect

    def wrapper(func_: Any) -> 'ComputedField':
        if not isinstance(func_, property):
            func_ = property(func_)
        type_ = inspect.signature(func_.fget).return_annotation  # type: ignore
        if type_ is inspect._empty:  # type: ignore[attr-defined]
            type_ = Any

        return ComputedField(
            name=func_.fget.__name__,  # type: ignore
            type_=type_,
            fget=func_.fget,  # type: ignore
            alias=alias,
            title=title,
            description=description,
        )

    if func is None:
        return wrapper

    return wrapper(func)


class ComputedField(Representation):
    __slots__ = (
        'name',
        'type_',
        'outer_type_',
        'fget',
        'fset',
        'class_validators',
        'alias',
        'title',
        'description',
        'config',
        'model_field',
        'required',
    )

    def __init__(
        self,
        *,
        name: str,
        type_: type,
        fget: Callable[[Optional['BaseModel']], Any],
        fset: Any = None,
        alias: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        config: Optional[Type['BaseConfig']] = None,
        model_field: Optional['ModelField'] = None,
    ) -> None:
        self.name: str = name
        self.type_: type = type_
        self.outer_type_: type = type_
        self.fget: Callable[[Optional['BaseModel']], Any] = fget
        self.fset: Any = fset
        self.class_validators: Optional[Dict[str, 'Validator']] = None

        self.alias: str = alias or name
        self.title: Optional[str] = title
        self.description: Optional[str] = description

        self.config: Optional[Type['BaseConfig']] = config
        self.model_field: Optional[ModelField] = model_field
        self.required: bool = False

    @property
    def field_info(self) -> PydanticFieldInfo:
        return PydanticFieldInfo(
            alias=self.alias,
            title=self.title,
            description=self.description or self.fget.__doc__,
            read_only=True,
        )

    def __get__(self, instance: Optional['BaseModel'], owner: Any) -> Any:
        if instance is None:
            return self
        return self.fget(instance)

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")

    def setter(self, fset):
        return type(self)(
            name=self.name,
            type_=self.type_,
            fget=self.fget,
            fset=fset,
            alias=self.alias,
            title=self.title,
            description=self.description,
            config=self.config,
            model_field=self.model_field,
        )

    def set_config_and_prepare_field(self, config: Type['BaseConfig']) -> None:
        self.config = config
        self.model_field = ModelField(
            name=self.name,
            type_=self.type_,
            class_validators=self.class_validators,
            model_config=self.config,
            default=None,
            required=self.required,
            alias=self.field_info.alias,  # type: ignore
            field_info=self.field_info,
        )

    @classmethod
    def __get_validators__(cls):
        yield
