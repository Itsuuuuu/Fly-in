from zone import Zone
from connection import Connection
from typing import Dict, List
from typing import Optional


class Graph:
    """Represents the drone's network graph.

       Attributes:
       start: The start zone in the connection
       end: The end zone in the connection
       zones: Dict of zone's network graph
       connections: List of connections's network graph
    """
    def __init__(self) -> None:
        self.start: Optional[Zone] = None
        self.end: Optional[Zone] = None
        self.zones: Dict[str, Zone] = {}
        self.connections: List[Connection] = []

    # Permet de créer une pince qui fouille dans le sac en vrac
    # des différentes connecions.
    def get_connection(
            self, zone_a: Zone, zone_b: Zone) -> Optional[Connection]:
        for connection in self.connections:
            if ((connection.zone_a == zone_a and
                    connection.zone_b == zone_b) or
                    (connection.zone_a == zone_b and
                        connection.zone_b == zone_a)):
                return connection
        return None
