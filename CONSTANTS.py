# main index through tables
TABLE_INDEX = "CENSUS_BLOCK_GROUP"

# years of data
YEAR = [
    2019,
    2020
]

# pattern of data tables
TABLE_DATA = "{year}_CBG_{table_id}"

# codes to splits
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


# United States names and codes
STATES = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    # 'American Samoa': 'AS', # remove?
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    # 'Guam': 'GU', # remove?
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    # 'Northern Mariana Islands': 'MP', # remove?
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'MN',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    # 'Virginia Islands': 'VI', # not in the data
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

COLUMNS = ['SEX_MALES', 'SEX_FEMALES', 'RACE_WHITE',
       'RACE_BLACK', 'RACE_AMERICAN_INDIAN_AND_ALASKA', 'RACE_ASIAN',
       'RACE_HAWAII_AND_ISLANDERS', 'RACE_SOME_OTHER_RACE_ALONE', 'RACE_MIXED',
       'AGE_UNDER_18', 'AGE_18_24', 'AGE_25_29', 'AGE_30_34', 'AGE_35_39',
       'AGE_40_44', 'AGE_45_49', 'AGE_50_54', 'AGE_55_59', 'AGE_60_64',
       'AGE_ABOVE_65', 'HOUSEHOLD_FEMALE_HOUSEHOLDER',
       'HOUSEHOLD_MALE_HOUSEHOLDER', 'HOUSEHOLD_MARRIED_COUPLE',
       'HOUSEHOLD_COHABITING_COUPLE', 'EDUCATION_BUSINESS',
       'EDUCATION_EDUCATION', 'EDUCATION_ARTS_HUMANITIES_AND_OTHER',
       'EDUCATION_SCIENCE_AND_ENGINEERING', 'INCOME_LESS_THAN_10000',
       'INCOME_10000_14999', 'INCOME_15000_19999', 'INCOME_20000_24999',
       'INCOME_25000_29999', 'INCOME_30000_34999', 'INCOME_35000_39999',
       'INCOME_40000_44999', 'INCOME_45000_49999', 'INCOME_50000_59999',
       'INCOME_60000_74999', 'INCOME_75000_99999', 'INCOME_100000_124999',
       'INCOME_125000_149999', 'INCOME_150000_199999', 'INCOME_200000_OR_MORE',
       'OCCUPANCY_OCCUPIED', 'OCCUPANCY_VACANT', 'VALUE_LESS_THAN_10000',
       'VALUE_10000_14999', 'VALUE_15000_19999', 'VALUE_20000_24999',
       'VALUE_25000_29999', 'VALUE_30000_34999', 'VALUE_35000_39999',
       'VALUE_40000_49999', 'VALUE_50000_59999', 'VALUE_60000_69999',
       'VALUE_70000_79999', 'VALUE_80000_89999', 'VALUE_90000_99999',
       'VALUE_100000_124999', 'VALUE_125000_149999', 'VALUE_150000_174999',
       'VALUE_175000_199999', 'VALUE_200000_249999', 'VALUE_250000_299999',
       'VALUE_300000_399999', 'VALUE_400000_499999', 'VALUE_500000_749999',
       'VALUE_750000_999999', 'VALUE_1000000_1499999', 'VALUE_1500000_1999999',
       'VALUE_2000000_OR_MORE', 'TIME_LESS_THAN_5_MINS', 'TIME_5_9_MINS',
       'TIME_10_14_MINS', 'TIME_15_19_MINS', 'TIME_20_24_MINS',
       'TIME_25_29_MINS', 'TIME_30_34_MINS', 'TIME_35_39_MINS',
       'TIME_40_44_MINS', 'TIME_45_59_MINS', 'TIME_60_89_MINS',
       'TIME_90_OR_MORE_MINS']
