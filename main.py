from asyncio import FastChildWatcher
import pygame as pg
from copy import copy
import sys

from EventManager.EventManager import EventManager
from Model.Model import GameEngine
from Controller.Controller import Controller
from View.View import GraphicalView
from View.sounds import Audio
from API.interface import Interface

def main(argv):
    # Initialization
    pg.init()

    # EventManager listen to events and notice model, controller, view
    ev_manager = EventManager()
    AIs = []
    special_modes = []
    for arg in argv[1:]:
        if arg.lower() in ('--nodebug', '-nd'):
            special_modes.append('NODEBUG')
        elif arg.lower() in ('--timeout', '-t'):
            special_modes.append('TIMEOUT')
        else:
            AIs.append(arg)

    assert len(AIs) <= 4, "too many AI"

    model      = GameEngine(ev_manager, AIs)
    controller = Controller(ev_manager, model)
    view       = GraphicalView(ev_manager, model)
    interface = Interface(ev_manager, model, special_modes)
    sound      = Audio(ev_manager, model)

    # Main loop
    model.run()

if __name__ == "__main__":
    main(sys.argv)
