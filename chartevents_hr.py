# import csv
# path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/CHARTEVENTS.csv'
# newfile = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/CHARTEVENTS_HR.csv'

# hr_code = [ '211', '220045' ]
# count = 0

# file = open( newfile , "w" )

# with open( path , newline='') as csvfile: 
#     reader = csv.reader(csvfile, delimiter=",")
#     for row in reader: 
#         if hr_code[ 0 ] in row or hr_code[ 1 ] in row: 
#             count = 0
#             for item in row:
#                 count = count + 1
#                 file.write( item )
#                 if not count == 15: 
#                     file.write(",")
#             file.write("\n")
    
# print( "all heart rate readings written to seperate HR file! ")

import csv

warn = str( input( "WARNING!: Do you want to run this file? you will lose data in HR avg file: " ) )
if not warn.lower() == 'yes': 
    exit()

path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/CHARTEVENTS_HR.csv'

#index 1 is patient_id 

newfile = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/HR_AVG.csv'

file = open( newfile, 'w' )
HT_SIZE = 200 
heart_rates = [ [] for i in range( HT_SIZE ) ]

#you should create a list of lists
#[ pat_id, total heart rate, num entries ]
#the hash table is a list of list of lists

with open( path, newline='' ) as csvfile: 
    reader = csv.reader( csvfile, delimiter=',' )
    for row in reader: 
        pat_id = int( row[ 1 ] )
        create_new_entry = True
        #create a hash table of size 100 - 200
        #each link in the hash table has a list of pat_id key % HT_SIZE
        #each item in the hash table is a list: [pat_id, heart rate total, num_entries]
        for item in heart_rates[ pat_id % HT_SIZE ]: 
            if ( item[ 0 ] == pat_id ): 
                create_new_entry = False
                try: 
                    if float( row[ 9 ] ) != 0:
                        item[ 1 ] = item[ 1 ] + float( row[ 9 ] )
                        item[ 2 ] = item[ 2 ] + 1
                except ValueError: 
                    continue
        if create_new_entry: 
            try: 
                heart_rates[ pat_id % HT_SIZE ].append( [ pat_id, float( row[ 9 ] ), 1 ])
            except ValueError: 
                continue

        # if not pat_id in [ item[ 0 ] for item in heart_rates[ pat_id % HT_SIZE ] ]:
        #     try: 
        #         heart_rates[ pat_id % HT_SIZE ].append( [ pat_id, float( row[ 9 ] ), 1 ] )
        #     except ValueError: 
        #         continue
        #     #may require some exception handeling
        # else: 
        #     for item in heart_rates[ pat_id % HT_SIZE ]: 
        #         if ( item[ 0 ] == pat_id ): 
        #             try: 
        #                 item[ 1 ] = item[ 1 ] + float( row[ 9 ] )
        #                 item[ 2 ] = item[ 2 ] + 1
        #             except ValueError: 
        #                 continue

# print( heart_rates[ 69843 % HT_SIZE ])
for lst in heart_rates: 
    for item in lst: 
        if item[ 2 ] != 0:
            file.write( str( item[ 0 ] ))
            file.write( "," )
            file.write( str( round ( item[ 1 ] / item[ 2 ], 3 ) ) ) 
            file.write( "\n" )
file.close()

            

        
