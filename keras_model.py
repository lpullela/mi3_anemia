import numpy as np
from numpy import loadtxt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc 
from sklearn.metrics import roc_auc_score

with open( 'X.npy', 'rb' ) as f: 
    X = np.load( f )

with open( 'y.npy', 'rb' ) as f: 
    y = np.load( f )

print( y )

X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.1, random_state=110)

model = Sequential()
model.add(Dense(X.shape[ 1 ], input_shape=(X.shape[ 1 ],), activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy' ])

model.fit(x=X_train, y=y_train, batch_size=32, epochs=20,
shuffle=True, verbose=1, validation_split=0.1)

model.summary()

score = model.evaluate( X_test, y_test, verbose=0 )
print( 'TEST LOSS:', round( score[0], 2 ))
print( 'TEST ACCURACY:', round( score[1], 4 ) * 100, end=''  )
print( '%' )

y_targets = [] 
y_pred =  model.predict( X_test )

for i in y_pred: 
    for j in i: 
        if j < 0.5: 
            y_targets.append( [ 0 ] )
        else: 
            y_targets.append( [ 1 ] )

cm = confusion_matrix(y_test, np.array( y_targets ))

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(1)

ax = sns.heatmap(cm, annot=True, cmap='Blues')

ax.set_title('Seaborn Confusion Matrix with labels\n\n');
ax.set_xlabel('\nPredicted Values')
ax.set_ylabel('Actual Values ');

## Ticket labels - List must be in alphabetical order
ax.xaxis.set_ticklabels(['False','True'])
ax.yaxis.set_ticklabels(['False','True'])

## Display the visualization of the Confusion Matrix.
plt.show()


fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range( X.shape[ 0 ] ):
    fpr[i], tpr[i], _ = roc_curve(y_test, y_targets )
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and ROC area
fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_pred.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

plt.figure(2)
lw = 2
plt.plot(
    fpr[2],
    tpr[2],
    color="darkorange",
    lw=lw,
    label="ROC curve (area = %0.2f)" % roc_auc[2],
)
plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver operating characteristic")
plt.legend(loc="lower right")
plt.show()