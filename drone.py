from zone import Zone, ZoneType
from typing import List


class Drone:
    """Represents the drones

       Attributes:
        id: The identification of drone
        current_zone: The currently's drone zone
        path: List of the drone's pathing
        arrived: Bool of the drone's end of path
    """

    def __init__(self, id: int, current_zone: Zone,
                 path: List[Zone] = [], arrived: bool = False) -> None:
        self.id = id
        self.current_zone = current_zone
        self.path = path
        self.arrived = arrived

        self.step_index = 0
        self.waiting_ticks = 0

    def get_next_zone(self):
        if self.step_index + 1 < len(self.path):
            return self.path[self.step_index + 1]

    def move_to_next(self, graph):
        if self.waiting_ticks > 0:
            self.waiting_ticks -= 1
            return False

        next_zone = self.get_next_zone()
        conn = graph.get_connection(self.current_zone, next_zone)

        if next_zone:
            if next_zone.zone_type == ZoneType.BLOCKED:
                return False

            if (next_zone.current_drones < next_zone.max_drone and
                    conn.current_links < conn.max_link_capacity):
                self.current_zone.current_drones -= 1
                next_zone.current_drones += 1

                conn.current_links += 1
                self.current_zone = next_zone
                self.step_index += 1

                if self.current_zone.zone_type == ZoneType.RESTRICTED:
                    self.waiting_ticks = 1

                if self.step_index == len(self.path) - 1:
                    self.arrived = True
                return True
            else:
                return False
        return False
