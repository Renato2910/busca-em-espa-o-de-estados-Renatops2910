from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutavel de 9 inteiros (0 = espaco vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado invalido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos validos a partir deste estado."""
        moves = {
            "up": -3,
            "down": 3,
            "left": -1,
            "right": 1,
        }
        invalid_moves = {
            "up": self.blank_index < 3,
            "down": self.blank_index > 5,
            "left": self.blank_index % 3 == 0,
            "right": self.blank_index % 3 == 2,
        }

        children = []

        for action, offset in moves.items():
            if invalid_moves[action]:
                continue

            new_blank_index = self.blank_index + offset
            new_tiles = list(self.tiles)
            new_tiles[self.blank_index], new_tiles[new_blank_index] = (
                new_tiles[new_blank_index],
                new_tiles[self.blank_index],
            )

            children.append(
                State(
                    tuple(new_tiles),
                    parent=self,
                    action=action,
                    cost=self.cost + 1,
                )
            )

        return children

    def path(self) -> List["State"]:
        """Retorna a sequencia de estados do estado inicial ate este."""
        current: Optional["State"] = self
        states = []

        while current is not None:
            states.append(current)
            current = current.parent

        return list(reversed(states))

    def actions(self) -> List[str]:
        """Retorna a sequencia de acoes do estado inicial ate este."""
        return [state.action for state in self.path()[1:] if state.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
