class SouqGameCharacter:
    """ SouqGame character class """

    def __init__(self, character_name: str, character_trades: dict[str, any]):
        self.character_name = character_name
        self.trades = character_trades
        # get if there are trades that make the character happy and save that the character is not happy at the beginning
        self.happy: dict[bool] = {}
        value_list = list(self.trades.values())
        while value_list != []:
            value = value_list[0]
            if type(value) == list:
                if len(value) == 1 and type(value[0]) == list:
                        value_list.append(value[0])
                elif len(value) == 2 and type(value[0]) == list and value[1] == "nichts":
                    self.happy[value[0][1]] = False
            del value_list[0]

    def get_accepted_items(self) -> list[str]:
        return list(self.trades.keys())

    def get_displayed_item(self, trade_item: str):
        """ method to get the displayed text of wanted item for a trade """
        displayed_item = self.trades[trade_item]
        if type(displayed_item) == str:
            return displayed_item
        elif type(displayed_item) == list and type(displayed_item[0]) == str:
            return displayed_item[0]
        elif type(displayed_item) == list and type(displayed_item[0]) == list and type(displayed_item[0][0]) == str:
            return displayed_item[0][0]
        else:
            raise UserWarning("value for trade_item is not confirm")        

    def get_displayed_trades(self) -> list[tuple[str, str]]:
        """ returns list with tuple (trade item, displayed item) to show player """
        displayed_trades: list[tuple[str, str]] = []
        for trade_item in self.get_accepted_items():
            displayed_item = self.get_displayed_item(trade_item)
            displayed_trades.append((trade_item.split("_")[0], displayed_item))
        return displayed_trades

    def trade(self, trade_item: str):
        """
        @param:
            trade_item: item for trading

        @return:
            -1: character does not trade this item
            -2: character needs to be happy for this trade
            str: new item for inventory
            list[int, str]: new location and character (inventory item keeps the same)
        """
        if trade_item in self.get_accepted_items():
            given_item = self.trades[trade_item]
            # normal trade (str: str)
            if type(given_item) == str:
                return given_item

            # only if happy trade (str: list[any])
            elif type(given_item) == list and len(given_item) == 1:
                if all(list(self.happy.values())):
                    if type(given_item[0]) == str:
                        return given_item[0]
                    elif type(given_item[0]) == list and type(given_item[0][0]) == str:
                        return given_item[0][1]
                else:
                    return -2

            elif type(given_item) == list and len(given_item) == 2:
                # makes happy trade (str: list[list[str, int], "nichts"])
                if type(given_item[0]) == list and given_item[1] == "nichts":
                    self.happy[given_item[0][1]] = True
                    return given_item[1]
                # normal trade with different name displayed (str: list[str, str]) or location swap trade (str: list[str, list[int, str]])
                elif type(given_item[0]) == str:
                    return given_item[1]

            raise UserWarning("ERROR: found unsupported structure for trading in data")
        else:
            return -1
