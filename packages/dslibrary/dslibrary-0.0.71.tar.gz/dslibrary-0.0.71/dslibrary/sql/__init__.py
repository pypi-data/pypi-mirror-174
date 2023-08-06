"""
SQL access to data that lacks an SQL engine.

Basic use:
    dataSource = {{ instance of SqlDataSupplier, such as MemoryDataSupplier }}
    cols, rows = run_select(sql, data_source)

Advanced use:
    # this is the connector to the data we're accessing
    # 'context' lets you define several things other than data sources, like 'debugLevel'
    dataSource = {{ instance of SqlDataSupplier, such as MemoryDataSupplier }}
    context = SqlUtil.SqlEvaluationContext( dataSuppliers=dataSource )
    # set up parser to parse sql statements, expressions, etc., and parse the select statement
    select = SqlParser("SELECT ...").parseSelect()
    # set up compiler and compile the select statement
    # 'stream' is an SqlTableStream instance
    stream = SqlCompiler().compileSelect( select, context )
    # 'fields' is an [] of SqlFieldInfo
    # each row is an iterable of values, in the same order as 'fields'
    fields = stream.getFields()
    for row in stream.getRowIterator()
        ...
"""


def run_select(sql, data_source):
    """
    Run SQL against a data source.

    :param sql:             A SELECT statement.
    :param data_source:     An instance of SqlDataSupplier, such as MemoryDataSupplier.
    :return:    A tuple of column information and a row iterator.  Each field is described by SqlFieldInfo.  Each
        iterated row is a tuple of column values.
    """
    from .eval_utils import SqlEvaluationContext
    from .parser import SqlParser
    from .compiler import SqlCompiler
    context = SqlEvaluationContext(data_suppliers=[data_source])
    select = SqlParser(sql).parse_select_only()
    stream = SqlCompiler().compile_select(select, context)
    return stream.getFields(), stream.getRowIterator()
