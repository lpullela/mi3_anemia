import csv 
path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/LABEVENTS.csv'

# anemia_lab_codes = [ '51222', '50811', '50852', '50855' ]
anemia_lab_codes = ['51222']
pat_id_list = [[] for i in range( 100 )]
normal_id_list = [ [] for i in range( 100 )]
pat_id_len = 0


row_num = 0
with open( path , newline='') as csvfile: 
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader: 
        count = 0
        if ( row_num == 0 ):
            row_num = 1
            continue
        try: 
            pat_id = row[ 1 ]
            if not pat_id in pat_id_list[ int ( pat_id ) % 100 ]: 
                pat_id_list[ int ( pat_id ) % 100 ].append(  pat_id  )
                pat_id_len = pat_id_len + 1 
        except IndexError:
            continue


# print( pat_id_list )
# print( len ( pat_id_list ) )
count = 0
normal_list_len = 0 
with open( path , newline='') as csvfile: 
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader: 
        is_normal = False
        count = count + 1
        if ( anemia_lab_codes[ 0 ] in row ) and not ( 'abnormal' in row ):
            pat_id = row[ 1 ]
            try: 
                key = int( pat_id ) % 100 
            except TypeError: 
                continue
            try: 
                if not pat_id in normal_id_list[ key ]: 
                    normal_id_list[ key ].append( pat_id )
                    normal_list_len = normal_list_len + 1
                    is_normal = True
            except IndexError: 
                continue
        if ( count % 1000 == 0 ):
            print( "Status: ", count/27854056 * 100, end='')
            print( "% complete" )

        if not is_normal: 
            print( pat_id, end='\t')
        

# for i in normal_id_list: 
#     for j in i: 
#         print( j, end=',')

print( "Number of Patients Total: ", pat_id_len )
print( "Number of Anemic Patients: ", pat_id_len  - normal_list_len )
print( "Percentage of Anemic Patients: ", ( pat_id_len - normal_list_len ) / pat_id_len * 100, end='')
print( "%" )




                
