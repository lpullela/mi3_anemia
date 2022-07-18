import csv

admissions_path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/ADMISSIONS.csv'
#create a hash table with all the patients and add to combined csv file 

combined_path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/combined.csv'

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
            data_ht[ int( row[ 1 ] ) % SIZE_HT ].append( [ row[ 1 ], row[ 11 ], row[ 13 ] ] )
            if not row[ 11 ] in religions: 
                religions.append( row[ 11 ] )
            if not row[ 13 ] in races: 
                races.append( row[ 13 ] )

religions.sort() 
races.sort()

print( "Religions: ", religions )
print( "Number of Religions: ", len( religions ))
print( "Races: ", races )
print( "number of races: ", len( races ) ) 

with open( combined_path, newline='' ) as csvfile: 
    reader = csv.reader( csvfile, delimiter=',' )
    writer = csv.writer( csvfile )
    row = []
    for line in reader: 
        for el in data_ht[ int( line[ 0 ] ) % SIZE_HT ]: 
            if el[ 0 ] == line[ 0 ]: 
                for item in el: 
                    row.append( item )
                    row.append( el[ 1 ] )
                    row.append( el[ 2 ] )
                 writer.writerow( row )

                


