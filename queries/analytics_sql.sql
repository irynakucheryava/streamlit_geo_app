select
    geom.CENSUS_BLOCK_GROUP,
    geom.STATE,
    // sex
    "B01001e2" as sex_males,
    "B01001e26" as sex_females,
    // race
    "B02001e2" as race_white,
    "B02001e3" as race_black,
    "B02001e4" as race_american_indian_and_alaska,
    "B02001e5" as race_asian,
    "B02001e6" as race_hawaii_and_islanders,
    "B02001e7" as race_some_other_race_alone,
    "B02001e8" as race_mixed,
    // age
    "B01001e3" + "B01001e27" + "B01001e4" + "B01001e28" + "B01001e5" + 
    "B01001e29" + "B01001e6" + "B01001e30" as age_under_18,
    "B01001e7" + "B01001e31" + "B01001e8" + "B01001e32" + "B01001e9" + 
    "B01001e33" + "B01001e10" + "B01001e34" as age_18_24,
    "B01001e11" + "B01001e35" as age_25_29,
    "B01001e12" + "B01001e36" as age_30_34,
    "B01001e13" + "B01001e37" as age_35_39,
    "B01001e14" + "B01001e38" as age_40_44,
    "B01001e15" + "B01001e39" as age_45_49,
    "B01001e16" + "B01001e40" as age_50_54,
    "B01001e17" + "B01001e41" as age_55_59,
    "B01001e18" + "B01001e42" + "B01001e19" + "B01001e43" as age_60_64,
    "B01001e20" + "B01001e44" + "B01001e21" + "B01001e45" + "B01001e22" + 
    "B01001e46" + "B01001e23" + "B01001e47" + "B01001e24" + "B01001e48" +
    "B01001e25" + "B01001e49" age_above_65,
    // household
    "B11012e8" as household_female_householder,
    "B11012e13" as household_male_householder,
    "B11012e2" as household_married_couple,
    "B11012e5" as household_cohabiting_couple,
    //education
    "B15012e10" as education_business,
    "B15012e11" as education_education,
    "B15012e12" + "B15012e13" + "B15012e14" + "B15012e15" + "B15012e16" as education_arts_humanities_and_other,
    "B15012e2" + "B15012e3" + "B15012e4" + "B15012e5" + "B15012e6" +
    "B15012e7" + "B15012e8" + "B15012e9" as education_science_and_engineering,
    // income
    "B19001e2" as income_less_than_10000,
    "B19001e3" as income_10000_14999,
    "B19001e4" as income_15000_19999,
    "B19001e5" as income_20000_24999,
    "B19001e6" as income_25000_29999,
    "B19001e7" as income_30000_34999,
    "B19001e8" as income_35000_39999,
    "B19001e9" as income_40000_44999,
    "B19001e10" as income_45000_49999,
    "B19001e11" as income_50000_59999,
    "B19001e12" as income_60000_74999,
    "B19001e13" as income_75000_99999,
    "B19001e14" as income_100000_124999,
    "B19001e15" as income_125000_149999,
    "B19001e16" as income_150000_199999,
    "B19001e17" as income_200000_or_more,
    // occupancy
    "B25002e2" as occupancy_occupied,
    "B25002e3" as occupancy_vacant,
    // value
    "B25075e2" as value_less_than_10000,
    "B25075e3" as value_10000_14999,
    "B25075e4" as value_15000_19999,
    "B25075e5" as value_20000_24999,
    "B25075e6" as value_25000_29999,
    "B25075e7" as value_30000_34999,
    "B25075e8" as value_35000_39999,
    "B25075e9" as value_40000_49999,
    "B25075e10" as value_50000_59999,
    "B25075e11" as value_60000_69999,
    "B25075e12" as value_70000_79999,
    "B25075e13" as value_80000_89999,
    "B25075e14" as value_90000_99999,
    "B25075e15" as value_100000_124999,
    "B25075e16" as value_125000_149999,
    "B25075e17" as value_150000_174999,
    "B25075e18" as value_175000_199999,
    "B25075e19" as value_200000_249999,
    "B25075e20" as value_250000_299999,
    "B25075e21" as value_300000_399999,
    "B25075e22" as value_400000_499999,
    "B25075e23" as value_500000_749999,
    "B25075e24" as value_750000_999999,
    "B25075e25" as value_1000000_1499999,
    "B25075e26" as value_1500000_1999999,
    "B25075e27" as value_2000000_or_more,
    // time to work
    "B08303e2" as time_less_than_5_mins,
    "B08303e3" as time_5_9_mins,
    "B08303e4" as time_10_14_mins,
    "B08303e5" as time_15_19_mins,
    "B08303e6" as time_20_24_mins,
    "B08303e7" as time_25_29_mins,
    "B08303e8" as time_30_34_mins,
    "B08303e9" as time_35_39_mins,
    "B08303e10" as time_40_44_mins,
    "B08303e11" as time_45_59_mins,
    "B08303e12" as time_60_89_mins,
    "B08303e12" as time_90_or_more_mins
from "{year}_CBG_GEOMETRY_WKT" as geom
left join "{year}_CBG_B01" as sex_age on geom.CENSUS_BLOCK_GROUP = sex_age.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B02" as race on geom.CENSUS_BLOCK_GROUP = race.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B11" as household on geom.CENSUS_BLOCK_GROUP = household.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B15" as education on geom.CENSUS_BLOCK_GROUP = education.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B19" as income on geom.CENSUS_BLOCK_GROUP = income.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B25" as occupancy on geom.CENSUS_BLOCK_GROUP = occupancy.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B08" as time on geom.CENSUS_BLOCK_GROUP = time.CENSUS_BLOCK_GROUP