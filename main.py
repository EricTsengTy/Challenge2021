import pygame as pg
from pygame.math import Vector2
from copy import copy
import sys

from EventManager.EventManager import EventManager
from Model.Model import GameEngine
from Controller.Controller import Controller
from View.View import GraphicalView
from View.sounds import Audio
from Model.GameObject.basic_game_object import Basic_Game_Object
from API.interface import Interface

def main(argv):
    # Initialization
    pg.init()
    
    # EventManager listen to events and notice model, controller, view
    ev_manager = EventManager()
    model      = GameEngine(ev_manager, argv[1:5])
    controller = Controller(ev_manager, model)
    view       = GraphicalView(ev_manager, model)
    interface = Interface(ev_manager, model)
    sound      = Audio(ev_manager, model)

    # Main loop
    model.run()

if __name__ == "__main__":
    main(sys.argv)
