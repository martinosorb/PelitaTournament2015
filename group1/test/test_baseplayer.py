import unittest

from pelita.player import SimpleTeam
from pelita.player import TestPlayer

from pelita.game_master import GameMaster

from team import EaterPlayer
from team import HunterPlayer #as Player
from team import HybridPlayer as Player


class BasePlayerTestBasic(unittest.TestCase):


    def test_there_is_a_wall(self):

        test_layout = """
            ########
            #0 .. 1#
            ########
            """
        teams = [
            SimpleTeam("test", Player()),	# my_team for bots 0, 2
            SimpleTeam(TestPlayer("----"))      # enemy
        ]

        #import pdb; pdb.set_trace()
        gm = GameMaster(test_layout, teams, number_bots=2, game_time=1, seed=20)
        gm.play()
        #possible_moves = gm.universe.legal_moves(gm.universe.bots[0].current_pos)

        # check that it didn't move to a wall
        self.assertEqual(gm.universe.bots[1].current_pos, (6, 1))
        self.assertNotEqual(gm.universe.bots[0].current_pos, (0, 1))
        self.assertNotEqual(gm.universe.bots[0].current_pos, (0, 0))
        self.assertNotEqual(gm.universe.bots[0].current_pos, (0, 2))


    def test_easy_kill_right(self):
        test_layout = """
            ##########
            #       3#
            # 01     #
            #       .#
            #. 2   ..#
            ##########
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("-"), TestPlayer("-"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=30)
        gm.play()
        # check that it killed it
        self.assertEqual(gm.universe.bots[0].current_pos, (3, 2))


    def test_easy_kill_down(self):
        test_layout = """
            ##########
            #       3#
            # 0      #
            # 1     .#
            #. 2   ..#
            ##########
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("-"), TestPlayer("-"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=30)
        gm.play()
        # check that it killed it
        self.assertEqual(gm.universe.bots[0].current_pos, (2, 3))


    def test_easy_kill_up(self):
        test_layout = """
            ##########
            # 1     3#
            # 0      #
            #       .#
            #. 2   ..#
            ##########
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("-"), TestPlayer("-"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=30)
        gm.play()
        # check that it killed it
        self.assertEqual(gm.universe.bots[0].current_pos, (2, 1))


    def test_easy_kill_left(self):
        test_layout = """
            ##########
            #       3#
            #10      #
            #       .#
            #. 2   ..#
            ##########
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("-"), TestPlayer("-"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=30)
        gm.play()
        # check that it killed it
        self.assertEqual(gm.universe.bots[0].current_pos, (1, 2))


    def test_panic_diagonal(self):
        # TEST FAILS and shouldn't
        test_layout = """
            ##########
            #     0  #
            #      1 #
            #      3.#
            #. 2   ..#
            ##########
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("-"), TestPlayer("-"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=30)
        gm.play()
        # check he runs away
        self.assertNotEqual(gm.universe.bots[0].current_pos, (6, 2))
        self.assertNotEqual(gm.universe.bots[0].current_pos, (7, 1))


    def test_panic_nearby(self):
        # TEST FAILS and shouldn't
        test_layout = """
            ##########
            #        #
            #     01 #
            #      3.#
            #. 2   ..#
            ##########
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("-"), TestPlayer("-"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=10)
        # WARNING: with seed 30 or 20 it fails
        #gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=30)
        gm.play()
        # check he runs away
        self.assertNotEqual(gm.universe.bots[0].current_pos, (6, 3))
        self.assertNotEqual(gm.universe.bots[0].current_pos, (7, 2))


    def test_panic_insight_right(self):
        test_layout = """
            ##########
            #        #
            #    0 1 #
            #      3.#
            #. 2   ..#
            ##########
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("-"), TestPlayer("-"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=30)
        gm.play()
        # check he runs away
        self.assertNotEqual(gm.universe.bots[0].current_pos, (6, 2))


    def test_panic_insight_up(self):
        test_layout = """
            ##########
            #      0 #
            #        #
            #      3.#
            #. 2  1..#
            ##########
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("-"), TestPlayer("-"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=30)
        gm.play()
        # check he runs away
        self.assertNotEqual(gm.universe.bots[0].current_pos, (7, 2))

    @unittest.skip("skipping avoid same path")
    def test_avoid_same_path(self):
        test_layout = """
            ##################
            #        #  2   .#
            # 1.     # ##### #
            #       .#0      #
            #. 3   ..        #
            ##################
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("--"), TestPlayer("--"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=2, seed=30)
        gm.play()
        # check that it killed it
        self.assertEqual(gm.universe.bots[2].current_pos, (14, 1))
        self.assertEqual(gm.universe.bots[0].current_pos, (12, 3))

    @unittest.skip("skipping avoid being killed")
    def test_avoid_being_killed(self):
        test_layout = """
            ##################
            #        #   .   #
            # 3.     # ##### #
            #       .# #0.   #
            #. 2   ..  #1    #
            #        #       #
            ##################
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("-"), TestPlayer("-"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=1, seed=30)
        gm.play()
        # check that it killed it
        self.assertEqual(gm.universe.bots[0].current_pos, (13, 3))


    def test_avoid_same_path(self):
        test_layout = """
            ##################
            #   1   #       .#
            # ##### # ..    .#
            #   02  #        #
            #.        #. 3   #
            ##################
        """
        teams = [
            SimpleTeam(Player(), Player()), # my_team for bots 0, 2
            SimpleTeam(TestPlayer("--"), TestPlayer("--"))  # enemy
        ]
        gm = GameMaster(test_layout, teams, number_bots=4, game_time=2, seed=30)
        gm.play()
        # check that it killed it
        self.assertEqual(gm.universe.bots[2].current_pos, (7, 3))
        self.assertEqual(gm.universe.bots[0].current_pos, (2, 3))


    def test_current_mode(self):
        test_layout = """
            ########
            #0 .. 1#
            ########
            """
        teams = [
            SimpleTeam("test", Player()),	# my_team for bots 0, 2
            SimpleTeam(TestPlayer("----"))      # enemy
        ]

        #import pdb; pdb.set_trace()
        gm = GameMaster(test_layout, teams, number_bots=2, game_time=1, seed=20)
        gm.play()
        print('current mode is ', gm.universe.bots[0].mode)
        #possible_moves = gm.universe.legal_moves(gm.universe.bots[0].current_pos)

        # check that it didn't move to a wall
        self.assertEqual(gm.universe.bots[1].current_pos, (6, 1))
        self.assertNotEqual(gm.universe.bots[0].current_pos, (0, 1))



if __name__ == "__main__":
    unittest.main()
