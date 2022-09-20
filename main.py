#!/usr/bin/env python3
import tcod

from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler
import procgen


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45

room_max_size = 10
room_min_size = 6
max_rooms = 30

TILESET = tcod.tileset.load_tilesheet("resources/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
WINDOW_TITLE = "Yet Another Roguelike Tutorial"
EVENT_HANDLER = EventHandler()


def main():
    player = Entity(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), '@', (255, 255, 255))
    npc = Entity(22, 25, '@', (255, 255, 0))
    entities = {npc, player}
    game_map = procgen.generate_dungeon(max_rooms, room_min_size, room_max_size, MAP_WIDTH, MAP_HEIGHT, player)

    engine = Engine(entities=entities, event_handler=EVENT_HANDLER, game_map=game_map, player=player)
    with tcod.context.new_terminal(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            tileset=TILESET,
            title=WINDOW_TITLE,
            vsync=True) as context:
        root_console = tcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        while True:
            engine.render(root_console, context)
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == '__main__':
    main()
