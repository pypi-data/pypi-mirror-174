import pandas as pd
from composable import pipeable
from composable.string import replace
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType, DateType
from pyspark.sql.functions import col, create_map, lit, when, isnull, lower
from pyspark.sql.column import Column
from itertools import chain
from functools import reduce
from more_itertools import flatten

DTYPES_TO_SPARK_TYPES = {'O':StringType,
                         'i':IntegerType,
                         'f':FloatType,
                         'M':DateType}


def get_spark_types(df, keys=[]):
    sql_type = lambda name, dtype: StructField(name, 
                                               DTYPES_TO_SPARK_TYPES[dtype.kind](),
                                               False if name in keys else True)
    cols_and_dtypes = lambda df: zip(df.columns, df.dtypes)
    return StructType([sql_type(col, dtype) for col, dtype in cols_and_dtypes(df)])



@pipeable
def to_pandas(rows):
    if rows:
        names = list(rows[0].asDict().keys()) # pyspark.Row keys perserve order
        return pd.DataFrame.from_dict([r.asDict() for r in rows])[names] # reorder to original order
    else:
        return pd.DataFrame()


col_startswith = pipeable(lambda prefix, cols: [c for c in cols if c.startswith(prefix)])
col_endswith =   pipeable(lambda suffix, cols: [c for c in cols if c.endswith(suffix)])
col_contains =   pipeable(lambda substr, cols: [c for c in cols if substr in c])

def col_selector(col_names, from_=None, to=None, inclusive=True):
    from_idx, to_idx = 0, len(col_names)
    if from_:
        from_idx = col_names.index(from_) if inclusive else col_names.index(from_) + 1
    if to:
        to_idx = col_names.index(to) if not inclusive else col_names.index(to) + 1
    return  col_names[from_idx:to_idx]

def get_column_list(col_names, from_=None, to=None, inclusive=True):
    selected_cols = col_selector(col_names, from_=from_, to=to, inclusive=inclusive)
    return  [c for c in col_names if c in selected_cols]

@pipeable
def cols_from(col, col_names, inclusive=True):
    return  get_column_list(col_names, from_=col, inclusive=inclusive)
    
    
@pipeable
def cols_to(col, col_names, inclusive=True):
    return  get_column_list(col_names, to=col, inclusive=inclusive)
    
    
@pipeable
def cols_between(col1, col2, col_names, inclusive=True):
    return get_column_list(col_names, from_=col1, to=col2, inclusive=inclusive)

@pipeable
def all_but(cols_to_exclude, col_names):
    return [c for c in col_names if c not in cols_to_exclude]

def recode(col_name, map_dict, default=None):
    if not isinstance(col, Column):
        col_name = col(col_name)
    mapping_expr = create_map([lit(x) for x in chain(*map_dict.items())])
    if default is None:
        return  mapping_expr.getItem(col_name)
    else:
        return when(~isnull(mapping_expr.getItem(col_name)), mapping_expr.getItem(col_name)).otherwise(default)

    
def ifelse(cond, then_expr, else_expr):
    '''Evaluates a condition and returns one of two expressions.

    
    Parameters
    ----------
    cond : :class:`~pyspark.sql.Column`
        a boolean :class:`~pyspark.sql.Column` expression.
    then_expr :
        a literal value, or a :class:`~pyspark.sql.Column` expression.
    else_expr :
        a literal value, or a :class:`~pyspark.sql.Column` expression.
    
    Examples
    --------
    >>> df.select(ifelse(df['age'] == 2, 3, 4).alias("age")).collect()
    [Row(age=3), Row(age=4)]
    '''
    return when(cond, then_expr).otherwise(else_expr)

def case_when(*pairs, else_=None):
    '''Evaluates a list of conditions and returns one of two result expressions.
    If :func:`pyspark.sql.Column.otherwise` is not invoked, None is returned for unmatched
    conditions.
    
    .. versionadded:: 1.4.0
    
    Parameters
    ----------
    pairs: tuples of the form (cond, expr), where
    cond : :class:`~pyspark.sql.Column`
        a boolean :class:`~pyspark.sql.Column` expression.
    expr :
        a literal value, or a :class:`~pyspark.sql.Column` expression.
    else_ :
        An optional else expression used when all previous conditions where False.
    
    Examples
    --------
    >>> df.select(case_when((df['age'] == 2, 3), (df['age'] == 4, 5)).alias("age")).collect()
    [Row(age=3), Row(age=5)]
    '''
    case_when_helper = lambda acc, nxt: acc.when(*nxt) if acc is not None else when(*nxt)
    cases = reduce(case_when_helper, pairs, None)
    return cases.otherwise(else_) if else_ is not None else cases

@pipeable
def pprint_schema(df):
    ''' prints a readable version of a pyspark.sql schema
    
        args:
            df - A pyspark dataframe
        
        returns:
            None
    ''' 
    str_ = pipeable(str)
    print_ = pipeable(print)
    
    (df.schema 
     >> str_ 
     >> replace(', StructField', ',\n' + 12*' '+ 'StructField')
     >> print_
    )
    
@pipeable
def pprint_rows(rows):
    ''' prints a readable a list of pyspark.sql rows
    
        args:
            rows - A list pyspark rows, generally the output of take/collect/sample
        
        returns:
            None
    '''
    str_ = pipeable(str)
    print_ = pipeable(print)
    
    (rows
     >> str_ 
     >> replace(', ', ',\n' + 5*' ')
     >> print_
    )
    
def text_facet(column, *facets):
    ''' Builds a boolean column expression, returning true for all strings matching one of the facets.
    
    args:
        c - A pyspark column label (string) or expresssion
        facets - one or more labels to be matched.
        
    returns:
        A pyspark column (boolean) expression
    '''
    column = col(column) if isinstance(column, str) else column
    facets = list(flatten(facets))
    return column.isin(facets)

def text_filter(column, pattern, case=True, regex=False):
    ''' Creates a boolean column expression checking for a given pattern,
    
    args:
        column - a string or pyspark column expression
        pattern - a string/pattern
        case - whether of not the search will be case sensitive (default=True)
        regex - whether or not the pattern is a regular expression (default=False)
    
    returns:
        A boolean column expression that will evaluate to True for all elements of
        a column containing/matching the pattern.
    '''
    column = col(column) if isinstance(column, str) else column
    if regex:
        return column.rlike(pattern)
    elif case:
        return column.contains(pattern)
    else:
        return lower(column).contains(pattern.lower())
        