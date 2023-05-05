select
    geom.CENSUS_BLOCK_GROUP,
    geom.STATE,
    // sex
    "B01001e2" as "sex_males",
    "B01001e26" as "sex_females",
    // race
    "B02001e2" as "race_white",
    "B02001e3" as "race_black",
    "B02001e4" as "race_american indian and alaska",
    "B02001e5" as "race_asian",
    "B02001e6" as "race_hawaii and islanders",
    "B02001e7" as "race_some ther race alone",
    "B02001e8" as "race_mixed",
    // age
    "B01001e3" + "B01001e27" + "B01001e4" + "B01001e28" + "B01001e5" + 
    "B01001e29" + "B01001e6" + "B01001e30" as "age_under 18",
    "B01001e7" + "B01001e31" + "B01001e8" + "B01001e32" + "B01001e9" + 
    "B01001e33" + "B01001e10" + "B01001e34" as "age_18-24",
    "B01001e11" + "B01001e35" as "age_25-29",
    "B01001e12" + "B01001e36" as "age_30-34",
    "B01001e13" + "B01001e37" as "age_35-39",
    "B01001e14" + "B01001e38" as "age_40-44",
    "B01001e15" + "B01001e39" as "age_45-49",
    "B01001e16" + "B01001e40" as "age_50-54",
    "B01001e17" + "B01001e41" as "age_55-59",
    "B01001e18" + "B01001e42" + "B01001e19" + "B01001e43" as "age_60-64",
    "B01001e20" + "B01001e44" + "B01001e21" + "B01001e45" + "B01001e22" + 
    "B01001e46" + "B01001e23" + "B01001e47" + "B01001e24" + "B01001e48" +
    "B01001e25" + "B01001e49" "age_65 and above",
    // household
    "B11012e8" as "household_female householder",
    "B11012e13" as "household_male householder",
    "B11012e2" as "household_married couple",
    "B11012e5" as "household_cohabiting couple",
    //education
    "B15012e10" as "education_business",
    "B15012e11" as "education_education",
    "B15012e12" + "B15012e13" + "B15012e14" + "B15012e15" + "B15012e16" as "education_arts humanities and other",
    "B15012e2" + "B15012e3" + "B15012e4" + "B15012e5" + "B15012e6" +
    "B15012e7" + "B15012e8" + "B15012e9" as "education_science and engineering",
    // income
    "B19001e2" as "income_10000 $ or less",
    "B19001e3" as "income_10 000-14 999 $",
    "B19001e4" as "income_15 000-19 999 $",
    "B19001e5" as "income_20 000-24 999 $",
    "B19001e6" as "income_25 000-29 999 $",
    "B19001e7" as "income_30 000-34 999 $",
    "B19001e8" as "income_35 000-39 999 $",
    "B19001e9" as "income_40 000-44 999 $",
    "B19001e10" as "income_45 000-49 999 $",
    "B19001e11" as "income_50 000-59 999 $",
    "B19001e12" as "income_60 000-74 999 $",
    "B19001e13" as "income_75 000-99 999 $",
    "B19001e14" as "income_100 000-124 999 $",
    "B19001e15" as "income_125 000-149 999 $",
    "B19001e16" as "income_150 000-199 999 $",
    "B19001e17" as "income_200 000 $ or more",
    // occupancy
    "B25002e2" as "occupancy_occupied",
    "B25002e3" as "occupancy_vacant",
    // value
    "B25075e2" as "value_10 000 $ or less",
    "B25075e3" as "value_10 000-14 999 $",
    "B25075e4" as "value_15 000-19 999 $",
    "B25075e5" as "value_20 000-24 999 $",
    "B25075e6" as "value_25 000-29 999 $",
    "B25075e7" as "value_30 000-34 999 $",
    "B25075e8" as "value_35 000-39 999 $",
    "B25075e9" as "value_40 000-49 999 $",
    "B25075e10" as "value_50 000-59 999 $",
    "B25075e11" as "value_60 000-69 999 $",
    "B25075e12" as "value_70 000-79 999 $",
    "B25075e13" as "value_80 000-89 999 $",
    "B25075e14" as "value_90 000-99 999 $",
    "B25075e15" as "value_100 000-124 999 $",
    "B25075e16" as "value_125 000-149 999 $",
    "B25075e17" as "value_150 000-174 999 $",
    "B25075e18" as "value_175 000-199 999 $",
    "B25075e19" as "value_200 000-249 999 $",
    "B25075e20" as "value_250 000-299 999 $",
    "B25075e21" as "value_300 000-399 999 $",
    "B25075e22" as "value_400 000-499 999 $",
    "B25075e23" as "value_500 000-749 999 $",
    "B25075e24" as "value_750 000-999 999 $",
    "B25075e25" as "value_1 000 000-1 499 999 $",
    "B25075e26" as "value_1 500 000-1 999 999 $",
    "B25075e27" as "value_2 000 000 $ or more",
    // time to work
    "B08303e2" as "time_to_work_less than 5 mins",
    "B08303e3" as "time_to_work_5-9 mins",
    "B08303e4" as "time_to_work_10-14 mins",
    "B08303e5" as "time_to_work_15-19 mins",
    "B08303e6" as "time_to_work_20-24 mins",
    "B08303e7" as "time_to_work_25-29 mins",
    "B08303e8" as "time_to_work_30-34 mins",
    "B08303e9" as "time_to_work_35-39 mins",
    "B08303e10" as "time_to_work_40-44 mins",
    "B08303e11" as "time_to_work_45-59 mins",
    "B08303e12" as "time_to_work_60-89 mins",
    "B08303e12" as "time_to_work_90 or more mins"
from "{year}_CBG_GEOMETRY_WKT" as geom
left join "{year}_CBG_B01" as sex_age on geom.CENSUS_BLOCK_GROUP = sex_age.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B02" as race on geom.CENSUS_BLOCK_GROUP = race.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B11" as household on geom.CENSUS_BLOCK_GROUP = household.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B15" as education on geom.CENSUS_BLOCK_GROUP = education.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B19" as income on geom.CENSUS_BLOCK_GROUP = income.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B25" as occupancy on geom.CENSUS_BLOCK_GROUP = occupancy.CENSUS_BLOCK_GROUP
left join "{year}_CBG_B08" as time on geom.CENSUS_BLOCK_GROUP = time.CENSUS_BLOCK_GROUP