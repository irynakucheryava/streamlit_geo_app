import streamlit as st
import pandas as pd
from snowflake.snowpark.session import Session
from utils import list_concat
from geo_utils import add_h3_index
from CONSTANTS import TABLE_INDEX


STATIC_TABLES = {
    "description": "2020_METADATA_CBG_FIELD_DESCRIPTIONS",
    "geographic": "2020_METADATA_CBG_GEOGRAPHIC_DATA"
}

STATIC_COLUMNS = {
    "2020_METADATA_CBG_FIELD_DESCRIPTIONS" : [
        "TABLE_ID",
        "TABLE_NUMBER",
        "TABLE_TITLE",
        "FIELD_LEVEL_5",
        "FIELD_LEVEL_6"
    ],
    "2020_METADATA_CBG_GEOGRAPHIC_DATA": [
        TABLE_INDEX,
        "LATITUDE",
        "LONGITUDE"
    ]
}

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

TABLES_2020 = [
    "2020_CBG_" + name[:3] for name in FIELD_PREFIXES
]

TABLES_2019 = [
    "2019_CBG_" + name[:3] for name in FIELD_PREFIXES
]


def init_connection():
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


def field_description(split : str = None, field_level_5 : list = None, field_level_6 : list = None):
    table = STATIC_TABLES["description"]
    columns = STATIC_COLUMNS[table]
    split_list = list_concat(FIELD_PREFIXES)
    where = f"""
        FIELD_LEVEL_1 = 'Estimate' 
        and LOWER(TABLE_TITLE) not like '%median%'
        and TABLE_NUMBER in ({split_list})
        and FIELD_LEVEL_5 is not null
    """
    if split is not None:
         where += f" and TABLE_TITLE = '{split}'"
    if field_level_5 is not None:
        field_lvl_5_con = list_concat(field_level_5)
        where += f" and FIELD_LEVEL_5 in ({field_lvl_5_con})"
    if field_level_6 is not None:
        field_lvl_6_con = list_concat(field_level_6)
        where += f" and FIELD_LEVEL_6 in ({field_lvl_6_con})"
    fd = read_table(table, columns, where)
    return fd
     
def cbg_coordinates(add_h3, h3_res=6):
    table = STATIC_TABLES["geographic"]
    cols = STATIC_COLUMNS[table]
    df_coord = read_table(table, cols)
    if add_h3:
        df_coord_h3 = add_h3_index(df_coord, h3_res)
        return df_coord_h3
    else:
        return df_coord

def read_dataset(table : str, columns : list = None, where: str = None):
    session = init_connection()
    if columns is not None:
        cols = ['"' + col + '"' for col in columns]
        cols = ", ".join(cols)
        query = f'''select {TABLE_INDEX}, {cols} from "{table}"'''
    else:
        query = f'''select * from "{table}"'''
    if where is not None:
            query += f" where {where}"
    df = pd.DataFrame(
        session.sql(query=query).collect(),
    )
    return df