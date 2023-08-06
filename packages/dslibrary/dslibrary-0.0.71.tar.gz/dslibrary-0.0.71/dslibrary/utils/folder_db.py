import os.path

from dslibrary.sql.file_sql_wr import file_sql_write
from dslibrary.utils.dbconn import Connection
from dslibrary.utils.file_utils import is_breakout_path, join_uri_path
from dslibrary import _DEFAULT


def connect_to_folder_as_database(folder: str, for_write: bool=False, sql_flavor: str="mysql", dsl=None, **kwargs):
    """
    Each file in the folder is a table.  Writes (i.e. CREATE TABLE, INSERT, UPDATE) are supported for some cases
    but are not yet tuned to perform well.  And since, for instance, append is not supported by s3, UPDATE will not
    work there.

    :param folder:      Folder containing files.  Can be either a local folder (i.e. /path/to/files), or a path to
                        an external filesystem folder (i.e. s3://bucket/path/to/files).
    :param for_write:   Enable writes.
    :param sql_flavor:  Which dialect to emulate.
    :param kwargs:      Additional arguments for calls to dslibrary.load_dataframe(), .open_resource(), etc..
    :return:        A DBI-style connection instance.
    """
    # use default dslibrary instance if none is supplied
    dsl = dsl or _DEFAULT
    def file_exists(fn: str):
        return dsl.can_open(join_uri_path(folder, fn), **kwargs)
    def table_reader(table_spec: tuple):
        table_name = table_spec[-1]
        if is_breakout_path(table_name):
            return
        # allow tables to match CSV files
        # TODO what about other file formats?
        if not table_name.endswith(".csv") and file_exists(table_name+".csv"):
            table_name += ".csv"
        return dsl.load_dataframe(join_uri_path(folder, table_name), **kwargs)
    def table_writer(table_spec: tuple, mode: str=None):
        if is_breakout_path(table_spec[-1]):
            return
        return dsl.open_resource(join_uri_path(folder, table_spec[-1]), mode=mode, **kwargs)
    def read(sql, parameters):
        df = dsl.sql_select(sql, parameters, table_loader=table_reader, **kwargs)
        rows = df.itertuples(index=False, name=None)
        # TODO iteration in chunks would make more efficient use of memory - see read_more below
        # name, type_code, display_size, internal_size, precision, scale, null_ok
        return [[col, str(dtype), None, None, None, None, True] for col, dtype in zip(df.columns, df.dtypes)], list(rows), None
    def write(sql, parameters):
        file_sql_write(table_writer, sql, parameters)
    return Connection(read=read, write=write if for_write else None, read_more=None, flavor=sql_flavor)
