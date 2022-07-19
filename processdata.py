#!/usr/bin/env python3

import csv
import numpy as np
import pandas as pd

loc = 'data/mimic-iii-clinical-database-1.4/'

anemia = ['28489', '2849', '2850', '2851', '28521', '28522', '28529', '2853', '2858', '2859']
heart_rate = 'HR'#220045
blood_pressure = 'B'
oxygen = 'O'
collected_features = [heart_rate, blood_pressure, oxygen]

admin = loc + 'ADMISSIONS.csv'
diagnoses = loc + 'DIAGNOSES_ICD.csv'
chart_item = loc + 'D_ITEMS.csv'#'CHART_EVENTS.csv'

admin_data = pd.read_csv(admin)
print("ADMIN DATA COLLECTED")

diagnosis_data = pd.read_csv(diagnoses)
print("DIAGNOSIS DATA COLLECTED")

diagnosis_anemia = diagnosis_data[diagnosis_data['ICD9_CODE'].isin(anemia)]
print("ANEMIC PATIENTS COLLECTED")

anemic_patients = diagnosis_anemia['HADM_ID'].drop_duplicates().values
print(anemic_patients)

feature = pd.read_csv(chart_item)
print(feature)

features = feature[feature['CATEGORY'].isin(['Routine Vital Signs'])]
print(features)
