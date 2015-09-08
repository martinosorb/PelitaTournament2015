from .hunter_player import HunterPlayer
import pdb

class HybridPlayer(HunterPlayer):

    def get_run_back_move(self):
        self.update_free_adj_list()  # Get all free positions as a network
        self.remove_dangerous_enemies()      
        pos_list = [(15+self.team.index, y) for y in range(16) if (15+self.team.index, y) in self.adj]
        distances = self.get_distances(pos_list)
        return_pos = self.get_closest_item(distances)
        return_path = self.shortest_path_to(return_pos)
        next_move = self.next_move_in_path(return_path)
        return next_move

    def get_move(self):

       # First Part of the Game: Until there are 20 food left.
       if len(self.enemy_food) > 20 and len(self.team_food) > 6:
            self.mode = 'Eater'
            self.say("Let's Have a Snack!")
            return self.get_efficient_eater_move()

       # Second Part of the Game: Until there are 4 food left.
       elif len(self.team_food) > 6:
            
            self.mode = 'Hunter'

            if self.me.is_destroyer:
                self.say("Hunting Now")
                return self.get_efficient_hunter_move()
            else:
                self.say("Running Back")
                return self.get_run_back_move()


       # End of Game: After there are 4 food left, be a dick.
       else:
           
           # First player defends a random own food.
           if self.team_bots[0] == self.me:
                
                self.say("Defending the Fort!")
                food_pos = self.get_closest_team_food()
                food_path = self.shortest_path_to(food_pos)
                try:
                    return self.next_move_in_path(food_path)
                except IndexError:
                    return (0,0)
                    
                
           else: 
               self.say("Hold down the fort!")
               return self.get_efficient_eater_move()
                
                 

       
