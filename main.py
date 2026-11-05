import pygame
import math
import heapq
import random

# ==========================================================
# 1. INITIALIZATION & ENGINE SETTINGS
# ==========================================================
pygame.init()

WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MULTIPLAYER AI ARENA // GRAVITATIONAL CORE")
clock = pygame.time.Clock()

# Palettes
BG = (6, 8, 16)
GRID_LINE = (22, 28, 48)
TILE_A = (16, 20, 36)
TILE_B = (24, 29, 50)

WHITE = (248, 250, 252)
MUTED = (148, 163, 184)
GOLD = (250, 204, 21)
CYAN = (56, 189, 248)
PURPLE = (168, 85, 247)
EMERALD = (52, 211, 153)
CORAL = (251, 113, 133)
RED = (239, 68, 68)
ELECTRIC_BLUE = (38, 222, 255)

PLAYER_SCHEMES = [
    {"default_name": "AGENT AZURE", "base": CYAN, "keys_label": "Arrows / Touch"},
    {"default_name": "AGENT VIOLET", "base": PURPLE, "keys_label": "W A S D"},
    {"default_name": "AGENT EMERALD", "base": EMERALD, "keys_label": "I J K L"},
    {"default_name": "AGENT CORAL", "base": CORAL, "keys_label": "T F G H"},
]

# Style 2: Cyber Terminal / Hacker Monospace Font Loader
def get_font(size, bold=False):
    for fn in ("consolas", "lucidaconsole", "ocraextended", "couriernew"):
        p = pygame.font.match_font(fn, bold=bold)
        if p:
            return pygame.font.Font(p, size)
    return pygame.font.Font(None, size)

# Classic / Professional Display Font Loader for Arena Title
def get_display_font(size, bold=True):
    for fn in ("copperplategothicbold", "bankgothic", "agencyfb", "impact", "bahnschrift", "consolas", "arial"):
        p = pygame.font.match_font(fn, bold=bold)
        if p:
            return pygame.font.Font(p, size)
    return pygame.font.Font(None, size)

FONT_HERO = get_font(32, True)
FONT_ARENA_TITLE_PC = get_display_font(34, True)
FONT_ARENA_TITLE_PHONE = get_display_font(20, True)
FONT_TAGLINE_PC = get_font(12, True)
FONT_TAGLINE_PHONE = get_font(9, True)

FONT_BRAND_MAIN = get_font(26, True)
FONT_BRAND_ACCENT = get_font(26, True)
FONT_TITLE = get_font(20, True)
FONT_SUB = get_font(15, True)
FONT_BODY = get_font(12, True)
FONT_TINY = get_font(11, True)

