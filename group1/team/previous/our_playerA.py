# -*- coding: utf-8 -*-
import pdb
from pelita import datamodel
from pelita.graph import AdjacencyList, NoPathException, diff_pos
from pelita.player import AbstractPlayer, SimpleTeam

from .base_player import BasePlayer


class OurPlayer(BasePlayer):
    def set_initial(self):
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.next_food = None

    def goto_pos(self, pos):
        return self.adjacency.a_star(self.current_pos, pos)[-1]
    def abs_pos(self, vector):
        return (self.current_pos[0]+vector[0], self.current_pos[1]+vector[1])

    def get_move(self):
        # from SmartRandom
        dangerous_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if (bot.is_destroyer and not bot.noisy)]
        killable_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if (bot.is_harvester and not bot.noisy)]

        # easy kill (kind of tested)
        for killable in killable_enemy_pos:
            if killable in self.legal_moves.values():
                self.say("Easy kill!")
                print("Easy kill!")
                move = diff_pos(self.current_pos, killable)
                return move

        # don't die
        forbidden_moves = []
        for dangerous in dangerous_enemy_pos:
            relative_pos = diff_pos(self.current_pos, dangerous)
            # check if the destroyer is nearby
            if relative_pos in ( (0,1), (1,0), (-1,0), (0,-1)):
                self.say("Enemy nearby!")
                forbidden_moves.append(relative_pos)
            if relative_pos in ( (0,2), (2,0), (-2,0), (0,-2)):
                self.say("Enemy in sight!")
                rpx, rpy = relative_pos
                forbidden_moves.append( (rpx//2, rpy//2) )
            if relative_pos in ( (1,1), (1,-1), (-1,1), (-1,-1)):
                self.say("Enemy on diagonal!")
                rpx, rpy = relative_pos
                forbidden_moves.append( (0, rpy) )
                forbidden_moves.append( (rpx, 0) )
        forbidden_absolute_positions = [self.abs_pos(fm) for fm in forbidden_moves]
        # forbidden_absolute_positions WAS tested (kind of)
        # it doesn't account for walls (relevant in the second case)

        # check, if food is still present
        # if the nearest is not suitable, choose one at random!
        if (self.next_food is None
                or self.next_food not in self.enemy_food):
            if not self.enemy_food:
                # all food has been eaten? ok. i’ll stop
                return datamodel.stop

            self.next_food = self.get_efficient_eater_move()

        try:
            move = self.get_efficient_eater_move()
            # if it's not allowed, take a random move
            if move in forbidden_moves:
                # but we are not checking if it's forbidden again!
                next_pos = self.rnd.choice(list(self.legal_moves.values()))
                move = diff_pos(self.current_pos, next_pos)
            return move
        except NoPathException:
            return datamodel.stop

