import logging
import time
from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Union

import sqlalchemy
from dateutil import parser
from sqlalchemy import text
from sqlalchemy.engine.row import Row

from chalk.features import DataFrame, Feature
from chalk.features.feature import FeatureSetBase
from chalk.sql.base.protocols import (
    BaseSQLSourceProtocol,
    ChalkQueryProtocol,
    DBSessionProtocol,
    IncrementalSettings,
    StringChalkQueryProtocol,
)
from chalk.utils.collections import get_unique_item


class Finalizer(str, Enum):
    OneOrNone = "OneOrNone"
    One = "One"
    First = "First"
    All = "All"


_logger = logging.getLogger(__name__)


def _maybe_coerce_feature_value(value: Any, feature: Feature, coerce: bool):
    if not coerce:
        return value

    if value is None:
        return value

    assert feature.typ is not None

    if issubclass(feature.typ.underlying, datetime) and isinstance(value, str):
        # Some SQL dialects/drivers, such as SQLite, will return datetimes as raw strings
        # TODO: there's no guarantee that this `value` is actually an ISO string. SQLite stores and returns them
        # in the format "%Y-%m-%d %H:%M:%S", which seems good enough for parser.isoparse()
        return parser.isoparse(value)

    return value


def _construct_features(
    cols: Union[List[Feature], Dict[str, Feature]], tuples: Optional[Row], coerce_raw_values: bool = False
):
    root_ns = get_unique_item(
        (f.root_namespace for f in (cols.values() if isinstance(cols, dict) else cols)), "root ns"
    )
    features_cls = FeatureSetBase.registry[root_ns]
    kwargs = {}

    if isinstance(cols, dict):
        if tuples is None:
            for k, feature in cols.items():
                kwargs[feature.attribute_name] = None
        else:
            row = dict(tuples)
            for k, feature in cols.items():
                assert feature.attribute_name is not None
                kwargs[feature.attribute_name] = _maybe_coerce_feature_value(
                    row[k] if row else None, feature, coerce_raw_values
                )
    else:
        assert tuples is not None
        assert len(tuples) == len(cols)
        for feature, val in zip(cols, tuples):
            assert feature.attribute_name is not None
            kwargs[feature.attribute_name] = _maybe_coerce_feature_value(val, feature, coerce_raw_values)
    return features_cls(**kwargs)


class StringChalkQuery(StringChalkQueryProtocol):
    def __init__(
        self,
        session: DBSessionProtocol,
        source: BaseSQLSourceProtocol,
        query: str,
        fields: Mapping[str, Union[Feature, str]],
        args: Optional[Mapping[str, str]],
    ):
        if len(fields) == 0:
            raise ValueError("Expected argument 'fields' to be a non-empty dict, but got {}")

        self._finalizer: Optional[Finalizer] = None
        self._session = session
        self._source = source
        self._query = text(query)
        self._fields = fields
        self._incremental_settings: Optional[Union[IncrementalSettings, bool]] = None
        if args is not None:
            self._query = self._query.bindparams(**args)

    def one_or_none(self):
        self._finalizer = Finalizer.OneOrNone
        return self

    def one(self):
        self._finalizer = Finalizer.One
        return self

    def all(self, incremental: Union[bool, IncrementalSettings] = False):
        self._finalizer = Finalizer.All
        if isinstance(incremental, bool) and incremental:
            self._incremental_settings = IncrementalSettings(lookback_period=None)
        elif isinstance(incremental, IncrementalSettings):
            self._incremental_settings = incremental
        return self

    def execute(self):
        tuples = self._session.execute(self._query)
        assert isinstance(tuples, sqlalchemy.engine.CursorResult)
        cols = {k: Feature.from_root_fqn(v) if isinstance(v, str) else v for (k, v) in self._fields.items()}
        self._finalizer = self._finalizer or Finalizer.All

        if self._finalizer == Finalizer.All:
            data = {x.root_fqn: [] for x in cols.values()}
            for tup in tuples.all():
                for field in self._fields.keys():
                    data[cols[field].root_fqn].append(tup[field])
            df = DataFrame(data=data)
            return df

        tup = None
        if self._finalizer == Finalizer.One:
            tup = tuples.one()

        if self._finalizer == Finalizer.First:
            tup = tuples.first()

        if self._finalizer == Finalizer.OneOrNone:
            tup = tuples.one_or_none()

        return _construct_features(cols, tup, coerce_raw_values=True)


