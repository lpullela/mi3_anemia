import numpy as np
from one_hot import create_tensor
import pandas as pd

df = pd.read_csv( 'compiled_df.csv')

def createXY(): 
    # dim = ( len( df ), len( create_tensor( df, 0 )[ 1 ]  ) )
    dim = ( 0, len( create_tensor( df, 0 )[ 1 ]  ) )
    X = np.empty( dim, int )
    y = []
    for i in range( len( df ) ): 
        if i % 200 == 0: 
            print( "Percent Done: ", i / len( df ) * 100, end='' )
            print( "%" )
        anemic, tensor = create_tensor( df, i )
        X = np.append( X, np.array( [ tensor ] ), axis=0 ) 
        y.append( anemic )

    y = np.array( y )
    return X, y

# def createY(): 
#     dim = ( len( df ), len( create_tensor( df, 0 )[ 1 ]  ) )
#     y = np.empty( ( dim[ 0 ], 1 ), int )
#     for i in range(  len( df )): 
#         anemic, tensor = create_tensor( df, i )
#         y = np.append( y, [ anemic ] )
#     return y

X, y = createXY()

with open( 'x.npy', 'wb' ) as f: 
    np.save( f, X )
    f.close()

with open( 'y.npy', 'wb' ) as f: 
    np.save( f, y )
    f.close()

print( "Done Saving!")
