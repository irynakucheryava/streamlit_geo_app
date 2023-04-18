import streamlit as st
import pandas as pd
from snowflake.snowpark.session import Session
from CONSTANTS import TABLE_INDEX
from utils import list_concat


FIELD_PREFIXES = [
    "B01001",
    "B02001",
    "B08303",
    "B11012",
    "B15012",
    "B19001",
    "B25002",
    "B25075"
]

# pattern for static tables
STATIC_TABLES = {
    "description": "{year}_METADATA_CBG_FIELD_DESCRIPTIONS",
    "geographic": "{year}_METADATA_CBG_GEOGRAPHIC_DATA",
    "states": "{year}_CBG_GEOMETRY_WKT"
}
# static columns
STATIC_COLUMNS = {
    "description" : [
        "TABLE_ID",
        "TABLE_NUMBER",
        "TABLE_TITLE",
        "FIELD_LEVEL_5",
        "FIELD_LEVEL_6"
    ],
    "geographic": [
        TABLE_INDEX,
        "LATITUDE",
        "LONGITUDE"
    ],
    "states": [
        TABLE_INDEX,
    ]
}
# static where
STATIC_WHERE = {
    "description": f'''FIELD_LEVEL_1 = 'Estimate' 
        and LOWER(TABLE_TITLE) not like '%median%'
        and TABLE_NUMBER in ({list_concat(FIELD_PREFIXES)})
        and FIELD_LEVEL_5 is not null
        ''',
    "geographic": None,
    "states": "STATE in (states_list)"
}


def init_connection():
    """Connector to snowflake."""
    sec = False
    if sec: # st.secrets:
        session = Session.builder.configs(**st.secrets["snowflake"]).create()
    else:
        # session = Session.builder.configs(
        #     {
        #         "account"   : credentials["account"],
        #         "user"      : credentials["user"],
        #         "password"  : credentials["password"],
        #         "role"      : credentials["role"],
        #         "warehouse" : credentials["warehouse"],
        #         "database"  : credentials["database"],
        #         "schema"    : credentials["schema"],
        #     }
        # )
        connection_parameters = {
            "account"   : "jkwomdq-qk60499",
            "user"      : "irynakucheryava",
            "password"  : "Kucheryava060393IK/",
            "role"      : "ACCOUNTADMIN",
            "warehouse" : "COMPUTE_WH",
            "database"  : "US_OPEN_CENSUS_DATA__NEIGHBORHOOD_INSIGHTS__FREE_DATASET",
            "schema"    : "PUBLIC"
        }
        session = Session.builder.configs(connection_parameters).create()
    return session


# @st.experimental_memo(ttl=1200)
def read_table(table : str, columns : list = None, where: str = None):
    """Read data from "select-from[-where]" querry."""
    session = init_connection()
    if columns is not None:
        cols = ", ".join(columns)
        query = f'''select {cols} from "{table}"'''
    else:
        query = f'''select * from "{table}"'''
    if where is not None:
            query += f" where {where}"
    df = pd.DataFrame(
        session.sql(query=query).collect(),
    )
    return df


def read_static(year, name, use_where : bool = True, **kwards):
    """Read static table"""
    table = STATIC_TABLES[name].format(year=year)
    columns = STATIC_COLUMNS[name]
    if use_where:
        where = STATIC_WHERE[name]
        for k, v in kwards.items():
            where = where.replace(k, v)
    else:
        where = None
    df_static = read_table(table, columns, where)
    return df_static


def read_dataset(table : str, columns : list = None):
    """Read tables with actual data."""
    session = init_connection()
    if columns is not None:
        # columns must be in double quotes here
        cols = ['"' + col + '"' for col in columns]
        cols = ", ".join(cols)
        query = f'''select {TABLE_INDEX}, {cols} from "{table}"'''
    else:
        query = f'''select * from "{table}"'''
    df = pd.DataFrame(
        session.sql(query=query).collect(),
    )
    return df


