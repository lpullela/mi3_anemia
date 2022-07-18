import csv
hr_file_path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/HR_AVG.csv'
bp_file_path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/BP_AVG.csv'
o2_file_path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/O2_AVG.csv'

path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/combined.csv'

warn = str( input( "WARNING!: Do you want to run this file? you will regenerate combined data file: " ) )
if not warn.lower() == 'yes': 
    exit()


data_ht = [ [] for i in range( 200 ) ]
pat_list = []



with open( o2_file_path, newline='' ) as csvfile: 
    o2_reader = csv.reader( csvfile, delimiter=',' )
    for row in o2_reader: 
        data_ht[ int( row[ 0 ] ) % 200 ].append( [ row[ 0 ] , row[ 1 ] ])

with open( hr_file_path, newline = '') as csvfile: 
    hr_reader = csv.reader( csvfile, delimiter="," )
    for row in hr_reader: 
        # match_found = False
        for item in data_ht[ int( row[ 0 ] ) % 200 ]: 
            try: 
                if item[ 0 ] == row[ 0 ]:
                    item.append( row[ 1 ] )
            except IndexError: 
                continue
                # match_found = True
        # if not match_found: 
        #     data_ht[ int( row[ 0 ] ) % 200 ].append( row[ 0 ] )


with open( bp_file_path, newline = '') as csvfile: 
    bp_reader = csv.reader( csvfile, delimiter="," )
    for row in bp_reader:
        for item in data_ht[ int( row[ 0 ] ) % 200 ]: 
            try: 
                if item[ 0 ] == row[ 0 ]: 
                    item.append( row[ 1 ] )
                    item.append( row[ 2 ] )
            except IndexError: 
                continue


file = open( path, 'w' )

file.write( "pat_id") #patient id
file.write( ",")
file.write( "o2_avg (pox)") #average o2 reading, pulse ox 
file.write( "," )
file.write( "hr_avg")
file.write( "," )
file.write( "bp_sys_avg (nonInv)")
file.write( "," )
file.write( "bp_diast_avg (nonInv)" )
file.write( "\n" )

for lst in data_ht: 
    for item in lst: 
        #name, hr, bp sys, bp diastolic, o2 
        if len( item ) == 5: 
            file.write( item[ 0 ] )
            file.write(",")
            file.write( item[ 1 ] )
            file.write( ",")
            file.write( item[ 2 ] )
            file.write( ",")
            file.write( item[ 3 ] )
            file.write( ",")
            file.write( item[ 4 ] )
            file.write( "\n")
print( data_ht )
file.close() 
print( "Done!" )


