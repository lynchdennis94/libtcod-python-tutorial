from __future__ import annotations

from typing import TYPE_CHECKING

import colors
from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    entity: Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.entity.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message = "You died!"
            self.engine.message_log.add_message(death_message, colors.PLAYER_DIE)
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.entity.name} is dead!"
            self.engine.message_log.add_message(death_message, colors.ENEMY_DIE)

        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.render_order = RenderOrder.CORPSE
        self.entity.name = f"remains of {self.entity.name}"

        print(death_message)
