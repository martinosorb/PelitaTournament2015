# -*- coding: utf-8 -*-
import pdb
from pelita import datamodel
from pelita.graph import AdjacencyList, NoPathException, diff_pos
from pelita.player import AbstractPlayer, SimpleTeam


class OurPlayer(AbstractPlayer):
    def set_initial(self):
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.next_food = None

    def goto_pos(self, pos):
        return self.adjacency.a_star(self.current_pos, pos)[-1]

    def get_move(self):
        # from SmartRandom
        dangerous_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if bot.is_destroyer]
        killable_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if bot.is_harvester]

        # easy kill (please test)
        for killable in killable_enemy_pos:
            if killable in self.legal_moves.items():
                move = diff_pos(self.current_pos, killable)
                self.say("Easy kill!")
                return move
        #pdb.set_trace()

        # panic
#        for dangerous in dangerous_enemy_pos:
#            if killable in self.legal_moves.items():
#                move = diff_pos(self.current_pos, killable)
#                self.say("Easy kill!")
#                return move

        

        # check, if food is still present
        # if the nearest is not suitable, choose one at random!
        if (self.next_food is None
                or self.next_food not in self.enemy_food):
            if not self.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop
            # SUBOPTIMAL (chooses at random)

            self.next_food = self.rnd.choice(self.enemy_food)

        try:
            next_pos = self.goto_pos(self.next_food)
            move = diff_pos(self.current_pos, next_pos)
            return move
        except NoPathException:
            return datamodel.stop

