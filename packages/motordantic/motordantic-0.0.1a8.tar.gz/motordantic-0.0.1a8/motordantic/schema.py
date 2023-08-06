import warnings
from typing import (
    Type,
    Dict,
    Dict,
    Optional,
    Tuple,
    Any,
    TYPE_CHECKING,
    Set,
    cast,
)
from enum import Enum

from pydantic.fields import ModelField
from pydantic.schema import (
    TypeModelOrEnum,
    TypeModelSet,
    field_schema,
    SkipField,
    ROOT_KEY,
    lenient_issubclass,
    default_ref_template,
    enum_process_schema,
    get_model,
    get_flat_models_from_model,
    get_model_name_map,
    get_schema_ref,
)

if TYPE_CHECKING:
    from .models import MongoModel


def model_type_schema(
    model: Type['MongoModel'],
    *,
    by_alias: bool,
    model_name_map: Dict[TypeModelOrEnum, str],
    ref_template: str,
    ref_prefix: Optional[str] = None,
    known_models: TypeModelSet,
) -> Tuple[Dict[str, Any], Dict[str, Any], Set[str]]:
    """
    You probably should be using ``model_schema()``, this function is indirectly used by that function.
    Take a single ``model`` and generate the schema for its type only, not including additional
    information as title, etc. Also return additional schema definitions, from sub-models.
    """
    properties = {}
    required = []
    definitions: Dict[str, Any] = {}
    nested_models: Set[str] = set()
    all_fields: Dict[str, ModelField] = {
        **model.__fields__,
        **{
            k: cast(ModelField, m.model_field)
            for k, m in model.__motordantic_computed_fields__.items()
        },
    }

    for k, f in all_fields.items():
        try:
            f_schema, f_definitions, f_nested_models = field_schema(
                f,
                by_alias=by_alias,
                model_name_map=model_name_map,
                ref_prefix=ref_prefix,
                ref_template=ref_template,
                known_models=known_models,
            )
        except SkipField as skip:
            warnings.warn(skip.message, UserWarning)
            continue
        definitions.update(f_definitions)
        nested_models.update(f_nested_models)
        if by_alias:
            properties[f.alias] = f_schema
            if f.required:
                required.append(f.alias)
        else:
            properties[k] = f_schema
            if f.required:
                required.append(k)
    if ROOT_KEY in properties:
        out_schema = properties[ROOT_KEY]
        out_schema['title'] = model.__config__.title or model.__name__
    else:
        out_schema = {'type': 'object', 'properties': properties}
        if required:
            out_schema['required'] = required
    if model.__config__.extra == 'forbid':
        out_schema['additionalProperties'] = False
    return out_schema, definitions, nested_models


def model_process_schema(
    model: TypeModelOrEnum,
    *,
    by_alias: bool = True,
    model_name_map: Dict[TypeModelOrEnum, str],
    ref_prefix: Optional[str] = None,
    ref_template: str = default_ref_template,
    known_models: Optional[TypeModelSet] = None,
    field: Optional[ModelField] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any], Set[str]]:
    """
    Used by ``model_schema()``, you probably should be using that function.

    Take a single ``model`` and generate its schema. Also return additional schema definitions, from sub-models. The
    sub-models of the returned schema will be referenced, but their definitions will not be included in the schema. All
    the definitions are returned as the second value.
    """
    from inspect import getdoc, signature

    known_models = known_models or set()
    if lenient_issubclass(model, Enum):
        model = cast(Type[Enum], model)
        s = enum_process_schema(model, field=field)
        return s, {}, set()
    model = cast(Type['MongoModel'], model)
    s = {'title': model.__config__.title or model.__name__}
    doc = getdoc(model)
    if doc:
        s['description'] = doc
    known_models.add(model)
    m_schema, m_definitions, nested_models = model_type_schema(
        model,
        by_alias=by_alias,
        model_name_map=model_name_map,
        ref_prefix=ref_prefix,
        ref_template=ref_template,
        known_models=known_models,
    )
    s.update(m_schema)
    schema_extra = model.__config__.schema_extra
    if callable(schema_extra):
        if len(signature(schema_extra).parameters) == 1:
            schema_extra(s)
        else:
            schema_extra(s, model)
    else:
        s.update(schema_extra)
    return s, m_definitions, nested_models


def model_schema(
    model: Type['MongoModel'],
    by_alias: bool = True,
    ref_prefix: Optional[str] = None,
    ref_template: str = default_ref_template,
) -> Dict[str, Any]:
    """
    Generate a JSON Schema for one model. With all the sub-models defined in the ``definitions`` top-level
    JSON key.

    :param model: a Pydantic model (a class that inherits from BaseModel)
    :param by_alias: generate the schemas using the aliases defined, if any
    :param ref_prefix: the JSON Pointer prefix for schema references with ``$ref``, if None, will be set to the
      default of ``#/definitions/``. Update it if you want the schemas to reference the definitions somewhere
      else, e.g. for OpenAPI use ``#/components/schemas/``. The resulting generated schemas will still be at the
      top-level key ``definitions``, so you can extract them from there. But all the references will have the set
      prefix.
    :param ref_template: Use a ``string.format()`` template for ``$ref`` instead of a prefix. This can be useful for
      references that cannot be represented by ``ref_prefix`` such as a definition stored in another file. For a
      sibling json file in a ``/schemas`` directory use ``"/schemas/${model}.json#"``.
    :return: dict with the JSON Schema for the passed ``model``
    """
    model = get_model(model)  # type: ignore
    flat_models = get_flat_models_from_model(model)
    model_name_map = get_model_name_map(flat_models)
    model_name = model_name_map[model]
    m_schema, m_definitions, nested_models = model_process_schema(
        model,
        by_alias=by_alias,
        model_name_map=model_name_map,
        ref_prefix=ref_prefix,
        ref_template=ref_template,
    )
    if model_name in nested_models:
        # model_name is in Nested models, it has circular references
        m_definitions[model_name] = m_schema
        m_schema = get_schema_ref(model_name, ref_prefix, ref_template, False)
    if m_definitions:
        m_schema.update({'definitions': m_definitions})
    return m_schema
