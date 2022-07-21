import math 
import pandas as pd
from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

colnum = 0

def o2_onehot( o2_col ): 
	bins = [ 85, 90, 91, 92, 93, 94, 95 ]
	start = 95
	while start < 100: 
		bins.append( start + 0.5 )
		start = start + 0.5
	
	one_hot_array = []

	for element in o2_col: 
		app = True
		for i in range ( len( bins )): 
			if element < bins[ i ]: 
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
		bins.append( start + 5 )
		start = start + 5
	
	one_hot_array = []

	for element in hr_col: 
		app = True
		for i in range ( len( bins )): 
			if element < bins[ i ]: 
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
		bins.append( start + 10 )
		start = start + 10
	
	one_hot_array = []

	for element in age_col: 
		app = True
		for i in range ( len( bins )): 
			if element < bins[ i ]: 
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
		bins.append( start + 10 )
		start = start + 10
	
	one_hot_array = []

	for element in age_col: 
		app = True
		for i in range ( len( bins )): 
			if element < bins[ i ]: 
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
		bins.append( start + 10 )
		start = start + 10
	
	one_hot_array = []

	for element in age_col: 
		app = True
		for i in range ( len( bins )): 
			if element < bins[ i ]: 
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
# df = pd.read_csv( 'compiled_df.csv' )
# onehot_df = pd.DataFrame()
# hr_lst = convert_to_onehot( hr_onehot( df[ "HR" ].tolist() ) )
# bpsys_lst = convert_to_onehot( bp_syst( df[ "BP_SYS" ].tolist() ) )
# print( "HR Encoding: ", hr_lst[ 0 ] )
# print( "BP Encoding: ", bpsys_lst[ 0 ] )
	




	 
	
