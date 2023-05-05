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

COLUMNS = [
    'sex_males', 'sex_females',

    "race_white",
    "race_black",
    "race_american indian and alaska",
    "race_asian",
    "race_hawaii and islanders",
    "race_some ther race alone",
    "race_mixed",
    "age_under 18",
    "age_18-24",
    "age_25-29",
    "age_30-34",
    "age_35-39",
    "age_40-44",
    "age_45-49",
    "age_50-54",
    "age_55-59",
    "age_60-64",
    "age_65 and above",
    
    "household_female householder",
    "household_male householder",
    "household_married couple",
    "household_cohabiting couple",
    
    "education_business",
    "education_education",
    "education_arts humanities and other",
    "education_science and engineering",

    "income_10 000 $ or less",
    "income_10 000-14 999 $",
    "income_15 000-19 999 $",
    "income_20 000-24 999 $",
    "income_25 000-29 999 $",
    "income_30 000-34 999 $",
    "income_35 000-39 999 $",
    "income_40 000-44 999 $",
    "income_45 000-49 999 $",
    "income_50 000-59 999 $",
    "income_60 000-74 999 $",
    "income_75 000-99 999 $",
    "income_100 000-124 999 $",
    "income_125 000-149 999 $",
    "income_150 000-99 999 $",
    "income_200 000 $ or more",

    "occupancy_occupied",
    "occupancy_vacant",
    
    "value_10 000 $ or less",
    "value_10 000-14 999 $",
    "value_15 000-19 999 $",
    "value_20 000-24 999 $",
    "value_25 000-29 999 $",
    "value_30 000-34 999 $",
    "value_35 000-39 999 $",
    "value_40 000-49 999 $",
    "value_50 000-59 999 $",
    "value_60 000-69 999 $",
    "value_70 000-79 999 $",
    "value_80 000-89 999 $",
    "value_90 000-99 999 $",
    "value_100 000-124 999 $",
    "value_125 000-149 999 $",
    "value_150 000-174 999 $",
    "value_175 000-199 999 $",
    "value_200 000-249 999 $",
    "value_250 000-299 999 $",
    "value_300 000-399 999 $",
    "value_400 000-499 999 $",
    "value_500 000-749 999 $",
    "value_750 000-999 999 $",
    "value_1 000 000-1 499 999 $",
    "value_1 500 000-1 999 999 $",
    "value_2 000 000 or more $",

    "time_to_work_less than 5 mins",
    "time_to_work_5-9 mins",
    "time_to_work_10-14 mins",
    "time_to_work_15-19 mins",
    "time_to_work_20-24 mins",
    "time_to_work_25-29 mins",
    "time_to_work_30-34 mins",
    "time_to_work_35-39 mins",
    "time_to_work_40-44 mins",
    "time_to_work_45-59 mins",
    "time_to_work_60-89 mins",
    "time_to_work_90 or more mins"
]
