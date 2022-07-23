import math 
import pandas as pd
import numpy
from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import csv

colnum = 0

def o2_onehot( o2_col ): 
	bins = [ 85, 90, 91, 92, 93, 94, 95 ]
	start = 95
	while start < 100: 
		bins.append( start + 0.25 )
		start = start + 0.25
	
	one_hot_array = []

	for element in o2_col: 
		app = True
		for i in range ( len( bins )): 
			if int( element ) < bins[ i ]: 
				one_hot_array.append( i )
				app = False
				break
		if app: 
			one_hot_array.append( len( bins ))
	
	return one_hot_array 

def hr_onehot( hr_col ): 
	bins = [ 50, 60 ]
	start = 60
	while start < 125: 
		bins.append( start + 2.5 )
		start = start + 2.5
	
	one_hot_array = []

	for element in hr_col: 
		app = True
		for i in range ( len( bins )): 
			if int( element ) < bins[ i ]: 
				one_hot_array.append( i )
				app = False
				break
		if app: 
			one_hot_array.append( len( bins ))
	
	return one_hot_array 

def age( age_col ): 
	bins = [ 20 ]
	start = 20
	while start < 90: 
		bins.append( start + 5 )
		start = start + 5
	
	one_hot_array = []

	for element in age_col: 
		app = True
		for i in range ( len( bins )): 
			if int( element ) < bins[ i ]: 
				one_hot_array.append( i )
				app = False
				break
		if app: 
			one_hot_array.append( len( bins ))
	
	return one_hot_array 

def bp_diast( age_col ): 
	bins = [ 60 ]
	start = 60
	while start < 100: 
		bins.append( start + 5 )
		start = start + 5
	
	one_hot_array = []

	for element in age_col: 
		app = True
		for i in range ( len( bins )): 
			if int( element ) < bins[ i ]: 
				one_hot_array.append( i )
				app = False
				break
		if app: 
			one_hot_array.append( len( bins ))
	
	return one_hot_array 

def bp_syst( age_col ): 
	bins = [ 80,100 ]
	start = 100
	while start < 160: 
		bins.append( start + 5 )
		start = start + 5
	
	one_hot_array = []

	for element in age_col: 
		app = True
		for i in range ( len( bins )): 
			if int( element ) < bins[ i ]: 
				one_hot_array.append( i )
				app = False
				break
		if app: 
			one_hot_array.append( len( bins ))
	
	return one_hot_array 


def convert_to_onehot( data ): 
	values = array( data )
	label_encoder = LabelEncoder()
	integer_encoded = label_encoder.fit_transform( values )
	onehot_encoder = OneHotEncoder( sparse=False )
	integer_encoded = integer_encoded.reshape( len( integer_encoded ), 1 )
	onehot_encoded = onehot_encoder.fit_transform( integer_encoded )

	return onehot_encoded



# def addToDataFrame( df, lst, colname ): 
# 	global colnum
# 	df.insert( colnum, colname, lst )
# 	colnum = colnum + 1	
# 	return df

# #main function: 
df = pd.read_csv( 'compiled_df.csv' )
# anemia = []
# csvfile = open( 'anemic_patients.csv', newline='')
# reader = csv.reader( csvfile, delimiter=",")
# reader_lst = []
# for row in reader: 
# 	reader_lst = reader_lst + row 

# count = 0
# total = 0 
# for element in df[ 'PAT_ID' ]: 
# 	if str( element ) in reader_lst: 
# 		anemia.append( 1 )
# 		count = count + 1
# 	else: 
# 		anemia.append( 0 )
# 	total = total + 1
	
# print( "Count of Anemics: ", count )
# print( "Percentage of Anemics: ", count / total * 100 , end="")
# print( "%" )
# df[ 'ANEMIA' ] = anemia
# onehot_df = pd.DataFrame()

# warn = input( "Do you want to regenerate csv file: ")
# if warn.lower() == 'yes':
# 	df.to_csv( 'compiled_df.csv', index=False )


# print( df )

o2_lst = numpy.array( convert_to_onehot( o2_onehot( df[ "O2" ] )) )
hr_lst = numpy.array( convert_to_onehot( hr_onehot( df[ "HR" ].tolist() ) ) )
bpsys_lst = numpy.array( convert_to_onehot( bp_syst( df[ "BP_SYS" ].tolist() ) ) )
bpdiast_lst = numpy.array( convert_to_onehot( bp_diast( df[ "BP_DIAST" ].tolist() ) ) )
age_lst = numpy.array( convert_to_onehot( age( df[ "AGE" ].tolist() ) ) )
rel_lst = numpy.array( convert_to_onehot( df[ "REL" ].tolist() ) )
race_lst = numpy.array( convert_to_onehot( df[ "RACE" ].tolist() ) )
gender_lst = numpy.array( convert_to_onehot( df[ 'SEX' ]) )

def create_tensor( df, row ): 
	global o2_lst, hr_lst, bpsys_lst, bpdiast_lst, age_lst, rel_lst, race_lst, gender_lst 
	# print( "O2 Encoding      : " , o2_lst[ 0 ] )
	# print( "HR Encoding      : ", hr_lst[ 0 ] )
	# print( "BP Systo Encoding: ", bpsys_lst[ 0 ] )
	# print( "BP Diast Encoding: ", bpdiast_lst[ 0 ] )
	# print( "Age Encoding     : ", age_lst[ 0 ] )
	stack = numpy.concatenate( [ o2_lst[ row ], hr_lst[ row ], bpsys_lst[ row ], bpdiast_lst[ row ], age_lst[ row ], rel_lst[ row ], race_lst[ row ], gender_lst[ row ] ] )
	# print( stack )

	return df[ "ANEMIA" ].tolist()[ row ], stack 
	#return ( anemia, vector of features )

# anemic, tensor = create_tensor( df, 0 )
# if anemic == 1: 
# 	print( "Patient is Anemic")
# else: 
# 	print( "patient is not anemic")

# print( "Tensor: ", tensor )

# print( '\n\n')

# anemic, tensor = create_tensor( df, 150 )
# if anemic == 1: 
# 	print( "Patient is Anemic")
# else: 
# 	print( "patient is not anemic")

# print( "Tensor: ", tensor )

# print( '\n\n')

# anemic, tensor = create_tensor( df, 100 )
# if anemic == 1: 
# 	print( "Patient is Anemic")
# else: 
# 	print( "patient is not anemic")

# print( "Tensor: ", tensor )


	 
	
