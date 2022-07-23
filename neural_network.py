import tensorflow as tf
from tensorflow.keras import models, layers, activations, backend as K 
import numpy as np
import shap
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from termcolor import colored as cl


with open( 'X.npy', 'rb' ) as f: 
    X = np.load( f )

with open( 'y.npy', 'rb' ) as f: 
    y = np.load( f )
    
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.1, random_state=150)

#model
hidden_layer_i = 0
def n_features_hidden_layer_inverse_square( n_features ): 
	global hidden_layer_i
    #int( round( ( n_features + 1 ) / ( 2 ** ( hidden_layer_i + 1 ) ) ) ) 
	result = int( n_features - 10 * ( ( hidden_layer_i + 1 ) ** 1.25 ) )
	hidden_layer_i = hidden_layer_i + 1
	return result

#compute formula, round, then type convert to an int

n_features = X.shape[ 1 ]
#transformation function for hidden layer activation
hidden_func = activations.relu

# define metrics
def Recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def Precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def F1(y_true, y_pred):
    precision = Precision(y_true, y_pred)
    recall = Recall(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def explainer_shap(model, X_names, X_instance, X_train=None, task="classification", top=10):
    ## create explainer
    ### machine learning
    if X_train is None:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_instance)
    ### deep learning
    else:
        explainer = shap.DeepExplainer(model, data=X_train[:100])
        shap_values = explainer.shap_values(X_instance.reshape(1,-1))[0].reshape(-1)

    ## plot
    ### classification
    if task == "classification":
        shap.decision_plot(explainer.expected_value, shap_values, link='logit', feature_order='importance',
                           features=X_instance, feature_names=X_names, feature_display_range=slice(-1,-top-1,-1))
    ### regression
    else:
        shap.waterfall_plot(explainer.expected_value[0], shap_values, 
                            features=X_instance, feature_names=X_names, max_display=top)

# DeepNN
### layer input
inputs = layers.Input(name="input", shape=(n_features,))
### hidden layer 1
h1 = layers.Dense(name="h1", units=n_features_hidden_layer_inverse_square( n_features ), activation='relu')(inputs)
h1 = layers.Dropout(name="drop1", rate=0.2)(h1)
### hidden layer 2
h2 = layers.Dense(name="h2", units=n_features_hidden_layer_inverse_square( n_features ), activation='relu')(h1)
h2 = layers.Dropout(name="drop2", rate=0.2)(h2)
### layer output
h3 = layers.Dense(name="h3", units=n_features_hidden_layer_inverse_square( n_features ), activation='relu')(h2)
h3 = layers.Dropout(name="drop3", rate=0.2)(h3)

h4 = layers.Dense(name="h4", units=n_features_hidden_layer_inverse_square( n_features ), activation='relu')(h3)
h4 = layers.Dropout(name="drop4", rate=0.2)(h4)

h5 = layers.Dense(name="h5", units=n_features_hidden_layer_inverse_square( n_features ), activation='relu')(h4)
h5 = layers.Dropout(name="drop5", rate=0.2)(h5)

h6 = layers.Dense(name="h6", units=n_features_hidden_layer_inverse_square( n_features ), activation='relu')(h5)
h6 = layers.Dropout(name="drop6", rate=0.2)(h6)


outputs = layers.Dense(name="output", units=1, activation='sigmoid')(h2)
model = models.Model(inputs=inputs, outputs=outputs, name="DeepNN")

model.compile(optimizer='adam', loss='binary_crossentropy', 
              metrics=['accuracy',F1])


training = model.fit(x=X_train, y=y_train, batch_size=32, epochs=20,
shuffle=True, verbose=1, validation_split=0.1)

model.summary()

score = model.evaluate( X_test, y_test, verbose=0 )
print( 'TEST LOSS:', score[0] )
print( 'TEST ACCURACY:', score[1] )




# list_feature_names = [ 'O2', 'HR', ]
#dummy variables
#change with 
#heart rate, blood pressure, demographic data, etc.
#which are relavant, which are not?

#exchange based on P-variables

# i = 1
# explainer_shap(model, 
#                X_names=list_feature_names, 
#                X_instance=X[i], 
#                X_train=X, 
#                task="classification", #task="regression"
#                top=10)



