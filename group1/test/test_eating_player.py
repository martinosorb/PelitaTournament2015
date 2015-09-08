import unittest

from pelita.player import SimpleTeam
from pelita.player import TestPlayer
import pdb

from pelita.game_master import GameMaster

from team import EaterPlayer

class EaterPlayerTest(unittest.TestCase):

    def test_seek_food_around_corner(self):
        my_team = SimpleTeam("test", EaterPlayer(), EaterPlayer())
        test_layout = """
                    ##############
                    #       .   3#
                    #### # ##   1#
                    # .   0      #
                    #      2##.. #
                    ##############
                    """
        teams = [
            # register my_team for bots 0, 2
            my_team,
            # for now enemies don't move
            SimpleTeam(TestPlayer(3*'-'), TestPlayer(3*'-'))
        ]

        gm = GameMaster(test_layout, teams, number_bots=4, game_time=3, seed=20)

        # play `game_time` rounds
        gm.play()
        # test if both players seeked the food
        self.assertEqual(gm.universe.bots[0].current_pos, (7, 1))
        self.assertEqual(gm.universe.bots[2].current_pos, (9, 3))


    def test_kill_before_seek_food(self):
        my_team = SimpleTeam("test", EaterPlayer(), EaterPlayer())
        test_layout = """
        ##############
        #.23      .  #
        #### ##   .  #
        #  0.       .#
        #  1    ##.. #
        ##############
        """
        teams = [
            # register my_team for bots 0, 2
            my_team,
            # for now enemies don't move
            SimpleTeam(TestPlayer(3*'>'), TestPlayer(3*'<'))
        ]

        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=20)

        # play `game_time` rounds
        gm.play()

        # test if both players killed enemy instead of seeking food
        self.assertEqual(gm.universe.bots[0].current_pos, (3, 4))
        self.assertEqual(gm.universe.bots[2].current_pos, (3, 1))
        self.assertEqual(gm.universe.teams[0].score, 10)



if __name__ == "__main__":
    unittest.main()
