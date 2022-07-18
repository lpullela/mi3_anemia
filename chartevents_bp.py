# import csv
# path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/CHARTEVENTS.csv'
# newfile = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/CHARTEVENTS_BP.csv'

# bp_arterial_codes = [ '225310' , '220050' ] #diastolic blood pressure, systolic bp
# bp_noninvasive_codes = [ '220181', '220179' ]

# count = 0

# file = open( newfile , "w" )

# def isBPRelated( row ): 
#     if bp_arterial_codes[ 0 ] in row or bp_arterial_codes[ 1 ] in row: 
#         return True
#     if bp_noninvasive_codes[ 0 ] in row or bp_noninvasive_codes[ 1 ] in row: 
#         return True
#     return False

# with open( path , newline='') as csvfile: 
#     reader = csv.reader(csvfile, delimiter=",")
#     for row in reader: 
#         if isBPRelated( row ): 
#             count = 0
#             for item in row:
#                 count = count + 1
#                 file.write( item )
#                 if not count == 15: 
#                     file.write(",")
#             file.write("\n")
    
# print( "all blood pressure readings written to seperate BP file! ")


import csv
path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/CHARTEVENTS_BP.csv'

#index 1 is patient_id 

newfile = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/BP_AVG.csv'

warn = str( input( "WARNING!: Do you want to run this file? you will lose data in BP avg file: " ) )
if not warn.lower() == 'yes': 
    exit()

file = open( newfile, 'w' )
HT_SIZE = 200 
blood_pressures = [ [] for i in range( HT_SIZE ) ]

#you should create a list of lists
#make these elements as tuples, second element is the count
#[ pat_id, sys_arterial, sys_noninvasive, diast_arterial, diast_noninvasive ]
#the hash table is a list of list of lists

def mapToCode( event_code ): 
    if event_code == 225310: 
        return 3
    if event_code == 220050: 
        return 1
    if event_code == 220181: 
        return 4
    if event_code == 220179: 
        return 2
    else: 
        return -1
    #returns an index value

def createNewEntry( row ): 
    index = mapToCode( row[ 4 ] )
    entry = []
    for i in range( 4 ): 
        if i == 0: 
            entry.append( int( row[ 1 ] ) ) 
        if index == i: 
            entry.append( [ int( row[ 4 ] ), 1 ] )
        else: 
            entry.append( [0, 0] )
    blood_pressures[ int( row[ 1 ] ) % HT_SIZE ].append( entry )


def addEntry( item, pat_id, event_code, bp ): 
    # bp_arterial_codes = [ '225310' , '220050' ] #diastolic blood pressure, systolic bp
    # bp_noninvasive_codes = [ '220181', '220179' ]
    index = mapToCode( event_code )
    if index != -1 and bp != 0: 
        item[ index ][ 0 ] = item[ index ][ 0 ] + bp
        item[ index ][ 1 ] = item[ index ][ 1 ] + 1
    return item


with open( path, newline='' ) as csvfile: 
    reader = csv.reader( csvfile, delimiter=',' )
    for row in reader: 
        pat_id = int( row[ 1 ] )
        create_new_entry = True
        #create a hash table of size 100 - 200
        #each link in the hash table has a list of pat_id key % HT_SIZE
        #each item in the hash table is a list: [pat_id, heart rate total, num_entries]
        for item in blood_pressures[ pat_id % HT_SIZE ]: 
            if ( item[ 0 ] == pat_id ): 
                create_new_entry = False
                try: 
                    # if float( row[ 9 ] ) != 0:
                    #     item[ 1 ] = item[ 1 ] + float( row[ 9 ] )
                    #     item[ 2 ] = item[ 2 ] + 1
                    item = addEntry( item, pat_id, int( row[ 4 ] ), int( row[ 8 ] ))
                except ValueError: 
                    continue
        if create_new_entry: 
            try: 
                createNewEntry( row )
            except ValueError: 
                continue

file = open( newfile, "w" )
for hash in blood_pressures: 
    for item in hash: 
        file.write( str( item[ 0 ] ) )
        if ( item[ 2 ][ 1 ] != 0 ): 
            file.write( "," )
            file.write( str( round( item[ 2 ][ 0 ] / item[ 2 ][ 1 ], 2 ) ) )
        if ( item[ 4 ][ 1 ] != 0 ): 
            file.write( "," )
            file.write( str( round( item[ 4 ][ 0 ] / item[ 4 ][ 1 ], 2 ) ) )
        file.write( "\n" )

