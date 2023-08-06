from typing import Union

import pandas as pd

from matheUI_backend.config import SCHARADE_DATA_FILES, SCHARADE_DATA_FOLDER

from .abstractGame import AbstactGame


class Scharade(AbstactGame):
    """ Scharade backend """

    def __init__(self, data_folder_path: str = SCHARADE_DATA_FOLDER, data_files: dict[str, str] = SCHARADE_DATA_FILES):
        """
        @params:
            data_folder_path: path to the folder with the scharade data (Form: '/....../')
            data_files: dictionary with name of the scharade sets and file name of the data (Form: {'standard': 'scharade.csv'})
        """
        self.data_folder_path = data_folder_path
        self.data_files = data_files

        self.scharade_sets: dict[str, pd.DataFrame] = {}
        for set_name in list(data_files.keys()):
            self.scharade_sets[set_name] = self._load_csv_dataframe(data_folder_path+data_files[set_name])

    def data_report(self):
        print(f"data contains {self.get_sets()} scharade sets")
        for set_name in self.get_sets():
            print(f"    {set_name}:")
            print(f"        total words: {len(self.scharade_sets[set_name])}")
            print(f"        words per difficulty:")
            for difficulty in sorted(self.scharade_sets[set_name]["DIFFICULTY"].unique()):
                num_difficulty = len(self.scharade_sets[set_name][self.scharade_sets[set_name]["DIFFICULTY"] == difficulty])
                print(f"            diff {difficulty}: {num_difficulty}")

    def get_sets(self) -> list[str]:
        return list(self.scharade_sets.keys())

    def get_df(self, set_name: str) -> pd.DataFrame:
        return self.scharade_sets[set_name]

    def get_difficulties_sets(self, sets: Union[str, list[str]] = "all") -> list[int]:
        """
        @return:
            list of difficulties that appear in the sets combination after droping duplicated words (keep first)
        """
        if sets == "all":
            sets = self.get_sets()
        elif type(sets) == str:
            sets = [sets]

        final_set: pd.DataFrame = pd.DataFrame(columns=["WORD", "DIFFICULTY"])
        for set_name in sets:
            final_set = final_set.append(self.scharade_sets[set_name], ignore_index=True)

        final_set.drop_duplicates(inplace=True)
        return sorted(list(final_set["DIFFICULTY"].unique()))
        

    def get_difficulty_of_word(self, set_name: str, word: str) -> int:
        df = self.scharade_sets[set_name]
        if word in list(df["WORD"]):
            return df[(df == word).any(axis=1)]["DIFFICULTY"].iloc[0]
        else:
            print(f"WARNING: word does not exist in word set '{set_name}'")

    def get_words_of_difficulty(self, set_name: str, difficulty: int) -> list[str]:
        df = self.scharade_sets[set_name]
        return list(df[df["DIFFICULTY"] == difficulty]["WORD"])

    def get_words_with_initial_letter(self, set_name: str, initial_letter: str) -> list[str]:
        df = self.scharade_sets[set_name]
        return list(df[df["WORD"].str.startswith(initial_letter.upper())]["WORD"])

    def get_frequency_of_initial_letter(self, set_name: str) -> dict[str, int]:
        """
        @param:
            set_name: name of word set
        @return:
            get dcitionary with alphabet as keys and number of words starting with this letter as values
        """
        letter_num_dict: dict[str, int] = {}
        for letter in list(map(chr,range(ord('A'),ord('Z')+1))):
            letter_num_dict[letter] = len(self.get_words_with_initial_letter(set_name, letter))
        return letter_num_dict
    
    def add_word(self, set_name: str, word: str, difficulty: int):
        if not word in list(self.scharade_sets[set_name]["WORD"]):
            self.scharade_sets[set_name] = self.scharade_sets[set_name].append({"WORD": word, "DIFFICULTY": difficulty}, ignore_index=True)
        else:
            print("INFO: word already exists --> overwrite difficulty")
            idx = list(self.scharade_sets[set_name]["WORD"]).index(word)
            self.scharade_sets[set_name].at[idx, "DIFFICULTY"] = difficulty

    def delete_word(self, set_name: str, word: str):
        idx = list(self.scharade_sets[set_name]["WORD"]).index(word)
        self.scharade_sets[set_name].drop(index=idx, inplace=True)
        self.scharade_sets[set_name].reset_index(inplace=True, drop=True)

    def update_data_files(self):
        """ function to update the data files with self.scharade_sets content """
        print("Do you want to save the following data? (yes/no)")
        self.data_report()
        print("answer:")
        answer = input()
        if answer == "yes":
            for set_name in self.get_sets():
                self._save_dataframe(self.scharade_sets[set_name], self.data_folder_path+self.data_files[set_name])
            print("data files updated")
        else:
            print("process stopped")

    def generate_round(self, sets: Union[str, list[str]] = "all", min_difficulty: Union[str, int] = "min", max_difficulty: Union[str, int] = "max"):
        """
        @params:
            sets: from which sets shall the words be. List of set_names or name of set (if 'all', use all available sets)
            min_difficulty: minimum difficulty for words ('min' for minimal difficulty)
            max_difficulty: maximum difficulty for words ('max' for maximal difficulty)

        @return:
            pandas Dataframe with shuffled words and columns "WORD", "DIFFICULTY

        NOTE: if words are redondant in the sets the difficulty of the anterior set in 'sets' will be used
        """
        if sets == "all":
            sets = self.get_sets()
        elif type(sets) == str:
            sets = [sets]

        set_combination_difficulties = self.get_difficulties_sets(sets)
        if min_difficulty == "min":
            min_difficulty = set_combination_difficulties[0]
        if max_difficulty == "max":
            max_difficulty = set_combination_difficulties[-1]

        final_set: pd.DataFrame = pd.DataFrame(columns=["WORD", "DIFFICULTY"])
        for set_name in sets:
            final_set = final_set.append(self.scharade_sets[set_name], ignore_index=True)

        # filter difficulties
        final_set = final_set[min_difficulty <= final_set["DIFFICULTY"]]
        final_set = final_set[final_set["DIFFICULTY"] <= max_difficulty]

        final_set.drop_duplicates(inplace=True)
        final_set = final_set.sample(frac=1.0).reset_index(drop=True)

        return final_set
