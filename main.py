import sys
from parser import Parser
from drone import Drone
from algorithm import find_path


def main() -> None:
    # Récupération sécurisée de la carte passée en argument
    show_capacity = "--capacity-info" in sys.argv
    map_file = sys.argv[2] if len(sys.argv) > 2 else "maps/easy/01_linear_path.txt"

    # Chargement et parsing de la carte
    nb_drones, graph = Parser().parse(map_file)
    path = find_path(graph)

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
            if show_capacity:
                print("")
        # 2. Sortie brute : Mouvements
        if instructions:
            print(f"Turn {tick}: " + " ".join(instructions))
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
