import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from datetime import datetime
import pymongo
from pymongo import MongoClient
import urllib.parse
import collections
from itertools import combinations_with_replacement
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cmx
import matplotlib.colors as colors
import numpy as np
import math
import datetime
from datetime import date
def forecast(username,new):
    usernamemongo = urllib.parse.quote_plus('arsha')
    passwordmongo = urllib.parse.quote_plus('inventory')
    url='mongodb+srv://{}:{}@cluster0.bws9v.mongodb.net/?retryWrites=true&w=majority'.format(usernamemongo,passwordmongo)
    cluster = MongoClient(url)
    db=cluster[username]
    test=db.DailyDemand
    df = pd.DataFrame(list(test.find({"Product_id":new})))
    del df['_id']
    del df['Product_id']
    df=pd.melt(df, var_name='Date', value_name='Demand')
    df['index']=df.index
    newdf=df.copy()
    df['Demand'] = df['Demand'] / df['Demand'].abs().max()
    



    class Regression(object):
   
        def __init__(self, n_iterations, learning_rate):
            self.n_iterations = n_iterations
            self.learning_rate = learning_rate

        def initialize_weights(self, n_features):
            """ Initialize weights randomly [-1/N, 1/N] """
            limit = 1 / math.sqrt(n_features)
            self.w = np.random.uniform(-limit, limit, (n_features, ))

        def fit(self, X, y):
            # Insert constant ones for bias weights
            X = np.insert(X, 0, 1, axis=1)
            self.training_errors = []
            self.initialize_weights(n_features=X.shape[1])

            # Do gradient descent for n_iterations
            for i in range(self.n_iterations):
                y_pred = X.dot(self.w)
                # Calculate l2 loss
                mse = np.mean(0.5 * (y - y_pred)**2 + self.regularization(self.w))
                self.training_errors.append(mse)
                # Gradient of l2 loss w.r.t w
                grad_w = -(y - y_pred).dot(X) + self.regularization.grad(self.w)
                # Update the weights
                self.w -= self.learning_rate * grad_w

        def predict(self, X):
            # Insert constant ones for bias weights
            X = np.insert(X, 0, 1, axis=1)
            y_pred = X.dot(self.w)
            return y_pred

    

    class PolynomialRidgeRegression(Regression):
    
        def __init__(self, degree, reg_factor, n_iterations=3000, learning_rate=0.01, gradient_descent=True):
            self.degree = degree
            self.regularization = l2_regularization(alpha=reg_factor)
            super(PolynomialRidgeRegression, self).__init__(n_iterations, 
                                                        learning_rate)

        def fit(self, X, y):
        
            X = normalize(polynomial_features(X, degree=self.degree))
            super(PolynomialRidgeRegression, self).fit(X, y)

        def predict(self, X):
        
            X = normalize(polynomial_features(X, degree=self.degree))
            return super(PolynomialRidgeRegression, self).predict(X)
    

    def k_fold_cross_validation_sets(X, y, k, shuffle=True):
        """ Split the data into k sets of training / test data """
        if shuffle:
            X, y = shuffle_data(X, y)

        n_samples = len(y)
        left_overs = {}
        n_left_overs = (n_samples % k)
        if n_left_overs != 0:
            left_overs["X"] = X[-n_left_overs:]
            left_overs["y"] = y[-n_left_overs:]
            X = X[:-n_left_overs]
            y = y[:-n_left_overs]

        X_split = np.split(X, k)
        y_split = np.split(y, k)
        sets = []
        for i in range(k):
            X_test, y_test = X_split[i], y_split[i]
            X_train = np.concatenate(X_split[:i] + X_split[i + 1:], axis=0)
            y_train = np.concatenate(y_split[:i] + y_split[i + 1:], axis=0)
            sets.append([X_train, X_test, y_train, y_test])

        # Add left over samples to last set as training samples
        if n_left_overs != 0:
            np.append(sets[-1][0], left_overs["X"], axis=0)
            np.append(sets[-1][2], left_overs["y"], axis=0)

        return np.array(sets)

    def normalize(X, axis=-1, order=2):
            """ Normalize the dataset X """
            l2 = np.atleast_1d(np.linalg.norm(X, order, axis))
            l2[l2 == 0] = 1
            return X / np.expand_dims(l2, axis)


    def mean_squared_error(y_true, y_pred):
        """ Returns the mean squared error between y_true and y_pred """
        mse = np.mean(np.power(y_true - y_pred, 2))
        return mse

    def train_test_split(X, y, test_size=0.5, shuffle=True, seed=None):
        """ Split the data into train and test sets """
        #if shuffle:
        #    X, y = shuffle_data(X, y, seed)
        # Split the training data from test data in the ratio specified in
        # test_size
        split_i = len(y) - int(len(y) // (1 / test_size))
        X_train, X_test = X[:split_i], X[split_i:]
        y_train, y_test = y[:split_i], y[split_i:]
        print("training and test set of X is divided as: ", len(X_train),len(X_test))
        print("training and test set of Y is divided as: ", len(y_train),len(y_test))
        return X_train, X_test, y_train, y_test


    def polynomial_features(X, degree):
        n_samples, n_features = np.shape(X)
        def index_combinations():
            combs = [combinations_with_replacement(range(n_features), i) for i in range(0, degree + 1)]
            flat_combs = [item for sublist in combs for item in sublist]
            return flat_combs
    
        combinations = index_combinations()
        n_output_features = len(combinations)
    
        X_new = np.empty((n_samples, n_output_features))
    
        for i, index_combs in enumerate(combinations):  
        
            X_new[:, i] = np.prod(X[:, index_combs], axis=1)

        return X_new

    def calculate_covariance_matrix(X, Y=None):
        """ Calculate the covariance matrix for the dataset X """
        if Y is None:
            Y = X
        n_samples = np.shape(X)[0]
        covariance_matrix = (1 / (n_samples-1)) * (X - X.mean(axis=0)).T.dot(Y - Y.mean(axis=0))

        return np.array(covariance_matrix, dtype=float)
 

    def calculate_correlation_matrix(X, Y=None):
        """ Calculate the correlation matrix for the dataset X """
        if Y is None:
            Y = X
        n_samples = np.shape(X)[0]
        covariance = (1 / n_samples) * (X - X.mean(0)).T.dot(Y - Y.mean(0))
        std_dev_X = np.expand_dims(calculate_std_dev(X), 1)
        std_dev_y = np.expand_dims(calculate_std_dev(Y), 1)
        correlation_matrix = np.divide(covariance, std_dev_X.dot(std_dev_y.T))

        return np.array(correlation_matrix, dtype=float)
    def standardize(X):
        """ Standardize the dataset X """
        X_std = X
        mean = X.mean(axis=0)
        std = X.std(axis=0)
        for col in range(np.shape(X)[1]):
            if std[col]:
                X_std[:, col] = (X_std[:, col] - mean[col]) / std[col]
        # X_std = (X - X.mean(axis=0)) / X.std(axis=0)
        return X_std

    def shuffle_data(X, y, seed=None):
        """ Random shuffle of the samples in X and y """
        if seed:
            np.random.seed(seed)
        idx = np.arange(X.shape[0])
        np.random.shuffle(idx)
        return X[idx], y[idx]

    class l2_regularization():
        """ Regularization for Ridge Regression """
        def __init__(self, alpha):
            self.alpha = alpha
    
        def __call__(self, w):
            return self.alpha * 0.5 *  w.T.dot(w)

        def grad(self, w):
            return self.alpha * w
    



    X = np.atleast_2d(df['index'].values).T
    y = df['Demand'].values
    y=np.array(y,dtype=np.float64)
    val=newdf['Demand'].abs().max()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
    poly_degree = 4
    pred_list=[]
    # Finding regularization constant using cross validation
    lowest_error = float("inf")
    best_reg_factor = None
    print ("Finding regularization constant using cross validation:")
    k = 10
    for reg_factor in np.arange(0, 0.1, 0.01):
        cross_validation_sets = k_fold_cross_validation_sets(X_train, y_train, k=k)
        #print(cross_validation_sets)
        mse = 0
        for _X_train, _X_test, _y_train, _y_test in cross_validation_sets:
            model = PolynomialRidgeRegression(degree=poly_degree, reg_factor=reg_factor,learning_rate=0.001,n_iterations=10000)
            model.fit(_X_train, _y_train)
            y_pred = model.predict(_X_test)
            _mse = mean_squared_error(_y_test, y_pred)
            mse += _mse
        mse /= k

        # Print the mean squared error
        print ("\tMean Squared Error: %s (regularization: %s)" % (mse, reg_factor))

        # Save reg. constant that gave lowest error
        if mse < lowest_error:
            best_reg_factor = reg_factor
            lowest_error = mse

    # Make final prediction
    model = PolynomialRidgeRegression(degree=poly_degree, 
                                    reg_factor=best_reg_factor,
                                    learning_rate=0.001,
                                    n_iterations=10000)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    filist=y_pred*val
    #pred_list.append(y_pred*val)
    mse = mean_squared_error(y_test, y_pred)
    print ("Mean squared error: %s (given by reg. factor: %s)" % (lowest_error, best_reg_factor))

    y_pred_line = model.predict(X)
    today_date=date.today().strftime('%d/%m/%Y')
    #.strftime('%d/%m/%Y')
    filist=filist[0:30]
    db.FinalDemand.remove( {"Product_id":new}, True )
    final_list={}
    for i in range(len(filist)):
        today_date= pd.to_datetime(today_date)+pd.Timedelta(days=1)
        val=today_date.strftime('%d/%m/%Y')
        final_list[val]= filist[i]   
        db.FinalDemand.update({"Product_id":new},{"$set" : {val:filist[i]}},upsert=True) 
     
    #st.write(final_list)
    
