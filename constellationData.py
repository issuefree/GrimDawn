"""Constellation data for the optimiser.

This is now generated from the Grim Dawn database rather than maintained by
hand. Regenerate after a game patch with:

    python devotion.py --regenerate

The previous hand-written file is kept as constellationData_hand.py, which is
what "python devotion.py --check-data" compares the game files against. It is
no longer used for scoring: it is missing 35 constellations the game has and
57 of its star values have drifted from the database.
"""
from constellationData_generated import *
