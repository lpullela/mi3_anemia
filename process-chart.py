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

spo2_1 = 220227
spo2_2 = 646
sao2 = 834
# codes for oxygen

o2 = [spo2_1, spo2_2]
# array of codes for oxygen

sRR = 224422

rr = [sRR]

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

hght = 920
adm_hght = 226730
# codes for height

height = [adm_hght]
# array of codes for height

wght = 762
adm_wght = 226512
# codes for weight

weight = [adm_wght]
# array of codes for weight

collected_features = bp_dia + bp_sys + hr + height + weight + rr
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

feature = pd.read_csv(chart_item, usecols = [hadm, charttime, valuenum, itemid], iterator=True, chunksize=1000000)
cf = pd.DataFrame(columns = [hadm, charttime, valuenum, itemid])

i = 0

for chunk in feature:
    cf = pd.concat([cf, chunk[chunk[itemid].isin(collected_features)]], ignore_index=True)
    print(i)
    i = i + 1
    #if i == 30:
        #break

headers = [hadm, charttime, valuenum]

#cf = feature[feature[itemid].isin(collected_features)]
#cf[charttime] = pd.Timestamp(cf[charttime]).round(freq = 'H').strftime('%Y-%m-%d %X')

print("CF")
print(cf)

def makeFrame(dF, idTitle, codes, columns, name):
    result = dF[dF[idTitle].isin(codes)]
    result = result[columns]
    result.rename(columns = {valuenum:name}, inplace = True)
    #result = result.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
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

#o2_read = makeFrame(cf, itemid, o2, headers, 'O2')
#print("O2 MEASUREMENTS")
#print(o2_read)

rr_read = makeFrame(cf, itemid, rr, headers, 'RR')
print("RESPIRATORY RATES")
print(rr_read)

bp_dia_read = makeFrame(cf, itemid, bp_dia, headers, 'DIASTOLIC')
print("BLOOD PRESSURE DIASTOLIC")
print(bp_dia_read)

bp_sys_read = makeFrame(cf, itemid, bp_sys, headers, 'SYSTOLIC')
print("BLOOD PRESSURE SYSTOLIC")
print(bp_sys_read)

height_read = makeFrame(cf, itemid, height, [hadm, valuenum], 'HEIGHT')
#height_read.drop_duplicates(subset=[hadm], keep='last')
print("HEIGHT")
print(height_read)

weight_read = makeFrame(cf, itemid, weight, [hadm, valuenum], 'WEIGHT')
#weight_read.drop_duplicates(subset=[hadm], keep='last')
print('WEIGHT')
print(weight_read)

total = combine([hr_read, bp_dia_read, bp_sys_read])
total = total.merge(height_read, how = 'inner', on = [hadm])
total = total.merge(weight_read, how = 'inner', on = [hadm])
total['ANAEMIC']=total[hadm].apply(lambda x: 1 if x in anemic_patients else 0)
#total = total.drop([charttime], axis = 1)
print("TOTAL")
print(total)

total.to_csv('preprocessed_chart_data.csv')
