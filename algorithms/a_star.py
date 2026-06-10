import heapq
from itertools import count

from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Retorna a soma das distancias de Manhattan das pecas."""
        distance = 0

        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue

            goal_index = tile - 1
            row, column = divmod(index, 3)
            goal_row, goal_column = divmod(goal_index, 3)
            distance += abs(row - goal_row) + abs(column - goal_column)

        return distance

    def search(self, initial: State) -> SearchResult:
        tie_breaker = count()
        frontier = [
            (initial.cost + self.heuristic(initial), next(tie_breaker), initial)
        ]
        best_cost = {initial: initial.cost}
        explored = set()
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current.cost != best_cost.get(current) or current in explored:
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost,
                )

            explored.add(current)
            nodes_expanded += 1

            for neighbor in current.neighbors():
                if neighbor in explored:
                    continue

                previous_cost = best_cost.get(neighbor)
                if previous_cost is not None and neighbor.cost >= previous_cost:
                    continue

                best_cost[neighbor] = neighbor.cost
                priority = neighbor.cost + self.heuristic(neighbor)
                heapq.heappush(
                    frontier,
                    (priority, next(tie_breaker), neighbor),
                )
                nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