class ChalkQuery(ChalkQueryProtocol):
    _session: DBSessionProtocol
    _source: BaseSQLSourceProtocol
    _features: List[Feature]
    _finalizer: Optional[Finalizer]
    _incremental_settings: Optional[Union[IncrementalSettings, bool]]

    def __init__(
        self,
        features: List[Feature],
        session: DBSessionProtocol,
        source: BaseSQLSourceProtocol,
        raw_session: Optional[Any] = None,
    ):
        self._session = session
        self._raw_session = raw_session or session
        self._features = features
        self._finalizer = None
        self._source = source
        self._incremental_settings = None

    def first(self):
        self._session.update_query(lambda x: x.limit(1))
        self._finalizer = Finalizer.First
        return self

    def one_or_none(self):
        self._session.update_query(lambda x: x.limit(1))
        self._finalizer = Finalizer.OneOrNone
        return self

    def one(self):
        self._session.update_query(lambda x: x.limit(1))
        self._finalizer = Finalizer.One
        return self

    def all(self, incremental: Union[bool, IncrementalSettings] = False):
        self._finalizer = Finalizer.All
        if isinstance(incremental, bool) and incremental:
            self._incremental_settings = IncrementalSettings(lookback_period=None)
        elif isinstance(incremental, IncrementalSettings):
            self._incremental_settings = incremental
        return self

    def filter_by(self, **kwargs):
        self._session.update_query(lambda x: x.filter_by(**kwargs))
        return self

    def filter(self, *criterion):
        self._session.update_query(lambda x: x.filter(*criterion))
        return self

    def limit(self, *limits):
        self._session.update_query(lambda x: x.limit(*limits))
        return self

    def order_by(self, *clauses):
        self._session.update_query(lambda x: x.order_by(*clauses))
        return self

    def group_by(self, *clauses):
        self._session.update_query(lambda x: x.group_by(*clauses))
        return self

    def having(self, criterion):
        self._session.update_query(lambda x: x.having(*criterion))
        return self

    def union(self, *q):
        self._session.update_query(lambda x: x.union(*q))
        return self

    def union_all(self, *q):
        self._session.update_query(lambda x: x.union_all(*q))
        return self

    def intersect(self, *q):
        self._session.update_query(lambda x: x.intersect(*q))
        return self

    def intersect_all(self, *q):
        self._session.update_query(lambda x: x.intersect_all(*q))
        return self

    def join(self, target, *props, **kwargs):
        self._session.update_query(lambda x: x.join(target, *props, **kwargs))
        return self

    def outerjoin(self, target, *props, **kwargs):
        self._session.update_query(lambda x: x.outerjoin(target, *props, **kwargs))
        return self

    def select_from(self, *from_obj):
        self._session.update_query(lambda x: x.select_from(*from_obj))
        return self

    @staticmethod
    def _get_finalizer_fn(f: Optional[Finalizer]):
        if f == Finalizer.First:
            return lambda x: x.first()
        if f == Finalizer.All:
            return lambda x: x.all()
        if f == Finalizer.One:
            return lambda x: x.one()
        if f == Finalizer.OneOrNone:
            return lambda x: x.one_or_none()
        if f is None:
            return lambda x: x.all()
        raise ValueError(f"Unknown finalizer {f}")

    def execute(self):
        start = time.perf_counter()
        try:
            column_descriptions = self._session._session.column_descriptions
            self._session.update_query(self._get_finalizer_fn(self._finalizer))
            tuples = self._session.result()
            self._raw_session.close()
            fqn_to_feature = {f.fqn: f for f in self._features}
            cols = [fqn_to_feature[value["name"]] for value in column_descriptions if value["name"] in fqn_to_feature]

            if isinstance(tuples, list):
                lists = defaultdict(list)

                for tuple in tuples:
                    for col_i, x in enumerate(tuple):
                        if isinstance(x, Enum):
                            x = x.value
                        lists[col_i].append(x)
                return DataFrame({col: lists[i] for i, col in enumerate(cols)})

            return _construct_features(cols, tuples, coerce_raw_values=False)
        finally:
            _logger.debug(f"query.execute: {time.perf_counter() - start}")
