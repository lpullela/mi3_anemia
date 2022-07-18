import csv
from nturl2path import pathname2url

#changing from demo to closed access files
# icd_9_codes = ['2800', '2801', '2808', '2809', '2810', '2811', '2812', '2813', '2814', '2818', '2819', '2822', '2823', '2828', '2829', '2830', '28310', '28319', '2839', '28409', '28489', '2849', '2850', '2851', '28521', '28522', '28529', '2853', '2858', '2859', '64820', '64821', '64822', '64823', '64824', '7735', '7740', '7765', '7766', 'V182', 'V780', 'V781']
#updated code

path1 = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/D_ICD_DIAGNOSES.csv'

icd_9_codes = [] 
with open( path1, newline='') as csvfile: 
    reader = csv.reader( csvfile, delimiter=",")
    for row in reader: 
        if ( 'anemia' in row[ 2 ].lower() ) or ( 'anemia' in row[ 3 ].lower() ): 
            icd_9_codes.append( row[ 1  ] )

# print( "Anemia Codes: ", icd_9_codes )
            

path2 = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-1.4/DIAGNOSES_ICD.csv'

anemia = [[] for i in range( 100 )]
anemia_ct = 0
total_patients_list = [[] for i in range ( 100 )]
total_patients = 0
with open( path2 , newline='') as csvfile: 
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader: 
        count = 0
        try: 
            if not row[ 1 ] == 'SUBJECT_ID' and not row[ 1 ] in total_patients_list[ int( row[ 1 ] ) % 100 ]: 
                total_patients_list[ int( row[ 1 ] ) % 100 ].append( row[ 1 ] )
                total_patients = total_patients + 1 
        except IndexError: 
            print('', end='')
        pat_id = ''
        for word in row: 
            if ( count == 2 ): 
                pat_id = word
            if ( count == 4 ): 
                try: 
                    if ( word in icd_9_codes ) and not row[ 1 ] == 'SUBJECT_ID' and not row[ 1 ] in anemia[ int( row[ 1 ] ) % 100  ]  : 
                        anemia[ int( row[ 1 ] ) % 100 ].append( row[ 1 ] )
                        anemia_ct = anemia_ct + 1
                    # print( pat_id )
                except IndexError: 
                    print( '', end='')
            count = count + 1 
        
val_anemia_count = 0

for i in anemia: 
    for j in i: 
        print( j, end=',' )
        val_anemia_count = val_anemia_count + 1
    
print( "Number of Patients with Anemia: ", anemia_ct )
# print( "Validation Anemia Count: ", val_anemia_count )
print( "Number of Patients Total: ", total_patients )
print( "Percentage of Patients with Anemia: ", anemia_ct/total_patients * 100, end='' )
print( "%")


                

            


