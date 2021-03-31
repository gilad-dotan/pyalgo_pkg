import copy
import random
import numpy as np
import ML_functions
from pyalgo.basic_modules import default_functions, default_values
from pyalgo.basic_modules.pytrainer_default_values import ML_functions_trainer_default_values, ML_functions_default_values
from pyalgo import basic_modules


class Basic_ML_functions:

    """
    This class provides a set of basic functions to build your machine-learning model
    """

    def __init__(self): pass

    @staticmethod
    def Sigmoid(X):
        return 1/(1 + np.exp(-X))

    @staticmethod
    def LinearFunction(X):
        return X

    @classmethod
    def Tanh(cls, X, Scaler=2):
        floatType = default_values.FloatType
        intType = default_values.IntType
        if not ((isinstance(Scaler, floatType)) or (isinstance(Scaler, intType))):
            raise TypeError("'Scaler' needs to be a float")

        return 2 * cls.Sigmoid(Scaler * X) - 1

    @staticmethod
    def Relu(X):
        try:
            return max(0, X)
        except:
            m, n = X.shape
            return np.max(np.append(np.zeros((m, 1)), X, axis=1), axis=1).reshape((-1, 1))



class ML_functions_Training(Basic_ML_functions):

    def __init__(self): pass

    @staticmethod
    def Get_Randomized_Theta(epsilon, dim):
        FloatType = default_values.FloatType
        IntType = default_values.IntType


        if not (isinstance(epsilon, IntType) or isinstance(epsilon, FloatType)):
            raise TypeError("'epsilon' needs to be a int type or float type")

        randomized_theta = []

        Theta1d_size = 1

        for i in dim:
            Theta1d_size *= i

        for i in range(Theta1d_size):
            randomized_theta.append((random.random() * (2*epsilon)) - epsilon)


        randomized_theta = np.array(randomized_theta).reshape((dim))

        return randomized_theta

    @staticmethod
    def Normal_Equation(X, Y, AddBias=True):

        if AddBias:
            m, n = X.shape
            X = np.append(np.ones((m, 1)), X, axis=1)

        ArrayType = default_values.ArrayType

        if not isinstance(X, ArrayType):
            raise TypeError("X needs to be an array type")

        out = np.transpose(X).dot(X)
        out = np.linalg.inv(out)

        out = out.dot(np.transpose(X))

        out = out.dot(Y)

        return np.transpose(out)

    @staticmethod
    def forward_propagation(X, Theta, AddBias=True):

        self = ML_functions_Training

        X = copy.deepcopy(X)
        Theta = copy.deepcopy(Theta)

        num_of_matrices = 1  # // will be used for neural networks \\
        m, n = X.shape

        if AddBias:
            X = np.append(np.ones((m, 1)), X, axis=1)

        if len(Theta.shape) >= 3:
            print("needs to be completed")
            raise NotImplementedError("Yet...")  # // Needs to be built \\

        elif ((len(Theta.shape) == 1) or (len(Theta.shape) == 2)):
            print(Theta.shape)
            print("Simple Regression")
            print(f"num_of_matrices: {num_of_matrices}")
            return X.dot(Theta).reshape((-1, 1))

    @staticmethod
    def cost_function(X, Y, Theta, NonLinearityFunction=ML_functions.Basic_ML_functions.LinearFunction(), Method='MSE', AddBias=True, Lambda=None):

        ArrayType = default_values.ArrayType   # variables that helps check if the inputs are in the right type
        BoolType = default_values.BoolType     # variables that helps check if the inputs are in the right type

        # // check that the inputs are valid \\
        if not isinstance(X, ArrayType):
            raise TypeError("X needs to be an array type")

        if Method not in basic_modules.pytrainer_default_values.ML_functions_default_values.cost_function_Methods:
            raise ValueError(f"'Method' needs to be from the list of options: {ML_functions_default_values.cost_function_Methods}")

        if not isinstance(AddBias, BoolType):
            raise ValueError("The parameter 'AddBias' needs to be a boolean type")
        J = 0
        self = ML_functions_Training



        # // get the default value to lambda if the user didn't specified ant value to lambda \\
        if Lambda == None:
            Lambda = ML_functions_trainer_default_values.Lambda_default_value
        elif Lambda < 0:
            raise ValueError("Lambda can't be negative")


        m, n = X.shape

        J = NonLinearityFunction(self.forward_propagation(X, Theta, AddBias=AddBias) - Y)
        if Method == 'MAE':  J = abs(J)
        if Method == 'MSE':  J *= J

        J = np.sum(J) / m
        if Method == 'MSE':  J /= 2

        if Method == 'MAE':  J += (Lambda / m) * np.sum(Theta * Theta)
        if Method == 'MSE':  J += (Lambda / (m*2)) * np.sum(Theta * Theta)

        return J