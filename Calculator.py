from abc import ABC, abstractmethod
from turtledemo.paint import switchupdown


class RecordRules(ABC):
    def __init__(self, language_dict):
        if not isinstance(language_dict, str):
            raise TypeError('language_dict must be a dict')
        elif language_dict is None:
            raise ValueError('language_dict cannot be None')
        self.language_dict = language_dict
class BasicRules(RecordRules):
    def __init__(self, language_dict):
        super().__init__(language_dict)

class Validation(ABC):
    def __init__(self, input_usr):
        if not isinstance(input_usr, str) or input_usr is None:
            raise TypeError('input_usr is Wrong')
        self.input_usr = input_usr
        self.clean_spaces()
    def clean_spaces(self,iteration=0):
        if iteration == len(self.input_usr):
            return self.input_usr
        if self.input_usr[iteration] == '':
            self.input_usr=self.input_usr[:iteration]+self.input_usr[iteration+1:]
        return self.clean_spaces(iteration+1)

class Node:
    def __init__(self, data=None,left=None,right=None ):
        self.data = data
        self.left = left
        self.right = right