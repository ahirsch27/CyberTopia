import pygame
import random
import json
import os
import time
import math

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 500
FPS = 60
SAVE_FILE = "save_data.json"
SCORE_FILE = "high_score.json"

# Colors
BLACK = (5, 5, 15)
CYBER_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
CYBER_RED = (255, 20, 60)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GRID_GRAY = (30, 30, 45)
NEON_ORANGE = (255, 165, 0)
NEON_GREEN = (57, 255, 20)

class Daemon:
    def __init__(self, name, hp, attack, color, level=1, exp=0, streak=0):
        self.name = name
        self.level = level
        self.exp = exp
        self.streak = streak
        self.color = color
        self.max_hp = hp + (level * 15)
        self.hp = self.max_hp
        self.base_attack = attack + (level * 5)
        
    def save_to_disk(self):
        data = {
            "name": self.name, "level": self.level, "exp": self.exp, "streak": self.streak,
            "max_hp_base": self.max_hp - (self.level * 15),
            "atk_base": self.base_attack - (self.level * 5),
            "color": self.color
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def draw(self, surface, x, y, offset=(0, 0), sprite=None):
        draw_x, draw_y = x + offset[0], y + offset[1]
        if sprite: surface.blit(sprite, (draw_x, draw_y))
        else: pygame.draw.rect(surface, self.color, (draw_x, draw_y, 120, 120), 2)
        
        font = pygame.font.SysFont("Courier", 18, bold=True)
        info = font.render(f"{self.name} [LVL {self.level}]", True, self.color)
        surface.blit(info, (draw_x, draw_y - 30))
        
        # Health Bar
        pygame.draw.rect(surface, (40, 40, 50), (draw_x, draw_y + 130, 200, 15))
        hp_ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(surface, self.color, (draw_x, draw_y + 130, 200 * hp_ratio, 15))
        pygame.draw.rect(surface, WHITE, (draw_x, draw_y + 130, 200, 15), 1)

# --- SCORE SYSTEM ---
def get_high_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            return json.load(f).get("best_streak", 0)
    return 0

def update_high_score(current_streak):
    best = get_high_score()
    if current_streak > best:
        with open(SCORE_FILE, "w") as f:
            json.dump({"best_streak": current_streak}, f)

# --- ENGINE HELPERS ---
def get_assets():
    assets = {"bg": None, "player": None, "enemy": None}
    try:
        assets["bg"] = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))
        assets["player"] = pygame.transform.scale(pygame.image.load("player.png"), (150, 150))
        assets["enemy"] = pygame.transform.scale(pygame.image.load("enemy.png"), (150, 150))
    except: pass
    return assets

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            d = json.load(f)
            return Daemon(d["name"], d["max_hp_base"], d["atk_base"], d["color"], d["level"], d["exp"], d.get("streak", 0))
    return None