# ==========================================================
# 2. ARENA MAP, LEVEL OBSTACLES & DYNAMIC CAMERA
# ==========================================================
COLS, ROWS = 21, 17
TILE_W, TILE_H = 60, 30
WALL_H = 28
GRAVITY_CENTER = (COLS // 2, ROWS // 2)

WALLS = set()

def generate_walls(level=1):
    """
    Creates increasingly dense, intricate obstacle maps for each of the 5 levels:
    - Level 1: Light tactical obstacles (open training ground).
    - Level 2: Symmetrical cyber corridor partitions.
    - Level 3: Dense chokepoints & quadrant barricades.
    - Level 4: Heavy labyrinthine circuit maze with tight escape lanes.
    - Level 5: Maximum density fortress labyrinth with narrow chokepoints.
    """
    WALLS.clear()
    gc_c, gc_r = GRAVITY_CENTER

    for r in range(ROWS):
        for c in range(COLS):
            # Safe zone around central Gravitational Core
            if abs(c - gc_c) <= 1 and abs(r - gc_r) <= 1:
                continue
            # Safe zone around the 4 player spawn corners
            if (c <= 2 and r <= 2) or (c >= COLS - 3 and r <= 2) or                (c <= 2 and r >= ROWS - 3) or (c >= COLS - 3 and r >= ROWS - 3):
                continue

            # Level 1: Light obstacles (4 perimeter pillars + small crossbars)
            if level == 1:
                if (c in (5, COLS - 6) and r in (4, ROWS - 5)):
                    WALLS.add((c, r))
                elif (c in (4, COLS - 5) and 4 <= r <= 5):
                    WALLS.add((c, r))
                elif (r in (3, ROWS - 4) and 8 <= c <= COLS - 9):
                    WALLS.add((c, r))

            # Level 2: Symmetrical cyber corridor partitions
            elif level == 2:
                if (c in (4, COLS - 5) and 3 <= r <= 6) or (c in (4, COLS - 5) and ROWS - 7 <= r <= ROWS - 4):
                    WALLS.add((c, r))
                elif (r in (3, ROWS - 4) and 7 <= c <= COLS - 8):
                    WALLS.add((c, r))
                elif (c in (7, COLS - 8) and 6 <= r <= ROWS - 7 and r != gc_r):
                    WALLS.add((c, r))

            # Level 3: Dense chokepoints & quadrant barricades
            elif level == 3:
                if (c in (4, COLS - 5) and 2 <= r <= 6) or (c in (4, COLS - 5) and ROWS - 7 <= r <= ROWS - 3):
                    WALLS.add((c, r))
                elif (r in (3, ROWS - 4) and 6 <= c <= COLS - 7):
                    WALLS.add((c, r))
                elif (c in (6, COLS - 7) and 5 <= r <= ROWS - 6 and r != gc_r):
                    WALLS.add((c, r))
                elif (r in (6, ROWS - 7) and (c in (8, COLS - 9))):
                    WALLS.add((c, r))

            # Level 4: Heavy labyrinthine circuit maze
            elif level == 4:
                if (c in (3, COLS - 4) and 2 <= r <= 6) or (c in (3, COLS - 4) and ROWS - 7 <= r <= ROWS - 3):
                    WALLS.add((c, r))
                if (r in (2, ROWS - 3) and 6 <= c <= COLS - 7 and c not in (9, 10, 11)):
                    WALLS.add((c, r))
                if (r in (4, ROWS - 5) and 7 <= c <= COLS - 8):
                    WALLS.add((c, r))
                if (c in (6, 8, COLS - 9, COLS - 7) and 5 <= r <= ROWS - 6 and r not in (gc_r, gc_r - 2, gc_r + 2)):
                    WALLS.add((c, r))
                if (r in (6, ROWS - 7) and c in (5, COLS - 6)):
                    WALLS.add((c, r))

            # Level 5: Maximum density apex fortress labyrinth
            else:
                if (c in (3, COLS - 4) and 2 <= r <= 7) or (c in (3, COLS - 4) and ROWS - 8 <= r <= ROWS - 3):
                    WALLS.add((c, r))
                if (r in (2, ROWS - 3) and 5 <= c <= COLS - 6 and c not in (8, 12)):
                    WALLS.add((c, r))
                if (c in (5, COLS - 6) and 4 <= r <= ROWS - 5 and r not in (gc_r - 1, gc_r + 1)):
                    WALLS.add((c, r))
                if (r in (4, ROWS - 5) and 6 <= c <= COLS - 7 and c != gc_c):
                    WALLS.add((c, r))
                if (c in (7, COLS - 8) and 6 <= r <= ROWS - 7 and r != gc_r):
                    WALLS.add((c, r))
                if (r in (6, ROWS - 7) and c in (9, COLS - 10)):
                    WALLS.add((c, r))

generate_walls(1)

cam_x, cam_y = 0.0, 0.0
screen_shake = 0.0
step_ripples = []
touch_controls_enabled = True

def iso_project(c, r):
    x = (c - r) * (TILE_W // 2)
    y = (c + r) * (TILE_H // 2)
    return x, y

def to_screen(iso_x, iso_y):
    shake_ox = random.uniform(-screen_shake, screen_shake) if screen_shake > 0 else 0
    shake_oy = random.uniform(-screen_shake, screen_shake) if screen_shake > 0 else 0
    sx = (WIDTH // 2 - 130) + (iso_x - cam_x) + shake_ox
    sy = (HEIGHT // 2) + (iso_y - cam_y) + shake_oy
    return round(sx), round(sy)

def screen_to_grid(mx, my):
    sx = mx - (WIDTH // 2 - 130) + cam_x
    sy = my - (HEIGHT // 2) + cam_y
    c = (sx / (TILE_W / 2) + sy / (TILE_H / 2)) / 2.0
    r = (sy / (TILE_H / 2) - sx / (TILE_W / 2)) / 2.0
    return round(c), round(r)

def tile_poly(c, r, offset_y=0):
    ix, iy = iso_project(c, r)
    top = to_screen(ix, iy - TILE_H // 2 + offset_y)
    right = to_screen(ix + TILE_W // 2, iy + offset_y)
    bottom = to_screen(ix, iy + TILE_H // 2 + offset_y)
    left = to_screen(ix - TILE_W // 2, iy + offset_y)
    return [top, right, bottom, left]

# ==========================================================
# 3. ALGORITHMS: A* SEARCH (MIN-HEAP) & DFS WANDER
# ==========================================================
def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def a_star(start, target):
    if start == target:
        return []
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start, target), 0, start))
    came_from = {}
    g_score = {start: 0}
    visited = set()
    counter = 0

    while open_heap:
        _, _, current = heapq.heappop(open_heap)
        if current in visited:
            continue
        visited.add(current)

        if current == target:
            path = []
            curr = target
            while curr != start:
                path.append(curr)
                curr = came_from[curr]
            path.reverse()
            return path

        for dc, dr in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nbr = (current[0] + dc, current[1] + dr)
            if not (0 <= nbr[0] < COLS and 0 <= nbr[1] < ROWS):
                continue
            if nbr in WALLS:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(nbr, float("inf")):
                came_from[nbr] = current
                g_score[nbr] = tentative_g
                f_score = tentative_g + heuristic(nbr, target)
                counter += 1
                heapq.heappush(open_heap, (f_score, counter, nbr))
    return []

def dfs_wander(start, depth=5):
    stack = [(start, [start])]
    visited = {start}
    furthest_path = [start]

    while stack:
        curr, path = stack.pop()
        if len(path) > len(furthest_path):
            furthest_path = path
        if len(path) >= depth:
            continue

        nbrs = [(curr[0] + dc, curr[1] + dr) for dc, dr in ((0, -1), (0, 1), (-1, 0), (1, 0))]
        random.shuffle(nbrs)
        for nbr in nbrs:
            if 0 <= nbr[0] < COLS and 0 <= nbr[1] < ROWS and nbr not in WALLS and nbr not in visited:
                visited.add(nbr)
                stack.append((nbr, path + [nbr]))
    return furthest_path[1:] if len(furthest_path) > 1 else []

# ==========================================================
# 4. GAME OBJECTS & RELIABLE MOVEMENT
# ==========================================================
class Player:
    def __init__(self, p_id, start_tile, keymap, scheme, custom_name=""):
        self.p_id = p_id
        self.grid_c, self.grid_r = start_tile
        self.x, self.y = iso_project(self.grid_c, self.grid_r)
        self.keymap = keymap
        self.color = scheme["base"]
        self.name = custom_name.strip() if custom_name.strip() else scheme["default_name"]
        self.carrying = 0
        self.score = 0
        self.trail = []
        self.is_caught_timer = 0
        self.speed_boost_timer = 0.0

    def move(self, dc, dr):
        """
        Crisp, reliable grid corridor movement from Document 2:
        UP: (0, -1)   | DOWN: (0, 1)
        LEFT: (-1, 0) | RIGHT: (1, 0)
        Moves directly along tile corridors without diagonal drift!
        """
        global step_ripples
        step = 2 if self.speed_boost_timer > 0 else 1
        nc = self.grid_c + dc * step
        nr = self.grid_r + dr * step
        if step == 2 and (nc, nr) in WALLS:
            nc = self.grid_c + dc
            nr = self.grid_r + dr

        if 0 <= nc < COLS and 0 <= nr < ROWS and (nc, nr) not in WALLS:
            self.grid_c, self.grid_r = nc, nr
            step_ripples.append([self.grid_c, self.grid_r, 1.0, self.color])

    def update(self, dt):
        tx, ty = iso_project(self.grid_c, self.grid_r)
        lerp_speed = 22.0 if self.speed_boost_timer > 0 else 14.0
        self.x += (tx - self.x) * min(1.0, lerp_speed * dt)
        self.y += (ty - self.y) * min(1.0, lerp_speed * dt)

        if abs(tx - self.x) > 1 or abs(ty - self.y) > 1 or self.carrying > 0 or self.speed_boost_timer > 0:
            if random.random() < 0.5:
                self.trail.append([self.x + random.uniform(-3, 3), self.y + random.uniform(-3, 3), 1.0])

        for p in self.trail:
            p[2] -= dt * (1.8 if self.speed_boost_timer > 0 else 2.5)
        self.trail = [p for p in self.trail if p[2] > 0]
        
        if self.is_caught_timer > 0:
            self.is_caught_timer -= dt
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt

class NPC:
    def __init__(self, start_tile, step_delay=580, npc_id=0):
        self.npc_id = npc_id
        self.grid_c, self.grid_r = start_tile
        self.x, self.y = iso_project(self.grid_c, self.grid_r)
        self.step_delay = step_delay
        self.last_move = 0
        self.target_path = []
        self.projected_path = []
        self.state = "DFS PATROL"
        self.trail = []
        
        self.stun_timer = 0.0
        self.charge_timer = 0.0
        self.is_charging = False
        self.target_player = None

    def stun(self, duration=3.5):
        self.stun_timer = duration
        self.is_charging = False
        self.charge_timer = 0.0

    def update_ai(self, players, current_time, dt):
        global step_ripples
        if self.stun_timer > 0:
            self.stun_timer -= dt
            self.state = f"EMP STUNNED ({self.stun_timer:.1f}s)"
            return

        active = [p for p in players]
        if not active:
            return

        def eval_threat(p):
            dist = heuristic((self.grid_c, self.grid_r), (p.grid_c, p.grid_r))
            return (-p.carrying * 8 + dist)

        sorted_targets = sorted(active, key=eval_threat)
        chosen = sorted_targets[0]
        dist_to_chosen = heuristic((self.grid_c, self.grid_r), (chosen.grid_c, chosen.grid_r))

        if (chosen.carrying > 0 or dist_to_chosen <= 6.5) and not self.is_charging:
            if random.random() < 0.25 and dist_to_chosen >= 3.0:
                self.is_charging = True
                self.charge_timer = 1.4
                self.target_player = chosen

        if self.is_charging:
            self.charge_timer -= dt
            self.state = f"TELEGRAPH CHARGE ({self.charge_timer:.1f}s)"
            self.projected_path = a_star((self.grid_c, self.grid_r), (self.target_player.grid_c, self.target_player.grid_r))
            if self.charge_timer <= 0:
                self.is_charging = False
                if self.projected_path:
                    steps = min(2, len(self.projected_path))
                    self.grid_c, self.grid_r = self.projected_path[steps - 1]
                    step_ripples.append([self.grid_c, self.grid_r, 1.2, RED])
                    self.last_move = current_time + 180
            return

        if current_time - self.last_move < self.step_delay:
            return
        self.last_move = current_time

        if chosen.carrying > 0 or dist_to_chosen <= 7.0:
            self.state = f"A* PURSUIT >> {chosen.name.split()[0]}"
            path = a_star((self.grid_c, self.grid_r), (chosen.grid_c, chosen.grid_r))
            self.projected_path = path[:4]
            if path:
                self.grid_c, self.grid_r = path[0]
                step_ripples.append([self.grid_c, self.grid_r, 1.0, RED])
        else:
            self.state = "DFS EXPLORATION"
            self.projected_path = []
            if not self.target_path:
                self.target_path = dfs_wander((self.grid_c, self.grid_r), depth=5)
            if self.target_path:
                self.grid_c, self.grid_r = self.target_path.pop(0)
                step_ripples.append([self.grid_c, self.grid_r, 0.8, (200, 50, 50)])

    def update_motion(self, dt):
        tx, ty = iso_project(self.grid_c, self.grid_r)
        self.x += (tx - self.x) * min(1.0, 9.0 * dt)
        self.y += (ty - self.y) * min(1.0, 9.0 * dt)

        if random.random() < 0.45:
            self.trail.append([self.x, self.y, 1.0])
        for p in self.trail:
            p[2] -= dt * 2.8
        self.trail = [p for p in self.trail if p[2] > 0]

class EnergyCore:
    def __init__(self, pos):
        self.grid_c, self.grid_r = pos
        self.pulse_offset = random.uniform(0, math.pi * 2)

class PowerUp:
    def __init__(self, pos, kind="BOOTS"):
        self.grid_c, self.grid_r = pos
        self.kind = kind
        self.pulse = random.uniform(0, math.pi * 2)

class Shockwave:
    def __init__(self, center_tile):
        self.c, self.r = center_tile
        self.radius = 0.0
        self.max_radius = 480.0
        self.alive = True

    def update(self, dt):
        self.radius += 520.0 * dt
        if self.radius >= self.max_radius:
            self.alive = False

# ==========================================================
# 5. RENDERING PIPELINE & RESTORED ROBOT MODELS FROM DOC 2
# ==========================================================
def draw_player_entity(p):
    """
    Nanotech Hover Disc & Satellite Orbits (from video_1.mp4):
    - Levitating layered anti-grav disc chassis with smooth vertical bob
    - Concentric rotating magnetic rings
    - Orbiting satellite nanotech motes that accelerate during speed boost
    - Dynamic energy core chamber that visibly holds collected quantum cores in a spiral orbit!
    """
    sx, sy = to_screen(p.x, p.y)
    t = pygame.time.get_ticks() * 0.001

    # Trail Particles
    for trail_pt in p.trail:
        tx, ty = to_screen(trail_pt[0], trail_pt[1])
        alpha = int(trail_pt[2] * 150)
        t_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        color = ELECTRIC_BLUE if p.speed_boost_timer > 0 else p.color
        pygame.draw.circle(t_surf, (*color, alpha), (5, 5), 3)
        screen.blit(t_surf, (tx - 5, ty - 5))

    # Anti-Gravity Ground Projection & Shadow
    shadow_pulse = 0.7 + 0.3 * math.sin(t * 3.5)
    shadow_surf = pygame.Surface((38, 20), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (8, 14, 26, int(160 * shadow_pulse)), (0, 0, 38, 20))
    pygame.draw.ellipse(shadow_surf, (*p.color, int(60 * shadow_pulse)), (4, 2, 30, 16), 1)
    screen.blit(shadow_surf, (sx - 19, sy - 9))

    # Floating Elevation Bob
    float_y = sy - 22 + math.sin(t * 4.0 + p.p_id * 1.2) * 4.0

    # Main Color Palette
    active_col = WHITE if p.is_caught_timer > 0 else (ELECTRIC_BLUE if p.speed_boost_timer > 0 else p.color)
    glow_col = tuple(min(255, int(c * 0.4)) for c in active_col)

    # 1. Base Magnetic Hover Disc (Layered 3D Ellipses)
    pygame.draw.ellipse(screen, (16, 24, 40), (sx - 20, int(float_y + 4), 40, 16))
    pygame.draw.ellipse(screen, (28, 42, 68), (sx - 20, int(float_y), 40, 16))
    pygame.draw.ellipse(screen, glow_col, (sx - 20, int(float_y), 40, 16), 2)
    pygame.draw.ellipse(screen, active_col, (sx - 15, int(float_y + 3), 30, 10), 1)

    # 2. Central Quantum Energy Reactor / Core Sphere
    core_bob = math.sin(t * 6.0 + p.p_id) * 2.0
    core_cy = float_y - 8 + core_bob
    
    # Outer reactor bloom
    core_glow = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.circle(core_glow, (*active_col, 50), (18, 18), 16)
    pygame.draw.circle(core_glow, (*active_col, 120), (18, 18), 9)
    pygame.draw.circle(core_glow, (255, 255, 255, 230), (18, 18), 4)
    screen.blit(core_glow, (sx - 18, int(core_cy - 18)))

    # 3. Rotating Satellite Nano-Rings & Orbits
    orbit_speed = 6.0 if p.speed_boost_timer > 0 else 3.2
    
    # Ring A (Tilted clockwise orbit)
    ring_rad_x, ring_rad_y = 26, 12
    ring_ang = t * orbit_speed
    sat1_x = sx + math.cos(ring_ang) * ring_rad_x
    sat1_y = core_cy + math.sin(ring_ang) * ring_rad_y
    sat2_x = sx + math.cos(ring_ang + math.pi) * ring_rad_x
    sat2_y = core_cy + math.sin(ring_ang + math.pi) * ring_rad_y

    # Draw orbit track ring
    track_surf = pygame.Surface((56, 28), pygame.SRCALPHA)
    pygame.draw.ellipse(track_surf, (*active_col, 75), (0, 0, 56, 28), 1)
    screen.blit(track_surf, (sx - 28, int(core_cy - 14)))

    # Draw satellite nodes
    pygame.draw.circle(screen, active_col, (int(sat1_x), int(sat1_y)), 3)
    pygame.draw.circle(screen, WHITE, (int(sat1_x), int(sat1_y)), 1)
    pygame.draw.circle(screen, active_col, (int(sat2_x), int(sat2_y)), 3)
    pygame.draw.circle(screen, WHITE, (int(sat2_x), int(sat2_y)), 1)

    # 4. Carrying Cores Indicator (Floating mini shards orbiting in a spiral circle around player)
    if p.carrying > 0:
        for idx in range(min(8, p.carrying)):
            c_ang = t * 4.5 + (idx * (math.pi * 2.0 / min(8, p.carrying)))
            cx = sx + math.cos(c_ang) * 18
            cy = core_cy - 14 + math.sin(c_ang) * 8
            # Floating micro energy crystal
            pygame.draw.polygon(screen, GOLD, [(cx, cy - 4), (cx + 4, cy), (cx, cy + 4), (cx - 4, cy)])
            pygame.draw.circle(screen, WHITE, (int(cx), int(cy)), 1)

    # Overhead Telemetry Label
    status_tag = f" [{p.carrying}]" + (" (SPEED!)" if p.speed_boost_timer > 0 else "")
    lbl = FONT_TINY.render(p.name.split()[0] + status_tag, True, active_col)
    lbl_rect = lbl.get_rect(center=(sx, int(float_y - 28)))
    screen.blit(lbl, lbl_rect)


def draw_npc_entity(npc):
    """
    Fractured Nanotech Monolith / Crimson Leviathan Prism (from video_1.mp4):
    - Levitating multi-tier geometric crimson prism
    - Detached orbiting shard shields that expand violently during Telegraph Charge
    - Malevolent glowing cyclops sensory eye with laser tracking
    - Violent electric arc discharge when EMP stunned
    """
    sx, sy = to_screen(npc.x, npc.y)
    t = pygame.time.get_ticks() * 0.001

    # Trail
    for pt in npc.trail:
        tx, ty = to_screen(pt[0], pt[1])
        alpha = int(pt[2] * 150)
        t_surf = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(t_surf, (239, 68, 68, alpha), (6, 6), 4)
        screen.blit(t_surf, (tx - 6, ty - 6))

    # Base Color Scheme based on state
    if npc.stun_timer > 0:
        aura_col = ELECTRIC_BLUE
        core_col = (100, 230, 255)
    elif npc.is_charging:
        aura_col = GOLD
        core_col = (255, 230, 100)
    else:
        aura_col = RED
        core_col = (255, 60, 90)

    # Menacing Ground Hazard Aperture
    ap_pulse = 0.6 + 0.4 * math.sin(t * 5.0)
    ap_rad_x = int(24 + (10 if npc.is_charging else 0) * ap_pulse)
    ap_surf = pygame.Surface((ap_rad_x * 2 + 4, 24), pygame.SRCALPHA)
    pygame.draw.ellipse(ap_surf, (35, 10, 20, 150), (2, 2, ap_rad_x * 2, 20))
    pygame.draw.ellipse(ap_surf, (*aura_col, int(90 * ap_pulse)), (2, 2, ap_rad_x * 2, 20), 2)
    screen.blit(ap_surf, (sx - ap_rad_x - 2, sy - 10))

    # Floating Elevation
    float_y = sy - 28 + math.sin(t * 3.5) * 5.0

    # 1. Floating Nanotech Shard Shield (Fragments that expand during charge)
    shard_spread = 28 if npc.is_charging else (32 if npc.stun_timer > 0 else 18)
    shard_spin_speed = 8.0 if npc.is_charging else (1.2 if npc.stun_timer > 0 else 2.5)
    
    for s_idx in range(4):
        ang = t * shard_spin_speed + s_idx * (math.pi / 2.0)
        sh_x = sx + math.cos(ang) * shard_spread
        sh_y = float_y + math.sin(ang) * (shard_spread * 0.45)
        
        # Diamond shard polygon
        s_pts = [
            (sh_x, sh_y - 6),
            (sh_x + 4, sh_y),
            (sh_x, sh_y + 6),
            (sh_x - 4, sh_y),
        ]
        pygame.draw.polygon(screen, (25, 8, 14), s_pts)
        pygame.draw.polygon(screen, aura_col, s_pts, 2)
        pygame.draw.circle(screen, WHITE, (int(sh_x), int(sh_y)), 1)

    # 2. Central Floating Crimson Monolith / Prism Core
    # Inverted dual tetrahedron
    top_p = (sx, float_y - 20)
    mid_r = (sx + 14, float_y - 4)
    bot_p = (sx, float_y + 12)
    mid_l = (sx - 14, float_y - 4)
    center_p = (sx, float_y - 2)

    # Facet shading for 3D crystalline look
    pygame.draw.polygon(screen, (38, 10, 20), [top_p, mid_r, center_p])
    pygame.draw.polygon(screen, (52, 14, 28), [top_p, center_p, mid_l])
    pygame.draw.polygon(screen, (28, 8, 16), [center_p, mid_r, bot_p])
    pygame.draw.polygon(screen, (42, 11, 22), [mid_l, center_p, bot_p])

    # Sharp perimeter edges
    pygame.draw.lines(screen, aura_col, True, [top_p, mid_r, bot_p, mid_l], 2)
    pygame.draw.line(screen, (255, 180, 200), top_p, center_p, 1)
    pygame.draw.line(screen, aura_col, center_p, bot_p, 1)

    # 3. Cyclops Sensory Eye (Center Eye that tracks player)
    eye_surf = pygame.Surface((28, 28), pygame.SRCALPHA)
    pygame.draw.circle(eye_surf, (*core_col, 80), (14, 14), 12)
    pygame.draw.circle(eye_surf, core_col, (14, 14), 5)
    pygame.draw.circle(eye_surf, WHITE, (14, 14), 2)
    screen.blit(eye_surf, (sx - 14, int(float_y - 16)))

    # 4. EMP Stun Disruptor Sparks
    if npc.stun_timer > 0:
        for _ in range(4):
            ox1 = random.randint(-18, 18)
            oy1 = random.randint(-24, 8)
            ox2 = ox1 + random.randint(-8, 8)
            oy2 = oy1 + random.randint(-8, 8)
            pygame.draw.line(screen, ELECTRIC_BLUE, (sx + ox1, float_y + oy1), (sx + ox2, float_y + oy2), 2)

    # Status Tag
    tag = FONT_TINY.render(npc.state, True, aura_col)
    screen.blit(tag, tag.get_rect(center=(sx, int(float_y - 32))))


def draw_floating_platform_underlayer(t, total_dep, target_quota):
    c_right = to_screen(*iso_project(COLS - 1, 0))
    c_bottom = to_screen(*iso_project(COLS - 1, ROWS - 1))
    c_left = to_screen(*iso_project(0, ROWS - 1))
    
    CHASM_DEPTH = 36
    drop_right = (c_right[0], c_right[1] + CHASM_DEPTH)
    drop_bottom = (c_bottom[0], c_bottom[1] + CHASM_DEPTH)
    drop_left = (c_left[0], c_left[1] + CHASM_DEPTH)

    ratio = min(1.0, total_dep / target_quota)
    accent_glow = (int(56 + 194 * ratio), int(189 + 15 * ratio), int(248 - 227 * ratio))
    
    shadow_surf = pygame.Surface((1000, 140), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (*accent_glow, 32), (0, 0, 1000, 130))
    screen.blit(shadow_surf, (drop_bottom[0] - 500, drop_bottom[1] - 30))

    pygame.draw.polygon(screen, (12, 15, 26), [c_left, c_bottom, drop_bottom, drop_left])
    pygame.draw.polygon(screen, (18, 22, 38), [c_bottom, c_right, drop_right, drop_bottom])
    pygame.draw.line(screen, (40, 50, 75), c_bottom, drop_bottom, 2)

def draw_floor_with_gravity_ripples(t, total_dep, target_quota):
    ripple_phase = (t * 2.4)
    active_ripples_dict = {(c, r): (intensity, col) for c, r, intensity, col in step_ripples}

    for r in range(ROWS):
        for c in range(COLS):
            poly = tile_poly(c, r)
            base_col = TILE_A if (r + c) % 2 == 0 else TILE_B
            dist_to_center = math.sqrt((c - GRAVITY_CENTER[0]) ** 2 + (r - GRAVITY_CENTER[1]) ** 2)
            wave = math.sin(dist_to_center * 0.9 - ripple_phase)
            line_col = list(GRID_LINE)
            fill_col = list(base_col)

            if wave > 0.65:
                pulse_amt = int((wave - 0.65) * 60)
                line_col[1] = min(255, line_col[1] + pulse_amt)
                line_col[2] = min(255, line_col[2] + pulse_amt)
            
            if (c, r) in active_ripples_dict:
                inten, r_col = active_ripples_dict[(c, r)]
                blend_amt = min(1.0, inten)
                fill_col = [int(fill_col[i] * (1 - blend_amt) + r_col[i] * 0.45 * blend_amt) for i in range(3)]
                line_col = [int(col_val * 0.8) for col_val in r_col]

            pygame.draw.polygon(screen, fill_col, poly)
            pygame.draw.polygon(screen, line_col, poly, 1)

def draw_animated_perimeter_and_pylons(t, total_dep, target_quota):
    corners = [to_screen(*iso_project(0, 0)), to_screen(*iso_project(COLS - 1, 0)),
               to_screen(*iso_project(COLS - 1, ROWS - 1)), to_screen(*iso_project(0, ROWS - 1))]
    ratio = min(1.0, total_dep / target_quota)
    laser_color = (int(56 + 194 * ratio), int(189 + 15 * ratio), int(248 - 227 * ratio))
    
    for i in range(4):
        p1, p2 = corners[i], corners[(i + 1) % 4]
        pygame.draw.line(screen, laser_color, (p1[0], p1[1] - 12), (p2[0], p2[1] - 12), 2)
        cur_phase = (t * 0.8 + i * 0.25) % 1.0
        cur_x = int(p1[0] + (p2[0] - p1[0]) * cur_phase)
        cur_y = int(p1[1] + (p2[1] - p1[1]) * cur_phase)
        pygame.draw.circle(screen, laser_color, (cur_x, cur_y - 12), 3)

def draw_wall(c, r, t):
    float_bob = math.sin(t * 2.5 + (c * 0.7 + r * 0.5)) * 3.5
    ix, iy = iso_project(c, r)
    top_p0 = to_screen(ix, iy - TILE_H // 2 + float_bob)
    top_p1 = to_screen(ix + TILE_W // 2, iy + float_bob)
    top_p2 = to_screen(ix, iy + TILE_H // 2 + float_bob)
    top_p3 = to_screen(ix - TILE_W // 2, iy + float_bob)

    ground_p1 = to_screen(ix + TILE_W // 2, iy)
    ground_p2 = to_screen(ix, iy + TILE_H // 2)
    ground_p3 = to_screen(ix - TILE_W // 2, iy)
    b1 = (ground_p1[0], ground_p1[1] + WALL_H)
    b2 = (ground_p2[0], ground_p2[1] + WALL_H)
    b3 = (ground_p3[0], ground_p3[1] + WALL_H)

    pygame.draw.polygon(screen, (22, 26, 42), [top_p3, top_p2, b2, b3])
    pygame.draw.polygon(screen, (32, 38, 62), [top_p2, top_p1, b1, b2])
    pygame.draw.polygon(screen, (46, 54, 86), [top_p0, top_p1, top_p2, top_p3])
    pygame.draw.polygon(screen, (75, 95, 145), [top_p0, top_p1, top_p2, top_p3], 1)
    pygame.draw.line(screen, (70, 180, 255), (top_p2[0], top_p2[1] + 4), (b2[0], b2[1] - 6), 2)

def draw_danger_trajectory(path):
    for c, r in path:
        poly = tile_poly(c, r)
        pygame.draw.polygon(screen, (239, 68, 68, 40), poly)
        pygame.draw.polygon(screen, (255, 100, 100), poly, 1)


# In-flight core absorption particles
core_absorb_particles = []

def trigger_core_deposit_fx(start_iso_x, start_iso_y, count):
    start_sx, start_sy = to_screen(start_iso_x, start_iso_y)
    c, r = GRAVITY_CENTER
    target_x, target_y = to_screen(*iso_project(c, r))
    for i in range(min(18, count * 4)):
        ang = random.uniform(0, math.pi * 2)
        dist = random.uniform(15, 45)
        core_absorb_particles.append({
            'x': start_sx + math.cos(ang) * dist,
            'y': start_sy + math.sin(ang) * dist,
            'tx': target_x,
            'ty': target_y - 35,
            'progress': random.uniform(0.0, 0.15),
            'speed': random.uniform(1.8, 3.2),
            'color': GOLD if i % 2 == 0 else CYAN
        })

def update_core_absorb_particles(dt):
    global core_absorb_particles
    for p in core_absorb_particles:
        p['progress'] += p['speed'] * dt
        # Spiral curved interpolation towards center
        p['x'] += (p['tx'] - p['x']) * min(1.0, 6.0 * dt) + math.sin(p['progress'] * 12.0) * 3.0
        p['y'] += (p['ty'] - p['y']) * min(1.0, 6.0 * dt)
    core_absorb_particles = [p for p in core_absorb_particles if p['progress'] < 1.0]

def draw_core_absorb_particles():
    for p in core_absorb_particles:
        alpha = int(255 * (1.0 - p['progress']))
        t_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(t_surf, (*p['color'], alpha), (4, 4), 3)
        screen.blit(t_surf, (int(p['x'] - 4), int(p['y'] - 4)))


def draw_core_sparkles(cx, cy, t):
    """
    Advanced Ethereal Sparkle & Celestial Starlight Particle System:
    - Floating luminous embers & starlight motes with natural vertical drift
    - Multi-layer soft radial glow halos (golden & celestial cyan)
    - Shimmering micro-diamond flares that twinkle organically without clunky pixel crosses
    """
    num_sparkles = 24
    for i in range(num_sparkles):
        # Multi-harmonic floating orbit
        speed = 0.8 + (i % 4) * 0.35
        ang = t * speed + i * (math.pi * 2.0 / num_sparkles)
        rad_x = 22 + (i * 9) % 48
        rad_y = 12 + (i * 6) % 24

        # Continuous gentle upward drift with sinusoidal wave
        drift_y = math.sin(t * 2.8 + i * 1.4) * 6.0 - ((t * 14.0 + i * 18.0) % 32.0)
        
        sp_x = int(cx + math.cos(ang) * rad_x)
        sp_y = int(cy + math.sin(ang) * rad_y + drift_y)

        # Smooth organic sine-wave life cycle
        twinkle = 0.5 + 0.5 * math.sin(t * 5.2 + i * 1.6)
        alpha = int(70 + 185 * twinkle)
        color = (250, 215, 70) if (i % 2 == 0) else (180, 235, 255)

        # Soft radial bloom halo
        r_outer = 4 if (i % 3 == 0) else 3
        halo_surf = pygame.Surface((r_outer * 4 + 4, r_outer * 4 + 4), pygame.SRCALPHA)
        pygame.draw.circle(halo_surf, (*color, max(0, alpha // 4)), (r_outer * 2, r_outer * 2), r_outer * 2)
        pygame.draw.circle(halo_surf, (*color, alpha), (r_outer * 2, r_outer * 2), r_outer)
        pygame.draw.circle(halo_surf, (255, 255, 255, alpha), (r_outer * 2, r_outer * 2), 1)
        screen.blit(halo_surf, (sp_x - r_outer * 2, sp_y - r_outer * 2))

        # Delicate optical diamond flare on brightest stars (soft, anti-aliased 1px glints)
        if twinkle > 0.62 and (i % 2 == 0):
            glint_len = int(3 + twinkle * 4)
            glint_alpha = int(alpha * 0.75)
            glint_surf = pygame.Surface((glint_len * 2 + 2, glint_len * 2 + 2), pygame.SRCALPHA)
            pygame.draw.line(glint_surf, (255, 255, 255, glint_alpha), (glint_len, 0), (glint_len, glint_len * 2), 1)
            pygame.draw.line(glint_surf, (255, 255, 255, glint_alpha), (0, glint_len), (glint_len * 2, glint_len), 1)
            screen.blit(glint_surf, (sp_x - glint_len, sp_y - glint_len))

def draw_gravity_core(total_collected, target_quota):
    c, r = GRAVITY_CENTER
    sx, sy = to_screen(*iso_project(c, r))
    t = pygame.time.get_ticks() * 0.001

    ratio = min(1.0, total_collected / max(1, target_quota))
    is_fully_charged = (total_collected >= target_quota)

    # Dynamic morphing palette: shifts from deep cyber cyan to transcendent celestial solar gold & white
    core_r = int(56 + (250 - 56) * ratio)
    core_g = int(189 + (215 - 189) * ratio)
    core_b = int(248 + (50 - 248) * ratio)
    active_color = (core_r, core_g, core_b)

    # Elevation: Lifts higher into the air with EVERY orb delivered!
    elevation_per_orb = 2.6
    base_elevation = int(22 + total_collected * elevation_per_orb)
    if is_fully_charged:
        base_elevation += 28 # Ascends majestically into the air!

    bob_speed = 5.2 if is_fully_charged else (3.2 + 1.2 * ratio)
    bob_height = 8.0 if is_fully_charged else 5.0
    monolith_y = sy - base_elevation + math.sin(t * bob_speed) * bob_height

    # 1. Base Energy Shrine Aperture & Anti-Grav Shadow
    shadow_w = int(46 + 14 * ratio)
    shadow_h = int(22 + 7 * ratio)
    shadow_surf = pygame.Surface((shadow_w * 2, shadow_h * 2), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (10, 16, 28, 170), (0, 0, shadow_w * 2, shadow_h * 2))
    pygame.draw.ellipse(shadow_surf, (*active_color, int(80 + 120 * ratio)), (shadow_w // 4, shadow_h // 4, shadow_w * 1.5, shadow_h * 1.5), 2)
    screen.blit(shadow_surf, (sx - shadow_w, sy - shadow_h))

    # 2. Celestial Vertical Laser Column / Ascension Beacon (Not a torch! Straight focused laser with smooth atmospheric falloff)
    if ratio > 0.12:
        beam_h = 240 if is_fully_charged else int(70 + 140 * ratio)
        beam_w = 26 if is_fully_charged else int(12 + 12 * ratio)
        
        beam_surf = pygame.Surface((beam_w * 2 + 10, beam_h), pygame.SRCALPHA)
        cx_b = beam_w + 5
        
        # Multi-slice vertical cylindrical gradient (straight laser column, fades smoothly towards top of screen)
        slices = 16
        slice_h = beam_h / slices
        for s in range(slices):
            norm = s / float(slices) # 0 at bottom, 1 at top of beam
            slice_y = int((slices - 1 - s) * slice_h)
            falloff = math.cos(norm * (math.pi / 2.0)) # 1.0 at core, fades gracefully to 0.0 at top
            
            # Outer soft atmospheric bloom
            outer_w = int(beam_w * (0.85 + 0.15 * math.sin(t * 3.0 + s * 0.4)))
            outer_a = int((50 if is_fully_charged else int(20 + 35 * ratio)) * falloff)
            pygame.draw.ellipse(beam_surf, (*active_color, outer_a),
                                (cx_b - outer_w, slice_y, outer_w * 2, int(slice_h * 2.2)))
            
            # Inner high-intensity laser shaft
            inner_w = max(2, int(outer_w * 0.38))
            inner_a = int((115 if is_fully_charged else int(40 + 65 * ratio)) * falloff)
            pygame.draw.ellipse(beam_surf, (*active_color, inner_a),
                                (cx_b - inner_w, slice_y, inner_w * 2, int(slice_h * 2.0)))

        # Super-concentrated white laser filament at the center axis
        filament_w = 4 if is_fully_charged else max(1, int(1 + 2 * ratio))
        fil_surf = pygame.Surface((filament_w * 2, beam_h), pygame.SRCALPHA)
        fil_alpha = 175 if is_fully_charged else int(60 + 95 * ratio)
        pygame.draw.rect(fil_surf, (255, 255, 255, fil_alpha), (0, 0, filament_w * 2, beam_h), border_radius=filament_w)
        beam_surf.blit(fil_surf, (cx_b - filament_w, 0))

        # Ascending quantum harmonic rings traveling up the beam towards the sky
        num_pulses = 3 if is_fully_charged else 2
        for p_idx in range(num_pulses):
            p_phase = (t * 1.6 + p_idx * (1.0 / num_pulses)) % 1.0
            ring_y = int((1.0 - p_phase) * (beam_h - 12))
            r_width = int(beam_w * 0.52)
            r_alpha = int((160 if is_fully_charged else 90) * math.sin(p_phase * math.pi))
            pygame.draw.ellipse(beam_surf, (255, 255, 255, r_alpha), (cx_b - r_width, ring_y, r_width * 2, 5), 1)

        screen.blit(beam_surf, (sx - cx_b, int(monolith_y - beam_h + 12)))

    # 3. Rotating 3D Concentric Orbit Rings (Number of rings & speed increase with cores)
    num_rings = 4 if is_fully_charged else (3 if ratio > 0.5 else 2)
    for ring_idx in range(num_rings):
        ring_speed = (t * (2.2 + ring_idx * 0.5) + ring_idx * (math.pi / 2.0))
        rad_x = int((38 + 14 * ratio) * (1.0 - ring_idx * 0.15))
        rad_y = int(rad_x * (0.42 + 0.08 * math.sin(t * 2.0 + ring_idx)))
        
        ring_surf = pygame.Surface((rad_x * 2 + 8, rad_y * 2 + 8), pygame.SRCALPHA)
        ring_alpha = 185 if is_fully_charged else int(90 + 90 * ratio)
        pygame.draw.ellipse(ring_surf, (*active_color, ring_alpha), (4, 4, rad_x * 2, rad_y * 2), 2 if not is_fully_charged else 3)
        screen.blit(ring_surf, (sx - rad_x - 4, int(monolith_y - rad_y - 4)))

        # Orbiting Power Node Crystals on the rings
        node_ang = ring_speed
        nx = sx + math.cos(node_ang) * rad_x
        ny = monolith_y + math.sin(node_ang) * rad_y
        pygame.draw.circle(screen, active_color, (int(nx), int(ny)), 3 if not is_fully_charged else 4)
        pygame.draw.circle(screen, WHITE, (int(nx), int(ny)), 2)

    # 4. Beautiful Morphing Core Crystal Geometry (Layered Octahedron / Stellar Prism)
    core_scale = 1.0 + (0.55 * ratio) + (0.15 * math.sin(t * 6.0) if is_fully_charged else 0)
    c_w = int(12 * core_scale)
    c_h = int(22 * core_scale)

    top_pt = (sx, monolith_y - c_h)
    bot_pt = (sx, monolith_y + c_h)
    mid_r = (sx + c_w, monolith_y)
    mid_l = (sx - c_w, monolith_y)
    center_pt = (sx, monolith_y - 2)

    facet_col1 = (min(255, active_color[0] + 40), min(255, active_color[1] + 40), min(255, active_color[2] + 40))
    facet_col2 = active_color
    facet_col3 = (max(0, active_color[0] - 40), max(0, active_color[1] - 40), max(0, active_color[2] - 40))

    pygame.draw.polygon(screen, facet_col1, [top_pt, mid_r, center_pt])
    pygame.draw.polygon(screen, facet_col2, [top_pt, center_pt, mid_l])
    pygame.draw.polygon(screen, facet_col3, [center_pt, mid_r, bot_pt])
    pygame.draw.polygon(screen, facet_col2, [mid_l, center_pt, bot_pt])

    # Sharp incandescent glowing wireframe perimeter
    pygame.draw.lines(screen, WHITE, True, [top_pt, mid_r, bot_pt, mid_l], 2)
    pygame.draw.line(screen, (255, 255, 255), top_pt, bot_pt, 1)

    # 5. Radiant Core Bloom Corona
    glow_size = 95 if is_fully_charged else int(45 + 38 * ratio)
    glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (*active_color, 45 if not is_fully_charged else 85), (glow_size, glow_size), glow_size)
    pygame.draw.circle(glow_surf, (*active_color, 120 if not is_fully_charged else 180), (glow_size, glow_size), int(glow_size * 0.55))
    pygame.draw.circle(glow_surf, (255, 255, 255, 230), (glow_size, glow_size), int(glow_size * 0.22))
    screen.blit(glow_surf, (sx - glow_size, int(monolith_y - glow_size)))

    # Draw absorbing particles in flight
    draw_core_absorb_particles()

    # 6. Ethereal Sparkling Starlight System (Only activates when all orbs are collected!)
    if is_fully_charged:
        draw_core_sparkles(sx, monolith_y, t)

    # HUD Status Tag
    status_msg = "CORE: COMPLETE // ASCENDED" if is_fully_charged else f"CORE: {total_collected}/{target_quota} [EMP READY]"
    tag = FONT_TINY.render(status_msg, True, GOLD if is_fully_charged else WHITE)
    t_rect = tag.get_rect(center=(sx, sy + 26))
    bg_box = t_rect.inflate(14, 6)
    pygame.draw.rect(screen, (15, 20, 32), bg_box, border_radius=4)
    pygame.draw.rect(screen, active_color, bg_box, 1, border_radius=4)
    screen.blit(tag, t_rect)

def draw_cores(cores):
    t = pygame.time.get_ticks() * 0.001
    for core in cores:
        sx, sy = to_screen(*iso_project(core.grid_c, core.grid_r))
        cy = sy - 14 + math.sin(t * 4.0 + core.pulse_offset) * 4
        points = [(sx, cy - 8), (sx + 5, cy), (sx, cy + 8), (sx - 5, cy)]
        pygame.draw.polygon(screen, (255, 240, 120), points)
        pygame.draw.polygon(screen, GOLD, points, 2)
        pygame.draw.circle(screen, WHITE, (sx, int(cy)), 2)

def draw_powerups(powerups):
    t = pygame.time.get_ticks() * 0.001
    for pw in powerups:
        sx, sy = to_screen(*iso_project(pw.grid_c, pw.grid_r))
        cy = sy - 16 + math.sin(t * 5.0 + pw.pulse) * 5
        pts = [(sx - 7, cy - 4), (sx + 7, cy - 4), (sx + 3, cy + 6), (sx - 3, cy + 6)]
        pygame.draw.polygon(screen, (20, 40, 60), pts)
        pygame.draw.polygon(screen, ELECTRIC_BLUE, pts, 2)
        tag = FONT_TINY.render("SPEED", True, ELECTRIC_BLUE)
        screen.blit(tag, tag.get_rect(center=(sx, cy - 14)))

def draw_shockwaves(shockwaves):
    sx, sy = to_screen(*iso_project(*GRAVITY_CENTER))
    for sw in shockwaves:
        rad_x, rad_y = int(sw.radius), int(sw.radius * 0.5)
        if rad_x > 0 and rad_y > 0:
            alpha = max(0, int(220 * (1.0 - sw.radius / sw.max_radius)))
            sw_surf = pygame.Surface((rad_x * 2 + 4, rad_y * 2 + 4), pygame.SRCALPHA)
            pygame.draw.ellipse(sw_surf, (38, 222, 255, alpha), (2, 2, rad_x * 2, rad_y * 2), 3)
            screen.blit(sw_surf, (sx - rad_x - 2, sy - rad_y - 2))

# ==========================================================
# 6. CYBER FRAME & TERMINAL OVERLAYS
# ==========================================================
def draw_cyber_frame(rect, accent=CYAN):
    x, y, w, h = rect.x, rect.y, rect.width, rect.height
    t = pygame.time.get_ticks() * 0.001

    for tx in range(x, x + w - 18, 20):
        pygame.draw.rect(screen, (16, 26, 46), (tx, y, 18, 8))
        pygame.draw.rect(screen, (34, 54, 88), (tx, y, 18, 8), 1)
        pygame.draw.rect(screen, (16, 26, 46), (tx, y + h - 8, 18, 8))
        pygame.draw.rect(screen, (34, 54, 88), (tx, y + h - 8, 18, 8), 1)
    for ty in range(y, y + h - 18, 20):
        pygame.draw.rect(screen, (16, 26, 46), (x, ty, 8, 18))
        pygame.draw.rect(screen, (34, 54, 88), (x, ty, 8, 18), 1)
        pygame.draw.rect(screen, (16, 26, 46), (x + w - 8, ty, 8, 18))
        pygame.draw.rect(screen, (34, 54, 88), (x + w - 8, ty, 8, 18), 1)

    inner_rect = pygame.Rect(x + 12, y + 12, w - 24, h - 24)
    bg_surf = pygame.Surface((inner_rect.w, inner_rect.h))
    bg_surf.fill((8, 16, 32))
    
    hex_size = 11
    dx, dy = hex_size * 1.732, hex_size * 1.5
    for row_idx, hy in enumerate(range(8, inner_rect.h + 12, int(dy))):
        col_offset = (dx / 2.0) if (row_idx % 2 == 1) else 0.0
        for hx_float in [c * dx + col_offset for c in range(-1, int(inner_rect.w / dx) + 2)]:
            hx = int(hx_float)
            if -hex_size < hx < inner_rect.w + hex_size:
                pts = [(hx + math.cos(math.radians(60 * a + 30)) * 10, hy + math.sin(math.radians(60 * a + 30)) * 10) for a in range(6)]
                pygame.draw.polygon(bg_surf, (15, 34, 62), pts, 1)

    vignette = pygame.Surface((inner_rect.w, inner_rect.h), pygame.SRCALPHA)
    pygame.draw.rect(vignette, (4, 8, 18, 140), (0, 0, inner_rect.w, inner_rect.h))
    bg_surf.blit(vignette, (0, 0))
    screen.blit(bg_surf, (inner_rect.x, inner_rect.y))

    def get_contour(pad, cut):
        return [
            (x + pad + cut, y + pad), (x + w // 2 - 80, y + pad),
            (x + w // 2 - 60, y + pad + 12), (x + w // 2 + 60, y + pad + 12),
            (x + w // 2 + 80, y + pad), (x + w - pad - cut, y + pad),
            (x + w - pad, y + pad + cut), (x + w - pad, y + h - pad - cut),
            (x + w - pad - cut, y + h - pad), (x + w // 2 + 80, y + h - pad),
            (x + w // 2 + 60, y + h - pad - 12), (x + w // 2 - 60, y + h - pad - 12),
            (x + w // 2 - 80, y + h - pad), (x + pad + cut, y + h - pad),
            (x + pad, y + h - pad - cut), (x + pad, y + pad + cut)
        ]

    chassis = get_contour(14, 34)
    pygame.draw.lines(screen, (20, 30, 52), True, chassis, 6)
    rail = get_contour(22, 26)
    pygame.draw.lines(screen, accent, True, rail, 2)
    pygame.draw.lines(screen, (220, 245, 255), True, rail, 1)

    for nx, ny in [(x + 48, y + 22), (x + w - 48, y + 22), (x + 22, y + 48), (x + w - 22, y + 48),
                   (x + 48, y + h - 22), (x + w - 48, y + h - 22), (x + 22, y + h - 48), (x + w - 22, y + h - 48)]:
        pulse = 0.6 + 0.4 * math.sin(t * 5.0)
        pygame.draw.circle(screen, accent, (nx, ny), int(4 + pulse * 2))
        pygame.draw.circle(screen, WHITE, (nx, ny), 2)

def draw_arena_header_brand(level, is_phone_mode=False):
    """
    Renders the classic, professional game title & tagline at top-left:
    - Big classic 'MULTIPLAYER AI ARENA' title with neon chromatic underglow
    - Unique tagline '• THINK  • MOVE  • SURVIVE' directly below
    - Automatically scales to a sleek, compact upper-screen format when in phone/touch mode
    """
    t = pygame.time.get_ticks() * 0.001

    if is_phone_mode:
        # Compact Phone / Touchscreen Layout at upper side
        bx, by = 20, 14
        
        # Sector indicator badge
        sec_tag = FONT_TAGLINE_PHONE.render(f"[ SECTOR 0{level} ]", True, CYAN)
        screen.blit(sec_tag, (bx, by))

        # Compact classic title
        t_surf_shadow = FONT_ARENA_TITLE_PHONE.render("MULTIPLAYER AI ARENA", True, (10, 35, 60))
        t_surf = FONT_ARENA_TITLE_PHONE.render("MULTIPLAYER AI ARENA", True, WHITE)
        screen.blit(t_surf_shadow, (bx + 1, by + 13))
        screen.blit(t_surf, (bx, by + 12))

        # Tagline: • THINK  • MOVE  • SURVIVE
        tagline = FONT_TAGLINE_PHONE.render("• THINK   • MOVE   • SURVIVE", True, GOLD)
        screen.blit(tagline, (bx + 1, by + 34))

        # Delicate neon divider rail
        pygame.draw.line(screen, (30, 50, 85), (bx, by + 48), (bx + 210, by + 48), 1)
        pygame.draw.circle(screen, CYAN, (bx + 210, by + 48), 2)

    else:
        # Classic Big PC / Desktop Layout at Upper Left inside arena
        bx, by = 34, 22

        # Level Intel Tag
        sec_tag = FONT_TINY.render(f"[ SECTOR 0{level} // NEURAL PURSUIT MATRIX ]", True, CYAN)
        screen.blit(sec_tag, (bx, by))

        # Title: Classic Big 'MULTIPLAYER AI ARENA'
        title_str = "MULTIPLAYER AI ARENA"
        
        # Chromatic neon pulse shadow
        pulse = 0.65 + 0.35 * math.sin(t * 3.8)
        glow_col = (int(18 * pulse), int(85 * pulse), int(155 * pulse))
        
        shadow_txt = FONT_ARENA_TITLE_PC.render(title_str, True, glow_col)
        screen.blit(shadow_txt, (bx + 2, by + 20))
        
        # Main crisp white title
        main_txt = FONT_ARENA_TITLE_PC.render(title_str, True, WHITE)
        screen.blit(main_txt, (bx, by + 18))

        # Tagline: • THINK  • MOVE  • SURVIVE in unique monospace gold/cyan font
        t_think = FONT_TAGLINE_PC.render("• THINK", True, GOLD)
        t_move = FONT_TAGLINE_PC.render("• MOVE", True, CYAN)
        t_survive = FONT_TAGLINE_PC.render("• SURVIVE", True, WHITE)

        w_th = t_think.get_width()
        w_mv = t_move.get_width()

        ty = by + 60
        screen.blit(t_think, (bx + 2, ty))
        screen.blit(t_move, (bx + 2 + w_th + 16, ty))
        screen.blit(t_survive, (bx + 2 + w_th + 16 + w_mv + 16, ty))

        # Cybernetic bottom energy rail with moving telemetry packet
        rail_len = 390
        ry = ty + 20
        pygame.draw.line(screen, (22, 36, 62), (bx, ry), (bx + rail_len, ry), 2)
        
        packet_phase = (t * 135) % rail_len
        pygame.draw.line(screen, CYAN, (bx + packet_phase - 16, ry), (bx + packet_phase, ry), 2)
        pygame.draw.circle(screen, WHITE, (int(bx + packet_phase), ry), 2)


def draw_hud(players, npcs, total_dep, target_quota, level):
    panel_w, panel_h = 260, HEIGHT - 40
    panel_x, panel_y = WIDTH - panel_w - 20, 20
    
    card_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    card_surf.fill((14, 18, 30, 220))
    screen.blit(card_surf, (panel_x, panel_y))
    pygame.draw.rect(screen, (60, 75, 110), (panel_x, panel_y, panel_w, panel_h), 1, border_radius=12)

    title = FONT_SUB.render(f"SECTOR 0{level} INTEL", True, WHITE)
    screen.blit(title, (panel_x + 18, panel_y + 18))
    sub = FONT_TINY.render("OBJECTIVE OVERVIEW", True, MUTED)
    screen.blit(sub, (panel_x + 18, panel_y + 38))

    pygame.draw.line(screen, (35, 45, 70), (panel_x + 16, panel_y + 56), (panel_x + panel_w - 16, panel_y + 56))

    cy = panel_y + 70
    screen.blit(FONT_TINY.render("STABILITY QUOTA", True, GOLD), (panel_x + 18, cy))
    cy += 18

    bar_w = panel_w - 36
    pygame.draw.rect(screen, (25, 30, 48), (panel_x + 18, cy, bar_w, 10), border_radius=5)
    progress_w = int(bar_w * min(1.0, total_dep / target_quota))
    if progress_w > 0:
        pygame.draw.rect(screen, GOLD, (panel_x + 18, cy, progress_w, 10), border_radius=5)
    cy += 16
    pct = FONT_TINY.render(f"{total_dep} / {target_quota} CORES SECURED", True, WHITE)
    screen.blit(pct, (panel_x + 18, cy))

    cy += 30
    pygame.draw.line(screen, (35, 45, 70), (panel_x + 16, cy), (panel_x + panel_w - 16, cy))
    cy += 10
    screen.blit(FONT_TINY.render("DEPLOYED AGENTS", True, MUTED), (panel_x + 18, cy))
    cy += 20

    for p in players:
        p_card = pygame.Rect(panel_x + 16, cy, panel_w - 32, 48)
        pygame.draw.rect(screen, (20, 26, 42), p_card, border_radius=6)
        pygame.draw.rect(screen, p.color, p_card, 1, border_radius=6)

        p_name = FONT_BODY.render(p.name[:14], True, p.color)
        screen.blit(p_name, (panel_x + 24, cy + 6))
        stat = FONT_TINY.render(f"Hold: {p.carrying}  |  Secured: {p.score}", True, WHITE)
        screen.blit(stat, (panel_x + 24, cy + 26))
        cy += 54

    cy += 10
    pygame.draw.line(screen, (35, 45, 70), (panel_x + 16, cy), (panel_x + panel_w - 16, cy))
    cy += 12
    screen.blit(FONT_TINY.render(f"SENTINEL SQUAD ({len(npcs)} AI)", True, MUTED), (panel_x + 18, cy))
    cy += 20

    for npc in npcs:
        state_col = ELECTRIC_BLUE if npc.stun_timer > 0 else (GOLD if npc.is_charging else RED)
        screen.blit(FONT_TINY.render(f"H-{npc.npc_id + 1}: {npc.state[:18]}", True, state_col), (panel_x + 18, cy))
        cy += 18

def draw_mobile_controls():
    """
    On-Screen Universal D-Pad for Touch/Mobile Screen Play:
    - Positioned at Bottom-Left with responsive hitboxes
    - Reliable orthogonal corridor step: UP, DOWN, LEFT, RIGHT
    """
    if not touch_controls_enabled:
        return {}
    
    pad_cx, pad_cy = 110, HEIGHT - 110
    btn_s = 48
    gap = 6
    
    btns = {
        'UP': pygame.Rect(pad_cx - btn_s // 2, pad_cy - btn_s - gap, btn_s, btn_s),
        'DOWN': pygame.Rect(pad_cx - btn_s // 2, pad_cy + gap, btn_s, btn_s),
        'LEFT': pygame.Rect(pad_cx - btn_s - gap, pad_cy - btn_s // 2, btn_s, btn_s),
        'RIGHT': pygame.Rect(pad_cx + gap, pad_cy - btn_s // 2, btn_s, btn_s),
    }

    labels = {'UP': '^ UP', 'DOWN': 'v DWN', 'LEFT': '< LFT', 'RIGHT': '> RGT'}
    for key, rect in btns.items():
        surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        surf.fill((16, 26, 44, 210))
        screen.blit(surf, (rect.x, rect.y))
        pygame.draw.rect(screen, CYAN, rect, 2, border_radius=8)
        lbl = FONT_TINY.render(labels[key], True, WHITE)
        screen.blit(lbl, lbl.get_rect(center=rect.center))

    tag = FONT_TINY.render("[ P1 TOUCH D-PAD ]", True, (90, 115, 155))
    screen.blit(tag, (pad_cx - tag.get_width() // 2, pad_cy + 58))
    return btns

def draw_modern_button(rect, text, hovered, active_color=CYAN):
    cut = 10
    pts = [
        (rect.x + cut, rect.y), (rect.right - cut, rect.y),
        (rect.right, rect.y + cut), (rect.right, rect.bottom - cut),
        (rect.right - cut, rect.bottom), (rect.x + cut, rect.bottom),
        (rect.x, rect.bottom - cut), (rect.x, rect.y + cut),
    ]
    fill = (22, 38, 68) if hovered else (12, 18, 34)
    pygame.draw.polygon(screen, fill, pts)
    pygame.draw.polygon(screen, (255, 255, 255) if hovered else active_color, pts, 2 if hovered else 1)
    txt = FONT_SUB.render(text, True, (255, 255, 255) if hovered else (210, 235, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))

def draw_menu_modal(mouse_pos):
    dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim.fill((4, 7, 16, 205))
    screen.blit(dim, (0, 0))

    card_w, card_h = 680, 510
    cx, cy = (WIDTH - card_w) // 2, (HEIGHT - card_h) // 2
    draw_cyber_frame(pygame.Rect(cx, cy, card_w, card_h), CYAN)

    tag = FONT_TINY.render("[ SYSTEM INITIALIZATION // GRAVITATIONAL CORE]", True, CYAN)
    screen.blit(tag, (cx + 42, cy + 34))

    head = FONT_HERO.render("MULTIPLAYER AI ARENA", True, WHITE)
    screen.blit(head, (cx + 42, cy + 56))

    d1_tag = FONT_TINY.render("DIRECTIVE 01 //", True, CYAN)
    d1_txt = FONT_BODY.render("EXTRACT SCATTERED QUANTUM CORES ACROSS THE SECTOR GRID.", True, (215, 228, 248))
    screen.blit(d1_tag, (cx + 42, cy + 104))
    screen.blit(d1_txt, (cx + 154, cy + 103))

    d2_tag = FONT_TINY.render("DIRECTIVE 02 //", True, ELECTRIC_BLUE)
    d2_txt = FONT_BODY.render("DEPOSIT CORES AT SINGULARITY SHRINE TO DEPLOY EMP SHOCKWAVE.", True, ELECTRIC_BLUE)
    screen.blit(d2_tag, (cx + 42, cy + 128))
    screen.blit(d2_txt, (cx + 154, cy + 127))

    d3_tag = FONT_TINY.render("DIRECTIVE 03 //", True, GOLD)
    d3_txt = FONT_BODY.render("EVADE HUNTER A* PURSUIT VECTORS; EQUIP OVERDRIVE THRUSTERS.", True, GOLD)
    screen.blit(d3_tag, (cx + 42, cy + 152))
    screen.blit(d3_txt, (cx + 154, cy + 151))

    screen.blit(FONT_SUB.render(">> INITIALIZE FLEET ROSTER (SELECT AGENT CAPACITY):", True, WHITE), (cx + 42, cy + 192))

    p_buttons = []
    btn_labels = ["[ 01 || SOLO ]", "[ 02 || DUAL ]",
                  "[ 03 || TRIAD ]", "[ 04 || SQUAD ]"]
    btn_w, btn_h = 284, 44
    for idx in range(4):
        bx = cx + 42 + (idx % 2) * 310
        by = cy + 230 + (idx // 2) * 58
        btn_rect = pygame.Rect(bx, by, btn_w, btn_h)
        hovered = btn_rect.collidepoint(mouse_pos)
        draw_modern_button(btn_rect, btn_labels[idx], hovered, active_color=PURPLE if idx >= 2 else CYAN)
        p_buttons.append((btn_rect, idx + 1))

    cy_foot = cy + 380
    pygame.draw.line(screen, (32, 48, 80), (cx + 42, cy_foot), (cx + card_w - 42, cy_foot))
    screen.blit(FONT_TINY.render("INPUT TELEMETRY // P1: ARROWS (OR TOUCH D-PAD) | P2: W-A-S-D", True, MUTED), (cx + 42, cy_foot + 14))
    screen.blit(FONT_TINY.render("INPUT TELEMETRY // P3: I-J-K-L                 | P4: T-F-G-H", True, MUTED), (cx + 42, cy_foot + 32))

    return p_buttons

def draw_name_entry_modal(mouse_pos, p_count, name_inputs, active_idx):
    """
    Dedicated Player Name Entry Screen:
    - Solo (1 player) -> Exactly 1 name box for Player 1
    - Dual (2 players) -> Exactly 2 name boxes for Player 1 and Player 2
    - Triad (3 players) -> Exactly 3 name boxes for Player 1, 2, and 3
    - Apex (4 players) -> All 4 name boxes
    """
    dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim.fill((4, 7, 16, 215))
    screen.blit(dim, (0, 0))

    card_w, card_h = 660, 490
    cx, cy = (WIDTH - card_w) // 2, (HEIGHT - card_h) // 2
    draw_cyber_frame(pygame.Rect(cx, cy, card_w, card_h), CYAN)

    tag = FONT_TINY.render(f"[ AGENT IDENTIFICATION PROTOCOL // {p_count} OPERATIVE ROSTER ]", True, CYAN)
    screen.blit(tag, (cx + 42, cy + 34))

    head = FONT_HERO.render("ENTER OPERATIVE CALLSIGNS", True, WHITE)
    screen.blit(head, (cx + 42, cy + 56))

    sub = FONT_BODY.render("INPUT AGENT NAMES BELOW (CLICK BOX OR PRESS TAB TO SWITCH):", True, MUTED)
    screen.blit(sub, (cx + 42, cy + 96))

    field_rects = []
    spacing = 58 if p_count <= 2 else 48
    input_y = cy + (150 if p_count <= 2 else 130)

    for i in range(p_count):
        scheme = PLAYER_SCHEMES[i]
        lbl = FONT_TINY.render(f"P{i + 1} ({scheme['default_name'].split()[1]}):", True, scheme['base'])
        screen.blit(lbl, (cx + 44, input_y + 10))

        f_rect = pygame.Rect(cx + 175, input_y, 420, 38)
        is_active = (i == active_idx)
        pygame.draw.rect(screen, (16, 24, 42), f_rect, border_radius=6)
        pygame.draw.rect(screen, WHITE if is_active else (40, 60, 95), f_rect, 2 if is_active else 1, border_radius=6)

        txt_str = name_inputs[i] if name_inputs[i] else f"Type name (Default: {scheme['default_name']})..."
        txt_col = WHITE if name_inputs[i] else (100, 120, 155)
        txt_surf = FONT_BODY.render(txt_str, True, txt_col)
        screen.blit(txt_surf, (f_rect.x + 12, f_rect.y + 11))

        if is_active and (pygame.time.get_ticks() // 500) % 2 == 0:
            cx_caret = f_rect.x + 12 + FONT_BODY.size(name_inputs[i])[0] + 2
            pygame.draw.line(screen, CYAN, (cx_caret, f_rect.y + 8), (cx_caret, f_rect.bottom - 8), 2)

        field_rects.append((f_rect, i))
        input_y += spacing

    launch_btn = pygame.Rect(WIDTH // 2 - 160, cy + card_h - 75, 320, 48)
    draw_modern_button(launch_btn, "[ LAUNCH ARENA ]", launch_btn.collidepoint(mouse_pos), CYAN)
    return field_rects, launch_btn


def draw_celebration_banner(level, timer):
    """
    Renders a sleek cinematic sci-fi banner at the top of the screen
    during the core ascension celebration, leaving the center core 100% visible!
    """
    t = pygame.time.get_ticks() * 0.001
    banner_w, banner_h = 720, 70
    bx = (WIDTH - banner_w) // 2
    by = 24

    surf = pygame.Surface((banner_w, banner_h), pygame.SRCALPHA)
    surf.fill((6, 12, 24, 185))
    screen.blit(surf, (bx, by))
    pygame.draw.rect(screen, GOLD, (bx, by, banner_w, banner_h), 1, border_radius=10)

    # Glowing corner accents
    pygame.draw.line(screen, WHITE, (bx + 2, by + 10), (bx + 10, by + 2), 2)
    pygame.draw.line(screen, WHITE, (bx + banner_w - 10, by + 2), (bx + banner_w - 2, by + 10), 2)

    pulse = 0.7 + 0.3 * math.sin(t * 6.0)
    tag_col = (int(250 * pulse), int(210 * pulse), 50)
    tag = FONT_TINY.render(f"[ SECTOR 0{level} STABILIZED // CORE EQUILIBRIUM ACHIEVED ]", True, tag_col)
    screen.blit(tag, tag.get_rect(center=(WIDTH // 2, by + 20)))

    head = FONT_TITLE.render("CELESTIAL GRAVITATIONAL CORE ASCENDED", True, WHITE)
    screen.blit(head, head.get_rect(center=(WIDTH // 2, by + 45)))

    # Skip prompt at bottom
    prompt = FONT_TINY.render("[ CLICK ANYWHERE OR WAIT TO ADVANCE ]", True, (130, 155, 195))
    screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT - 36)))


def draw_victory_modal(mouse_pos, winner_text, current_level, restart_rect, next_lvl_rect):
    dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim.fill((4, 7, 16, 215))
    screen.blit(dim, (0, 0))

    card_w, card_h = 620, 390
    cx, cy = (WIDTH - card_w) // 2, (HEIGHT - card_h) // 2
    draw_cyber_frame(pygame.Rect(cx, cy, card_w, card_h), GOLD)

    status_tag = f"[ SECTOR 0{current_level} STABILIZED // CORE EQUILIBRIUM SECURED ]"
    tag = FONT_TINY.render(status_tag, True, GOLD)
    screen.blit(tag, tag.get_rect(center=(WIDTH // 2, cy + 50)))

    head_title = "CAMPAIGN COMPLETE // ALL SECTORS SECURED!" if current_level == 5 else f"LEVEL 0{current_level} ACCOMPLISHED"
    head = FONT_HERO.render(head_title, True, WHITE)
    screen.blit(head, head.get_rect(center=(WIDTH // 2, cy + 86)))

    lead = FONT_SUB.render(f">> {winner_text} <<", True, CYAN)
    screen.blit(lead, lead.get_rect(center=(WIDTH // 2, cy + 130)))

    sub = FONT_BODY.render("QUANTUM GRAVITATIONAL COLLAPSE AVERTED. ALL TELEMETRY SECURED.", True, (200, 218, 240))
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, cy + 160)))

    if current_level < 5:
        draw_modern_button(next_lvl_rect, f"[ ADVANCE TO SECTOR 0{current_level + 1} ]", next_lvl_rect.collidepoint(mouse_pos), GOLD)
        draw_modern_button(restart_rect, "[ REPLAY LEVEL ]", restart_rect.collidepoint(mouse_pos), CYAN)
    else:
        draw_modern_button(restart_rect, "[ RESTART CAMPAIGN ]", restart_rect.collidepoint(mouse_pos), GOLD)

# ==========================================================
# 7. MAIN EXECUTION & GAME LOOP
# ==========================================================
def main():
    global cam_x, cam_y, screen_shake, step_ripples, touch_controls_enabled
    running = True

    players = []
    npcs = []
    cores = []
    powerups = []
    shockwaves = []
    
    current_level = 1
    max_cores = 7
    total_deposited = 0
    target_quota = 8

    # Game States: "MENU", "NAME_ENTRY", "RUNNING", "CELEBRATION", "VICTORY"
    game_state = "MENU"
    selected_p_count = 1
    name_inputs = ["", "", "", ""]
    active_field_idx = 0
    winner_text = ""
    celebration_timer = 0.0

    btn_next_level = pygame.Rect(WIDTH // 2 - 170, HEIGHT // 2 + 10, 340, 46)
    btn_restart = pygame.Rect(WIDTH // 2 - 170, HEIGHT // 2 + 70, 340, 46)

    def get_level_settings(lvl):
        # 5 Progressive Difficulty Levels
        levels = {
            1: {"quota": 8, "npcs": 1, "npc_speed": 640},
            2: {"quota": 12, "npcs": 1, "npc_speed": 540},
            3: {"quota": 15, "npcs": 2, "npc_speed": 480},
            4: {"quota": 18, "npcs": 2, "npc_speed": 420},
            5: {"quota": 20, "npcs": 3, "npc_speed": 360},
        }
        return levels.get(lvl, levels[5])

    def replenish_items():
        while len(cores) < max_cores:
            c, r = random.randint(1, COLS - 2), random.randint(1, ROWS - 2)
            if (c, r) not in WALLS and (c, r) != GRAVITY_CENTER:
                if not any(core.grid_c == c and core.grid_r == r for core in cores):
                    cores.append(EnergyCore((c, r)))

        while len(powerups) < 2:
            c, r = random.randint(1, COLS - 2), random.randint(1, ROWS - 2)
            if (c, r) not in WALLS and (c, r) != GRAVITY_CENTER:
                if not any(p.grid_c == c and p.grid_r == r for p in powerups):
                    powerups.append(PowerUp((c, r), "BOOTS"))

    def start_level(lvl, p_count, custom_names):
        nonlocal players, npcs, total_deposited, target_quota, game_state, current_level
        current_level = lvl
        cfg = get_level_settings(lvl)
        target_quota = cfg["quota"]
        total_deposited = 0
        
        # Generates the unique obstacle map for the specific level
        generate_walls(lvl)
        
        players.clear()
        controls = [
            {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT},
            {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d},
            {"up": pygame.K_i, "down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l},
            {"up": pygame.K_t, "down": pygame.K_g, "left": pygame.K_f, "right": pygame.K_h},
        ]
        spawns = [(1, 1), (COLS - 2, ROWS - 2), (1, ROWS - 2), (COLS - 2, 1)]

        for i in range(p_count):
            p = Player(i, spawns[i], controls[i], PLAYER_SCHEMES[i], custom_names[i])
            players.append(p)

        npcs.clear()
        npc_spawns = [(COLS // 2, 1), (1, ROWS // 2), (COLS - 2, ROWS // 2)]
        for ni in range(cfg["npcs"]):
            n = NPC(npc_spawns[ni % len(npc_spawns)], cfg["npc_speed"], ni)
            npcs.append(n)

        cores.clear()
        powerups.clear()
        shockwaves.clear()
        step_ripples.clear()
        core_absorb_particles.clear()
        replenish_items()
        game_state = "RUNNING"

    while running:
        dt = clock.tick(60) / 1000.0
        current_time = pygame.time.get_ticks()
        t = current_time * 0.001
        mouse_pos = pygame.mouse.get_pos()
        dpad_buttons = {}

        if screen_shake > 0:
            screen_shake = max(0.0, screen_shake - dt * 15.0)

        for r_item in step_ripples:
            r_item[2] -= dt * 1.5
        step_ripples = [r for r in step_ripples if r[2] > 0]

        # ------------------ EVENT HANDLING ------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == "RUNNING":
                        game_state = "MENU"
                    else:
                        running = False

                elif game_state == "NAME_ENTRY":
                    if event.key == pygame.K_TAB or event.key == pygame.K_DOWN:
                        active_field_idx = (active_field_idx + 1) % selected_p_count
                    elif event.key == pygame.K_UP:
                        active_field_idx = (active_field_idx - 1) % selected_p_count
                    elif event.key == pygame.K_BACKSPACE:
                        name_inputs[active_field_idx] = name_inputs[active_field_idx][:-1]
                    elif event.key == pygame.K_RETURN:
                        start_level(current_level, selected_p_count, name_inputs)
                    elif event.unicode and len(name_inputs[active_field_idx]) < 16 and event.unicode.isprintable():
                        name_inputs[active_field_idx] += event.unicode.upper()

                elif game_state == "RUNNING":
                    # Direct, reliable orthogonal corridor movement from Document 2
                    for p in players:
                        if event.key == p.keymap["up"]:
                            p.move(0, -1)
                        elif event.key == p.keymap["down"]:
                            p.move(0, 1)
                        elif event.key == p.keymap["left"]:
                            p.move(-1, 0)
                        elif event.key == p.keymap["right"]:
                            p.move(1, 0)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "MENU":
                    menu_buttons = draw_menu_modal(mouse_pos)
                    for btn_rect, p_num in menu_buttons:
                        if btn_rect.collidepoint(event.pos):
                            selected_p_count = p_num
                            game_state = "NAME_ENTRY"
                            active_field_idx = 0
                            break

                elif game_state == "NAME_ENTRY":
                    field_rects, launch_btn = draw_name_entry_modal(mouse_pos, selected_p_count, name_inputs, active_field_idx)
                    for f_box, idx in field_rects:
                        if f_box.collidepoint(event.pos):
                            active_field_idx = idx
                    if launch_btn.collidepoint(event.pos):
                        start_level(1, selected_p_count, name_inputs)

                elif game_state == "CELEBRATION":
                    game_state = "VICTORY"

                elif game_state == "VICTORY":
                    if current_level < 5 and btn_next_level.collidepoint(event.pos):
                        start_level(current_level + 1, selected_p_count, name_inputs)
                    elif btn_restart.collidepoint(event.pos):
                        if current_level == 5:
                            game_state = "MENU"
                        else:
                            start_level(current_level, selected_p_count, name_inputs)

                elif game_state == "RUNNING" and players:
                    # Mobile D-Pad Touch Handling
                    p1 = players[0]
                    handled_touch = False
                    if dpad_buttons:
                        if dpad_buttons['UP'].collidepoint(event.pos):
                            p1.move(0, -1)
                            handled_touch = True
                        elif dpad_buttons['DOWN'].collidepoint(event.pos):
                            p1.move(0, 1)
                            handled_touch = True
                        elif dpad_buttons['LEFT'].collidepoint(event.pos):
                            p1.move(-1, 0)
                            handled_touch = True
                        elif dpad_buttons['RIGHT'].collidepoint(event.pos):
                            p1.move(1, 0)
                            handled_touch = True
                            
                    # Screen tap-to-move support
                    if not handled_touch and event.pos[0] < WIDTH - 280:
                        tc, tr = screen_to_grid(event.pos[0], event.pos[1])
                        dc = tc - p1.grid_c
                        dr = tr - p1.grid_r
                        if abs(dc) > 0 or abs(dr) > 0:
                            if abs(dc) >= abs(dr):
                                p1.move(1 if dc > 0 else -1, 0)
                            else:
                                p1.move(0, 1 if dr > 0 else -1)

        # ------------------ GAMEPLAY SIMULATION ------------------
        if game_state in ("RUNNING", "CELEBRATION"):
            update_core_absorb_particles(dt)
            for sw in shockwaves:
                sw.update(dt)
            shockwaves = [sw for sw in shockwaves if sw.alive]

            for p in players:
                p.update(dt)

                for core in cores[:]:
                    if p.grid_c == core.grid_c and p.grid_r == core.grid_r:
                        p.carrying += 1
                        cores.remove(core)

                for pw in powerups[:]:
                    if p.grid_c == pw.grid_c and p.grid_r == pw.grid_r:
                        p.speed_boost_timer = 5.0
                        powerups.remove(pw)

                replenish_items()

                if (p.grid_c, p.grid_r) == GRAVITY_CENTER and p.carrying > 0:
                    trigger_core_deposit_fx(p.x, p.y, p.carrying)
                    p.score += p.carrying
                    total_deposited += p.carrying
                    p.carrying = 0

                    shockwaves.append(Shockwave(GRAVITY_CENTER))
                    for n in npcs:
                        n.stun(3.5)
                    screen_shake = 7.0

                    if total_deposited >= target_quota and game_state == "RUNNING":
                        game_state = "CELEBRATION"
                        celebration_timer = 4.2
                        top_p = max(players, key=lambda pl: pl.score)
                        winner_text = f"Top Agent: {top_p.name} with {top_p.score} Cores Delivered!"
                        for n in npcs:
                            n.stun(12.0)
                        screen_shake = 5.0

            for n in npcs:
                n.update_ai(players, current_time, dt)
                n.update_motion(dt)

                for p in players:
                    if (p.grid_c, p.grid_r) == (n.grid_c, n.grid_r):
                        if p.is_caught_timer <= 0 and n.stun_timer <= 0:
                            p.is_caught_timer = 1.2
                            screen_shake = 5.0
                            if p.carrying > 0:
                                for _ in range(p.carrying):
                                    rc = max(1, min(COLS - 2, p.grid_c + random.randint(-1, 1)))
                                    rr = max(1, min(ROWS - 2, p.grid_r + random.randint(-1, 1)))
                                    if (rc, rr) not in WALLS:
                                        cores.append(EnergyCore((rc, rr)))
                                p.carrying = 0
                            p.score = max(0, p.score - 1)

            if game_state == "CELEBRATION":
                celebration_timer -= dt
                # Smooth cinematic camera pan directly focusing on the radiant Gravitational Core
                gc_x, gc_y = iso_project(*GRAVITY_CENTER)
                cam_x += (gc_x - cam_x) * min(1.0, 3.5 * dt)
                cam_y += (gc_y - cam_y) * min(1.0, 3.5 * dt)
                if celebration_timer <= 0:
                    game_state = "VICTORY"
            else:
                avg_x = sum(p.x for p in players) / len(players)
                avg_y = sum(p.y for p in players) / len(players)
                cam_x += (avg_x - cam_x) * min(1.0, 6.0 * dt)
                cam_y += (avg_y - cam_y) * min(1.0, 6.0 * dt)

        # ------------------ RENDERING ------------------
        screen.fill(BG)

        draw_floating_platform_underlayer(t, total_deposited, target_quota)
        draw_floor_with_gravity_ripples(t, total_deposited, target_quota)
        draw_animated_perimeter_and_pylons(t, total_deposited, target_quota)

        if game_state == "RUNNING":
            for n in npcs:
                if n.projected_path and n.stun_timer <= 0:
                    draw_danger_trajectory(n.projected_path)

        render_queue = []
        for w in WALLS:
            render_queue.append((w[0] + w[1], "wall", w))

        render_queue.append((GRAVITY_CENTER[0] + GRAVITY_CENTER[1], "gravity", None))

        for core in cores:
            render_queue.append((core.grid_c + core.grid_r, "core", core))

        for pw in powerups:
            render_queue.append((pw.grid_c + pw.grid_r, "powerup", pw))

        for p in players:
            render_queue.append((p.grid_c + p.grid_r, "player", p))

        for n in npcs:
            render_queue.append((n.grid_c + n.grid_r, "npc", n))

        render_queue.sort(key=lambda item: item[0])

        for depth, kind, obj in render_queue:
            if kind == "wall":
                draw_wall(obj[0], obj[1], t)
            elif kind == "gravity":
                draw_gravity_core(total_deposited, target_quota)
            elif kind == "core":
                draw_cores([obj])
            elif kind == "powerup":
                draw_powerups([obj])
            elif kind == "player":
                draw_player_entity(obj)
            elif kind == "npc":
                draw_npc_entity(obj)

        draw_shockwaves(shockwaves)

        if game_state == "RUNNING":
            is_mobile_view = touch_controls_enabled and (WIDTH < 1000 or pygame.display.get_surface().get_width() < 1000)
            draw_arena_header_brand(current_level, is_phone_mode=is_mobile_view)
            draw_hud(players, npcs, total_deposited, target_quota, current_level)
            dpad_buttons = draw_mobile_controls()
        elif game_state == "MENU":
            draw_menu_modal(mouse_pos)
        elif game_state == "NAME_ENTRY":
            draw_name_entry_modal(mouse_pos, selected_p_count, name_inputs, active_field_idx)
        elif game_state == "CELEBRATION":
            draw_celebration_banner(current_level, celebration_timer)
        elif game_state == "VICTORY":
            draw_victory_modal(mouse_pos, winner_text, current_level, btn_restart, btn_next_level)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
