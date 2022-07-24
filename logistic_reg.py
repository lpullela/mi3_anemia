import pandas as pd 
import numpy as np 
import itertools 
import matplotlib.pyplot as plt 
from matplotlib import rcParams
from termcolor import colored as cl
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression 
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import jaccard_score as jss # evaluation metric
from sklearn.metrics import precision_score 
from sklearn.metrics import classification_report 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import log_loss
from sklearn.metrics import roc_curve, auc 
from sklearn.metrics import roc_auc_score

rcParams[ 'figure.figsize' ] = ( 20, 10 )

with open( 'X.npy', 'rb' ) as f: 
    X = np.load( f )

with open( 'y.npy', 'rb' ) as f: 
    y = np.load( f )

print( "Shape of X: ", X.shape )
print( "Shape of y: ", y.shape )

X = StandardScaler().fit( X ).transform(X )
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.3, random_state=100)

lr = LogisticRegression( C = 0.1, solver='liblinear')
lr.fit( X_train, y_train )

result = lr.score( X_test, y_test )

yhat = lr.predict( X_test )
yhat_prob = lr.predict_proba( X_test )

print(cl('Jaccard Similarity Score of our model is {}'.format(jss(y_test, yhat).round(2)), attrs = ['bold']))

print(cl('Precision Score of our model is {}'.format(precision_score(y_test, yhat).round(2)), attrs = ['bold']))

print(cl('Log Loss of our model is {}'.format(log_loss(y_test, yhat).round(2)), attrs = ['bold']))

print(cl(classification_report(y_test, yhat), attrs = ['bold']))

def plot_confusion_matrix(cm, classes,normalize = False, title = 'Confusion matrix', cmap = plt.cm.Blues):
    if normalize:
        cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation = 'nearest', cmap = cmap)
    plt.title(title, fontsize = 22)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation = 45, fontsize = 13)
    plt.yticks(tick_marks, classes, fontsize = 13)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment = 'center',
                 fontsize = 15,
                 color = 'white' if cm[i, j] > thresh else 'black')

    plt.tight_layout()
    plt.ylabel('True label', fontsize = 16)
    plt.xlabel('Predicted label', fontsize = 16)

# Compute confusion matrix

cnf_matrix = confusion_matrix(y_test, yhat, labels = [1,0])
np.set_printoptions(precision = 2)


# Plot non-normalized confusion matrix

plt.figure(1)
plot_confusion_matrix(cnf_matrix, classes = ['churn=1','churn=0'], normalize = False,  title = 'Confusion matrix')
plt.savefig('confusion_matrix.png')



fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range( X.shape[ 0 ] ):
    fpr[i], tpr[i], _ = roc_curve(y_test, yhat_prob[:,1] )
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and ROC area
fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), yhat_prob[ :,1 ].ravel())
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