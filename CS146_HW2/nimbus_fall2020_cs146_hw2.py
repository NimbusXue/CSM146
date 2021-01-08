# -*- coding: utf-8 -*-
"""Nimbus-Fall2020-CS146-HW2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14l-iMpEEsAJKnLmQ3HKHbSb4d5rWXOuV
"""

# This code was adapted from course material by Jenna Wiens (UMichigan).

# python libraries
import os

# numpy libraries
import numpy as np

# matplotlib libraries
import matplotlib.pyplot as plt

# To add your own Drive Run this cell.
from google.colab import drive
drive.mount('/content/drive')

######################################################################
# classes
######################################################################


class Data:
    def __init__(self, X=None, y=None):
        """
        Data class.
        
        Attributes
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
        """

        # n = number of examples, d = dimensionality
        self.X = X
        self.y = y

    def load(self, filename):
        """
        Load csv file into X array of features and y array of labels.
        
        Parameters
        --------------------
            filename -- string, filename
        """


        # load data
        with open(filename, "r") as fid:
            data = np.loadtxt(fid, delimiter=",")

        # separate features and labels
        self.X = data[:, :-1]
        self.y = data[:, -1]

    def plot(self, **kwargs):
        """Plot data."""

        if "color" not in kwargs:
            kwargs["color"] = "b"

        plt.scatter(self.X, self.y, **kwargs)
        plt.xlabel("x", fontsize=16)
        plt.ylabel("y", fontsize=16)
        plt.show()

# wrapper functions around Data class
def load_data(filename):
    data = Data()
    data.load(filename)
    return data


def plot_data(X, y, **kwargs):
    data = Data(X, y)
    data.plot(**kwargs)

class PolynomialRegression:
    def __init__(self, m=1, reg_param=0):
        """
        Ordinary least squares regression.
        
        Attributes
        --------------------
            coef_   -- numpy array of shape (d,)
                       estimated coefficients for the linear regression problem
            m_      -- integer
                       order for polynomial regression
            lambda_ -- float
                       regularization parameter
        """

        # self.coef_ represents the weights of the regression model
        self.coef_ = None
        self.m_ = m
        self.lambda_ = reg_param

    def generate_polynomial_features(self, X):
        """
        Maps X to an mth degree feature vector e.g. [1, X, X^2, ..., X^m].
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,1), features
        
        Returns
        --------------------
            Phi     -- numpy array of shape (n,(m+1)), mapped features
        """

        n, d = X.shape

        ### ========== TODO : START ========== ###
        # part b: modify to create matrix for simple linear model
        first_col = np.ones(shape=(n,1))
        Phi = np.append(first_col, X, axis=1)
        # part g: modify to create matrix for polynomial model
        m = self.m_
        for i in range(2,m+1):
            a = np.array(X**i)
            Phi = np.append(Phi,a,axis=1)
        if m==0:
          Phi=first_col

        ### ========== TODO : END ========== ###

        return Phi

    def fit_GD(self, X, y, eta=None, eps=0, tmax=10000, verbose=False):
        """
        Finds the coefficients of a {d-1}^th degree polynomial
        that fits the data using least squares batch gradient descent.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
            eta     -- float, step size
            eps     -- float, convergence criterion
            tmax    -- integer, maximum number of iterations
            verbose -- boolean, for debugging purposes
        
        Returns
        --------------------
            self    -- an instance of self
        """
        if self.lambda_ != 0:
            raise Exception("GD with regularization not implemented")

        X = self.generate_polynomial_features(X)  # map features
        n, d = X.shape
        eta_input = eta
        self.coef_ = np.zeros(d)  # coefficients
        err_list = np.zeros((tmax, 1))  # errors per iteration

        # GD loop
        for t in range(tmax):
            ### ========== TODO : START ========== ###
            # part f: update step size
            # change the default eta in the function signature to 'eta=None'
            # and update the line below to your learning rate function
            if eta_input is None:
                eta = 1/float(2+t)  # change this line
            else:
                eta = eta_input
            ### ========== TODO : END ========== ###

            ### ========== TODO : START ========== ###
            # part d: update w (self.coef_) using one step of GD
            # hint: you can write simultaneously update all w using vector math


            # track error
            # hint: you cannot use self.predict(...) to make the predictions
            y_pred = X.dot(self.coef_)  # change this line
            gradient = 2 * np.sum((y_pred - y).reshape(n,1)*X, axis=0)
            self.coef_ -= (eta * gradient)
            err_list[t] = np.sum(np.power(y - y_pred, 2)) / float(n)
            ### ========== TODO : END ========== ###

            # stop?
            if t > 0 and abs(err_list[t] - err_list[t - 1]) <= eps:
                break

            # debugging
            # debugging
            if verbose :
                x = np.reshape(X[:,1], (n,1))
                cost = self.cost(x,y)
                print ("iteration: %d, cost: %f" % (t+1, cost))

        print("number of iterations: %d" % (t + 1))

        return self

    def fit(self, X, y, l2regularize=None):
        """
        Finds the coefficients of a {d-1}^th degree polynomial
        that fits the data using the closed form solution.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
            l2regularize    -- set to None for no regularization. set to positive double for L2 regularization
                
        Returns
        --------------------        
            self    -- an instance of self
        """

        X = self.generate_polynomial_features(X)  # map features

        ### ========== TODO : START ========== ###
        # part e: implement closed-form solution
        # hint: use np.dot(...) and np.linalg.pinv(...)
        #       be sure to update self.coef_ with your solution
        self.coef_ = np.linalg.pinv(X.T.dot(X)).dot(X.T).dot(y)
        
        return self


        ### ========== TODO : END ========== ###

    def predict(self, X):
        """
        Predict output for X.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
        
        Returns
        --------------------
            y       -- numpy array of shape (n,), predictions
        """
        if self.coef_ is None:
            raise Exception("Model not initialized. Perform a fit first.")

        X = self.generate_polynomial_features(X)  # map features

        ### ========== TODO : START ========== ###
        # part c: predict y
        y = X.dot(self.coef_)
        ### ========== TODO : END ========== ###

        return y

    def cost(self, X, y):
        """
        Calculates the objective function.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
        
        Returns
        --------------------
            cost    -- float, objective J(w)
        """
        ### ========== TODO : START ========== ###
        # part d: compute J(w)
        cost = np.sum((self.predict(X) - y) ** 2)
        ### ========== TODO : END ========== ###
        return cost

    def rms_error(self, X, y):
        """
        Calculates the root mean square error.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
        
        Returns
        --------------------
            error   -- float, RMSE
        """
        ### ========== TODO : START ========== ###
        # part h: compute RMSE
        error = np.sqrt(self.cost(X,y)/X.shape[0])
        ### ========== TODO : END ========== ###
        return error

    def plot_regression(self, xmin=0, xmax=1, n=50, **kwargs):
        """Plot regression line."""
        if "color" not in kwargs:
            kwargs["color"] = "r"
        if "linestyle" not in kwargs:
            kwargs["linestyle"] = "-"

        X = np.reshape(np.linspace(0, 1, n), (n, 1))
        y = self.predict(X)
        plot_data(X, y, **kwargs)
        plt.show()

