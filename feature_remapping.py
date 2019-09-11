


import numpy as np
import bs_ds as bs
import pandas as pd
from bs_ds.imports import *



# drop_cols = ['Fiscal_Year_Released','Days_to_Recidivism','New_Conviction_Offense_Classification',
# 'New_Conviction_Offense_Type','New_Conviction_Offense_Sub_Type','Recidivism_Type']
drop_cols = ['Fiscal Year Released', 'Days to Recidivism', 'New Conviction Offense Classification',
 'New Conviction Offense Type', 'New Conviction Offense Sub Type', 'Recidivism Type']

## RENAME COLUMNS
# feature remapping notes / code ## df.rename(mapper=column_legend, axis=1, inplace=True)
column_legend = {"Fiscal Year Released": "yr_released",
                 "Recidivism Reporting Year": "report_year", 
                 "Race - Ethnicity": "race_ethnicity",
                  "Age At Release ": "age_released",
                   "Convicting Offense Classification": "crime_class", 
                    "Convicting Offense Type": "crime_type",
                    "Convicting Offense Subtype": "crime_subtype",
                    "Release Type": "release_type", 
                    "Main Supervising District": "super_dist",
                    "Recidivism - Return to Prison": "recidivist",
                    "Part of Target Population": "target_pop",
                    "Sex": "sex"}




## REMAP RACE/ETHNICITY
# Defining Dictionary Map for race_ethnicity categories: df['race_ethnicity'] = df['race_ethnicity'].map(race_ethnicity_map)
race_ethnicity_map = {'White - Non-Hispanic':'White',
                        'Black - Non-Hispanic': 'Black',
                        'White - Hispanic' : 'Hispanic',
                        'American Indian or Alaska Native - Non-Hispanic' : 'American Native',
                        'Asian or Pacific Islander - Non-Hispanic' : 'Asian or Pacific Islander',
                        'Black - Hispanic' : 'Black',
                        'American Indian or Alaska Native - Hispanic':'American Native',
                        'White -' : 'White',
                        'Asian or Pacific Islander - Hispanic' : 'Asian or Pacific Islander',
                        'N/A -' : np.nan,
                        'Black -':'Black'}

## REMAP CRIME_CLASS
# Remapping df['crime_class'] = df['crime_class'].map(crime_class_map)
crime_class_map = {'Other Felony (Old Code)': np.nan ,#or other felony
                  'Other Misdemeanor':np.nan,
                   'Felony - Mandatory Minimum':np.nan, # if minimum then lowest sentence ==  D Felony
                   'Special Sentence 2005': 'Sex Offender',
                   'Other Felony' : np.nan ,
                   'Sexual Predator Community Supervision' : 'Sex Offender',
                   'D Felony': 'D Felony',
                   'C Felony' :'C Felony',
                   'B Felony' : 'B Felony',
                   'A Felony' : 'A Felony',
                   'Aggravated Misdemeanor':'Aggravated Misdemeanor',
                   'Felony - Enhancement to Original Penalty':'Felony - Enhanced',
                   'Felony - Enhanced':'Felony - Enhanced' ,
                   'Serious Misdemeanor':'Serious Misdemeanor',
                   'Simple Misdemeanor':'Simple Misdemeanor'}


## ENCODING AGE:
age_map = {
    "Under 25": 0,
    "25-34": 1,
    "35-44": 2,
    "45-54": 3,
    "55 and Older": 4}


## REMAP BINARY CATEGORIES
recidivist_map = {'No':0,'Yes':1}
target_pop_map = {'No':0,'Yes':1}
sex_map = {'Male':0,'Female':1}


# df['max_sentence'] =  years by crime class
crime_class_max_sentence_map = {'A Felony': 75,  # Life
                                'Aggravated Misdemeanor': 2, # 2 years
                                'B Felony': 50, # 25 or 50 years
                                'C Felony': 10, # 10 years
                                'D Felony': 5,  # 5 yeras
                                'Felony - Enhanced': 10, # Add on to class C and D felonies, hard to approximate. 
                                'Serious Misdemeanor': 1, # 1 year
                                'Sex Offender': 10, # 10 years
                                'Simple Misdemeanor': 0.83} # 30 days



## NEW MAPPINGS: 
report_yr_map = {2013:0,
2014:1,
2015:2,
2016:3,
2017:4,
2018:5}

remapping_dict={
    'columns':column_legend,
    'race_ethnicity':race_ethnicity_map,
    'crime_class':crime_class_map,
    'age_released':age_map,
    'recidivist':recidivist_map,
    'target_pop':target_pop_map,
    'sex':sex_map,
    'max_sentence':crime_class_max_sentence_map,
    'report_year':report_yr_map
    }

print('See `remapping_dict` for all column and feature name dicts.')




if __name__=='__main__':
    print('Running renamming and null removal workflow.')
    full_all_prisoners_file = "datasets/FULL_3-Year_Recidivism_for_Offenders_Released_from_Prison_in_Iowa.csv"
    df = pd.read_csv(full_all_prisoners_file)
    df.drop(drop_cols,axis=1,inplace=True)
    df.rename(mapper=column_legend,axis=1,inplace=True)

    ## DEALING WITH NULLS
    df.dropna(subset=['age_released','race_ethnicity','sex','release_type'],inplace=True)    
    df['super_dist'].fillna("unknown", inplace=True)


    ##RENAMING FEATURES
    df['race_ethnicity'] = df['race_ethnicity'].map(race_ethnicity_map)
    df['crime_class'] = df['crime_class'].map(crime_class_map)
    df['age_released'] = df['age_released'].map(age_map)

    df['recidivist'] = df['recidivist'].map(recidivist_map)
    df['sex'] = df['sex'].map(sex_map)
    df['target_pop'] = df['target_pop'].map(target_pop_map)

    ## CREATING FEATURES
    # df['felony'] = Engineering a simple 'felony' true false category
    df['felony'] = df['crime_class'].str.contains('felony',case=False)
    df['crime_types_combined'] = df['crime_type']+'_'+df['crime_subtype']
    # Combining crime_type and crime_subtype into types_combined
    df['crime_class_type_subtype']= df['crime_class']+'_'+df['crime_type']+'_'+df['crime_subtype']
    df['max_sentence'] =df['crime_class'].map(crime_class_max_sentence_map)
    df.dropna(inplace=True)