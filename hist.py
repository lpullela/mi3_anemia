import pandas as pd
import matplotlib.pyplot as plt

def make_hist( col, label, RANGE, BINS=20 ): 
    df = pd.read_csv( "compiled_df.csv" )
    graph = plt.hist( df[ col ], bins=BINS, range = RANGE, fill=False, color='blue' )
    graph = plt.xlabel( label )
    graph = plt.ylabel( "FREQ" )
    graph = plt.show()

    return graph

# make_hist( "BP_SYS", "BP_SYS", RANGE=[60,200])
# make_hist( "BP_DIAST", "BP_DIAST", RANGE=[30,140] ).show()
make_hist( "HR", "Heart Rate", RANGE=[30,200] ).show()