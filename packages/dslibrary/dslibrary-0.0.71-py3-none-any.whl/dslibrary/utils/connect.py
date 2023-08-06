from urllib.parse import urlparse
import re
import typing
import json


def connect_to_database(uri: str, library: str=None, for_write: bool=False, dsl=None, **kwargs):
    """
    Try, by various means, to connect to a database.  If 'uri' points to a folder (a local folder or a remote folder
    such as an s3 bucket), the files in that folder will be treated as tables

    :param uri:        URI of database.
    :param library:     A specific library to use, if available
    :param for_write:   Whether to enable write operations.
    :param sniff_only:  True to return a ConnectStrategy instead of a connection.
    :param dsl:         Instance of dslibrary for access to resources, i.e. when using connect_to_folder_as_database().
    :returns:  a DBI driver
    """
    # determine flavor of connection and work out which libraries to try
    libraries = []
    if library:
        libraries.append(library)
    uri_parts = uri.split(":", maxsplit=1)
    if uri_parts[0] == "jdbc":
        uri_parts = uri_parts[1:]
    if uri_parts[0] in ("postgres", "postgresql"):
        libraries.append("psycopg2")
    if uri_parts[0] == "mysql":
        libraries.append("pymysql")
    if uri_parts[0] == "mssql":
        libraries.append("pymssql")
    if uri_parts[0] == "sqlite":
        libraries.append("sqlite")
    params = _process_params(uri, **kwargs)
    params.pop("scheme", None)
    for lib in libraries:
        if lib in METHODS:
            conn = METHODS[lib](**params, for_write=for_write)
            if conn:
                return conn
    # uri could point to a folder, which we can treat as a database
    if ":" not in uri or "://" in uri:
        # we can point to a folder and each file is treated as a table
        from dslibrary.utils.folder_db import connect_to_folder_as_database
        return connect_to_folder_as_database(uri, for_write=for_write, dsl=dsl, **kwargs)
    raise ValueError(f"No driver installed/supported for {uri_parts[0]}")


class ConnectStrategy(object):
    """
    How to connect to a database.
    """
    def __init__(self, opener: typing.Callable, open_args: dict=None):
        """
        :param opener:      The connection method.
        :param open_args:   Arguments to pass.
        """
        self.opener = opener
        self.open_args = open_args


def _process_params(uri: str, **kwargs):
    """
    Use a URI to provide most of the needed values for connecting to a database.  'kwargs' supplies overrides.
    :param uri:         A URI which can supply most of the needed values.
    :param kwargs:      Additional overrides.
    :return:        A {} with all the extracted, named connection parameters.
    """
    if uri.startswith("jdbc:"):
        uri = uri[5:]
    if ":" not in uri:
        host, path = uri, ""
    else:
        parsed = urlparse(uri)
        host = parsed.netloc
        path = parsed.path
        if path.startswith("/"):
            path = path[1:]
    user = pwd = ""
    if "@" in host:
        # NOTE: '@' can occur in 'user', i.e. for Google's git repositories
        u_p, host = re.split(r'@(?!.*@)', host)
        if ":" in u_p:
            user, pwd = u_p.split(":")
        else:
            user, pwd = u_p, ""
    if ":" in host:
        host, port = host.split(":", maxsplit=1)
    else:
        port = None
    params = {
        "host": host,
        "port": int(port) if port else None,
        "database": path,
        "username": user,
        "password": pwd
    }
    params.update(kwargs)
    return params


def connect_pymysql(host, port=None, username=None, password=None, database=None, autocommit=True, for_write: bool=False, sniff_only: bool=False, **kwargs):
    try:
        import pymysql
    except ImportError:
        return
    port = port or 3306
    params = dict(user=username, password=password, host=host, port=port, database=database or None, autocommit=autocommit, **kwargs)
    if sniff_only:
        return ConnectStrategy(opener=pymysql.connect, open_args=params)
    conn = pymysql.connect(**params)
    if not for_write:
        _set_conn_read_only(conn)
    conn._flavor = "mysql"
    return conn


def connect_pymssql(host, port=None, username=None, password=None, database=None, autocommit=True, for_write: bool=False, sniff_only: bool=False, **kwargs):
    try:
        import pymssql
    except ImportError:
        raise Exception("MS SQL library not installed")
    more = {}
    if "timeout" in kwargs:
        more["timeout"] = int(kwargs["timeout"])
    params = dict(
        server=host,
        user=username,
        password=password,
        database=database,
        autocommit=autocommit,
        **more
    )
    if sniff_only:
        return ConnectStrategy(opener=pymssql.connect, open_args=params)
    conn = pymssql.connect(**params)
    if not for_write:
        _set_conn_read_only(conn)
    conn._flavor = "mssql"
    return conn


