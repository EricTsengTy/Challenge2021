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
    debug_mode = False
    for arg in argv[1:]:
        if arg.lower() in ('--debug', '-d'):
            debug_mode = True
        else:
            AIs.append(arg)

    assert len(AIs) <= 4, "too many AI"

    model      = GameEngine(ev_manager, AIs)
    controller = Controller(ev_manager, model)
    view       = GraphicalView(ev_manager, model)
    interface = Interface(ev_manager, model, debug_mode)
    sound      = Audio(ev_manager, model)

    # Main loop
    model.run()

if __name__ == "__main__":
    main(sys.argv)
