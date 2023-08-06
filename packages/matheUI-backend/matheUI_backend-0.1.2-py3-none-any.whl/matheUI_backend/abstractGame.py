import os
import pickle
from abc import ABCMeta, abstractmethod

import pandas as pd


class AbstactGame(metaclass = ABCMeta):

    @abstractmethod
    def data_report(self):
        """ method to provide report about used data """
        print("no data used")

    @abstractmethod
    def update_data_files(self):
        """ method to update data files with class object changes """
        print("no data used")

    @abstractmethod
    def generate_round(self, **kwargs):
        """ method to generate round for game """
        print("generate_round is not implemented yet")

    def _pickle_dict(self, dictionary: dict, file_path: str = "test.pkl"):
        """ save dictionary as pickle file """
        with open(os.path.dirname(__file__)+file_path, 'wb') as f:
            pickle.dump(dictionary, f)

    def _load_pickled_dict(self, file_path: str) -> dict:
        """ load pickled dictionary """
        with open(os.path.dirname(__file__)+file_path, 'rb') as f:
            dictionary = pickle.load(f)
        return dictionary

    def _save_dataframe(self, df: pd.DataFrame, file_path: str = "test.csv"):
        """ save pandas dataframe as csv file """
        df.to_csv(os.path.dirname(__file__)+file_path)

    def _load_csv_dataframe(self, file_path: str) -> pd.DataFrame:
        """ load pandas dataframe from csv file """
        df = pd.read_csv(os.path.dirname(__file__)+file_path, index_col=0)
        return df

    def save_game(self, file_name: str):
        """ create game object checkpoint as pickle file """
        with open(os.path.dirname(__file__)+"/../data/Checkpoints/"+file_name+".pkl", 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_game(file_name: str):
        """ load game checkpoint from pickle file """
        with open(os.path.dirname(__file__)+"/../data/Checkpoints/"+file_name+".pkl", 'rb') as f:
            game = pickle.load(f)
        return game
