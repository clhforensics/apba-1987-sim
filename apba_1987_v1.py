import random
import time

# ==========================================
#        APBA BASKETBALL v1.0 (PATCHED)
# ==========================================
# Features:
# - Weighted Usage (Stars shoot more)
# - 8 Team Roster (1987)
# - Full Box Score & Stats
# - Fatigue System (MPG Thresholds)
# - Home Court Momentum ("Crowd Erupts")
# - Strategic Timeouts (Rest & Momentum Stopping)
# 
# PATCH NOTES:
# 1. Pace increased (10-20 sec/possession) for realistic scores (90s-100s).
# 2. Timeouts now give +10 min stamina boost to prevent "Timeout Spam".
# 3. Box Score formatting cleaned up.
# ==========================================

# --- DATA: (Name, FG%, FT%, Has_3PT, Usage, MPG) ---
LEAGUE_DATA = {
    "LAL": {
        "city": "Los Angeles", "name": "Lakers",
        "roster": [
            ("Magic Johnson", 0.522, 0.848, True, 16, 37),
            ("James Worthy", 0.539, 0.751, False, 18, 34),
            ("Kareem Abdul-Jabbar", 0.564, 0.714, False, 14, 31),
            ("Byron Scott", 0.489, 0.892, True, 13, 33),
            ("A.C. Green", 0.538, 0.611, False, 8, 28),
            ("Michael Cooper", 0.438, 0.850, True, 9, 27),
            ("Mychal Thompson", 0.480, 0.743, False, 7, 20),
        ]
    },
    "BOS": {
        "city": "Boston", "name": "Celtics",
        "roster": [
            ("Larry Bird", 0.525, 0.910, True, 20, 40),
            ("Kevin McHale", 0.604, 0.836, False, 17, 39),
            ("Robert Parish", 0.556, 0.724, False, 13, 37),
            ("Dennis Johnson", 0.444, 0.824, True, 12, 37),
            ("Danny Ainge", 0.486, 0.843, True, 11, 35),
            ("Bill Walton", 0.521, 0.795, False, 5, 12), 
            ("Jerry Sichting", 0.571, 0.924, True, 4, 15),
        ]
    },
    "DET": {
        "city": "Detroit", "name": "Pistons",
        "roster": [
            ("Isiah Thomas", 0.463, 0.785, True, 19, 37),
            ("Joe Dumars", 0.469, 0.762, True, 14, 31),
            ("Adrian Dantley", 0.534, 0.861, False, 16, 33),
            ("Bill Laimbeer", 0.501, 0.894, True, 11, 34),
            ("Dennis Rodman", 0.545, 0.587, False, 5, 27),
            ("Vinnie Johnson", 0.462, 0.786, False, 12, 28),
            ("John Salley", 0.562, 0.614, False, 6, 20),
        ]
    },
    "CHI": {
        "city": "Chicago", "name": "Bulls",
        "roster": [
            ("Michael Jordan", 0.482, 0.857, False, 28, 40),
            ("Charles Oakley", 0.510, 0.736, False, 11, 36),
            ("John Paxson", 0.460, 0.801, True, 10, 33),
            ("Gene Banks", 0.539, 0.767, False, 8, 29),
            ("Dave Corzine", 0.475, 0.736, False, 7, 28),
            ("Brad Sellers", 0.455, 0.728, False, 6, 22),
        ]
    },
    "ATL": {
        "city": "Atlanta", "name": "Hawks",
        "roster": [
            ("Dominique Wilkins", 0.463, 0.818, True, 22, 37),
            ("Kevin Willis", 0.536, 0.709, False, 13, 32),
            ("Doc Rivers", 0.451, 0.828, False, 10, 31),
            ("Tree Rollins", 0.546, 0.724, False, 5, 23),
            ("Spud Webb", 0.438, 0.762, False, 9, 16),
            ("Randy Wittman", 0.503, 0.793, False, 9, 29),
        ]
    },
    "PHI": {
        "city": "Philadelphia", "name": "76ers",
        "roster": [
            ("Charles Barkley", 0.594, 0.761, True, 18, 38),
            ("Maurice Cheeks", 0.527, 0.877, False, 11, 36),
            ("Cliff Robinson", 0.465, 0.696, False, 14, 32),
            ("Roy Hinson", 0.477, 0.758, False, 11, 30),
            ("Mike Gminski", 0.457, 0.846, False, 11, 30),
        ]
    },
    "MIL": {
        "city": "Milwaukee", "name": "Bucks",
        "roster": [
            ("Terry Cummings", 0.511, 0.662, False, 18, 34),
            ("Sidney Moncrief", 0.488, 0.813, False, 13, 32),
            ("Jack Sikma", 0.463, 0.847, False, 11, 30),
            ("Paul Pressey", 0.477, 0.800, True, 10, 33),
            ("Ricky Pierce", 0.534, 0.880, False, 15, 28),
        ]
    },
    "DAL": {
        "city": "Dallas", "name": "Mavericks",
        "roster": [
            ("Mark Aguirre", 0.495, 0.770, True, 20, 34),
            ("Rolando Blackman", 0.495, 0.884, False, 16, 35),
            ("Derek Harper", 0.501, 0.720, True, 13, 33),
            ("Sam Perkins", 0.482, 0.828, False, 12, 33),
            ("Roy Tarpley", 0.518, 0.695, False, 9, 25),
        ]
    }
}

