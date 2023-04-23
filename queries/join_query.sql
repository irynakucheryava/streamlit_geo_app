select 
    // Gender
    "B01001e10" + "B01001e11" + "B01001e12" + "B01001e13" + "B01001e14" + "B01001e15" + "B01001e16" + "B01001e17" +     
    "B01001e18" + "B01001e19" + "B01001e20" + "B01001e21" + "B01001e22" + "B01001e23" + "B01001e24" + "B01001e25" +
    "B01001e3" + "B01001e4" + "B01001e5" + "B01001e6" + "B01001e7" + "B01001e8" + "B01001e9" as sex_males,
    "B01001e26" + "B01001e27" + "B01001e28" + "B01001e29" + "B01001e30" + "B01001e31" + "B01001e32" + "B01001e33" +     
    "B01001e34" + "B01001e35" + "B01001e36" + "B01001e37" + "B01001e38" + "B01001e39" + "B01001e40" + "B01001e41" +
    "B01001e42" + "B01001e43" + "B01001e44" + "B01001e45" as sex_females,
    // Age
    "B01001e3" + "B01001e27" + "B01001e4" + "B01001e28" + "B01001e5" + "B01001e29" + "B01001e6" + "B01001e30" as age_under_18,
    "B01001e7" + "B01001e31" + "B01001e8" + "B01001e32" + "B01001e9" + "B01001e33" + "B01001e10" + "B01001e34" as age_18_24,
    "B01001e11" + "B01001e35" as age_25_29,
    "B01001e12" + "B01001e36" as age_30_34,
    "B01001e13" + "B01001e37" as age_35_39,
    "B01001e14" + "B01001e38" as age_40_44,
    "B01001e15" + "B01001e39" as age_45_49,
    "B01001e16" + "B01001e40" as age_50_54,
    "B01001e17" + "B01001e41" as age_55_59,
    "B01001e18" + "B01001e42" + "B01001e19" + "B01001e43" as age_60_64,
    "B01001e20" + "B01001e44" + "B01001e21" + "B01001e45" + "B01001e22" + "B01001e46" + "B01001e23" + "B01001e47" + "B01001e24" + "B01001e48" +
    "B01001e25" + "B01001e49" age_above_65,
    // Race
    "B02001e2" as race_white,
    "B02001e3" as race_black,
    "B02001e4" as race_american_indian_and_alaska,
    "B02001e5" as race_asian,
    "B02001e6" as race_hawaii_and_islanders,
    "B02001e7" + "B02001e8" + "B02001e9" + "B02001e10" + as race_mixed,
    // Household
    "B11001Ae2" + "B11001Ae3" + "B11001Ae4" + "B11001Ae5" + "B11001Ae6" + 
    "B11001Be2" + "B11001Be3" + "B11001Be4" + "B11001Be5" + "B11001Be6" + 
    "B11001Ce2" + "B11001Ce3" + "B11001Ce4" + "B11001Ce5" + "B11001Ce6" + 
    "B11001De2" + "B11001De3" + "B11001De4" + "B11001De5" + "B11001De6" + 
    "B11001Fe2" + "B11001Fe3" + "B11001Fe4" + "B11001Fe5" + "B11001Fe6" +
    "B11001Ge2" + "B11001Ge3" + "B11001Ge4" + "B11001Ge5" + "B11001Ge6" + 
    "B11001He2" + "B11001He3" + "B11001He4" + "B11001He5" + "B11001He6" +
    "B11001Ie2" + "B11001Ie3" + "B11001Ie4" + "B11001Ie5" + "B11001Ie6" as household_family_household,
    "B11001Ae7" + "B11001Ae8" + "B11001Ae9" +
    "B11001Be7" + "B11001Be8" + "B11001Be9" +
    "B11001Ce7" + "B11001Ce8" + "B11001Ce9" +
    "B11001De7" + "B11001De8" + "B11001De9" +
    "B11001Fe7" + "B11001Fe8" + "B11001Fe9" +
    "B11001Ge7" + "B11001Ge8" + "B11001Ge9" +
    "B11001He7" + "B11001He8" + "B11001He9" +
    "B11001Ie7" + "B11001Ie8" + "B11001Ie9" as household_non_family_household,
    // marital status
    "B12001e10" + "B12001e19" as maritalstatus_divorced,
    "B12001e12" + "B12001e3" as maritalstatus_never_married,
    "B12001e19" + "B12001e9" as maritalstatus_widowed,
    "B12001e13" + "B12001e14" + "B12001e15" + "B12001e16" + "B12001e17" +
    "B12001e4" + "B12001e5" + "B12001e6" + "B12001e7" + "B12001e8" as maritalstatus_married,
    // Education
    "B15002e10" + "B15002e27" as education_12thgrade,
    "B15002e11" + "B15002e28" as education_high_school,
    "B15002e12" + "B15002e29" + 
    "B15002e13" + "B15002e30"as education_collegde
    "B15002e14" + "B15002e31" as education_associate_degree,
    "B15002e15" + "B15002e32" as education_bachelor_degree,
    "B15002e16" + "B15002e33" as education_master_degree,
    "B15002e17" + "B15002e34" as education_professional_school_degree,
    "B15002e18" + "B15002e35" as education_doctorate_degree
from "2019_CBG_B01" as sex_age
join "2019_CBG_B02" as race on sex_age.CENSUS_BLOCK_GROUP = race.CENSUS_BLOCK_GROUP
join "2019_CBG_B11" as household on sex_age.CENSUS_BLOCK_GROUP = household.CENSUS_BLOCK_GROUP
join "2019_CBG_B12" as marital_status on sex_age.CENSUS_BLOCK_GROUP = marital_status.CENSUS_BLOCK_GROUP
join "2019_CBG_B15" as education on sex_age.CENSUS_BLOCK_GROUP = education.CENSUS_BLOCK_GROUP