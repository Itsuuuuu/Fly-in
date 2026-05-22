from zone import Zone


class Connection:
    """Represents a connection between two zones.

       Attributes:
        zone_a: The first zone in the connection.
        zone_b: The second zone in the connection.
        max_link_capacity: The number max of drone
        that can take the connection together.
    """
    def __init__(self, zone_a: Zone, zone_b: Zone, max_link_capacity: int = 1):
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

        self.current_links = 0