# --- CLASSES ---

class Player:
    def __init__(self, data):
        self.name = data[0]
        self.fg_percent = data[1]
        self.ft_percent = data[2]
        self.has_3pt = data[3]
        self.usage = data[4]
        self.mpg = data[5]  # The "Wall"
        self.stamina_boost = 0 # Added via Timeouts
        
        # Stats
        self.points = 0
        self.shots = 0
        self.makes = 0
        self.threes_made = 0
        self.ft_attempts = 0
        self.ft_made = 0
        
        self.card = self.generate_card()

    def generate_card(self):
        card_data = {}
        valid_rolls = [(d1*10)+d2 for d1 in range(1,7) for d2 in range(1,7)]
        total_makes = int(36 * self.fg_percent)
        for i, roll in enumerate(valid_rolls):
            if i < total_makes:
                if self.has_3pt and (roll == 11 or roll == 66):
                    card_data[roll] = "GOAL_3"
                else:
                    card_data[roll] = "GOAL_2"
            else:
                card_data[roll] = "MISS"
        return card_data
    
    def get_fatigue_limit(self):
        return self.mpg + self.stamina_boost

    def rest(self):
        # PATCH 2: Timeout gives a BETTER "Second Wind" (Adds 10 mins to limit)
        # This prevents teams from burning all timeouts in 2 minutes.
        self.stamina_boost += 10

class Team:
    def __init__(self, key):
        data = LEAGUE_DATA[key]
        self.city = data["city"]
        self.name = data["name"]
        self.score = 0
        self.timeouts = 6
        self.roster = [Player(p) for p in data["roster"]]
        
        self.usage_bucket = []
        for p in self.roster:
            for _ in range(p.usage):
                self.usage_bucket.append(p)

    def get_shooter(self):
        return random.choice(self.usage_bucket)
    
    def call_timeout(self):
        if self.timeouts > 0:
            self.timeouts -= 1
            # Rest all players
            for p in self.roster:
                p.rest()
            return True
        return False

# --- LOGIC HELPERS ---

def shoot_free_throws(player):
    made = 0
    for _ in range(2):
        if random.random() <= player.ft_percent:
            made += 1
    return made

def check_fatigue(player, current_minute):
    # If game time exceeds player's limit, roll for fatigue miss
    if current_minute > player.get_fatigue_limit():
        # 1 in 3 chance fatigue causes a miss on a good roll
        if random.randint(1, 3) == 1:
            return True
    return False

# --- MAIN GAME LOOP ---

