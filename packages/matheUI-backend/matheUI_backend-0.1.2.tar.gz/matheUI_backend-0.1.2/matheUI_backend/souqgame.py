from typing import Union

from matheUI_backend.config import SOUQGAME_DATA_FILES, SOUQGAME_DATA_FOLDER

from .abstractGame import AbstactGame
from .souqgame_level import SouqGameLevel


class SouqGame(AbstactGame):
    """ SouqGame backend """

    def __init__(self, data_folder_path: str = SOUQGAME_DATA_FOLDER, data_files: dict[str, list[str]] = SOUQGAME_DATA_FILES):
        """
        @params:
            data_folder_path: path to the folder with the level data (Form: '/....../')
            data_files: dictionary with list of level file paths for one level group (Form: {'Mittelalter': ["souq_level_11.pkl", ...], ...})
        """
        self.data_folder_path = data_folder_path
        self.data_files = data_files

        self.level_dicts: dict[str, dict[dict[str, any]]] = {}
        for level_group in list(data_files.keys()):
            self.level_dicts[level_group] = {}
            for level_path in data_files[level_group]:
                self.level_dicts[level_group][level_path.split(".")[0]] = self._load_pickled_dict(data_folder_path+level_path)

    def data_report(self):
        print(f"level groups: {len(self.get_level_groups())}")
        for level_group in self.get_level_groups():
            print(f"    {level_group}: {len(self.get_level_names_in_level_group(level_group))}")
            for level_name in self.get_level_names_in_level_group(level_group):
                print(f"        {level_name}: {len(self.get_characters_in_level(level_group, level_name))}")
                for character in self.get_characters_in_level(level_group, level_name):
                    print(f"            {character}")

    def get_level_groups(self) -> list[str]:
        return list(self.level_dicts.keys())

    def get_level_names_in_level_group(self, level_group: str) -> list[str]:
        """ returns list of level names for a level group """
        return list(self.level_dicts[level_group].keys())

    def get_level(self, level_group: str, level_name: str) -> dict[str, any]:
        """ returns level dictionary """
        return self.level_dicts[level_group][level_name]

    def get_characters_in_level(self, level_group: str, level_name: str):
        """ returns all character of one level """
        level = self.get_level(level_group, level_name)
        data = level["data"]
        if type(data) == dict:
            return list(data.keys())
        elif type(data) == list:
            character_list: list = []
            for location_dict in data:
                character_list += list(location_dict.keys())
            return character_list
        else:
            raise UserWarning("ERROR: wrong structure of level data")

    @staticmethod
    def build_level(start_item: str, end_item: str, start_pos: str, data: Union[list[dict[str, dict[str, any]]], dict[str, dict[str, any]]], equal: list[tuple[str, str]]):
        """
        method to create a level dictionary

        @params:
            start_item: item that the player starts with
            end_item: the level ends when the player has this item
            start_pos: character name the player starts (sometimes helpful to trick the player)
            data: dictionary with character and what they trade (for multiple locations list of such dictonaries)
                key-value-form: '<character_name>': {<trade form>, ...}

                trade-forms:
                    normal-trade:
                        str: str (e.g. 'Holz': 'Tisch')
                    displayed-trade: first string is displayed, second string is item player gets in inventory
                        str: list[str, str] (e.g. 'Holz': ['"besonderer" Tisch', 'kaputter Tisch'])
                    only-if-happy-trade: trades only if character is happy
                        str: list[any] (any can contain a normal-, displayed-, or location-trade) (e.g. 'Holz': ['Tisch'], 'Holz': [['"besonderer" Tisch', 'kaputter Tisch']], ...)
                    make-happy-trade: trading gives player 'nichts' as item and makes character happy on position int (useful if needs multiple trades for complete happy)
                        str: list[[<displayed text>, int], "nichts"] (e.g. 'Schokolade': [["glücklich", 0], "nichts"])
                    location-trade: trade changes location of player and item keeps the same ("*" means the current inventory does not matter)
                        "*": list[<displayed text>, [int, <character name>]] (int is the position in the data list the player is send to and <character name> the character inside this new location) (e.g. '*': ["Ortszauber", [1, "Schamane"]])

                NOTE: if you want to create multiple options for one item and the same character (e.g. 'Kuh': 'Mistgabel' and 'Kuh': 'Schwein'), you have to add "_1" and "_2" so that the dictionary keys are unique again (the underscore numbers will not be displayed and are just for internal operations)

            equal: list of item tuples that are for trading equal (e.g. ("Stock", "Kampfstab"))
        """
        return dict(
            start_item=start_item, 
            end_item=end_item,
            start_pos=start_pos,
            data=data,
            equal=equal,
        )

    def update_data_files(self):
        print("no changing of data intended (for now)")

    def generate_round(self, level_group: str, level_name: str) -> SouqGameLevel:
        """ returns SouqGameLevel class object for playing the level """
        return SouqGameLevel(self.get_level(level_group, level_name))