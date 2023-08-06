from .souqgame_character import SouqGameCharacter


class SouqGameLevel:
    """ level management class """

    def __init__(self, level_dict: dict[str, any]):
        self._start_item = level_dict["start_item"]
        self.end_item = level_dict["end_item"]
        self._start_pos = level_dict["start_pos"]
        self._data = level_dict["data"]

        self.characters: list[dict[str, SouqGameCharacter]] = []
        if type(self._data) == list:
            for location_characters in self._data:
                location_characters_dict: dict[str, SouqGameCharacter] = {}
                for character in list(location_characters.keys()):
                    location_characters_dict[character] = SouqGameCharacter(character, location_characters[character])
                self.characters += [location_characters_dict]
        else:
            location_characters_dict: dict[str, SouqGameCharacter] = {}
            for character in list(self._data.keys()):
                location_characters_dict[character] = SouqGameCharacter(character, self._data[character])
            self.characters = [location_characters_dict]

        self.equal = level_dict["equal"]

        self.pos = level_dict["start_pos"] # current player position
        self.location: int = 0 # current location (only relevant if multiple locations exist)
        self.inventory = level_dict["start_item"] # current item (first item is start item)

    @property
    def location_number(self):
        """ number of different locations """
        return len(self.characters)

    def move_forward(self):
        """ moves position one character forward """
        pos_idx = self.get_current_characters().index(self.pos)
        total_len_characters = len(self.get_current_characters())
        if pos_idx == total_len_characters-1:
            new_pos_idx = 0
        else:
            new_pos_idx = pos_idx + 1
        self.pos = self.get_current_characters()[new_pos_idx]

    def move_backwards(self):
        """ moves position one character back """
        pos_idx = self.get_current_characters().index(self.pos)
        total_len_characters = len(self.get_current_characters())
        if pos_idx == 0:
            new_pos_idx = total_len_characters-1
        else:
            new_pos_idx = pos_idx - 1
        self.pos = self.get_current_characters()[new_pos_idx]

    def is_first_or_last_character(self) -> bool:
        """ returns True if current character is first or last in its location """
        if self.pos == self.get_current_characters()[0] or self.pos == self.get_current_characters()[-1]:
            return True
        else:
            return False

    def get_current_character(self) -> SouqGameCharacter:
        """ returns SouqGameCharacter class object of current character """
        return self.characters[self.location][self.pos]

    def get_current_characters(self) -> list[str]:
        """ returns character name list of current location """
        return list(self.characters[self.location].keys())

    def get_current_position_trades(self) -> list[tuple[str, str]]:
        """ returns list with tuples of trade item and displayed text for wanted item """
        return self.get_current_character().get_displayed_trades()

    def get_current_character_happiness(self) -> list[bool]:
        """ returns list with booleans of different happy states of current character """
        return list(self.get_current_character().happy.values())

    def is_in_inventory(self, item: str):
        """ checks if item is in inventory or equal to item in inventory """
        if item == self.inventory or (item, self.inventory) in self.equal or (self.inventory, item) in self.equal or item == "*":
            return True
        else:
            return False

    def trade(self, option: int):
        """
        @param:
            option: index of option from 'get_current_position_trades' method output

        @return:
            2: successful location swap
            1: successfully traded
            0: level finished
            -1: character does not trade this item
            -2: character needs to be happy for this trade
        """
        trade_option = self.get_current_position_trades()[option]
        if self.is_in_inventory(trade_option[0]):
            trade_result = self.get_current_character().trade(self.get_current_character().get_accepted_items()[option]) # for solving problem with unique dictionary keys
            if type(trade_result) == int:
                return trade_result
            elif type(trade_result) == str:
                self.inventory = trade_result
                if self.is_in_inventory(self.end_item):
                    return 0
                else:
                    return 1
            elif type(trade_result) == list:
                self.location = trade_result[0]
                self.pos = trade_result[1]
                return 2
            
            raise UserWarning("ERROR: something unexpected happened -> problem in SouqGameCharacter.trade result")
        else:
            return -1
