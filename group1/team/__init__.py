#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pelita.player import SimpleTeam

from .demo_player import DrunkPlayer
from .hunter_player import HunterPlayer
from .eater_player import EaterPlayer
from .hybrid_player import HybridPlayer

# (please use relative imports inside your module)

# The default factory method, which this module must export.
# It must return an instance of `SimpleTeam`  containing
# the name of the team and the respective instances for
# the first and second player.

def hunter_factory():
    return SimpleTeam("EasyKillH", HunterPlayer(), HunterPlayer())

# For testing purposes, one may use alternate factory methods::
#
def eater_factory():
    return SimpleTeam("EasyKillE", EaterPlayer(), EaterPlayer())
#

def factory():
    return SimpleTeam("EasyKill", HybridPlayer(), HybridPlayer())


# To be used as follows::
#
#     $ ./pelitagame path_to/groupN/:alternate_factory
