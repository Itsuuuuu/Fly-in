from graph import Graph
from zone import Zone, ZoneType
from typing import Tuple
from connection import Connection
import sys


class Parser:
    def parse_zone(self, line: str) -> Zone:
        # Detecter [
        start_data = line.find('[')
        if start_data != -1:
            hub_data = line[:start_data].split()
        else:
            hub_data = line.split()

        # Extraire name, x, y
        name = hub_data[1]
        try:
            x = int(hub_data[2])
        except ValueError:
            print(f"Error parsing: coordonate x can't be negative")
            sys.exit(1)
        try:
            y = int(hub_data[3])
        except ValueError:
            print(f"Error parsing: coordonate x can't be negative")
            sys.exit(1)
       
        # Extraire métadonnées
        dict_meta_data = {}
        if start_data != -1:
            end_data = line.find(']')
            metadata = line[start_data + 1: end_data]
            for data in metadata.split():
                if '=' in data:
                    key, value = data.split('=')
                    if key in dict_meta_data:
                        print(f"Parsing error: duplicate metadata '{key}' found!")
                        sys.exit(1)
                    dict_meta_data[key] = value

        color = dict_meta_data.get('color')

        max_drones_str = dict_meta_data.get('max_drones', '1')
        try:
            max_drones = int(max_drones_str)
        except ValueError:
            print(f"Parsing error: 'max_drones' must be an integer, got '{max_drones_str}'")
            sys.exit(1)
        if max_drones <= 0:
            print(f"Parsing error: 'max_drones' must be a positive integer, got '{max_drones}'")
            sys.exit(1)

        zone_type_str = dict_meta_data.get('zone', 'normal')
        final_type = ZoneType.NORMAL
        try:
            final_type = ZoneType(zone_type_str)
        except ValueError:
            print(f"Parsing error: unknown zone type '{zone_type_str}'")
        zone = (
            Zone(name, x, y, zone_type=final_type,
                 color=color, max_drones=max_drones)
        )
        return zone

    def parse(self, filename: str) -> Tuple[int, Graph]:
        graph = Graph()
        nb = 0
        has_start_hub = False
        has_end_hub = False
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue

                    # Get number of drones
                    elif line.startswith("nb_drones:"):
                        try:
                            nb_drones = line.split()
                            if len(nb_drones) < 2:
                                raise ValueError(
                                    "Missing value after nb_drones:"
                                    )
                            nb = int(nb_drones[1])
                            if nb <= 1:
                                raise ValueError(
                                    f"Number of drones must be > 1, got {nb}"
                                    )
                        except ValueError as e:
                            print(f"Error parsing nb_drones: {e}!")
                            sys.exit(1)

                    # Get the start_hub data
                    elif line.startswith("start_hub:"):
                        if has_start_hub:
                            print("Error second start_hub ignored.")
                            sys.exit(1)
                        else:
                            zone = self.parse_zone(line)
                            graph.start = zone
                            graph.zones[zone.name] = zone
                            has_start_hub = True

                    elif line.startswith("end_hub:"):
                        if has_end_hub:
                            print("Error second end_hub ignored.")
                            sys.exit()
                        else:
                            zone = self.parse_zone(line)
                            zone.max_drone = 9999
                            graph.end = zone
                            graph.zones[zone.name] = zone
                            has_end_hub = True

                    elif line.startswith("hub:"):
                        zone = self.parse_zone(line)
                        graph.zones[zone.name] = zone

                    elif line.startswith("connection:"):
                        start_data = line.find('[')
                        if start_data != -1:
                            hub_data = line[:start_data].split()
                        else:
                            hub_data = line.split()
                        names = hub_data[1].split('-')
                        name_a = names[0]
                        name_b = names[1]

                        if (name_a not in graph.zones or
                                name_b not in graph.zones):
                            print(f"Error: Connection between unknown "
                                  f"zones {name_a}-{name_b}")
                            continue
                        if graph.get_connection(
                                graph.zones[name_a],
                                graph.zones[name_b]) is not None:
                            continue
                        dict_connexion_meta = {}
                        if start_data != -1:
                            end_data = line.find(']')
                            metadata = line[start_data + 1: end_data]
                            for data in metadata.split():
                                if '=' in data:
                                    key, value = data.split('=')
                                    if key in dict_connexion_meta:
                                        print(f"Parsing error: duplicate metadata '{key}' found")
                                        sys.exit(1)
                                    dict_connexion_meta[key] = value
                        capacity_str = dict_connexion_meta.get('max_link_capacity', '1')
                        try:
                            capacity = int(capacity_str)
                        except ValueError:
                            print(f"Parsing error: 'max_link_capacity' must be an integer, got '{capacity_str}'")
                            sys.exit(1)
                        
                        if capacity <= 0:
                            print(f"Parsing error: 'max_link_capacity' must be a positive integer, got'{capacity}'")
                            sys.exit(1)

                        connection = Connection(
                            graph.zones[name_a],
                            graph.zones[name_b],
                            max_link_capacity=capacity
                        )
                        graph.connections.append(connection)
                        # Permet d'ajouter dans le carnet
                        # d'adresse de chaque zone, les zones adjacentes
                        (graph.zones[name_a].neighbors.
                         append(graph.zones[name_b]))
                        (graph.zones[name_b].neighbors.
                         append(graph.zones[name_a]))

        except FileNotFoundError:
            print(f"Error {filename} not found")
            sys.exit(1)
        if graph.start is None or graph.end is None:
            print(f"Parsing error: 'start_hub' or 'end_hub' is missing in the map")
            sys.exit(1)
        return nb, graph
