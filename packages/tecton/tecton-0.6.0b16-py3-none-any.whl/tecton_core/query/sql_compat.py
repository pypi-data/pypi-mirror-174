import enum
from typing import Any
from typing import List
from typing import Optional

import pypika
from pypika import AliasedQuery
from pypika import analytics
from pypika import CustomFunction
from pypika import Field
from pypika.dialects import PostgreSQLQuery
from pypika.dialects import SnowflakeQuery
from pypika.functions import DateAdd
from pypika.queries import Selectable
from pypika.terms import Term
from pypika.utils import format_alias_sql

from tecton_core import conf


class CustomQuery(pypika.queries.QueryBuilder):
    """
    Defines a custom-query class. It's needed for us to wrap some user-defined sql string from transformations in a QueryBuilder object.
    """

    def __init__(self, sql: str):
        super().__init__(self)
        self.sql = sql
        self.withs: List[Selectable] = []

    def with_(self, selectable: Selectable, name: str):
        """
        overrides QueryBuilder.with_
        """
        t = AliasedQuery(name, selectable)
        self.withs.append(t)
        return self

    def get_sql(self, with_alias: bool = False, subquery: bool = False, **kwargs):
        """
        overrides QueryBuilder.get_sql
        """
        sql = ""
        if self.withs:
            sql += "WITH " + ",".join(
                clause.name + " AS (" + clause.get_sql(subquery=False, with_alias=False, **kwargs) + ") "
                for clause in self.withs
            )
        sql += self.sql
        if with_alias:
            self.alias = "sq0"
            sql = f"({sql})"
            return format_alias_sql(sql, self.alias or self._table_name, **kwargs)
        return sql


class LastValue(analytics.LastValue):
    """
    Fixed version of pypika's LastValue to handle Athena wanting "ignore nulls"
     to be outside the parens of the window func.
    """

    def get_special_params_sql(self, **kwargs: Any) -> Optional[str]:
        if dialect() == Dialect.ATHENA:
            return None
        else:
            return super(LastValue, self).get_special_params_sql(**kwargs)

    def get_function_sql(self, **kwargs: Any) -> str:
        sql = super(LastValue, self).get_function_sql(**kwargs)
        if dialect() == Dialect.ATHENA:
            sql += " IGNORE NULLS" if self._ignore_nulls else ""
        return sql


class Dialect(str, enum.Enum):
    SNOWFLAKE = "snowflake"
    ATHENA = "athena"


def dialect() -> Dialect:
    # TODO(Daryl) - infer the sql dialect from the fv itself,
    # We just use the conf for now as athena transformations are still under development.
    d = conf.get_or_none("SQL_DIALECT")
    try:
        return Dialect(d)
    except:
        raise Exception(f"Unsupported sql dialect: set SQL_DIALECT to {[x.value for x in Dialect]}")


def Query():
    if dialect() == Dialect.SNOWFLAKE:
        return SnowflakeQuery
    else:
        return PostgreSQLQuery


def to_timestamp(time_str: str) -> Term:
    if dialect() == Dialect.SNOWFLAKE:
        c = CustomFunction("to_timestamp", ["time_str"])
    else:
        c = CustomFunction("from_iso8601_timestamp", ["time_str"])
    return c(time_str)


def date_add(interval: str, amount: int, time_field: Term) -> Term:
    if dialect() == Dialect.SNOWFLAKE:
        # snowflake uses dateadd rather than date_add
        c = CustomFunction("dateadd", ["interval", "amount", "time_field"])
    else:
        c = DateAdd
    return c(interval, amount, time_field)


def to_unixtime(timestamp: Term) -> Term:
    if dialect() == Dialect.SNOWFLAKE:
        c = CustomFunction("date_part", ["epoch", "timestamp"])
        return c(Field("epoch_second"), timestamp)
    else:
        c = CustomFunction("to_unixtime", ["timestamp"])
        return c(timestamp)


def from_unixtime(unix_timestamp: Term) -> Term:
    if dialect() == Dialect.SNOWFLAKE:
        c = CustomFunction("to_timestamp", ["unix_timestamp"])
    else:
        c = CustomFunction("from_unixtime", ["unix_timestamp"])
    return c(unix_timestamp)
