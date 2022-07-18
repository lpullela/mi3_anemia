import csv
FILE = 'DIAGNOSES_ICD.csv'
path = '/Users/layapullela/Projects/MI3-2022/mimic3-anemia/mimic-iii-clinical-database-demo-1.4/D_ICD_DIAGNOSES.csv'

with open( path , newline='') as csvfile: 
    reader = csv.reader(csvfile, delimiter=",")
    
    anemic = 0
    total = 0 
    icd_9_codes = []

    for row in reader: 
        count = 0
        anemia = False
        for word in row:
            if ( count == 1 ):
                icd_9 = word
            count = count + 1
            if ( "anemia" in word or "Anemia" in word ):
                anemia = True
        if anemia: 
            icd_9_codes.append( icd_9 )
            icd_9 = ''

print( icd_9_codes )
          

        
