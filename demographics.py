import csv
from dates import calc_age

admissions_path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/ADMISSIONS.csv'
#create a hash table with all the patients and add to combined csv file 

combined_path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/combined.csv'
new_file = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/final.csv'
patients_path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/PATIENTS.csv'

warn = input( "Are you sure you want to proceed with changing the combined.csv file?: ")
if not warn.lower() == 'yes': 
    exit() 

1, 11, 13

data_ht = [ [] for i in range( 200 ) ]
SIZE_HT = 200

races = []
religions = []


with open( admissions_path, newline='' ) as csvfile: 
    reader = csv.reader( csvfile, delimiter=',' )
    for row in reader: 
        if not row[ 1 ] == 'SUBJECT_ID':
            data_ht[ int( row[ 1 ] ) % SIZE_HT ].append( [ row[ 1 ], row[ 3 ], row[ 11 ], row[ 13 ] ] )
            if not row[ 11 ] in religions: #add to the list to see all the categories
                religions.append( str( row[ 11 ] ))
            if not row[ 13 ] in races: 
                races.append( str( row[ 13 ] ))

religions.sort() #convert to numbers
races.sort() #convert to numbers

# print( "Religions: ", religions )
# print( "Number of Religions: ", len( religions ))
# print( "Races: ", races )
# print( "number of races: ", len( races ) ) 

#convert races to numbers

def createDict( lst ): 
    new_dict = {}
    keys = len( lst )
    values = lst
    for i in range( keys ): 
        new_dict[ i ] = values[ i ]

    return {value:key for key, value in new_dict.items()}

races_dict = createDict( races )
religions_dict = createDict( religions )

for lst in data_ht: 
    for item in lst: 
        item[ 2 ] = str( religions_dict[ item[ 2 ] ] )
        item[ 3 ] = str( races_dict[ item[ 3 ] ] )



#current data hash table: [ patient_id, religion, race ]
#we want to add: [ ... age, gender ]
#append elements [ 1:end ] for each list -> list in hash table
#add to row based on patient id

#question: 
#are these the only features we want to use? 

#adding patients data to the above hash table: 
#adding age as months

def genToNum( char ): 
    if char.lower() == 'm': 
        return '0'
    if char.lower() == 'f': 
        return '1'
    return '2'

with open( patients_path, newline='' ) as csvfile: 
    reader = csv.reader( csvfile, delimiter=',' )
    for row in reader: 
        if row[ 1 ] == 'SUBJECT_ID': 
            continue
        for item in data_ht[ int( row[ 1 ] ) % SIZE_HT ]: 
            if item[ 0 ] == row[ 1 ]: 
                item.append( genToNum ( row[ 2 ] ) ) #gender: 0 for males and 1 for females, 2 for other
                item.append( str(calc_age( item[ 1 ], row[ 3 ] ))) #date of birth, most be converted into months
                item.pop( 1 )

print( data_ht[ 0 ][ 0 ])


# count = 0
# over_85 = 0
# for item in data_ht: 
#     for pat in item: 
#         if int( pat[ 4 ] ) > 89:
#             over_85 = over_85 + 1
#         count = count + 1

# print( "Percentage of patients over 85: ", round( over_85 /count * 100 , 3 ) , end = "" )
# print( "%" )



with open( combined_path, newline='' ) as csvfile: 
    with open( new_file, 'w', newline='' ) as csvfile_new: 
        writer = csv.writer( csvfile_new, delimiter = ',')
        reader = csv.reader( csvfile, delimiter=',' )
        for row in reader: 
            try: 
                for item in data_ht[ int( row[ 0 ] ) % 200 ]: 
                    if item[ 0 ] == row[ 0 ]:
                        newrow = row + item[ 1:None ]
                        writer.writerow( newrow )
                        newrow.clear()
            except ValueError: 
                continue
csvfile.close()

csvfile_new.close()



        
                


