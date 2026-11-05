# ⚡ Multiplayer AI Arena: Gravitational Core

> A high-performance, multi-platform tactical arena game engineered in Python and Pygame. Features autonomous A* Min-Heap pathfinding intelligence, real-time multi-agent pursuit, cross-platform PC/Mobile touch support, dynamic core ascension visuals, and a 5-level progressive campaign.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-Engine-orange.svg)
![Architecture](https://img.shields.io/badge/AI-A%*_%26_DFS-purple.svg)

---

## 🎮 Game Overview
Players navigate an elevated isometric cyber-chasm arena, extracting scattered quantum cores and depositing them at the central **Gravitational Core** shrine. Depositing cores triggers an **EMP shockwave** that stuns incoming hostile AI sentinels and charges the core toward sector stabilization.

### ✨ Key Features
* **Multiplayer Fleet Roster:** Scale seamlessly from 1 to 4 players with dedicated operational callsign name registration.
* **Cross-Platform Dual Controls:** 
  * **PC / Desktop:** 4-directional grid corridor navigation using keyboard bindings (`Arrows`, `WASD`, `IJKL`, `TFGH`).
  * **Mobile / Touch:** On-screen universal tactile D-Pad overlay and tap-to-move support.
* **Advanced AI Subsystems:**
  * **A* Search Algorithm (Min-Heap):** Powers Hunter AI pursuit vectors using optimized Euclidean heuristics and grid-node cost tracking.
  * **Depth-First Search (DFS):** Drives autonomous exploratory wander behavior during patrol states.
  * **Telegraph Charge Vectoring:** Predictive line-of-sight tracking that projects hazard trajectories before hostile sentinel burst-dashes.
* **5 Progressive Campaign Sectors:** Escalating difficulty maps featuring increasingly dense obstacles, tighter corridors, and up to 3 concurrent AI sentinels.
* **Immersive Visual Systems:** Nanotech hover disc player model with revolving quantum ore collection orbit rings, crimson levitating monolith AI sentinels, hexagonal honeycomb lattice backgrounds, step resonance footprints, and a radiant ascending central core with starlight sparkle particle systems.

---

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3.x
* **Game Engine:** Pygame
* **Typography:** Cyber terminal monospace font loader (`consolas`, `lucidaconsole`, `ocraextended`)
* **Core Algorithms:** A* Min-Heap pathfinding, DFS exploration, screen-aligned orthogonal grid movement.
* **Rendering Pipeline:** Depth-sorted rendering queue ensuring correct occlusion between isometric walls, core shrines, powerups, players, and AI entities.

---

## 🕹️ Controls Guide

| Platform | Control Mode | Bindings |
| :--- | :--- | :--- |
| **PC / Desktop** | Operational Roster P1 | Arrow Keys |
| **PC / Desktop** | Operational Roster P2 | `W A S D` |
| **PC / Desktop** | Operational Roster P3 | `I J K L` |
| **PC / Desktop** | Operational Roster P4 | `T F G H` |
| **Mobile / Touch** | Virtual D-Pad / Tap-to-Move | On-screen tactile overlay |

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3 and Pygame installed:
```bash
pip install pygame
```
```mermaid
graph TD
    Start([NPC AI Update Tick]) --> StunCheck{Is NPC EMP Stunned?}
    
    StunCheck -->|Yes| Stunned[State: EMP STUNNED / Wait]
    StunCheck -->|No| ChargeCheck{Telegraph Charge Triggered?}
    
    ChargeCheck -->|Yes| Charge[State: TELEGRAPH CHARGE <br/> Direct A* Path to Target Player]
    ChargeCheck -->|No| DistCheck{Player Carrying Cores <br/> or Within Range <= 7 Tiles?}
    
    DistCheck -->|Yes| AStar[State: A* PURSUIT <br/> Compute Min-Heap Open Set <br/> using Euclidean Heuristic]
    DistCheck -->|No| DFS[State: DFS EXPLORATION <br/> Stack-based Wander Behavior]
    
    AStar --> Move[Execute Next Grid Step & <br/> Trigger Step Resonance Ripple]
    DFS --> Move
    Charge --> Move
    
    AStar --> Move[Execute Next Grid Step & <br/> Trigger Step Resonance Ripple]
    DFS --> Move
    Charge --> Move
'''
