import math
import numpy as np
import pandas as pd
import investpy
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import learning_curve, GridSearchCV
import datetime
import os
from data_creator import data_model
import pickle


def predictor(data, pred, ticker):

    name = input("Select 'new' for a new stock or pass and predict a default stock: ")

    # If the input says 'new', it will run a new trained model.
    if name == 'new':
        # Split target and predictors.
        X = data.drop(['Price', 'Date', 'Stock'], axis=1)
        y = data['Price']


        # split data in train/test.
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.20,
                                                            random_state=33)

        # Training the model:
        model = GradientBoostingRegressor(n_estimators=3000)

        params = {'learning_rate': [0.1, 0.05, 0.02, 0.01],
                  'max_depth': [4, 6],
                  'min_samples_leaf': [3, 5, 9, 17],
                  'max_features': [1, 0.3, 0.1]}

        grid_search = GridSearchCV(model,
                                   param_grid=params,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=1)

        grid_search.fit(X_train, y_train)

        best = grid_search.best_estimator_

    else:
        # Here we use a model pickeled for the default stocks that are already stored:
        with open(f'{ticker}_model.pkl', 'rb') as f:
            model = pickle.load(f)

        best = model.best_estimator_

    # Create the output dataframe with the price prediction:
    pred['Price'] = best.predict(pred)
    print('The prediction for tomorrow is: ')
    print(pred)

    return pred
