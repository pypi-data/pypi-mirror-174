from dslibrary.sql.exceptions import SqlException
from dslibrary.sql.misc import is_valid_table_name, sql_enquote_id, is_valid_field_name
from dslibrary.utils.connect import enquote_sql_identifier


def data_to_sql(table_name: (str, list), cols, rows=None, append: bool=False, mode: str=None, do_insert: bool=True):
    """
    Generate SQL to create a table and add data.
    :param table_name:  Name for table being saved. A [] implies a hierarchical specification, like schema.table.
    :param cols:        Column names.
    :param rows:        Values for each row.
    :param append:      Whether to append to existing table data.
    :param mode:        Database flavor.
    :return:    A generator for SQL statements to run.  A sequence of (sql, parameters).
    """
    if isinstance(table_name, str):
        if not is_valid_table_name(table_name, mode):
            raise SqlException(f"invalid table name '{table_name}' for engine '{mode}'")
    else:
        for t_sub in table_name:
            if not is_valid_table_name(t_sub, mode):
                raise SqlException(f"invalid table name '{t_sub}' for engine '{mode}'")
    enquote = lambda name: sql_enquote_id(name, mode)
    if isinstance(table_name, str):
        table_name_quoted = enquote(table_name)
    else:
        table_name_quoted = ".".join(map(enquote, table_name))
    if not append:
        if mode == "mssql":
            yield \
                "IF object_id({table}, 'U') is not null\n" \
                "    DROP TABLE {table}\n" \
                "".format(table=table_name_quoted), []
        else:
            yield "DROP TABLE IF EXISTS %s" % table_name_quoted, []
    types = []
    if not isinstance(rows, (list, set, tuple)):
        rows = list(rows)
    for col, coldata in zip(cols, zip(*rows)):
        if not is_valid_field_name(col, mode):
            raise SqlException(f"invalid field name '{col}' for engine '{mode}'")
        t, nulls = _guess_type(coldata, mode=mode)
        types.append("%s%s" % (t, "" if nulls else " NOT NULL"))
    fields = ", ".join("%s %s" % (enquote(col), t) for col, t in zip(cols, types))
    if mode == "mssql":
        yield \
            "IF object_id({table}, 'U') is not null\n" \
            "    CREATE TABLE {table} ({fields})\n" \
            "".format(table=table_name_quoted, fields=fields), []
    else:
        yield "CREATE TABLE IF NOT EXISTS %s (%s)" % (table_name_quoted, fields), []
    if do_insert:
        ins0 = "INSERT INTO %s (%s) VALUES " % (table_name_quoted, ", ".join(map(enquote, cols)))
        sqls = []
        params = []
        for row in (rows or []):
            sql = "(%s)" % ", ".join(map(lambda v: "%s", row))
            sqls.append(sql)
            params += list(row)
            if len(sqls) >= 1000:
                yield "%s%s" % (ins0, ", ".join(sqls)), params
                sqls.clear()
                params.clear()
        if sqls:
            yield "%s%s" % (ins0, ", ".join(sqls)), params


class TypeGuesser(object):
    def __init__(self, mode: str):
        self.mode = mode
        self.nulls = False
        self.maxlen = 0
        self.types = [0, 0, 0]

    def add(self, value):
        if value is None:
            self.nulls = True
            return
        if isinstance(value, int):
            self.types[0] = 1
        elif isinstance(value, float):
            self.types[1] = 1
        else:
            self.types[2] = 1
            l = len(str(value))
            if l > self.maxlen:
                self.maxlen = l

    def summarize(self):
        if self.mode == "bigquery":
            if self.types[2]:
                t = "STRING"
            elif self.types[1]:
                t = "FLOAT64"
            else:
                t = "INT64" if self.types[0] else "STRING"
            return t, self.nulls
        else:
            if self.types[2]:
                t = "VARCHAR"
            elif self.types[1]:
                t = "DOUBLE PRECISION"
            else:
                t = "INTEGER" if self.types[0] else "VARCHAR"
        if t == "VARCHAR":
            # VARCHAR requires a length
            # - 'maxlen' is the longest string we saw
            # - we increase this number a bit in order to account for rows we haven't examined
            if self.maxlen < 10:
                self.maxlen = 10
            t += "(%s)" % (self.maxlen + self.maxlen // 4 + 8)
        return t, self.nulls


def _guess_type(values, mode=None):
    g = TypeGuesser(mode)
    for v in values:
        g.add(v)
    return g.summarize()


def data_sample_to_schema(cols, rows, mode: str=None):
    """
    Generate a schema based on a data sample.
    :param cols:        Column names.
    :param rows:        Row values.
    :param mode:        Type of database.
    """
    def type_cols(values):
        name, nulls = _guess_type(values, mode=mode)
        return {
            "column_type": name,
            "is_nullable": nulls
        }
    values = [[] for _ in cols]
    for row in rows:
        for n in range(len(cols)):
            values[n].append(row[n])
    return [{"column_name": col, **type_cols(values[n])} for n, col in enumerate(cols)]


def dataframe_to_sql(dataframe, table_name: str, append: bool=False, flavor: str=None):
    """
    Generate SQL statements to create a table and add data.

    :param dataframe:   A dataframe to render into SQL.
    :param table_name:  Name of table to create or extend.
    :param append:      True to append, False to replace.
    :param flavor:      Name of a particular type of database, to adjust details of SQL format.
    :returns a generator of (sql, parameter list)
    """
    enquote = lambda name, **k: enquote_sql_identifier(name, flavor=flavor, **k)
    if not append:
        yield "DROP TABLE IF EXISTS %s" % enquote(table_name), []
    # TODO expand to cover more types
    if flavor == "bigquery":
        dtype_to_sql = {"int32": "INT64", "int64": "INT64", "float64": "NUMERIC", "datetime64": "TIMESTAMP"}
        str_type = "STRING"
    else:
        dtype_to_sql = {"int32": "INTEGER", "int64": "INTEGER", "float64": "DOUBLE PRECISION", "datetime64": "TIMESTAMP"}
        str_type = "VARCHAR"
    cols = list(dataframe.columns)
    types = []
    for col, dtype in zip(cols, dataframe.dtypes):
        sql_type = dtype_to_sql.get(str(dtype))
        if not sql_type:
            max_len = int(dataframe[col].str.len().max()) + 3
            sql_type = f"{str_type}({max_len:d})"
        types.append(sql_type)
    rows = dataframe.itertuples(index=False, name=None)
    fields = ", ".join("%s %s" % (enquote(col, allow_separator=False), t) for col, t in zip(cols, types))
    yield "CREATE TABLE IF NOT EXISTS %s (%s)" % (enquote(table_name), fields), []
    ins0 = "INSERT INTO %s (%s) VALUES " % (enquote(table_name), ", ".join(map(enquote, cols)))
    sqls = []
    params = []
    for row in (rows or []):
        sql = "(%s)" % ", ".join(map(lambda v: "%s", row))
        sqls.append(sql)
        params += list(row)
        if len(sqls) >= 1000:
            yield "%s%s" % (ins0, ", ".join(sqls)), params
            sqls.clear()
            params.clear()
    if sqls:
        yield "%s%s" % (ins0, ", ".join(sqls)), params
