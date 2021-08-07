# Predicting Prisoner Recidivism in Iowa
## Identifying Risk Factors with Machine Learning

**Author**: James M. Irving, Ph.D.

The contents of this repository detail an analysis of the module one project. This analysis is detailed in hopes of making the work accessible and replicable.



<img src="images/iowa_in_jail.png">

### Business problem:
The state of Iowa has a prisoner recidivism issue that it has asked for help in understanding. 
In 2015, nearly 1/3 of all released prisoners from Iowa were returning to prison within 3 years of being released.
<img src="images/recidivism_report_1.png">
<img src="images/recidivism_report_2.png">

### Data 

- Source: Iowa Department of Corrections 
    - Original Kaggle Dataset:
        - https://www.kaggle.com/slonnadube/recidivism-for-offenders-released-from-prison
    - Up-to-Date Dataset
        - https://data.iowa.gov/Correctional-System/3-Year-Recidivism-for-Offenders-Released-from-Pris/mw8r-vqy4

<img src="images/LSA_map_with_counties_districts_and_B54A5BBCE4156.jpg">

- **Statistics about recidivism in prisoners from a 3 year prisoner**
- **Target:**
    - Recidivism - Return to Prison
- **Features:**
    - Fiscal Year Released
    - Recidivism Reporting Year
    - Race - Ethnicity
    - Age At Release
    - Convicting Offense Classification
    - Convicting Offense Type
    - Convicting Offense Subtype
    - Main Supervising District
    - Release Type
    - Release type: Paroled to Detainder united
    - Part of Target Population

## Methods
- Used multiple machine learning models to find model with the best recall score for correctly identify which prisoners will return to jain.
- Features related to the crime committed after release and the time until return to jail were removed, since they are not appropriate to use to predict who will be a recidivist. 
    - All features were categorical, except for age, which was converted to a numeric vallue (e.g. "35 - 45"-> "40"


- The large number of categorical features and imbalanced classes made it very difficult for most machine learning models to achieve quality performance. 
- The models tried were:

<img src="images/modeling.png">

## Results

### Best Model

- [ ] Add scores

#### Feature Importances
<img src="images/feature_importance.png" width=70%>

> The top 4 most important features for predicting recidivism are:
    1. Age At Release
    2. Supervising Judicial District
    3. Release Type
    4. Crime Type/Subtype




#### Age at Release
<img src="images/fig_age_released.png" width=70%>

> Younger released prisoners are more likely to return to crime. 


#### Supervising Judicial District
<img src="images/fig_judicial_district.png" width=70%>
> Some Superivising Judicial districts are more likely to produce recivists.

#### Release Type
<img src="images/fig_release_type.png" width=70%>

#### Crime Type/Subtype
<img src="images/fig_crime_types.png" width=70%>


## Recommendations:

- Using our model,Iowa Department of corrections can predict which prisoners may become recidivist.
- Using this information, Iowa can implement pre-release educational programs to target at-risk prisoners.
- Following release, Iowa could also provide  post-release support and intervention to at-risk prisoners. 


## Limitations & Next Steps

The lack of numerical features was a major hurdle. The next steps should be to pull in additional information regarding the judical districts and their associated counties (population/crime rate/income, etc)

<!-- 
### For further information
Please review the narrative of our analysis in [our jupyter notebook](./index.ipynb) or review our [presentation](./SampleProjectSlides.pdf)

For any additional questions, please contact **james.irving.phd@gmail.com**


##### Repository Structure:

Here is where you would describe the structure of your repoistory and its contents, for exampe:

```

├── README.md               <- The top-level README for reviewers of this project.
├── index.ipynb             <- narrative documentation of analysis in jupyter notebook
├── presentation.pdf        <- pdf version of project presentation
└── images
    └── images               <- both sourced externally and generated from code
└── data
    └── 

``` -->
