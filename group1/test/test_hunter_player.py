import unittest

from pelita.player import SimpleTeam
from pelita.player import TestPlayer
import pdb

from pelita.game_master import GameMaster

from team import HunterPlayer

class HunterPlayerTest(unittest.TestCase):

    @unittest.skip("skipping common target")
    def test_common_target(self):
        my_team = SimpleTeam("test", HunterPlayer(), HunterPlayer())
        test_layout = '''
        ####################
        #    1    0       .#
        #### ###           #
        # .   2            #
        #    3            ##
        ####################
        '''
        teams = [
            # register my_team for bots 0, 2
            my_team,
            # for now enemies don't move
            SimpleTeam(TestPlayer('<<<'), TestPlayer('<<<'))
        ]

        gm = GameMaster(test_layout, teams, number_bots=4, game_time=3, seed=20)

        # play `game_time` rounds
        gm.play()
        #pdb.set_trace()
        # test if both players seeked the food
        self.assertEqual(gm.universe.bots[0].current_pos, (7, 1))
        self.assertEqual(gm.universe.bots[2].current_pos, (4, 2))
        #self.assertEqual(gm.universe.bots[2].current_pos, (4, 4))


if __name__ == "__main__":
    unittest.main()