file.close()

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

#examples of a few patients: 
# print( "Patient:                   ", blood_pressures[ 150 ][ 0 ][ 0 ] )
# print( "Arterial BP Systolic:      ", round( blood_pressures[ 150 ][ 0 ][ 1 ][ 0 ]/blood_pressures[ 150 ][ 0 ][ 1 ][ 1 ] , 2 ) )
# print( "Non-Invasive BP Systolic:  ", round( blood_pressures[ 150 ][ 0 ][ 2 ][ 0 ]/blood_pressures[ 150 ][ 0 ][ 2 ][ 1 ] , 2 ))
# #print( "Arterial BP: Diastolic: ", round( blood_pressures[ 150 ][ 0 ][ 3 ][ 0 ]/blood_pressures[ 150 ][ 0 ][ 3 ][ 1 ] , 3 ) )
# print( "Non-Invasive BP Diastolic: ", round( blood_pressures[ 150 ][ 0 ][ 4 ][ 0 ]/blood_pressures[ 150 ][ 0 ][ 4 ][ 1 ] , 2 ))

# print()
# print( "Patient:                   ", blood_pressures[ 42 ][ 0 ][ 0 ] )
# # print( "Arterial BP Systolic:      ", round( blood_pressures[ 42 ][ 0 ][ 1 ][ 0 ]/blood_pressures[ 42 ][ 0 ][ 1 ][ 1 ] , 2 ) )
# print( "Non-Invasive BP Systolic:  ", round( blood_pressures[ 42 ][ 0 ][ 2 ][ 0 ]/blood_pressures[ 42 ][ 0 ][ 2 ][ 1 ] , 2 ))
# # print( "Arterial BP: Diastolic: ", round( blood_pressures[ 150 ][ 0 ][ 3 ][ 0 ]/blood_pressures[ 150 ][ 0 ][ 3 ][ 1 ] , 3 ) )
# print( "Non-Invasive BP Diastolic: ", round( blood_pressures[ 42 ][ 0 ][ 4 ][ 0 ]/blood_pressures[ 42 ][ 0 ][ 4 ][ 1 ] , 2 ))

# hash = 78
# el = 2
# print()
# print( "Patient:                   ", blood_pressures[ hash ][ el ][ 0 ] )
# # print( "Arterial BP Systolic:      ", round( blood_pressures[ hash ][ el ][ 1 ][ 0 ]/blood_pressures[ hash ][ el ][ 1 ][ 1 ] , 2 ) )
# print( "Non-Invasive BP Systolic:  ", round( blood_pressures[ hash ][ el ][ 2 ][ 0 ]/blood_pressures[ hash ][ el ][ 2 ][ 1 ] , 2 ))
# # print( "Arterial BP: Diastolic: ", round( blood_pressures[ hash ][ el ][ 3 ][ 0 ]/blood_pressures[ hash ][ el ][ 3 ][ 1 ] , 3 ) )
# print( "Non-Invasive BP Diastolic: ", round( blood_pressures[ hash ][ el ][ 4 ][ 0 ]/blood_pressures[ hash ][ el ][ 4 ][ 1 ] , 2 ))

# hash = 199
# el = 3
# print()
# print( "Patient:                   ", blood_pressures[ hash ][ el ][ 0 ] )
# # print( "Arterial BP Systolic:      ", round( blood_pressures[ hash ][ el ][ 1 ][ 0 ]/blood_pressures[ hash ][ el ][ 1 ][ 1 ] , 2 ) )
# print( "Non-Invasive BP Systolic:  ", round( blood_pressures[ hash ][ el ][ 2 ][ 0 ]/blood_pressures[ hash ][ el ][ 2 ][ 1 ] , 2 ))
# # print( "Arterial BP: Diastolic: ", round( blood_pressures[ hash ][ el ][ 3 ][ 0 ]/blood_pressures[ hash ][ el ][ 3 ][ 1 ] , 3 ) )
# print( "Non-Invasive BP Diastolic: ", round( blood_pressures[ hash ][ el ][ 4 ][ 0 ]/blood_pressures[ hash ][ el ][ 4 ][ 1 ] , 2 ))

# for lst in heart_rates: 
#     for item in lst: 
#         if item[ 2 ] != 0:
#             file.write( str( item[ 0 ] ))
#             file.write( "," )
#             file.write( str( round ( item[ 1 ] / item[ 2 ], 3 ) ) ) 
#             file.write( "\n" )
# file.close()