######################################################################
# main
######################################################################

def main():
    # load data with correct file path

    ### ========== TODO : START ========== ###
    data_directory_path =  "/content/drive/My Drive/Fall2020-CS146-HW2"
    ### ========== TODO : END ========== ###

    train_data = load_data(os.path.join(data_directory_path, "train.csv"))
    test_data = load_data(os.path.join(data_directory_path,"test.csv"))

    ### ========== TODO : START ========== ###
    # part a: main code for visualizations
    print("Visualizing data...")
    X_train, y_train = train_data.X, train_data.y
    X_test, y_test = test_data.X, test_data.y
    plot_data(X_train, y_train)
    plot_data(X_test, y_test)

    ### ========== TODO : END ========== ###

    ### ========== TODO : START ========== ###
    # parts b-f: main code for linear regression
    print("Investigating linear regression...")
    print('part d')
    model = PolynomialRegression(1)
    model.coef_ = np.zeros(2)
    c = model.cost (train_data.X, train_data.y) 
    print(f'model_cost:{c}')

    learning_rates = [0.000001, 0.00001, 0.001, 0.0168]
    coef = []
    J_value = []
    times = []
    import time
    for r in learning_rates:
        time_begin = time.time()
        model = PolynomialRegression()
        model.coef_ = np.zeros(2)
        model = model.fit_GD(X_train, y_train, eta=r)
        times.append(time.time()-time_begin)
        coef.append(model.coef_)
        J_value.append(model.cost(X_train, y_train))
    print("coefficients")
    print (coef)
    print("final values")
    print (J_value)
    print("times")
    print (times)
    
    print('part e')
    time_begin = time.time()
    model = PolynomialRegression()
    model.coef_ = np.zeros(2)
    model.fit(X_train, y_train)
    time_required=time.time()-time_begin
    print('time required for closed form solution')
    print(time_required)
    print ('Closed form solution coefficients:')
    print (model.coef_)

    print('part f')
    model = PolynomialRegression()
    model.coef_ = np.zeros(2)
    model = model.fit_GD(X_train, y_train)
    print ('coefficients for part f changing learning rate:')
    print (model.coef_)
    ### ========== TODO : END ========== ###

    ### ========== TODO : START ========== ###
    # parts g-i: main code for polynomial regression
    print("Investigating polynomial regression...")
    RMSE_train = []
    RMSE_test = []
    c = []
    for m in range(11):
        model = PolynomialRegression(m)
        model.coef_ = np.zeros(m)
        model.fit(X_train, y_train)
        RMSE_train.append(model.rms_error(X_train, y_train))
        RMSE_test.append(model.rms_error(X_test, y_test))
        c.append(model.coef_)
    
    plt.figure()
    plt.plot(list(range(11)), RMSE_train,label='RMSE on training data')
    plt.plot(list(range(11)), RMSE_test,label='RMSE on test data')
    plt.legend()
    plt.xlabel('m')
    plt.ylabel('RMSE')
    plt.show()
    print(c)
    
    ### ========== TODO : END ========== ###

    print("Done!")

if __name__ == "__main__":
    main()