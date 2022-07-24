#!/usr/bin/env python3

import csv
import numpy as np
import pandas as pd

loc = 'data/mimic-iii-clinical-database-1.4/'
# file location of spreadsheets

anemia = ['28489', '2849', '2850', '2851', '28521', '28522', '28529', '2853', '2858', '2859']
# codes for anemia

heart_rate = 220045
# codes for heart rate

hr = [heart_rate]
# array of codes for heart rate

oxygen = 220227
# codes for oxygen

o2 = [oxygen]
# array of codes for oxygen

bp_dia_r = 227242
bp_dia_l = 224643
bp_dia_1 = 220051
bp_dia_2 = 225310
bp_dia_ni = 220180
# codes for diastolic blood pressure

bp_sys_r = 227243
bp_sys_l = 224167
bp_sys_1 = 220050
bp_sys_2 = 225309
bp_sys_ni = 220179
# codes for systolic blood pressure


bp_dia = [bp_dia_r, bp_dia_l, bp_dia_1, bp_dia_2, bp_dia_ni]
bp_sys = [bp_sys_r, bp_sys_l, bp_sys_1, bp_sys_2, bp_sys_ni]
# arrays of codes for diastolic and systolic blood pressure

collected_features = bp_dia + bp_sys + o2 + hr
# array of all collected features codes

admit = loc + 'ADMISSIONS.csv'
diagnoses = loc + 'DIAGNOSES_ICD.csv'
chart_item = loc + 'CHARTEVENTS.csv'

#admit_data = pd.read_csv(admit)

itemid = 'ITEMID'
icd9 = 'ICD9_CODE'
hadm = 'HADM_ID'
charttime = 'CHARTTIME'
valuenum = 'VALUENUM'

diagnosis_data = pd.read_csv(diagnoses, usecols = [hadm, icd9])

print(diagnosis_data)
diagnosis_anemia = diagnosis_data[diagnosis_data[icd9].isin(anemia)]
print(diagnosis_anemia)
anemic_patients = diagnosis_anemia[hadm].drop_duplicates()
print("ANEMIC PATIENTS")
print(anemic_patients)
# anemic patients array

feature = pd.read_csv(chart_item, usecols = [hadm, charttime, valuenum, itemid])
print(feature)

headers = [hadm, charttime, valuenum]

cf = feature[feature[itemid].isin(collected_features)]
print(cf)

def makeFrame(dF, idTitle, codes, columns, name):
    result = dF[dF[idTitle].isin(codes)]
    result = result[columns]
    result.rename(columns = {valuenum:name}, inplace = True)
    return result

def mergeFrames(dF1, dF2):
    return dF2.merge(dF1, how = 'inner', on = [hadm, charttime])

def combine(DF):
    result = DF[0]
    for index, frame in enumerate(DF):
        if index != 0:
            result = mergeFrames(result, frame)
    return result
        

hr_read = makeFrame(cf, itemid, hr, headers, 'HR')
print("HEART RATES")
print(hr_read)

o2_read = makeFrame(cf, itemid, o2, headers, 'O2')
print("O2 MEASUREMENTS")
print(o2_read)

bp_dia_read = makeFrame(cf, itemid, bp_dia, headers, 'DIASTOLIC')
print("BLOOD PRESSURE DIASTOLIC")
print(bp_dia_read)

bp_sys_read = makeFrame(cf, itemid, bp_sys, headers, 'SYSTOLIC')
print("BLOOD PRESSURE SYSTOLIC")
print(bp_sys_read)

total = combine([hr_read, o2_read, bp_dia_read, bp_sys_read])
total['ANAEMIC']=total[hadm].apply(lambda x: 1 if x in anemic_patients else 0)
total = total.drop([charttime], axis = 1)
print("TOTAL")
print(total)

total.to_csv('total.csv')
