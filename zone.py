from enum import Enum
from typing import Optional


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    """Represents a zone in the drone network.

       Attributes:
        name: The name of the zone (hub, roof1, ...).
        x, y:  The coordinates of the zone.
        zone_type: The type of the zone.
        color: The color of the zone.
        max_drone: The number maximum of drone that
                   can be in the zone.
    """
    def __init__(
            self, name: str, x: int, y: int,
            zone_type: ZoneType = ZoneType.NORMAL,
            color: Optional[str] = None, max_drones: int = 1):
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drone = max_drones

        self.current_drones = 0
        self.neighbors = []
