import collections.abc
import dataclasses
import enum
import logging
from datetime import date, datetime, timezone
from typing import Any, Type, Union, get_origin, get_type_hints

import cattrs
import pendulum
import polars as pl
import pydantic
import pytz
from dateutil import parser
from polars.internals.construction import is_namedtuple
from sqlalchemy import Boolean, Float, Integer, Text
from sqlalchemy.types import TypeEngine

from chalk.features.feature import Feature
from chalk.utils.enum import get_enum_value_type
from chalk.utils.sqlalchemy import UtcDateTime

try:
    import attrs
except ImportError:
    # Imports not available. Attrs is not required.
    attrs = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None

_log = logging.getLogger(__name__)


class FeatureCodec:
    def __init__(self):
        self.converter = cattrs.Converter()
        self.converter.register_structure_hook(datetime, lambda v, _: parser.isoparse(v))
        self.converter.register_unstructure_hook(
            datetime, lambda v: (v if v.tzinfo else pytz.utc.localize(v)).isoformat()
        )

    def _default_encode(self, value: Any):
        if isinstance(value, set):
            return {self._default_encode(x) for x in value}
        if isinstance(value, list):
            return [self._default_encode(x) for x in value]
        if isinstance(value, (str, int, float)):
            return value
        if isinstance(value, enum.Enum):
            return self._default_encode(value.value)
        if isinstance(value, datetime):
            tz = value.tzinfo or (datetime.now(timezone.utc).astimezone().tzinfo)
            return pendulum.instance(value, tz).isoformat()
        if isinstance(value, date):
            return value.isoformat()
        if np is not None and isinstance(value, np.integer):
            return int(value)
        if np is not None and isinstance(value, np.floating):
            return float(value)
        if pd is not None and isinstance(value, pd.Timestamp):
            return pendulum.instance(value.to_pydatetime()).isoformat()
        if isinstance(value, pydantic.BaseModel):
            return value.dict()
        if (attrs is not None and attrs.has(type(value))) or dataclasses.is_dataclass(value):
            return self.converter.unstructure(value)
        if isinstance(value, collections.abc.Iterable):
            return [self._default_encode(x) for x in value]
        raise TypeError(f"Unable to encode value of type {type(value).__name__}")

    def encode(
        self,
        feature: Feature,
        value: Any,
    ):
        if value is None:
            return None

        if feature.encoder is not None:
            return feature.encoder(value)

        return self._default_encode(value)

    def encode_fqn(self, fqn: str, value: Any):
        return self.encode(Feature.from_root_fqn(fqn), value)

    def _default_decode_value(
        self,
        feature: Feature,
        value: Any,
    ):
        assert feature.typ is not None
        if issubclass(feature.typ.underlying, enum.Enum):
            value = feature.typ.underlying(value)
        if issubclass(feature.typ.underlying, datetime):
            value = parser.isoparse(value)
        elif issubclass(feature.typ.underlying, date):
            # note: datetime is a subclass of date, so we must be careful to decode accordingly
            value = date.fromisoformat(value)
        if issubclass(feature.typ.underlying, pydantic.BaseModel):
            return feature.typ.underlying(**value)
        elif (attrs is not None and attrs.has(feature.typ.underlying)) or dataclasses.is_dataclass(
            feature.typ.underlying
        ):
            return self.converter.structure(value, feature.typ.underlying)
        if not isinstance(value, feature.typ.underlying):
            raise TypeError(f"Unable to decode value {value} to type {feature.typ.underlying.__name__}")
        return value

    def _default_decode(
        self,
        feature: Feature,
        value: Any,
    ):
        assert feature.typ is not None
        if value is None:
            if feature.typ.is_nullable:
                return None
            else:
                raise ValueError(f"Value is none but feature {feature} is not nullable")
        if feature.typ.collection_type is not None and get_origin(feature.typ.collection_type) == set:
            if not isinstance(value, set):
                raise TypeError(f"Feature {feature} is a set but value {value} is not")
            return {self._default_decode_value(feature, x) for x in value}
        elif feature.typ.collection_type is not None and get_origin(feature.typ.collection_type) == list:
            if not isinstance(value, list):
                raise TypeError(f"Feature {feature} is a list but value {value} is not")
            return [self._default_decode_value(feature, x) for x in value]
        else:
            return self._default_decode_value(feature, value)

    def decode(
        self,
        feature: Feature,
        value: Any,
    ):
        if value is None:
            return None

        if feature.decoder is not None:
            return feature.decoder(value)

        return self._default_decode(feature, value)

    def decode_fqn(
        self,
        fqn: str,
        value: Any,
    ):
        return self.decode(Feature.from_root_fqn(fqn), value)

    def get_pandas_dtype(self, fqn: str) -> str:
        feature = Feature.from_root_fqn(fqn)
        typ = feature.typ
        assert typ is not None, "typ should be specified"
        underlying = typ.underlying
        if issubclass(underlying, enum.Enum):
            # For enums, require all members to have the same type
            underlying = get_enum_value_type(underlying)
        # See https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes
        if issubclass(underlying, str):
            return "string"
        if issubclass(underlying, bool):
            return "boolean"
        if issubclass(underlying, int):
            return "Int64"
        if issubclass(underlying, float):
            return "Float64"
        if issubclass(underlying, datetime):
            # This assumes timezone-aware. For timezone-unaware the `pandas_dtype` must be set directly on the Feature
            return "datetime64[ns, utc]"
        _log.info(
            f"Defaulting to pandas type 'object' for fqn {fqn} of type {typ.underlying.__name__}. Set the `pandas_dtype` attribute for better specificity."
        )
        return "object"

    def get_polars_dtype(self, fqn: str) -> Union[pl.DataType, Type[pl.DataType]]:
        feature = Feature.from_root_fqn(fqn)
        if feature.polars_dtype is not None:
            return feature.polars_dtype
        typ = feature.typ
        assert typ is not None, "typ should be specified"
        typ.collection_type
        underlying = typ.underlying
        dtype = self._get_pl_dtype_for_type(underlying, fqn)
        if typ.collection_type is not None:
            dtype = pl.List(dtype)
        return dtype

    def _get_pl_dtype_for_type(self, underlying: type, fqn: str) -> Union[pl.DataType, Type[pl.DataType]]:
        if issubclass(underlying, enum.Enum):
            # For enums, require all members to have the same type
            underlying = get_enum_value_type(underlying)
        if issubclass(underlying, str):
            return pl.Utf8
        if issubclass(underlying, bool):
            return pl.Boolean
        if issubclass(underlying, int):
            return pl.Int64
        if issubclass(underlying, float):
            return pl.Float64
        if issubclass(underlying, datetime):
            return pl.Datetime(time_unit="us", time_zone="UTC")
        if issubclass(underlying, date):
            return pl.Date
        if dataclasses.is_dataclass(underlying) or is_namedtuple(underlying, annotated=True):
            # Polars always treats dataclasses and namedtuples as structs
            annotations = get_type_hints(underlying)
            return pl.Struct(
                fields=[
                    pl.Field(name=k, dtype=self._get_pl_dtype_for_type(v, f"{fqn}.{k}"))
                    for (k, v) in annotations.items()
                ]
            )
        _log.info(
            f"Defaulting to polars type 'object' for fqn {fqn} of type {underlying.__name__}. Set the `polars_dtype` attribute for better specificity."
        )
        return pl.Object

    def get_sqlalchemy_type(self, fqn: str) -> Union[TypeEngine, Type[TypeEngine]]:
        feature = Feature.from_root_fqn(fqn)
        if feature.sqlalchemy_dtype is not None:
            return feature.sqlalchemy_dtype
        typ = feature.typ
        assert typ is not None, "typ should be specified"
        underlying = typ.underlying
        if issubclass(underlying, enum.Enum):
            # For enums, require all members to have the same type
            underlying = get_enum_value_type(underlying)
        # See https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes
        if issubclass(underlying, str):
            return Text
        if issubclass(underlying, bool):
            return Boolean
        if issubclass(underlying, int):
            return Integer
        if issubclass(underlying, float):
            return Float
        if issubclass(underlying, datetime):
            # This type requires the local timezone attribute to be set, but it will be stored as
            # a timezone-unaware timestamp in UTC. It will be converted back into a UTC tz-aware object
            # when parsed by python
            return UtcDateTime
        raise TypeError(
            f"Unable to infer a SQLAlchemy Dtype for field {fqn}. Please set the `sqlalchemy_dtype` attribute."
        )


FEATURE_CODEC = FeatureCodec()