def connect_psycopg2(host, port=None, username=None, password=None, database=None, autocommit=True, for_write: bool=False, sniff_only: bool=False, **kwargs):
    try:
        import psycopg2
        import psycopg2.extensions
    except ImportError:
        return
    # see: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS
    allowed_dsn = {
        #"host", "hostaddr", "port", "dbname", "user", "password", "passfile",
        "channel_binding", "connect_timeout", "client_encoding",
        "options", "application_name", "fallback_application_name",
        "keepalives", "keepalives_idle", "keepalives_interval",
        "keepalives_count",
        "tcp_user_timeout", "tty", "replication", "gssencmode", "sslmode", "requiressl",
        "sslcompression", "sslcert", "sslkey", "sslpassword", "sslrootcert", "sslcrl", "sslcrldir",
        "sslcni", "requirepeer", "ssl_min_protocol_version", "ssl_max_protocol_version",
        "krbsrvname", "gsslib", "service", "target_session_attrs"
    }
    kwargs = {k: v for k, v in kwargs.items() if k in allowed_dsn}
    dsn_parts = {"host": host, "port": port or 5432, "dbname": database or "postgres"}
    if username:
        dsn_parts["user"] = username
    if password:
        dsn_parts["password"] = password
    pg_args_str = " ".join("%s=%s" % (k, v) for k, v in sorted(dsn_parts.items()))
    params = dict(dsn=pg_args_str, **kwargs)
    if sniff_only:
        return ConnectStrategy(opener=psycopg2.connect, open_args=params)
    conn = psycopg2.connect(**params)
    if autocommit:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    if not for_write:
        _set_conn_read_only(conn)
    try:
        conn._flavor = "postgres"
    except:
        pass
    return conn


def connect_sqlite(host, database=None, for_write: bool=False, sniff_only: bool=False, **kwargs):
    try:
        import sqlite3
    except ImportError:
        return
    for ignore in ["port", "username", "password", "database", "autocommit"]:
        kwargs.pop(ignore, None)
    if for_write:
        params = dict(database=host, **kwargs)
    else:
        params = dict(database=f'file:{host or database}?mode=ro', uri=True, **kwargs)
    if sniff_only:
        return ConnectStrategy(opener=sqlite3.connect, open_args=params)
    conn = sqlite3.connect(**params)
    conn._flavor = "sqlite"
    return conn


def connect_bigquery(host=None, database=None, for_write: bool=False, sniff_only: bool=False, **kwargs):
    try:
        from .bigq import create_bgq_connection
    except ImportError:
        return
    service_account = None
    project = None
    if "service_account" in kwargs:
        service_account = kwargs.pop("service_account")
    elif isinstance(database, str) and database.startswith("{"):
        service_account = json.loads(database)
    elif isinstance(database, dict):
        service_account = database
    if "project" in kwargs:
        project = kwargs.pop("project")
    params = dict(service_account=service_account, project=project, **kwargs)
    if not for_write:
        params["read_only"] = True
    if sniff_only:
        return ConnectStrategy(opener=create_bgq_connection, open_args=params)
    conn = create_bgq_connection(**params)
    conn._flavor = "bigquery"
    return conn


def _set_conn_read_only(conn):
    """
    Try to enforce a read-only connection
    """
    try:
        conn.cursor().execute("set transaction read only")
    except:
        print(f"couldn't set read-only mode on connection: {conn.__class__.__name__}")


def enquote_sql_identifier(name, allow_separator: bool=True, flavor: str=None):
    name = str(name)
    # '.' in name will be treated as separator between schema and table name
    if "." in name and allow_separator:
        return ".".join(map(enquote_sql_identifier, name.split('.')))
    # postgres needs quoting of uppercase
    if flavor == "postgres":
        if re.search(r'[^a-z0-9_]', name) or name[:1].isdigit():
            return f'"{name}"'
        return name
    # all other engines
    if re.search(r'[^A-Za-z0-9_]', name) or name[:1].isdigit():
        if flavor == "mysql":
            return f'`{name}`'
        return f'"{name}"'
    return name


def db_conn_flavor(connector) -> str:
    """
    Determine connector flavor.
    """
    if hasattr(connector, "_flavor") and connector._flavor:
        return connector._flavor
    name = connector.__class__.__name__.lower()
    if "postg" in name or "psycopg" in name:
        return "postgres"


METHODS = {
    "pymysql": connect_pymysql,
    "psycopg2": connect_psycopg2,
    "pymssql": connect_pymssql,
    "sqlite": connect_sqlite,
    "bigquery": connect_bigquery,
}