def play_game(team_v, team_h):
    print(f"\n" + "="*60)
    print(f"!!! TIP OFF: {team_v.city} vs {team_h.city} !!!")
    print(f"Home Court Advantage: {team_h.city} Crowd is Ready")
    print("="*60)
    time.sleep(1)
    
    possession = team_v
    home_streak = 0
    crowd_erupting = False
    
    for quarter in range(1, 5):
        time_remaining = 720
        print(f"\n--- START Q{quarter} ---")
        
        while time_remaining > 0:
            # Game Clock Math
            current_minute = ((quarter - 1) * 12) + ((720 - time_remaining) / 60)
            
            # --- STRATEGIC TIMEOUT CHECK ---
            # 1. Stop the Run (Visitor calls TO if crowd erupts)
            if crowd_erupting and possession == team_v:
                if team_v.call_timeout():
                    print(f"   [TIMEOUT] {team_v.city} calls timeout to silence the crowd!")
                    crowd_erupting = False
                    home_streak = 0
            
            shooter = possession.get_shooter()
            
            # --- CROWD RATTLE CHECK ---
            rattled = False
            if possession == team_v and crowd_erupting:
                if random.randint(1, 4) == 1:
                    rattled = True

            # --- THE SHOT ---
            if rattled:
                print(f"Q{quarter} {shooter.name} is RATTLED by the noise! Miss.")
                result = "MISS"
            else:
                d1, d2 = random.randint(1, 6), random.randint(1, 6)
                roll = (d1 * 10) + d2
                result = shooter.card.get(roll, "MISS")
            
            # --- FATIGUE CHECK ---
            gassed_miss = False
            if "GOAL" in result:
                if check_fatigue(shooter, current_minute):
                    print(f"Q{quarter} {shooter.name} (Short)... GASSED! Miss.")
                    result = "MISS"
                    gassed_miss = True

            # --- RESOLUTION ---
            if result == "GOAL_3":
                print(f"Q{quarter} {shooter.name} ({roll}) -> FROM DEEP! (3 pts)")
                possession.score += 3
                shooter.points += 3
                shooter.makes += 1
                shooter.threes_made += 1
                shooter.shots += 1
                
                if possession == team_h: home_streak += 1
                else: 
                    home_streak = 0
                    if crowd_erupting:
                        print(f"   >>> {shooter.name} SILENCES THE CROWD!")
                        crowd_erupting = False

            elif result == "GOAL_2":
                print(f"Q{quarter} {shooter.name} ({roll}) -> Scores.")
                possession.score += 2
                shooter.points += 2
                shooter.makes += 1
                shooter.shots += 1
                
                if possession == team_h: home_streak += 1
                else: 
                    home_streak = 0
                    if crowd_erupting:
                        print(f"   >>> {shooter.name} SILENCES THE CROWD!")
                        crowd_erupting = False

            else: # MISS
                # Foul Check (10%)
                if random.randint(1, 10) == 1 and not rattled and not gassed_miss:
                    print(f"Q{quarter} {shooter.name} ({roll}) -> WHISTLE! FOUL.")
                    ft_made = shoot_free_throws(shooter)
                    possession.score += ft_made
                    shooter.points += ft_made
                    shooter.ft_attempts += 2
                    shooter.ft_made += ft_made
                    print(f"   -> FTs: {ft_made}/2")
                    if possession == team_v and ft_made > 0:
                        home_streak = 0
                else:
                    shooter.shots += 1
                    # If player missed because GASSED, Team calls Timeout to Rest
                    if gassed_miss:
                        if possession.call_timeout():
                            print(f"   [TIMEOUT] {possession.city} calls timeout to rest players.")

            # --- MOMENTUM UPDATE ---
            if possession == team_h and home_streak >= 3 and not crowd_erupting:
                crowd_erupting = True
                print("   !!! THE CROWD ERUPTS !!! (Defense Bonus Active)")

            # Swap & Time
            possession = team_h if possession == team_v else team_v
            
            # PATCH 1: Faster Pace (10-20 seconds per play instead of 14-24)
            # This increases possession count to realistic 1987 levels.
            time_remaining -= random.randint(10, 20)

    # --- FINAL BOX SCORE ---
    print(f"\n" + "="*60)
    print(f"FINAL: {team_v.city} {team_v.score} - {team_h.city} {team_h.score}")
    print("="*60)
    
    for t in [team_v, team_h]:
        print(f"\n--- {t.city} Stats ---")
        print(f"{'PLAYER':<20} {'PTS':<5} {'FG':<8} {'3PT':<5} {'FT':<5} {'MPG'}")
        print("-" * 55)
        # Sort by points
        sorted_roster = sorted(t.roster, key=lambda x: x.points, reverse=True)
        for p in sorted_roster:
            fg_str = f"{p.makes}-{p.shots}"
            ft_str = f"{p.ft_made}-{p.ft_attempts}"
            # PATCH 3: Formatting clean up (int() on minutes, better spacing)
            print(f"{p.name:<20} {p.points:<5} {fg_str:<8} {p.threes_made:<5} {ft_str:<5} {int(p.mpg)}")

# --- MENU ---
def main():
    while True:
        print("\n" + "="*40)
        print("   APBA BASKETBALL v1.0 (PATCHED)   ")
        print("="*40)
        keys = list(LEAGUE_DATA.keys())
        for i, key in enumerate(keys):
            print(f"{i+1}. {LEAGUE_DATA[key]['city']} {LEAGUE_DATA[key]['name']}")
        print("Q. Quit")
        
        c1 = input("\nVisitor (Number): ")
        if c1.lower() == 'q': break
        c2 = input("Home (Number): ")
        
        try:
            v_idx, h_idx = int(c1)-1, int(c2)-1
            play_game(Team(keys[v_idx]), Team(keys[h_idx]))
            input("\nPress Enter to return to menu...")
        except:
            print("Invalid Input.")

if __name__ == "__main__":
    main()