import random
from typing import Union

from matheUI_backend.config import (AGENT_UNDERCOVER_PLACES_FILES,
                                    AGENT_UNDERCOVER_PLACES_FOLDER)

from .abstractGame import AbstactGame


class AgentUndercover(AbstactGame):
    """ AgentUndercover backend """

    def __init__(self, places_folder: str = AGENT_UNDERCOVER_PLACES_FOLDER, places_files: dict[str, str] = AGENT_UNDERCOVER_PLACES_FILES):
        """
        @params:
            places_folder: path to the folder with the places data (Form: '/....../')
            places_files: dictionary with name of the places group and file name of the data (Form: {'standard': 'standard_places.pkl'})
        """
        self.places_folder = places_folder
        self.places_files = places_files
        
        self.places_dicts: dict[str, dict[str, list[str]]] = {}
        for places_group in list(places_files.keys()):
            self.places_dicts[places_group] = self._load_pickled_dict(places_folder+places_files[places_group])

    def data_report(self):
        """ data report (places groups, places, professions) """
        print(f"{len(self.get_places_groups())} different groups of places {self.get_places_groups()}")
        for places_group in self.get_places_groups():
            print()
            print(f"{places_group} places (number: {len(self.get_places(places_group))}):")
            for place in self.get_places(places_group):
                print(f"    {place}: {len(self.get_professions(places_group, place))}")
                for profession in self.get_professions(places_group, place):
                    print(f"        {profession}")

    def get_professions(self, places_group: str, place: str) -> list[str]:
        return self.places_dicts[places_group][place]

    def get_places(self, places_group: str) -> list[str]:
        return list(self.places_dicts[places_group].keys())

    def get_places_groups(self) -> list[str]:
        return list(self.places_dicts.keys())

    def add_place(self, places_group: str, place_name: str, professions: list[str]):
        if len(professions) <= 5:
            print("WARNING: You should have more than 5 professions for one place")
 
        if place_name not in self.places_dicts[places_group]:
            self.places_dicts[places_group][place_name] = professions
        else:
            print(f"WARNING: place already exists in '{places_group}' -> overwrite professions")
            self.places_dicts[places_group][place_name] = professions

    def delete_place(self, places_group: str, place_name: str):
        del self.places_dicts[places_group][place_name]

    def add_profession(self, places_group: str, place_name: str, profession: str):
        if profession not in self.places_dicts[places_group][place_name]:
            self.places_dicts[places_group][place_name] += [profession]
        else:
            print(f"INFO: profession already exists in '{places_group}'/'{place_name}'")

    def delete_profession(self, places_group: str, place_name: str, profession: str):
        self.places_dicts[places_group][place_name].remove(profession)

    def update_data_files(self):
        """ function to update the data files with self.places_dict content """
        print("Do you want to save the following data? (yes/no)")
        self.data_report()
        print("answer:")
        answer = input()
        if answer == "yes":
            for places_group in self.get_places_groups():
                self._pickle_dict(self.places_dicts[places_group], self.places_folder+self.places_files[places_group])
            print("data files updated")
        else:
            print("process stopped")

    def generate_round(self, player_number: int, spy_number: int, places_groups: Union[str, list[str]] = "all") -> tuple[str, list[str]]:
        """
        @params:
            player_number: number of roles that shall be generated
            spy_number: number of spies in the roles (has to be smaller than player_number)
            places_groups: which groups of places shall be used
                'all': all groups in self.places_dict
                str: string of group name
                list[str]: list with group names
        
        @return:
            tuple of place name and list with roles
        """
        if places_groups == "all":
            places_groups = self.get_places_groups()
        elif type(places_groups) == str:
            places_groups = [places_groups]

        round_places: dict[str, list[str]] = {}
        for places_group in places_groups:
            round_places.update(self.places_dicts[places_group])
        
        if round_places == {}:
            raise RuntimeError(f"wrong places_groups '{places_groups}' -> possible places_groups '{list(self.places_dicts.keys())}'")

        if spy_number >= player_number:
            raise RuntimeError("'spy_number' must be smaller than 'player_number'")

        place = random.choice(list(round_places.keys()))
        professions = random.choices(round_places[place], k=player_number-spy_number)
        roles = professions + ["Spion"]*spy_number
        random.shuffle(roles)

        return place, roles
