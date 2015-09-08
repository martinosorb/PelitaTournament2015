from .base_player import BasePlayer

class HunterPlayer(BasePlayer):

    locked_target = None

    def get_efficient_hunter_move(self):
        """Retruns next move toward the closest enemy that is save to eat,
           avoiding dangerous enemies and friends, encouraging team bots
           to take different paths toward the enemy (hopefully trapping him)
        
        Note: if no safe bots are found, will return (0,0) as a move, to avoid
        illegal or moves.  Should probably do something else in this case.
        """

        self.update_free_adj_list()  # Get all free positions as a network

        # Filter out the dangerous enemies and friends
        self.remove_dangerous_enemies()
        if self.other_team_bots[0].current_pos != self.current_pos:
             self.remove_friends()

        # Find the nearest safe enemy and return the path to it.
        enemy_id_dict = self.get_safe_enemy_id()

        if HunterPlayer.locked_target not in list(enemy_id_dict.values()):
            HunterPlayer.locked_target = None

        if HunterPlayer.locked_target is not None:
            enemy_pos = self.enemy_bots[HunterPlayer.locked_target].current_pos
            next_move = self.next_move_in_path(self.shortest_path_to(enemy_pos))
        else:
            enemy_pos = self.get_closest_safe_enemy()
            if enemy_pos:
                self.say("I've found one!")
                HunterPlayer.locked_target = enemy_id_dict[enemy_pos]
                next_move = self.next_move_in_path(self.shortest_path_to(enemy_pos))
            else:
                next_move = self.get_efficient_eater_move()
        return next_move 



    def get_move(self):
        return self.get_efficient_hunter_move()
