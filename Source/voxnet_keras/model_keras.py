#!/usr/bin/python3

import keras
assert keras.__version__ == "1.0.0", "keras version not supported"

from keras import backend as K

from keras.models import Sequential

from keras.layers import Convolution3D, MaxPooling3D
from keras.layers.core import Activation, Dense, Dropout, Flatten
from keras.layers.advanced_activations import LeakyReLU

from keras.optimizers import SGD

import logging
import pdb


class model_vt (object):

    def __init__(self):
        """initiate Model according to voxnet paper"""
        # Stochastic Gradient Decent (SGD) with momentum
        # lr=0.01 for LiDar dataset
        # lr=0.001 for other datasets
        # decay of 0.00016667 approx the same as learning schedule (0:0.001,60000:0.0001,600000:0.00001)
        self._optimizer = SGD(lr=0.001, momentum=0.9, decay=0.00016667, nesterov=False)

        # init model
        self._mdl= Sequential()
        
        # convolution 1
        self._mdl.add(Convolution3D(input_shape=(1, 32, 32, 32),
                                    nb_filter=32,
                                    kernel_dim1=5,
                                    kernel_dim2=5,
                                    kernel_dim3=5,
                                    init='normal', #TODO
                                    weights=None, #TODO
                                    border_mode='valid',
                                    subsample=(2, 2, 2),
                                    dim_ordering='th',
                                    W_regularizer=None,
                                    b_regularizer=None,
                                    activity_regularizer=None,
                                    W_constraint=None,
                                    b_constraint=None))
        
        logging.debug("Layer1:Conv3D shape={0}".format(self._mdl.output_shape))
        self._mdl.add(Activation(LeakyReLU(alpha=0.1)))
        
        # dropout 1
        self._mdl.add(Dropout(p=0.2))

        # convolution 2
        self._mdl.add(Convolution3D(nb_filter=32,
                                    kernel_dim1=3,
                                    kernel_dim2=3,
                                    kernel_dim3=3,
                                    init='normal', #TODO
                                    weights=None, #TODO
                                    border_mode='valid',
                                    subsample=(1, 1, 1),
                                    dim_ordering='th',
                                    W_regularizer=None,
                                    b_regularizer=None,
                                    activity_regularizer=None,
                                    W_constraint=None,
                                    b_constraint=None))
        
        logging.debug("Layer3:Conv3D shape={0}".format(self._mdl.output_shape))
        self._mdl.add(Activation(LeakyReLU(alpha=0.1)))
        
        # max pool 1
        self._mdl.add(MaxPooling3D(pool_size=(2, 2, 2),
                                  strides=None,
                                  border_mode='valid',
                                  dim_ordering='th'))
        
        logging.debug("Layer4:MaxPool3D shape={0}".format(self._mdl.output_shape))

        # dropout 2
        self._mdl.add(Dropout(p=0.3))

        # dense 1 (fully connected layer)
        self._mdl.add(Flatten())
        logging.debug("Layer5:Flatten shape={0}".format(self._mdl.output_shape))
        
        self._mdl.add(Dense(output_dim=128, # TODO not sure ...
                               init='normal',  #TODO np.random.normal, K.random_normal
                               activation='linear',
                               weights=None,
                               W_regularizer=None,
                               b_regularizer=None,
                               activity_regularizer=None,
                               W_constraint=None,
                               b_constraint=None))
        
        logging.debug("Layer6:Dense shape={0}".format(self._mdl.output_shape))

        # dropout 3
        self._mdl.add(Dropout(p=0.4))

        # dense 2
        self._mdl.add(Dense( output_dim=1, # TODO not sure ...
                               init='normal', #TODO np.random.normal, K.random_normal
                               activation='linear',
                               weights=None,
                               W_regularizer=None,
                               b_regularizer=None,
                               activity_regularizer=None,
                               W_constraint=None,
                               b_constraint=None))
        
        logging.debug("Layer8:Dense shape={0}".format(self._mdl.output_shape))

        # compile model
        self._mdl.compile(loss=self._objective, optimizer=self._optimizer)


    def _objective(self, y_true, y_pred):
        #TODO replace!
        return K.mean(K.square(y_pred - y_true), axis=-1)


    def fit(self, X_train, y_train, cv=10):
        #TODO add cross-validation
        self.mdl.fit()


    def add_data(self):
        #TODO load old weigths
        #TODO improve fit with old weigths
        self.mdl.fit()


    def evaluate(self, X_test, y_test):
        #TODO make sure to use score from modelnet40/10 paper
        self.mdl.evaluate(X_test, y_test)


    def predict(self,X_predict):
        #TODO add prediction from PointCloud
        self.mdl.predict(X_predict)



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    model_vt()





