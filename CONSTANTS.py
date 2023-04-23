# main index through tables
TABLE_INDEX = "CENSUS_BLOCK_GROUP"

# years of data
YEAR = [
    2019,
    2020
]

# pattern of data tables
TABLE_DATA = "{year}_CBG_{table_id}"

# splits
SPLITS = [
    'Sex By Age',
    'Race',
    'Travel Time To Work',
    'Households By Type',
    "Total Fields Of Bachelor's Degrees Reported",
    'Occupancy Status',
    'Value'
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
