# 🚀 **Pulse Vector** 🌌

**A mind-bending interstellar adventure where you navigate through layers of depth, chase stars, and master the art of parallax flight.**

---

## 📋 **Table of Contents**
- [Controls](#controls)
- [Game Mechanics](#game-mechanics)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)

---

## 🎮 **Controls**

| **Action**       | **Key/Mouse**             | **Description** |
|------------------|--------------------------|-----------------|
| **Move Up**      | `W`                      | Moves the ship upward on the 2D plane |
| **Move Down**    | `S`                      | Moves the ship downward on the 2D plane |
| **Move Left**    | `A`                      | Moves the ship left on the 2D plane |
| **Move Right**   | `D`                      | Moves the ship right on the 2D plane |
| **Change Depth (Outward)** | `Scroll Down` | Scrolls "outward" to move the ship deeper into space layers |
| **Change Depth (Inward)** | `Scroll Up`  | Scrolls "inward" to bring the ship closer to the foreground |
| **Fire Bullets** | `SPACE`                 | Fires a bullet in the ship's direction (fires continuously if held) |
| **Target a Star**| `Left Mouse Click`      | Targets a star to focus orbit and control ship's zoom behavior |
| **Release Target**| Click Empty Space     | Releases the currently targeted star |
| **Zoom to Target**| Auto (on star click)   | When a star is clicked, the view shifts toward the star's depth |
| **Quit Game**    | `ESC` / Close Window    | Closes the game |

> **Note:** Scroll behavior allows you to shift the ship through "inward", "middle", and "outward" positions. This changes the player's relationship to the layers of depth.

---

## ⚙️ **Game Mechanics**

### 🚀 **Spaceship Movement**
- The spaceship moves using `WASD` keys on a **2D plane**, but with an additional twist: **depth control**.
- Use the **scroll wheel** to move "inward" or "outward" through layers of space, creating a parallax effect.
- The spaceship's design changes depending on its depth and movement, giving it a dynamic and evolving aesthetic.

### 🌟 **Stars & Targeting**
- **Stars** are randomly positioned objects with unique depths and velocities.
- Click on a star to **lock on to it**. The camera will center on the star, and you can orbit around it.
- As you lock onto a star, the ship's velocity is adjusted relative to the star's orbit.
- Releasing the star will allow the player to "slingshot" away using stored orbital velocity.

### 🔥 **Bullets & Firing**
- Press and hold `SPACE` to fire bullets. Bullets can be fired in three modes:
  - **Inward Bullets**: Fired when the ship is in the "inward" scroll mode.
  - **Outward Bullets**: Fired when the ship is in the "outward" scroll mode.
  - **Neutral Bullets**: Fired when the ship is in the "middle" scroll mode.
- Bullets have limited lifespan and are influenced by the parallax depth system, appearing larger or smaller based on their depth.
- Bullets obey **inverse toroidal wrapping**, meaning they reappear on the opposite side of the screen if they leave the edge, but their Y-position is flipped for added chaos.

### 💫 **Depth & Parallax**
- Space isn’t flat. **Depth is the key mechanic**.
- Each star, bullet, and spaceship operates on a unique depth value.
- Stars in the background move slower than stars in the foreground, creating a stunning **parallax effect**.
- As you scroll "inward" or "outward", objects at varying depths move at different rates, enhancing the sense of dimensionality.
- Clicking on a star causes the camera to center on it, and the ship enters orbit. The **orbit speed** is based on the distance and velocity relative to the star.

### ⚡ **Boosts & Orbit Slingshots**
- When targeting a star, the ship's orbital velocity increases. If the player releases the star, they "slingshot" away with boosted speed.
- This boost can be used to navigate faster or evade threats in future iterations of the game.

### 🔄 **Inverse Toroidal Wrapping**
- When the player, stars, or bullets exit one side of the screen, they reappear on the opposite side, but **inverted on the Y-axis**.
- This adds an unpredictable element to gameplay, as players must consider how objects "rebound" off screen edges.

---

## ✨ **Features**
- **Parallax Depth System**: Shift in and out of layers of space using the scroll wheel.
- **Dynamic Ship Design**: The ship's design changes as you shift scroll modes and move in different directions.
- **Realistic Star Orbits**: Target stars and orbit them, then slingshot away.
- **Continuous Fire**: Hold down `SPACE` to release a flurry of bullets across layers of depth.
- **Smooth Movement**: Responsive movement and depth-based inertia give a true feeling of "space flight."
- **Cosmic Aesthetics**: Minimal color design with depth-based color transitions and size shifts.
- **Toroidal Wrapping**: Objects reappear on the opposite side of the screen with mirrored positions, maintaining immersion.

---

## 🛠️ **Installation**

1. **Install Python**: Ensure Python 3.x is installed on your system.
2. **Install Pygame**: Run the following command to install Pygame.
   ```bash
   pip install pygame
