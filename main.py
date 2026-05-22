import sys
import os
from parser import Parser
from drone import Drone
from algorithm import find_path


def main() -> None:
    show_capacity = "--capacity-info" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--capacity-info"]
    # Récupération sécurisée de la carte passée en argument
    
    map_file = sys.argv[1] if len(sys.argv) > 1 else "maps/easy/01_linear_path.txt"
    
    # map_file = args[0] if len(args) > 0 else "map/easy/01_linear_path.txt"
    if not os.path.exists(map_file):
        print(f"\033[91mError: map not found, usage: make run maps/.../... .txt\033[0m")
        sys.exit(0)

    # Chargement et parsing de la carte
    nb_drones, graph = Parser().parse(map_file)
    path = find_path(graph)

    if not path:
        print("Parsing error: no path found\n")
        sys.exit(1)

    # Initialisation de la flotte de drones
    drones = [Drone(id=i, current_zone=graph.start, path=path) for i in range(1, nb_drones + 1)]
    graph.start.current_drones = nb_drones
    
    initial_stat = [f"L{d.id}-{d.current_zone.name}" for d in drones]
    tick = 0
    print("\n\033[94m ----- Starting simulation -----\033[0m")
    print(f"Turn {tick}: " + " ".join(initial_stat))
    
    # Boucle principale de la simulation
    while graph.end.current_drones < nb_drones:
        tick += 1

        for conn in graph.connections:
            conn.current_links = 0
            
        instructions = []
        # Tri pour éviter les blocages
        drones_order = sorted(drones, key=lambda d: d.step_index, reverse=True)
        
        for drone in drones_order:
            if not drone.arrived:
                if drone.move_to_next(graph):
                    instructions.append(f"D{drone.id}-{drone.current_zone.name}")
                    
        # 2. Sortie brute : Mouvements
        if instructions:
            print(f"Turn {tick}: " + " ".join(instructions))
        if show_capacity:
            print("---Capacity info---")
            for zone in graph.zones.values():
                print(f"Zone {zone.name}: {zone.current_drones}/{zone.max_drone} drones")
            for conn in graph.connections:
                print(f"Connection: {conn.zone_a.name}-{conn.zone_b.name}: {conn.current_links}/{conn.max_link_capacity} used")
            print("-------------------------")

    # 3. Sortie brute : Score final
    print("\n")
    print(f"\033[38;5;214m{tick} turn\033[0m")

    print("\n\033[94m--- Affichage de la carte du réseau ---\033[0m")
    from vizualizer import draw_static_map
    try:
        draw_static_map(graph)
    except KeyboardInterrupt:
        print("\n\033[93m[!] ctrl+c used, visualize interrupted.\033[0m")


if __name__ == "__main__":
    main()