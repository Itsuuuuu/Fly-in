import matplotlib.pyplot as plt

def draw_static_map(graph):
    plt.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Pour dessiner les connexions
    for conn in graph.connections:
        ax.plot([conn.zone_a.x, conn.zone_b.x], 
                [conn.zone_a.y, conn.zone_b.y], 
                color='darkgray', linestyle='-', linewidth=2, zorder=1)
        
    # Dessiner les zones avec leurs couleurs
    for zone_name, zone in graph.zones.items():
        if zone == graph.start:
            zone_color = 'green'
        elif zone == graph.end:
            zone_color = 'red'
        elif zone.color:
            zone_color = zone.color
        else:
            # --- AMÉLIORATION : Couleur automatique selon le Type de Zone ---
            from zone import ZoneType
            if zone.type == ZoneType.BLOCKED:
                zone_color = 'black'
            elif zone.type == ZoneType.RESTRICTED:
                zone_color = 'orange'
            elif zone.type == ZoneType.PRIORITY:
                zone_color = 'purple'
            else:
                zone_color = 'royalblue'
            
        # Dessiner le cercle du hub
        ax.scatter(zone.x, zone.y, color=zone_color, s=500, edgecolors='black', linewidths=1.5, zorder=2)
        
        # Nom de la zone juste au-dessus du cercle
        ax.text(zone.x, zone.y + 0.2, zone.name, fontsize=10, ha='center', va='bottom', weight='bold')

    # Configuration de la fenêtre et des axes
    ax.set_title(f"Fly-in Network Map — {len(graph.zones)} Zones", fontsize=14, weight='bold', pad=15)
    
    # Ajustement automatique des marges pour que tout rentre dans l'écran
    all_x = [z.x for z in graph.zones.values()]
    all_y = [z.y for z in graph.zones.values()]
    ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
    ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
    
    # Masquer la grille et les axes gradués inutiles pour un graphe de réseau
    ax.axis('off')
    
    # Affichage de la fenêtre plot
    plt.tight_layout()
    plt.show()
