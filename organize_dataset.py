import csv
import pandas as pd 

path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/final.csv'

df = pd.read_csv( path )
df.columns = ['PAT_ID','O2', 'HR', 'BP_SYS','BP_DIAST', 'REL', 'RACE', 'SEX', 'AGE']

df.sort_values( ['PAT_ID'], ascending=True, inplace=True )

print( df )

df.to_csv( "compiled_df.csv", index=False)