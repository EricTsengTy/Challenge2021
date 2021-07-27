import Const

class Color_Selector():
    def __init__(self, players):
        self.color_player = {color : None for color in Const.COLOR_TABLE}
        for player in players:
            self.color_player[player.color] = player

    def previous_color(self, player):
        color_index = Const.COLOR_TABLE.index(player.color)
        color_index = (color_index - 1) % Const.COLOR_TABLE_SIZE
        while self.color_player[Const.COLOR_TABLE[color_index]] != None:
            color_index = (color_index - 1) % Const.COLOR_TABLE_SIZE
        self.color_player[player.color] = None
        player.color = Const.COLOR_TABLE[color_index]
        player.color_index = color_index
        self.color_player[player.color] = player
        #print(player.color)

    def next_color(self, player):
        color_index = Const.COLOR_TABLE.index(player.color)
        color_index = (color_index + 1) % Const.COLOR_TABLE_SIZE
        while self.color_player[Const.COLOR_TABLE[color_index]] != None:
            color_index = (color_index + 1) % Const.COLOR_TABLE_SIZE
        self.color_player[player.color] = None
        player.color = Const.COLOR_TABLE[color_index]
        player.color_index = color_index
        self.color_player[player.color] = player
        #print(player.color)
