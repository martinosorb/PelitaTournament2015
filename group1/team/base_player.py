# -*- coding: utf-8 -*-

# (Specifying utf-8 is always a good idea in Python 2.)

from pelita.player import AbstractPlayer
from pelita.datamodel import stop
from pelita import graph
import networkx
# use relative imports for things inside your module
from .utils import utility_function
import pdb


def astar_safe(*args, **kwargs):
    try:
        return networkx.astar_path(*args, **kwargs)
    except (networkx.exception.NetworkXNoPath, KeyError):
        return [args[1], args[1]]



#networkx.astar_path(self.adj, self.current_pos, target)


class BasePlayer(AbstractPlayer):
    """ Basically a clone of the RandomPlayer. """

    def __init__(self):
        # Do some basic initialisation here. You may also accept additional
        # parameters which you can specify in your factory.
        # Note that any other game variables have not been set yet. So there is
        # no ``self.current_uni`` or ``self.current_state``
        self.sleep_rounds = 0
        self.adj = None  # Spot for future Adjacency matrix
        self.mode = None

    def set_initial(self):
        pass
        # Now ``self.current_uni`` and ``self.current_state`` are known.
        # ``set_initial`` is always called before ``get_move``, so we can do some
        # additional initialisation here

        # Just printing the universe to give you an idea, please remove all
        # print statements in the final player.
        # print(self.current_uni.pretty)

    def check_pause(self):
        # make a pause every fourth step because whatever :)
        if self.sleep_rounds <= 0:
            if self.rnd.random() > 0.75:
                self.sleep_rounds = 3

        if self.sleep_rounds > 0:
            self.sleep_rounds -= 1
            texts = ["What a headache!", "#aspp2015", "Python School Munich"]
            self.say(self.rnd.choice(texts))
            return stop

    def update_free_adj_list(self):
        #Update self.adj with All non-wall positions in maze
        free_pos = self.current_uni.free_positions()

        self.adj = networkx.Graph(graph.AdjacencyList(free_pos))


    def remove_adj_elements(self, target_list):
        """Removes all tuples from target.  If target is a single position tuple, just returns that.
            Does nothing if target_list is empty or evaluates to False."""

        if not target_list:
            return

        # Put an alone target into a tuple of tuples, to make list-like
        if not isinstance(target_list[0], tuple):
            target_list = [target_list]

        # Remove each target from the adjacency matrix.
        for target in target_list:
            if target in self.adj:
                self.adj.remove_node(target)

    def remove_dangerous_enemies(self):
        """Remove the positions of dangerous enemy bots from the self.adj adjacency network."""

        dangerous_bot_positions = [bot.current_pos for bot in self.enemy_bots if (bot.is_destroyer and not bot.noisy)]

        if dangerous_bot_positions:
            dangerous_squares = []
            for pos in dangerous_bot_positions:
                for move in [(0,0), (1,0), (-1, 0), (0, 1), (0, -1)]:
                    new_pos = (pos[0]+move[0], pos[1]+move[1])
                    if new_pos in self.adj and new_pos != self.current_pos:
                        dangerous_squares.append(new_pos)
            self.remove_adj_elements(dangerous_squares)
        else:
            pass



    def remove_friends(self):
        """Remove the positions of friend bots from the self.adj adjacency network."""
        self.remove_adj_elements([bot.current_pos for bot in self.other_team_bots])


    def shortest_path_to(self, target):
        """Returns a list of positions that lead from the target position to the current position"""
        return astar_safe(self.adj, self.current_pos, target)


    def get_distances(self, pos_list):
        """Returns dictionary of distances to pos_list positions"""
        pos_dict = {}

        for pos in pos_list:
               path = astar_safe(self.adj, self.current_pos, pos)
               dist = len(path)
               try:
                   pos_dict[pos] = dist if path[0] != path[1] else 300
               except IndexError:
                   pos_dict[pos] = 0

        return pos_dict

    def get_food_distances(self):
        """Returns dictionary of distances to food positions"""
        return self.get_distances(self.enemy_food)

    def get_team_food_distances(self):
        """Returns dictionary of distances to food positions"""
        return self.get_distances(self.team_food)

    def get_safe_enemy_distances(self):
        """Returns dictionary of distances to safe enemies, or None if no enemies are safe to attack."""
        safe_enemy_pos_list = [bot.current_pos for bot in self.enemy_bots if not bot.in_own_zone]

        #Perhaps no enemies are safe to attack.  In that case, return None
        if len(safe_enemy_pos_list) == 0:
            return None
        else:
            return self.get_distances(safe_enemy_pos_list)

    def get_safe_enemy_id(self):
        """Returns dictionary of distances to safe enemies, or None if no enemies are safe to attack."""
        safe_enemy_ids = {bot.current_pos:Id for Id, bot in enumerate(self.enemy_bots) if not bot.in_own_zone}
        return safe_enemy_ids

    def get_dangerous_enemy_distances(self):
        """Returns dictionary of distances to safe enemies, or None if no enemies are safe to attack."""
        dangerous_enemy_pos_list = [bot.current_pos for bot in self.enemy_bots if bot.is_destroyer]

        #Perhaps no enemies are safe to attack.  In that case, return None
        if len(dangerous_enemy_pos_list) == 0:
            return None
        else:
            return self.get_distances(dangerous_enemy_pos_list)

    def get_closest_item(self, distance_dict):
        """Returns the item in a distance dictionary that is the shortest distance away."""
        min_item, min_dist = None, 3000
        for key, value in distance_dict.items():
            if value < min_dist:
                min_item, min_dist = key, value

        return min_item

    def get_closest_food(self):
        """Returns the position of the closest food pellet, based on the current self.adj
        adjacency network."""
        food_dict = self.get_food_distances()

        return self.get_closest_item(food_dict)

    def get_closest_team_food(self):
        """Returns the position of the closest food pellet, based on the current self.adj
        adjacency network."""
        food_dict = self.get_team_food_distances()

        return self.get_closest_item(food_dict)

    def get_closest_safe_enemy(self):
        """Returns the position of the closest safe enemy to attack, based ont he current
        self.adj adjacency network."""
        safe_enemy_dict = self.get_safe_enemy_distances()
        if safe_enemy_dict:
            return self.get_closest_item(safe_enemy_dict)
        else:
            return None

    def get_closest_dangerous_enemy(self):
        """Returns the position of the closest safe enemy to attack, based ont he current
        self.adj adjacency network."""
        dangerous_enemy_dict = self.get_dangerous_enemy_distances()
        if dangerous_enemy_dict:
            return self.get_closest_item(dangerous_enemy_dict)
        else:
            return None


    def next_move_in_path(self, pathlist):
        """Returns the next move to make to move along the path given (a
        list of tuples to take in order."""

        # Paths are returned in backwards order, so take the last pos

        next_move = tuple([nc-cc for nc, cc in zip(pathlist[1], self.current_pos)])

        # Check if next_move leads to dangerous space.  If so, choose a
        # random other move.
        enemy_positions = [bot.current_pos for bot in self.enemy_bots if (bot.is_destroyer and not bot.noisy)]

        for near_enemy in enemy_positions:
            poss_moves = list(self.legal_moves.keys())
            for move in [(0,0), (1,0), (-1, 0), (0, 1), (0, -1)]:
                check_pos = (near_enemy[0]+move[0], near_enemy[1]+move[1])

                if self.legal_moves[next_move] == check_pos:
                    try:
                        poss_moves.remove(next_move)
                    except:
                        self.say("Shit!")
                    if len(poss_moves) > 0:
                        next_move = self.rnd.choice(poss_moves)
                    else:
                        next_move = (0,0)
                        break



        return next_move


    def check_easykill(self):
        """Returns a move if right next to a killable enemy."""
        killable_enemy_pos = [bot.current_pos
            for bot in self.enemy_bots if (bot.is_harvester and not bot.noisy)]

        # easy kill (kind of tested)
        for killable in killable_enemy_pos:
            if killable in self.legal_moves.values():
                move = graph.diff_pos(self.current_pos, killable)
                return move


    def get_efficient_hunter_move(self):
        """Retruns next move toward the closest enemy that is save to eat,
           avoiding dangerous enemies and friends, encouraging team bots
           to take different paths toward the enemy (hopefully trapping him)

        Note: if no safe bots are found, will return (0,0) as a move, to avoid
        illegal or moves.  Should probably do something else in this case.
        """
        raise NotImplementedError("Should import from HunterPlayer if you want to use this!")

    def get_efficient_eater_move(self):
        """Returns next move toward the closest pellet, avoiding enemies and
        friends, so that the friends will go along different directions."""
        self.update_free_adj_list()  # Get all free positions as a network

        next_move = self.check_easykill()
        if next_move:
            self.say("Easy kill!")
        else:
            # Filter out the enemies and friends
            self.remove_dangerous_enemies()
            self.remove_friends()

            # Get the next move along the shortest path to the nearest food pellet.
            #enemy_pos = self.get_closest_safe_enemy()
            food_pos = self.get_closest_food()
            food_path = self.shortest_path_to(food_pos)
            next_move = self.next_move_in_path(food_path)

            #pdb.set_trace()
        return next_move

    def get_move(self):
        raise NotImplementedError("Import EaterPlayer, HunterPlayer, or HybridPlayer instead.")
