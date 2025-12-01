# APBA Pro Basketball 1987 Simulator (Python Edition)

## Overview
A Python-based statistical simulation of the 1987 NBA season, inspired by the classic APBA tabletop board game. This project recreates the "solitaire sports" experience of the 80s using modern logic engines to handle fatigue, crowd momentum, and weighted player usage.

**Version:** 1.0 (Final)
**Author:** clhforensics

## Features

### 🏀 Statistical Dice Engine
* **11-66 Logic:** Uses the classic two-die combination (36 outcomes) mapped to real-life 1987 shooting percentages.
* **Weighted Usage:** Players are assigned usage rates based on their '87 shot attempts. Michael Jordan will dominate the ball; Brad Sellers will not.
* **The "Clutch" Gene:** 3-Point logic allows shooters like Larry Bird and Byron Scott to strike from deep on specific rolls.

### 🧠 Dynamic AI Coaching
* **Fatigue System:** Tracks simulated minutes played. If a player exceeds their real-life MPG (Minutes Per Game), they risk becoming "GASSED," significantly lowering their shooting percentage.
* **Timeout Strategy:** The CPU coach utilizes timeouts strategically:
    1.  **To Rest:** Calling time to give tired players a "Second Wind" (stamina boost).
    2.  **To Silence the Crowd:** Calling time immediately when the opponent goes on a 6-0 run.

### 🏟️ Atmosphere Engine
* **Home Court Advantage:** The "Crowd Eruption" mechanic triggers when the home team hits 3 consecutive shots.
* **Rattle Check:** Visiting teams suffer a penalty to shooting rolls while the crowd is erupting.

## Included Rosters (1986-87 Season)
The simulator includes the "Elite 8" of the 1987 season:
* **Los Angeles Lakers** (Magic, Worthy, Kareem)
* **Boston Celtics** (Bird, McHale, Parish)
* **Detroit Pistons** (Isiah, Laimbeer, Rodman)
* **Chicago Bulls** (Jordan, Oakley, Paxson)
* **Atlanta Hawks** (Wilkins, Webb)
* **Philadelphia 76ers** (Barkley, Cheeks)
* **Milwaukee Bucks** (Cummings, Moncrief)
* **Dallas Mavericks** (Aguirre, Blackman)

## How to Run
This simulation uses standard Python libraries (`random`, `time`) with no external dependencies.

1.  Clone the repository:
    ```bash
    git clone [https://github.com/clhforensics/apba-1987-sim.git](https://github.com/clhforensics/apba-1987-sim.git)
    ```
2.  Run the simulator:
    ```bash
    python3 apba_1987.py
    ```
3.  Follow the on-screen menu to select your matchup (Visitor vs Home).

## Future Roadmap
* **Season Mode:** Simulating a full 82-game schedule.
* **CSV Export:** Logging box scores to spreadsheets for season tracking.
* **Historical Expansion:** Adding the 1996 Bulls and 2016 Warriors.

---
*Note: This simulation is a fan project and is not affiliated with the APBA Game Company.*