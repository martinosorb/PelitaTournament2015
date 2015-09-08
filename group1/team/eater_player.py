from .base_player import BasePlayer

class EaterPlayer(BasePlayer):

    def get_move(self):
        return self.get_efficient_eater_move()