def spawn_enemy(lvl):
    return Daemon("SENTINEL.sys", 60 + (lvl*12), 10 + (lvl*3), NEON_PINK, lvl)

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    assets = get_assets()
    f_main = pygame.font.SysFont("Courier", 22, True)
    
    player = load_game()
    current_state = "BATTLE" if player else "SELECT"
    enemy = spawn_enemy(player.level) if player else None
    
    starters = [
        {"name": "GLITCH_CAT", "hp": 100, "atk": 20, "color": CYBER_BLUE, "rect": pygame.Rect(50, 200, 200, 100)},
        {"name": "CYBER_HOUND", "hp": 800, "atk": 70, "color": NEON_ORANGE, "rect": pygame.Rect(300, 200, 200, 100)},
        {"name": "NEON_TOAD", "hp": 150, "atk": 15, "color": NEON_GREEN, "rect": pygame.Rect(550, 200, 200, 100)}
    ]
    
    log_msg = "  ~UPLINK ESTABLISHED~" + "\n" + "[A] ATTACK | [S] REPAIR"
    shake_intensity, shake_duration = 0, 0
    running = True

    while running:
        t = pygame.time.get_ticks()
        bob = math.sin(t * 0.005) * 10
        off = (random.randint(-shake_intensity, shake_intensity), random.randint(-shake_intensity, shake_intensity)) if shake_duration > 0 else (0,0)
        if shake_duration > 0: shake_duration -= 1
        
        screen.fill(BLACK)

        if assets["bg"]: 
            screen.blit(assets["bg"], off)
        else:
            for i in range(0, WIDTH, 40): pygame.draw.line(screen, GRID_GRAY, (i+off[0], 0), (i+off[0], HEIGHT))
            for i in range(0, HEIGHT, 40): pygame.draw.line(screen, GRID_GRAY, (0, i+off[1]), (WIDTH, i+off[1]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False 
            
            if current_state == "SELECT" and event.type == pygame.MOUSEBUTTONDOWN:
                for s in starters:
                    if s["rect"].collidepoint(event.pos):
                        player = Daemon(s["name"], s["hp"], s["atk"], s["color"])
                        player.save_to_disk()
                        enemy = spawn_enemy(player.level)
                        current_state = "BATTLE"

            elif current_state == "BATTLE" and player and player.hp > 0 and enemy.hp > 0:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    dmg = random.randint(player.base_attack, player.base_attack + 10)
                    enemy.hp -= dmg
                    log_msg = f"HIT! {dmg} DMG"
                    shake_intensity, shake_duration = 15, 8
                    
                    if enemy.hp <= 0:
                        player.streak += 1
                        player.exp += 60
                        update_high_score(player.streak)
                        if player.exp >= 100:
                            player.level += 1; player.exp = 0; player.max_hp += 20; player.hp = player.max_hp; player.base_attack += 5
                            log_msg = "SYSTEM UPGRADE!"
                        else: log_msg = f"ENEMY DELETED. STREAK: {player.streak}"
                        player.save_to_disk()
                        pygame.display.flip(); time.sleep(0.5)
                        enemy = spawn_enemy(player.level)
                    else:
                        player.hp -= random.randint(enemy.base_attack, enemy.base_attack + 5)
                        shake_intensity, shake_duration = 25, 12
                        if player.hp <= 0:
                            log_msg = "CRITICAL FAILURE. PRESS [R] TO REBOOT."

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    heal = 25 + (player.level * 5)
                    player.hp = min(player.max_hp, player.hp + heal)
                    log_msg = f"SYSTEM REPAIR: +{heal} HP"
                    
                    player.hp -= random.randint(enemy.base_attack, enemy.base_attack + 5)
                    shake_intensity, shake_duration = 25, 12
                    if player.hp <= 0:
                        log_msg = "CRITICAL FAILURE. PRESS [R] TO REBOOT."

            elif current_state == "BATTLE" and player and player.hp <= 0:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
                    player, enemy = None, None
                    current_state = "SELECT"

        # --- DRAWING ---
        if current_state == "SELECT":
            f_title = pygame.font.SysFont("Courier", 28, bold=True)
            title_surf = f_title.render("SELECT YOUR DAEMON PROTOCOL", True, WHITE)
            screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 80))

            best = get_high_score()
            score_surf = f_main.render(f"GLOBAL BEST STREAK: {best}", True, GOLD)
            screen.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, 120))

            for s in starters:
                is_hovering = s["rect"].collidepoint(pygame.mouse.get_pos())
                if is_hovering:
                    border_color, text_color, border_thickness = s["color"], s["color"], 4
                else:
                    border_color, text_color, border_thickness = WHITE, WHITE, 2 

                pygame.draw.rect(screen, border_color, s["rect"], border_thickness)
                name_surf = f_main.render(s["name"], True, text_color)
                text_x = s["rect"].x + (s["rect"].width // 2) - (name_surf.get_width() // 2)
                text_y = s["rect"].y + (s["rect"].height // 2) - (name_surf.get_height() // 2)
                screen.blit(name_surf, (text_x, text_y))
        
        elif current_state == "BATTLE" and player:
            player.draw(screen, 100, 220 + bob, off, assets["player"])
            if enemy: enemy.draw(screen, 500, 80 - bob, off, assets["enemy"])
            # Battle Log
            log_surf = f_main.render(log_msg, True, WHITE)
            screen.blit(log_surf, (WIDTH//2 - log_surf.get_width()//2, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(FPS)

    # --- SHUTDOWN SEQUENCE ---
    if player:
        player.save_to_disk()
        print(">>> DISCONNECTED: SESSION DATA SECURED.")

    pygame.quit()

if __name__ == "__main__":
    run_game()