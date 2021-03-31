from pyalgo.pytrainer.ML_functions import *

class trainer(ML_functions_Training):

    def __init__(self, add_bias=False, description=None):

        self.add_bias = add_bias
        self.description = description

    def print_model_settings(self):
        print(f'add_bias --> {self.add_bias}')
        print(f"description --> '{self.description}'")