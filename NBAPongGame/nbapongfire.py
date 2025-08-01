import pygame
import random
import sys
import os
import json
from datetime import datetime
import math

# Initialize Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PADDLE_BORDER_RADIUS = 8
CENTER_CIRCLE_RADIUS = 75
LOGO_DISPLAY_MAX_DIM = CENTER_CIRCLE_RADIUS * 1.5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COURT_LINE_COLOR = (220, 220, 220)
RETRO_GREEN_SCREEN = (102, 204, 255)
BUTTON_COLOR = (50, 50, 150)
BUTTON_HOVER_COLOR = (80, 80, 180)
BUTTON_TEXT_COLOR = WHITE
SELECTED_TEXT_COLOR = (255, 255, 0) # Yellow for selected
INPUT_BOX_COLOR = (200, 200, 200)
INPUT_TEXT_COLOR = BLACK
DIFFICULTY_BUTTON_COLORS = {
    "EASY": (60, 180, 75), "NORMAL": (255, 225, 25),
    "HARD": (245, 130, 48), "EXTREME": (230, 25, 75),
}
DIFFICULTY_BUTTON_HOVER_COLORS = {
    "EASY": (80, 200, 95), "NORMAL": (255, 235, 75),
    "HARD": (250, 150, 70), "EXTREME": (240, 50, 95),
}
DARK_DESATURATED_BLUE = (100, 170, 170)
BASKETBALL_ORANGE = (211, 84, 0)
SHADOW_COLOR = (0, 0, 0, 100)

# Paddle Properties
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100  # This is the ORIGINAL/MAX height
PLAYER_PADDLE_SPEED = 20 # Base speed
SHADOW_OFFSET_X = 3
SHADOW_OFFSET_Y = 3

BALL_RADIUS = 10
BASE_BALL_SPEED_X = 5
BASE_BALL_SPEED_Y = 5
actual_initial_ball_speed_x = BASE_BALL_SPEED_X
actual_initial_ball_speed_y = BASE_BALL_SPEED_Y

# Ball Trail Properties
BALL_TRAIL_LENGTH = 10
ball_trail_positions = []

# Ball Rotation Properties
ball_rotation_angle = 0
BALL_ROTATION_SPEED = 5

# "On Fire" Power-up Constants
FIRE_STREAK_GOAL_COUNT = 3
FIRE_STREAK_TIME_WINDOW_MS = 20000  # 20 seconds
ON_FIRE_PADDLE_SPEED_BOOST = 3       # Additional speed for paddle
ON_FIRE_BALL_SPEED_MULTIPLIER = 1.2 # e.g., 20% faster ball
ON_FIRE_PADDLE_COLOR = (255, 69, 0) # Fiery orange-red
ON_FIRE_PADDLE_BORDER_COLOR = (255, 215, 0) # Gold/Yellow border
FIRE_AURA_COLORS = [ # Base glow aura, less prominent now
    (255, 0, 0, 50),
    (255, 140, 0, 80),
    (255, 165, 0, 100),
]
FLAME_PARTICLE_COLORS = [
    (255, 223, 0), (255,191,0), # Yellows
    (255, 165, 0), (255, 140, 0), # Oranges
    (255, 100, 0), (245, 60, 0) # Reds
]
MAX_FLAME_PARTICLES = 100
FLAME_PARTICLES_PER_FRAME = 5


DIFFICULTY_SETTINGS = {
    "EASY":   {"ai_paddle_speed": 3, "ai_speed_factor": 0.30, "ball_speed_multiplier": 0.80},
    "NORMAL": {"ai_paddle_speed": 4, "ai_speed_factor": 0.40, "ball_speed_multiplier": 1.10},
    "HARD":   {"ai_paddle_speed": 8, "ai_speed_factor": 0.70, "ball_speed_multiplier": 1.25},
    "EXTREME": {"ai_paddle_speed": 10, "ai_speed_factor": 1.00, "ball_speed_multiplier": 2.00},
}
selected_difficulty = "NORMAL"

NBA_TEAMS_LIST = [
    {"name": "LAKERS", "primary": (85, 37, 130), "secondary": (253, 185, 39), "logo_file": "LakersLogo.png"},
    {"name": "CELTICS", "primary": (0, 122, 51), "secondary": (139, 113, 73), "logo_file": "CelticsLogo.png"},
    {"name": "KNICKS", "primary": (0, 107, 182), "secondary": (245, 132, 38), "logo_file": "KnicksLogo.png"},
    {"name": "PACERS", "primary": (0, 45, 98), "secondary": (253, 187, 48), "logo_file": "PacersLogo.png"},
    {"name": "BULLS", "primary": (206, 17, 65), "secondary": (6, 25, 34), "logo_file": "BullsLogo.png"},
    {"name": "WARRIORS", "primary": (29, 66, 138), "secondary": (255, 199, 44), "logo_file": "WarriorsLogo.png"},
    {"name": "HEAT", "primary": (152, 0, 46), "secondary": (249, 160, 27), "logo_file": "HeatLogo.png"},
    {"name": "BUCKS", "primary": (0, 71, 27), "secondary": (240, 235, 210), "logo_file": "BucksLogo.png"},
    {"name": "76ERS", "primary": (0, 107, 182), "secondary": (237, 23, 76), "logo_file": "76ersLogo.png"},
    {"name": "SUNS", "primary": (29, 17, 96), "secondary": (229, 95, 32), "logo_file": "SunsLogo.png"},
    {"name": "NETS", "primary": (0, 0, 0), "secondary": (120, 120, 120), "logo_file": "NetsLogo.png"},
    {"name": "NUGGETS", "primary": (13, 34, 64), "secondary": (255, 198, 39), "logo_file": "NuggetsLogo.png"},
    {"name": "CLIPPERS", "primary": (200,16,46), "secondary": (29,66,138), "logo_file": "ClippersLogo.png"},
    {"name": "MAVERICKS", "primary": (0,83,188), "secondary": (0,43,92), "logo_file": "MavericksLogo.png"},
    {"name": "GRIZZLIES", "primary": (93,118,169), "secondary": (18,24,49), "logo_file": "GrizzliesLogo.png"},
    {"name": "WIZARDS", "primary": (0, 43, 92), "secondary": (227, 24, 55), "logo_file": "WizardsLogo.png"},
    {"name": "RAPTORS", "primary": (206, 17, 65), "secondary": (6, 25, 34), "logo_file": "RaptorsLogo.png"},
    {"name": "CAVALIERS", "primary": (134, 0, 56), "secondary": (253, 187, 48), "logo_file": "CavaliersLogo.png"},
    {"name": "PISTONS", "primary": (200, 16, 46), "secondary": (29, 66, 138), "logo_file": "PistonsLogo.png"},
    {"name": "SPURS", "primary": (6, 25, 34), "secondary": (196, 206, 211), "logo_file": "SpursLogo.png"},
    {"name": "TIMBERWOLVES", "primary": (12, 35, 64), "secondary": (120, 190, 32), "logo_file": "TimberwolvesLogo.png"},
    {"name": "THUNDER", "primary": (0, 125, 195), "secondary": (239, 59, 36), "logo_file": "ThunderLogo.png"},
    {"name": "TRAIL BLAZERS", "primary": (224, 58, 62), "secondary": (6, 25, 34), "logo_file": "TrailblazersLogo.png"},
    {"name": "JAZZ", "primary": (0, 43, 92), "secondary": (249, 160, 27), "logo_file": "JazzLogo.png"},
    {"name": "KINGS", "primary": (91, 43, 130), "secondary": (99, 113, 122), "logo_file": "KingsLogo.png"},
    {"name": "HAWKS", "primary": (200, 16, 46), "secondary": (253, 185, 39), "logo_file": "HawksLogo.png"},
    {"name": "HORNETS", "primary": (29, 17, 96), "secondary": (0, 120, 140), "logo_file": "HornetsLogo.png"},
    {"name": "MAGIC", "primary": (0, 125, 197), "secondary": (196, 206, 211), "logo_file": "MagicLogo.png"},
    {"name": "ROCKETS", "primary": (206, 17, 65), "secondary": (196, 206, 211), "logo_file": "RocketsLogo.png"},
    {"name": "PELICANS", "primary": (0, 22, 65), "secondary": (180, 151, 90), "logo_file": "PelicansLogo.png"},
]

# --- Fonts ---
CUSTOM_TITLE_FONT_NAME = "212 Sports.otf"
CUSTOM_TITLE_FONT_SIZE = 50
ON_FIRE_FONT_SIZE = 36
try:
    CUSTOM_TITLE_FONT = pygame.font.Font(CUSTOM_TITLE_FONT_NAME, CUSTOM_TITLE_FONT_SIZE)
    try:
        ON_FIRE_FONT = pygame.font.Font(CUSTOM_TITLE_FONT_NAME, ON_FIRE_FONT_SIZE)
    except pygame.error:
        print(f"Warning: Custom font '{CUSTOM_TITLE_FONT_NAME}' for 'On Fire' message not found. Falling back to monospace.")
        ON_FIRE_FONT = pygame.font.SysFont("monospace", ON_FIRE_FONT_SIZE, bold=True)
    RETRO_FONT_LARGE = pygame.font.SysFont("monospace", 50, bold=True)
except pygame.error as e:
    print(f"Warning: Custom title font '{CUSTOM_TITLE_FONT_NAME}' not found: {e}. Falling back.")
    CUSTOM_TITLE_FONT = pygame.font.SysFont("monospace", 50, bold=True)
    ON_FIRE_FONT = pygame.font.SysFont("monospace", ON_FIRE_FONT_SIZE, bold=True)
    RETRO_FONT_LARGE = CUSTOM_TITLE_FONT
try:
    RETRO_FONT_MEDIUM = pygame.font.SysFont("monospace", 35, bold=True)
    RETRO_FONT_SMALL = pygame.font.SysFont("monospace", 25)
    SCORE_FONT = pygame.font.SysFont("monospace", 36, bold=True)
    TEAM_NAME_FONT = pygame.font.SysFont("monospace", 20, bold=True)
    GAME_CLOCK_FONT = pygame.font.SysFont("monospace", 48, bold=True)
    QUARTER_DISPLAY_FONT = pygame.font.SysFont("monospace", 24, bold=True)
    MESSAGE_FONT = pygame.font.SysFont("monospace", 30, bold=True)
    INPUT_FONT = pygame.font.SysFont("monospace", 32)
    LEADERBOARD_FONT = pygame.font.SysFont("monospace", 20)
except pygame.error as e:
    print(f"Warning: Monospace font error: {e}. Using fallbacks.")
    if 'ON_FIRE_FONT' not in locals(): ON_FIRE_FONT = pygame.font.Font(None, 40)
    if 'RETRO_FONT_MEDIUM' not in locals(): RETRO_FONT_MEDIUM = pygame.font.Font(None, 50)
    if 'RETRO_FONT_SMALL' not in locals(): RETRO_FONT_SMALL = pygame.font.Font(None, 35)
    if 'SCORE_FONT' not in locals(): SCORE_FONT = pygame.font.Font(None, 50)
    if 'TEAM_NAME_FONT' not in locals(): TEAM_NAME_FONT = pygame.font.Font(None, 30)
    if 'GAME_CLOCK_FONT' not in locals(): GAME_CLOCK_FONT = pygame.font.Font(None, 60)
    if 'QUARTER_DISPLAY_FONT' not in locals(): QUARTER_DISPLAY_FONT = pygame.font.Font(None, 30)
    if 'MESSAGE_FONT' not in locals(): MESSAGE_FONT = pygame.font.Font(None, 40)
    if 'INPUT_FONT' not in locals(): INPUT_FONT = pygame.font.Font(None, 40)
    if 'LEADERBOARD_FONT' not in locals(): LEADERBOARD_FONT = pygame.font.Font(None, 25)

# --- Setup Screen ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NBA Retro Pong")
clock = pygame.time.Clock()

# --- Load Assets ---
start_screen_wallpaper = None
ball_bounce_sound = None
cheering_sound = None
original_ball_image = None
scaled_ball_image = None
original_fireball_image = None
scaled_fireball_image = None
team_logos_surfaces = {}
team_select_logo_surfaces = {}
base_path = os.path.dirname(os.path.abspath(__file__))
music_loaded_successfully = False

try:
    image_path = os.path.join(base_path, "NBAPongLogo.png")
    start_screen_wallpaper_original = pygame.image.load(image_path).convert_alpha()
    start_screen_wallpaper = pygame.transform.scale(start_screen_wallpaper_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error loading start screen wallpaper: {e}")

try:
    ball_image_path = os.path.join(base_path, "Basketball.png")
    original_ball_image = pygame.image.load(ball_image_path).convert_alpha()
    scaled_ball_image = pygame.transform.smoothscale(original_ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))
except pygame.error as e:
    print(f"Error loading ball image 'Basketball.png': {e}. Will use default drawing.")
    scaled_ball_image = None

try:
    fireball_image_path = os.path.join(base_path, "Fireball.png")
    original_fireball_image = pygame.image.load(fireball_image_path).convert_alpha()
    scaled_fireball_image = pygame.transform.smoothscale(original_fireball_image, (BALL_RADIUS * 2 - 4, BALL_RADIUS * 2 - 4))
except pygame.error as e:
    print(f"Error loading ball image 'Fireball.png': {e}. Will use aura fallback.")
    scaled_fireball_image = None


try:
    sound_path_bounce = os.path.join(base_path, "BallBounce.wav")
    ball_bounce_sound = pygame.mixer.Sound(sound_path_bounce)
except pygame.error as e: print(f"Error loading sound 'BallBounce.wav': {e}")
try:
    sound_path_cheer = os.path.join(base_path, "Cheering.wav")
    cheering_sound = pygame.mixer.Sound(sound_path_cheer)
except pygame.error as e: print(f"Error loading sound 'Cheering.wav': {e}")

try:
    music_file_name = "Hoops and Hype.mp3"
    music_path = os.path.join(base_path, music_file_name)
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        music_loaded_successfully = True
        print(f"Menu music '{music_file_name}' loaded successfully.")
    else:
        print(f"Warning: Music file '{music_file_name}' not found at {music_path}")
except pygame.error as e:
    print(f"Error loading music '{music_file_name}': {e}")


def scale_logo(logo_surf, max_dim):
    original_width, original_height = logo_surf.get_size()
    if original_width == 0 or original_height == 0: return None
    ratio = min(max_dim / original_width, max_dim / original_height) if original_width > 0 and original_height > 0 else 1
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    if new_width > 0 and new_height > 0:
        return pygame.transform.smoothscale(logo_surf, (new_width, new_height))
    return None

def load_all_team_logos():
    global team_logos_surfaces, team_select_logo_surfaces
    gameplay_logo_max_dim = CENTER_CIRCLE_RADIUS * 1.6
    team_select_preview_max_dim = LOGO_DISPLAY_MAX_DIM * 1.2
    for team_data in NBA_TEAMS_LIST:
        if team_data.get("logo_file"):
            logo_filename = team_data["logo_file"]
            try:
                logo_path = os.path.join(base_path, logo_filename)
                if not os.path.exists(logo_path):
                    print(f"Warning: Logo file not found: {logo_path} for {team_data['name']}")
                    continue
                logo_surf_original = pygame.image.load(logo_path).convert_alpha()
                scaled_gameplay_logo = scale_logo(logo_surf_original, gameplay_logo_max_dim)
                if scaled_gameplay_logo: team_logos_surfaces[team_data["name"]] = scaled_gameplay_logo
                else: print(f"Warning: Could not scale gameplay logo for {team_data['name']}")

                scaled_select_logo = scale_logo(logo_surf_original, team_select_preview_max_dim)
                if scaled_select_logo: team_select_logo_surfaces[team_data["name"]] = scaled_select_logo
                else:
                    team_select_logo_surfaces[team_data["name"]] = scaled_gameplay_logo
                    if not scaled_gameplay_logo: print(f"Warning: Could not scale team select logo for {team_data['name']}")
            except Exception as e: print(f"Error loading logo for {team_data['name']}: {e}")
load_all_team_logos()

# --- Game State Variables ---
game_state = "START_SCREEN"
game_mode = None 
player1_team_data = NBA_TEAMS_LIST[0]
player2_team_data = NBA_TEAMS_LIST[1] if len(NBA_TEAMS_LIST) > 1 else NBA_TEAMS_LIST[0]
home_court_team_data = None
p1_selection_index = 0
p2_selection_index = 1 if len(NBA_TEAMS_LIST) > 1 else 0


# --- Username and Leaderboard ---
player1_username = ""
player2_username = "" 
username_input_active = False 
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50)
LEADERBOARD_FILE = "leaderboard.json"
leaderboard_data = []
leaderboard_view_mode = "1P" 

# --- "On Fire" State Variables ---
player1_fire_streak_scores = 0
player1_fire_streak_timer_start_time = 0
player1_is_on_fire = False
player2_fire_streak_scores = 0 
player2_fire_streak_timer_start_time = 0 
player2_is_on_fire = False 
flame_particles = [] # New: For the flame particle effect


def load_leaderboard():
    global leaderboard_data
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                leaderboard_data = json.load(f)
        else:
            leaderboard_data = []
    except Exception as e:
        print(f"Error loading leaderboard: {e}")
        leaderboard_data = []

def save_score_to_leaderboard():
    global leaderboard_data, player1_username, player2_username, player1_score, player2_score, selected_difficulty, game_mode, player1_team_data, player2_team_data
    
    entry = {
        "username": player1_username.strip() if player1_username.strip() else "Player 1",
        "p1_score": player1_score,
        "p2_score": player2_score,
        "difficulty": selected_difficulty if game_mode == "1P" else "N/A_2P", 
        "p1_team": player1_team_data["name"] if player1_team_data else "N/A",
        "p2_team": player2_team_data["name"] if player2_team_data else "N/A",
        "mode": game_mode, 
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if game_mode == "2P":
        entry["player2_username"] = player2_username.strip() if player2_username.strip() else "Player 2"

    leaderboard_data.append(entry)
    leaderboard_data.sort(key=lambda x: (x.get("p1_score", 0), x.get("timestamp", "")), reverse=True)
    leaderboard_data = leaderboard_data[:20] 
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard_data, f, indent=4)
    except Exception as e:
        print(f"Error saving leaderboard: {e}")

load_leaderboard()

# --- Game Objects ---
paddle1_rect, paddle2_rect = None, None
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_speed = [0,0]
player1_score, player2_score = 0, 0

# --- Timekeeping ---
QUARTER_DURATION_SECONDS = 60 
current_quarter = 1
quarter_time_remaining_ms = QUARTER_DURATION_SECONDS * 1000
game_paused_for_quarter_break = False
game_over_flag = False
winner_message = ""

# --- UI Helper ---
def draw_text_with_glow(text, font, main_color, glow_color, surface, x, y, center=True, glow_offset=1):
    offsets = []
    for i in range(-glow_offset, glow_offset + 1):
        for j in range(-glow_offset, glow_offset + 1):
            if i != 0 or j != 0:
                offsets.append((i,j))

    text_surf_main = font.render(text, True, main_color)
    text_rect = text_surf_main.get_rect()

    if center: text_rect.center = (x,y)
    else: text_rect.topleft = (x,y)

    for off_x, off_y in offsets:
        glow_surf = font.render(text, True, glow_color)
        surface.blit(glow_surf, (text_rect.x + off_x, text_rect.y + off_y))

    surface.blit(text_surf_main, text_rect)
    return text_rect


def draw_text(text, font, color, surface, x, y, center=True):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center: textrect.center = (x,y)
    else: textrect.topleft = (x,y)
    surface.blit(textobj, textrect)
    return textrect

# --- Paddle Size Update Function ---
def update_paddle_sizes():
    global paddle1_rect, paddle2_rect, player1_is_on_fire, player2_is_on_fire, PADDLE_HEIGHT, SCREEN_HEIGHT, screen

    if paddle1_rect:
        old_p1_centery = paddle1_rect.centery
        if player2_is_on_fire:  
            paddle1_rect.height = PADDLE_HEIGHT / 2
        else:
            paddle1_rect.height = PADDLE_HEIGHT
        paddle1_rect.centery = old_p1_centery
        paddle1_rect.clamp_ip(screen.get_rect()) 

    if paddle2_rect:
        old_p2_centery = paddle2_rect.centery
        if player1_is_on_fire:  
            paddle2_rect.height = PADDLE_HEIGHT / 2
        else:
            paddle2_rect.height = PADDLE_HEIGHT
        paddle2_rect.centery = old_p2_centery
        paddle2_rect.clamp_ip(screen.get_rect()) 


# --- Game Initialization ---
def initialize_game_elements(full_reset=True):
    global paddle1_rect, paddle2_rect, ball_pos, ball_speed, player1_score, player2_score, home_court_team_data
    global actual_initial_ball_speed_x, actual_initial_ball_speed_y
    global current_quarter, quarter_time_remaining_ms, game_paused_for_quarter_break, game_over_flag, winner_message
    global ball_trail_positions, ball_rotation_angle, flame_particles # Added flame_particles
    global player1_fire_streak_scores, player1_fire_streak_timer_start_time, player1_is_on_fire
    global player2_fire_streak_scores, player2_fire_streak_timer_start_time, player2_is_on_fire
    global player1_username, player2_username 

    if full_reset:
        player1_username = ""
        player2_username = ""

    player1_fire_streak_scores = 0
    player1_fire_streak_timer_start_time = 0
    player1_is_on_fire = False
    player2_fire_streak_scores = 0
    player2_fire_streak_timer_start_time = 0
    player2_is_on_fire = False
    flame_particles.clear() # New: Clear flame particles on reset

    ball_trail_positions = []
    ball_rotation_angle = 0

    paddle1_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddle2_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddle1_rect = pygame.Rect(50, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2_rect = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    update_paddle_sizes() 

    if game_mode == "1P":
        multiplier = DIFFICULTY_SETTINGS[selected_difficulty]["ball_speed_multiplier"]
    else: 
        multiplier = DIFFICULTY_SETTINGS["NORMAL"]["ball_speed_multiplier"]

    actual_initial_ball_speed_x = BASE_BALL_SPEED_X * multiplier
    actual_initial_ball_speed_y = BASE_BALL_SPEED_Y * multiplier

    reset_ball_gameplay()
    player1_score, player2_score = 0, 0

    if player1_team_data and player2_team_data:
        home_court_team_data = random.choice([player1_team_data, player2_team_data])
    elif player1_team_data:
        home_court_team_data = player1_team_data
    elif player2_team_data:
        home_court_team_data = player2_team_data
    else:
        home_court_team_data = NBA_TEAMS_LIST[0] if NBA_TEAMS_LIST else None

    current_quarter, quarter_time_remaining_ms = 1, QUARTER_DURATION_SECONDS * 1000
    game_paused_for_quarter_break, game_over_flag, winner_message = False, False, ""


# --- Gameplay Functions ---
def draw_court():
    if home_court_team_data:
        screen.fill(home_court_team_data["primary"])
        line_color = home_court_team_data["secondary"]

        r1, g1, b1 = home_court_team_data["primary"]
        r2, g2, b2 = home_court_team_data["secondary"]
        circle_outline_color = line_color

        primary_brightness = r1 + g1 + b1
        secondary_brightness = r2 + g2 + b2

        if abs(primary_brightness - secondary_brightness) < 150: 
            line_color = WHITE
            if primary_brightness > (255*3*0.6): 
                circle_outline_color = BLACK
            else: 
                circle_outline_color = WHITE

        pygame.draw.circle(screen, circle_outline_color, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CENTER_CIRCLE_RADIUS, 3)

        team_name = home_court_team_data["name"]
        if team_name in team_logos_surfaces:
            logo_surface = team_logos_surfaces[team_name]
            screen.blit(logo_surface, logo_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

        pygame.draw.line(screen, line_color, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 3)
    elif home_court_team_data is None and NBA_TEAMS_LIST: 
        screen.fill(BLACK)
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), CENTER_CIRCLE_RADIUS, 3)
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 3)
    else: 
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT), 3)


def draw_paddles_gameplay():
    if not paddle1_rect or not paddle2_rect: return

    shadow_rect_p1_offset = paddle1_rect.move(SHADOW_OFFSET_X, SHADOW_OFFSET_Y)
    shadow_surf_p1 = pygame.Surface((paddle1_rect.width, paddle1_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf_p1, SHADOW_COLOR, shadow_surf_p1.get_rect(), 0, PADDLE_BORDER_RADIUS)
    screen.blit(shadow_surf_p1, shadow_rect_p1_offset.topleft)

    if player1_is_on_fire:
        pygame.draw.rect(screen, ON_FIRE_PADDLE_COLOR, paddle1_rect,0, PADDLE_BORDER_RADIUS)
        pygame.draw.rect(screen, ON_FIRE_PADDLE_BORDER_COLOR, paddle1_rect, 3, PADDLE_BORDER_RADIUS)
    elif player1_team_data:
        pygame.draw.rect(screen, player1_team_data["primary"], paddle1_rect,0, PADDLE_BORDER_RADIUS)
        pygame.draw.rect(screen, player1_team_data["secondary"], paddle1_rect, 3, PADDLE_BORDER_RADIUS)
    else:
        pygame.draw.rect(screen, WHITE, paddle1_rect,0, PADDLE_BORDER_RADIUS)

    shadow_rect_p2_offset = paddle2_rect.move(SHADOW_OFFSET_X, SHADOW_OFFSET_Y)
    shadow_surf_p2 = pygame.Surface((paddle2_rect.width, paddle2_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf_p2, SHADOW_COLOR, shadow_surf_p2.get_rect(), 0, PADDLE_BORDER_RADIUS)
    screen.blit(shadow_surf_p2, shadow_rect_p2_offset.topleft)

    if player2_is_on_fire: 
        pygame.draw.rect(screen, ON_FIRE_PADDLE_COLOR, paddle2_rect,0, PADDLE_BORDER_RADIUS)
        pygame.draw.rect(screen, ON_FIRE_PADDLE_BORDER_COLOR, paddle2_rect, 3, PADDLE_BORDER_RADIUS)
    elif player2_team_data:
        pygame.draw.rect(screen, player2_team_data["primary"], paddle2_rect,0, PADDLE_BORDER_RADIUS)
        pygame.draw.rect(screen, player2_team_data["secondary"], paddle2_rect, 3, PADDLE_BORDER_RADIUS)
    else:
        pygame.draw.rect(screen, WHITE, paddle2_rect,0, PADDLE_BORDER_RADIUS)

def draw_ball():
    global ball_trail_positions, ball_rotation_angle, scaled_ball_image, flame_particles
    global player1_is_on_fire, player2_is_on_fire, scaled_fireball_image

    is_either_player_on_fire = player1_is_on_fire or player2_is_on_fire

    # Draw Ball Trail
    for i, pos_tuple in enumerate(ball_trail_positions):
        trail_pos_x, trail_pos_y = pos_tuple
        alpha = max(0, int(150 * (i / BALL_TRAIL_LENGTH))) 
        trail_color_base = FIRE_AURA_COLORS[1][:3] if is_either_player_on_fire else BASKETBALL_ORANGE
        radius_factor = (i / BALL_TRAIL_LENGTH)
        trail_radius = int(BALL_RADIUS * (0.3 + 0.7 * radius_factor)) 

        if trail_radius > 0:
            trail_surf = pygame.Surface((trail_radius * 2, trail_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (*trail_color_base, alpha), (trail_radius, trail_radius), trail_radius)
            screen.blit(trail_surf, (int(trail_pos_x - trail_radius), int(trail_pos_y - trail_radius)))

    # Draw Ball Shadow
    shadow_center_x = int(ball_pos[0] + SHADOW_OFFSET_X)
    shadow_center_y = int(ball_pos[1] + SHADOW_OFFSET_Y)
    
    current_ball_effective_radius = BALL_RADIUS
    if is_either_player_on_fire:
        if scaled_fireball_image: current_ball_effective_radius = BALL_RADIUS - 4 
        else: current_ball_effective_radius = BALL_RADIUS + 4 
            
    shadow_radius_eff = current_ball_effective_radius
    temp_shadow_surf_size = shadow_radius_eff * 2 + 4 
    temp_shadow_surf = pygame.Surface((temp_shadow_surf_size, temp_shadow_surf_size), pygame.SRCALPHA)
    pygame.draw.circle(temp_shadow_surf, SHADOW_COLOR,
                       (temp_shadow_surf_size // 2, temp_shadow_surf_size // 2),
                       shadow_radius_eff)
    blit_pos_x = shadow_center_x - (temp_shadow_surf_size // 2)
    blit_pos_y = shadow_center_y - (temp_shadow_surf_size // 2)
    screen.blit(temp_shadow_surf, (blit_pos_x, blit_pos_y))

    # Determine which ball image to use or if aura/particle fallback
    current_ball_to_draw = scaled_ball_image 
    use_flame_effect = False # Controls particle/aura drawing

    if is_either_player_on_fire:
        if scaled_fireball_image:
            current_ball_to_draw = scaled_fireball_image
            # Optionally, still draw some particles even with fireball image for more effect
            # use_flame_effect = True 
        else: 
            use_flame_effect = True # Use particles/aura if no fireball image
            current_ball_to_draw = scaled_ball_image # Draw normal ball under flames

    # --- Flame Particle Effect ---
    if use_flame_effect:
        current_time_ms = pygame.time.get_ticks()
        
        # Generate new particles
        if len(flame_particles) < MAX_FLAME_PARTICLES:
            for _ in range(FLAME_PARTICLES_PER_FRAME):
                angle = random.uniform(0, 2 * math.pi)
                # Start particles slightly inside the ball for a better "emanating" look
                radius_offset = BALL_RADIUS * random.uniform(0.5, 0.9) 
                start_x = ball_pos[0] + math.cos(angle) * radius_offset
                start_y = ball_pos[1] + math.sin(angle) * radius_offset
                
                # Velocity: mostly upwards, some spread
                vel_x = random.uniform(-0.8, 0.8) 
                vel_y = random.uniform(-1.5, -0.5) # Stronger upward motion
                
                # Lifetime in frames (e.g., 0.3 to 0.8 seconds)
                life = random.randint(int(FPS * 0.3), int(FPS * 0.8)) 
                
                color = random.choice(FLAME_PARTICLE_COLORS)
                size = random.randint(3, 7) # Slightly larger particles for more visual impact
                flame_particles.append({'pos': [start_x, start_y], 
                                        'vel': [vel_x, vel_y], 
                                        'life': life, 
                                        'max_life': life, # Store max_life for alpha calculation
                                        'color': color, 
                                        'size': size})
        
        # Update and draw existing particles
        for i in range(len(flame_particles) -1, -1, -1): # Iterate backwards for safe removal
            p = flame_particles[i]
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]
            p['life'] -= 1
            
            if p['life'] <= 0:
                flame_particles.pop(i)
            else:
                # Fade out: alpha decreases as life diminishes
                alpha = int(255 * (p['life'] / p['max_life'])) 
                # Make particles shrink slightly as they die
                current_size = int(p['size'] * (p['life'] / p['max_life']))
                if current_size < 1: current_size = 1

                # Create a temporary surface for each particle to handle alpha
                particle_surf = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
                # Draw ellipse for a more flame-like shape
                pygame.draw.ellipse(particle_surf, (*p['color'], alpha), particle_surf.get_rect())
                screen.blit(particle_surf, (int(p['pos'][0] - current_size), int(p['pos'][1] - current_size)))

    # Draw the Ball (Image or Fallback Circle)
    if current_ball_to_draw:
        rotated_ball_image = pygame.transform.rotate(current_ball_to_draw, -ball_rotation_angle)
        ball_rect = rotated_ball_image.get_rect(center=(int(ball_pos[0]), int(ball_pos[1])))
        screen.blit(rotated_ball_image, ball_rect.topleft)
    elif not use_flame_effect: # Only draw default circle if not on fire AND no ball image
        pygame.draw.circle(screen, BASKETBALL_ORANGE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
        rad_angle = math.radians(ball_rotation_angle)
        x1 = ball_pos[0] + BALL_RADIUS * math.cos(rad_angle); y1 = ball_pos[1] + BALL_RADIUS * math.sin(rad_angle)
        x2 = ball_pos[0] - BALL_RADIUS * math.cos(rad_angle); y2 = ball_pos[1] - BALL_RADIUS * math.sin(rad_angle)
        pygame.draw.line(screen, BLACK, (int(x1), int(y1)), (int(x2), int(y2)), 1)
        rad_angle_perp = math.radians(ball_rotation_angle + 90)
        x3 = ball_pos[0] + BALL_RADIUS * math.cos(rad_angle_perp); y3 = ball_pos[1] + BALL_RADIUS * math.sin(rad_angle_perp)
        x4 = ball_pos[0] - BALL_RADIUS * math.cos(rad_angle_perp); y4 = ball_pos[1] - BALL_RADIUS * math.sin(rad_angle_perp)
        pygame.draw.line(screen, BLACK, (int(x3), int(y3)), (int(x4), int(y4)), 1)
    # If on fire without image, the particles are the main visual, default ball circle isn't drawn unless specified


def draw_on_fire_message():
    global player1_is_on_fire, player2_is_on_fire, ON_FIRE_FONT
    message_text = ""
    if player1_is_on_fire:
        message_text = "PLAYER 1 IS ON FIRE!"
    elif player2_is_on_fire:
        if game_mode == "1P": message_text = "CPU IS ON FIRE!"
        else: message_text = f"{player2_username.upper() if player2_username.strip() else 'PLAYER 2'} IS ON FIRE!"

    if message_text:
        main_color = (255, 80, 0) 
        glow_color = (255, 255, 50) 
        message_y = ON_FIRE_FONT.get_height() // 2 + 5 
        draw_text_with_glow(message_text, ON_FIRE_FONT, main_color, glow_color, screen, SCREEN_WIDTH // 2, message_y, center=True, glow_offset=2)


def draw_scores_and_names_gameplay():
    text_color_scores = WHITE
    if home_court_team_data and sum(home_court_team_data["primary"]) > (255*3 * 0.65) : 
        text_color_scores = BLACK

    p1_display_name = player1_username.strip() if player1_username.strip() else "PLAYER 1"
    p1_team_name_str = player1_team_data['name'] if player1_team_data else "Team 1"

    score_box_y_offset = 0
    if player1_is_on_fire or player2_is_on_fire: 
        try: score_box_y_offset = ON_FIRE_FONT.get_height() + 10 
        except AttributeError: score_box_y_offset = 40

    score1_text_surf = SCORE_FONT.render(str(player1_score), True, text_color_scores)
    score1_bg_w = score1_text_surf.get_width() + 20
    score1_bg_h = score1_text_surf.get_height() + 10
    score1_bg_surf = pygame.Surface((score1_bg_w, score1_bg_h), pygame.SRCALPHA); score1_bg_surf.fill((0,0,0,120)) 
    screen.blit(score1_bg_surf, (SCREEN_WIDTH // 4 - score1_bg_w // 2, 15 + score_box_y_offset))
    screen.blit(score1_text_surf, (SCREEN_WIDTH // 4 - score1_text_surf.get_width() // 2, 20 + score_box_y_offset))

    p1_name_y = 60 + score_box_y_offset
    p1_main_text_color = player1_team_data["primary"] if player1_team_data else WHITE
    if player1_is_on_fire: p1_main_text_color = ON_FIRE_PADDLE_COLOR
    p1_glow_color = WHITE
    draw_text_with_glow(f"{p1_display_name} ({p1_team_name_str})", TEAM_NAME_FONT, p1_main_text_color, p1_glow_color, screen, SCREEN_WIDTH // 4, p1_name_y, True, 1)

    if game_mode == "1P": p2_display_name = "CPU"
    else: p2_display_name = player2_username.strip() if player2_username.strip() else "PLAYER 2"
    p2_team_name_str = player2_team_data['name'] if player2_team_data else "Team 2"

    score2_text_surf = SCORE_FONT.render(str(player2_score), True, text_color_scores)
    score2_bg_w = score2_text_surf.get_width() + 20
    score2_bg_h = score2_text_surf.get_height() + 10
    score2_bg_surf = pygame.Surface((score2_bg_w, score2_bg_h), pygame.SRCALPHA); score2_bg_surf.fill((0,0,0,120))
    screen.blit(score2_bg_surf, (SCREEN_WIDTH * 3 // 4 - score2_bg_w // 2, 15 + score_box_y_offset))
    screen.blit(score2_text_surf, (SCREEN_WIDTH * 3 // 4 - score2_text_surf.get_width() // 2, 20 + score_box_y_offset))

    p2_name_y = 60 + score_box_y_offset
    p2_main_text_color = player2_team_data["primary"] if player2_team_data else WHITE
    if player2_is_on_fire: p2_main_text_color = ON_FIRE_PADDLE_COLOR
    p2_glow_color = WHITE
    draw_text_with_glow(f"{p2_display_name} ({p2_team_name_str})", TEAM_NAME_FONT, p2_main_text_color, p2_glow_color, screen, SCREEN_WIDTH * 3 // 4, p2_name_y, True, 1)


def draw_game_timer_and_quarter():
    y_offset = 0 
    if player1_is_on_fire or player2_is_on_fire:
        try: y_offset = ON_FIRE_FONT.get_height() + 10
        except AttributeError: y_offset = 40

    timer_bg_w, timer_bg_h = 200, 75
    timer_bg_x, timer_bg_y = SCREEN_WIDTH//2 - timer_bg_w//2, 15 + y_offset
    timer_bg_surf = pygame.Surface((timer_bg_w, timer_bg_h), pygame.SRCALPHA)
    timer_bg_surf.fill((0,0,0,180)) 
    screen.blit(timer_bg_surf, (timer_bg_x, timer_bg_y))
    pygame.draw.rect(screen, (200,0,0), (timer_bg_x,timer_bg_y,timer_bg_w,timer_bg_h), 3, 5) 

    seconds_total = max(0, quarter_time_remaining_ms) // 1000
    minutes = seconds_total // 60
    seconds = seconds_total % 60
    time_surface = GAME_CLOCK_FONT.render(f"{minutes:02}:{seconds:02}", True, (255, 0, 0)) 
    screen.blit(time_surface, time_surface.get_rect(center=(SCREEN_WIDTH//2, timer_bg_y + timer_bg_h * 0.4)))

    quarter_surface = QUARTER_DISPLAY_FONT.render(f"QTR: {current_quarter}", True, WHITE)
    screen.blit(quarter_surface, quarter_surface.get_rect(center=(SCREEN_WIDTH//2, timer_bg_y + timer_bg_h * 0.78)))


def reset_ball_gameplay():
    global ball_pos, ball_speed, ball_trail_positions, ball_rotation_angle, flame_particles # Added flame_particles
    global player1_is_on_fire, player2_is_on_fire 

    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    current_base_x_speed = actual_initial_ball_speed_x
    current_base_y_speed = actual_initial_ball_speed_y

    if player1_is_on_fire or player2_is_on_fire: 
        current_base_x_speed *= ON_FIRE_BALL_SPEED_MULTIPLIER
        current_base_y_speed *= ON_FIRE_BALL_SPEED_MULTIPLIER

    ball_speed = [random.choice([current_base_x_speed, -current_base_x_speed]),
                  random.choice([current_base_y_speed, -current_base_y_speed])]

    ball_trail_positions = [] 
    ball_rotation_angle = 0
    # flame_particles.clear() # Clear here too, or rely on "on fire" status change to clear


def move_ball_gameplay():
    global player1_score, player2_score, ball_pos, ball_speed, ball_trail_positions, ball_rotation_angle, flame_particles
    global player1_is_on_fire, player1_fire_streak_scores, player1_fire_streak_timer_start_time
    global player2_is_on_fire, player2_fire_streak_scores, player2_fire_streak_timer_start_time 

    if game_paused_for_quarter_break or game_over_flag: return

    if ball_speed[0] != 0 or ball_speed[1] != 0: 
        ball_rotation_angle = (ball_rotation_angle + BALL_ROTATION_SPEED) % 360

    ball_trail_positions.append((ball_pos[0], ball_pos[1]))
    if len(ball_trail_positions) > BALL_TRAIL_LENGTH:
        ball_trail_positions.pop(0)

    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    if not (BALL_RADIUS <= ball_pos[1] <= SCREEN_HEIGHT - BALL_RADIUS):
        ball_speed[1] *= -1
        ball_pos[1] = max(BALL_RADIUS, min(ball_pos[1], SCREEN_HEIGHT - BALL_RADIUS)) 

    ball_collision_rect = pygame.Rect(ball_pos[0]-BALL_RADIUS, ball_pos[1]-BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
    paddles_to_check = [(paddle1_rect, 1), (paddle2_rect, -1)] 

    for pad_rect, direction_multiplier in paddles_to_check:
        if pad_rect and ball_collision_rect.colliderect(pad_rect):
            if (ball_speed[0] * direction_multiplier < 0): 
                ball_speed[0] *= -1.05 
                if direction_multiplier == 1 : ball_pos[0] = pad_rect.right + BALL_RADIUS
                else: ball_pos[0] = pad_rect.left - BALL_RADIUS

                delta_y = ball_pos[1] - pad_rect.centery
                normalized_hit_pos = delta_y / (pad_rect.height / 2.0) if pad_rect.height > 0 else 0
                normalized_hit_pos = max(-1.0, min(normalized_hit_pos, 1.0)) 
                max_y_deflection_speed = actual_initial_ball_speed_y * 1.7 
                if (player1_is_on_fire and pad_rect == paddle1_rect) or \
                   (player2_is_on_fire and pad_rect == paddle2_rect):
                    max_y_deflection_speed *= ON_FIRE_BALL_SPEED_MULTIPLIER
                
                ball_speed[1] = normalized_hit_pos * max_y_deflection_speed
                if ball_bounce_sound: ball_bounce_sound.play()
                break 

    scored = False
    current_time_ms = pygame.time.get_ticks() 

    if ball_pos[0] - BALL_RADIUS <= 0: 
        player2_score += 1
        if cheering_sound: cheering_sound.play()
        if player1_is_on_fire: 
            player1_is_on_fire = False
            flame_particles.clear() # Clear P1 flames
        player1_fire_streak_scores = 0 
        player1_fire_streak_timer_start_time = 0

        if not player2_is_on_fire: 
            if player2_fire_streak_scores == 0: 
                player2_fire_streak_timer_start_time = current_time_ms
                player2_fire_streak_scores = 1
            else: 
                if (current_time_ms - player2_fire_streak_timer_start_time) <= FIRE_STREAK_TIME_WINDOW_MS:
                    player2_fire_streak_scores += 1
                else: 
                    player2_fire_streak_timer_start_time = current_time_ms
                    player2_fire_streak_scores = 1
            
            if player2_fire_streak_scores >= FIRE_STREAK_GOAL_COUNT and \
               (current_time_ms - player2_fire_streak_timer_start_time) <= FIRE_STREAK_TIME_WINDOW_MS:
                player2_is_on_fire = True
                # flame_particles.clear() # Ensure fresh particles for P2 if any old ones existed
                player2_fire_streak_scores = 0 
                player2_fire_streak_timer_start_time = 0
        else: 
            player2_fire_streak_scores = 0
            player2_fire_streak_timer_start_time = 0
        scored = True

    elif ball_pos[0] + BALL_RADIUS >= SCREEN_WIDTH: 
        player1_score += 1
        if cheering_sound: cheering_sound.play()
        if player2_is_on_fire: 
            player2_is_on_fire = False
            flame_particles.clear() # Clear P2 flames
        player2_fire_streak_scores = 0 
        player2_fire_streak_timer_start_time = 0
        
        if not player1_is_on_fire:
            if player1_fire_streak_scores == 0:
                player1_fire_streak_timer_start_time = current_time_ms
                player1_fire_streak_scores = 1
            else:
                if (current_time_ms - player1_fire_streak_timer_start_time) <= FIRE_STREAK_TIME_WINDOW_MS:
                    player1_fire_streak_scores += 1
                else:
                    player1_fire_streak_timer_start_time = current_time_ms
                    player1_fire_streak_scores = 1
            
            if player1_fire_streak_scores >= FIRE_STREAK_GOAL_COUNT and \
               (current_time_ms - player1_fire_streak_timer_start_time) <= FIRE_STREAK_TIME_WINDOW_MS:
                player1_is_on_fire = True
                # flame_particles.clear() # Ensure fresh particles for P1
                player1_fire_streak_scores = 0
                player1_fire_streak_timer_start_time = 0
        else: 
            player1_fire_streak_scores = 0
            player1_fire_streak_timer_start_time = 0
        scored = True

    if scored:
        update_paddle_sizes() 
        reset_ball_gameplay()

def move_paddles_gameplay(keys_pressed):
    global player1_is_on_fire, player2_is_on_fire 

    if game_paused_for_quarter_break or game_over_flag or not paddle1_rect or not paddle2_rect: return

    effective_player1_paddle_speed = PLAYER_PADDLE_SPEED
    if player1_is_on_fire: effective_player1_paddle_speed += ON_FIRE_PADDLE_SPEED_BOOST
    if keys_pressed[pygame.K_w] and paddle1_rect.top > 0: paddle1_rect.y -= effective_player1_paddle_speed
    if keys_pressed[pygame.K_s] and paddle1_rect.bottom < SCREEN_HEIGHT: paddle1_rect.y += effective_player1_paddle_speed

    if game_mode == "2P": 
        effective_player2_paddle_speed = PLAYER_PADDLE_SPEED
        if player2_is_on_fire: effective_player2_paddle_speed += ON_FIRE_PADDLE_SPEED_BOOST
        if keys_pressed[pygame.K_UP] and paddle2_rect.top > 0: paddle2_rect.y -= effective_player2_paddle_speed
        if keys_pressed[pygame.K_DOWN] and paddle2_rect.bottom < SCREEN_HEIGHT: paddle2_rect.y += effective_player2_paddle_speed
    else: 
        ai_settings = DIFFICULTY_SETTINGS[selected_difficulty]
        current_ai_paddle_speed = ai_settings["ai_paddle_speed"]
        if player2_is_on_fire: current_ai_paddle_speed += ON_FIRE_PADDLE_SPEED_BOOST
        ai_reaction_factor = ai_settings["ai_speed_factor"] 
        target_y = ball_pos[1] 
        if ball_speed[0] > 0: 
            time_to_reach_paddle = (paddle2_rect.centerx - ball_pos[0]) / ball_speed[0] if ball_speed[0] != 0 else float('inf')
            if 0 < time_to_reach_paddle < (SCREEN_WIDTH / abs(ball_speed[0] if ball_speed[0] != 0 else 1)) * 0.75 :
                predicted_y_at_paddle = ball_pos[1] + ball_speed[1] * time_to_reach_paddle
                target_y = ball_pos[1] * (1 - ai_reaction_factor) + predicted_y_at_paddle * ai_reaction_factor
        
        movement_diff = target_y - paddle2_rect.centery
        error_offset = 0
        current_paddle2_height = paddle2_rect.height if paddle2_rect.height > 0 else PADDLE_HEIGHT
        if selected_difficulty == "EASY": error_offset = current_paddle2_height * 0.3 * random.uniform(-1, 1)
        elif selected_difficulty == "NORMAL": error_offset = current_paddle2_height * 0.15 * random.uniform(-1, 1)
        movement_diff += error_offset
        move_amount = movement_diff * 0.1 
        if abs(move_amount) > current_ai_paddle_speed: 
            move_amount = current_ai_paddle_speed if move_amount > 0 else -current_ai_paddle_speed
        paddle2_rect.y += move_amount

    paddle1_rect.clamp_ip(screen.get_rect())
    paddle2_rect.clamp_ip(screen.get_rect())

def update_game_time():
    global quarter_time_remaining_ms, current_quarter, game_paused_for_quarter_break, game_over_flag, winner_message, ball_speed, flame_particles
    global player1_is_on_fire, player1_fire_streak_scores, player1_fire_streak_timer_start_time
    global player2_is_on_fire, player2_fire_streak_scores, player2_fire_streak_timer_start_time

    if game_over_flag or game_paused_for_quarter_break: return

    current_time_ms = pygame.time.get_ticks()
    delta_time_ms = clock.get_time() 
    quarter_time_remaining_ms -= delta_time_ms

    if player1_fire_streak_scores > 0 and not player1_is_on_fire:
        if (current_time_ms - player1_fire_streak_timer_start_time) > FIRE_STREAK_TIME_WINDOW_MS:
            player1_fire_streak_scores = 0
            player1_fire_streak_timer_start_time = 0

    if player2_fire_streak_scores > 0 and not player2_is_on_fire:
        if (current_time_ms - player2_fire_streak_timer_start_time) > FIRE_STREAK_TIME_WINDOW_MS:
            player2_fire_streak_scores = 0
            player2_fire_streak_timer_start_time = 0

    if quarter_time_remaining_ms <= 0:
        quarter_time_remaining_ms = 0
        ball_speed = [0,0] 

        if current_quarter < 4:
            current_quarter += 1
            quarter_time_remaining_ms = QUARTER_DURATION_SECONDS * 1000
            game_paused_for_quarter_break = True
            player1_is_on_fire = False; player1_fire_streak_scores = 0; player1_fire_streak_timer_start_time = 0
            player2_is_on_fire = False; player2_fire_streak_scores = 0; player2_fire_streak_timer_start_time = 0
            flame_particles.clear() # Clear flames at quarter break
            update_paddle_sizes() 
        else: 
            game_over_flag = True
            p1_name_display = player1_username.strip() if player1_username.strip() else (player1_team_data.get('name', "Player 1") if player1_team_data else "Player 1")
            if game_mode == "1P": p2_name_display = "CPU"
            else: p2_name_display = player2_username.strip() if player2_username.strip() else (player2_team_data.get('name', "Player 2") if player2_team_data else "Player 2")

            if player1_score > player2_score: winner_message = f"{p1_name_display.upper()} WINS!"
            elif player2_score > player1_score: winner_message = f"{p2_name_display.upper()} WINS!"
            else: winner_message = "IT'S A TIE!"
            
            save_score_to_leaderboard()
            player1_is_on_fire = False; player1_fire_streak_scores = 0; player1_fire_streak_timer_start_time = 0
            player2_is_on_fire = False; player2_fire_streak_scores = 0; player2_fire_streak_timer_start_time = 0
            flame_particles.clear() # Clear flames at game over
            update_paddle_sizes()

# --- Main Loop ---
running = True
while running:
    mouse_clicked = False
    mouse_pos = pygame.mouse.get_pos()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            mouse_clicked = True

        if game_state == "USERNAME_INPUT":
            if event.type == pygame.KEYDOWN:
                if username_input_active:
                    if event.key == pygame.K_RETURN:
                        if not player1_username.strip(): player1_username = "Player 1" 
                        username_input_active = False
                        if game_mode == "1P": 
                            game_state = "DIFFICULTY_SELECT"
                        else: 
                            game_state = "TEAM_SELECT_P1"
                    elif event.key == pygame.K_BACKSPACE: player1_username = player1_username[:-1]
                    elif len(player1_username) < 15 and event.unicode.isprintable(): player1_username += event.unicode
            if mouse_clicked: username_input_active = input_box.collidepoint(mouse_pos)
        
        elif game_state == "USERNAME_INPUT_P2":
            if event.type == pygame.KEYDOWN:
                if username_input_active:
                    if event.key == pygame.K_RETURN:
                        if not player2_username.strip(): player2_username = "Player 2" 
                        username_input_active = False
                        game_state = "TEAM_SELECT_P2"
                    elif event.key == pygame.K_BACKSPACE: player2_username = player2_username[:-1]
                    elif len(player2_username) < 15 and event.unicode.isprintable(): player2_username += event.unicode
            if mouse_clicked: username_input_active = input_box.collidepoint(mouse_pos)

        elif game_state in ("TEAM_SELECT_P1", "TEAM_SELECT_P2"):
            if event.type == pygame.KEYDOWN and NBA_TEAMS_LIST:
                # Handle team cycling
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    idx_ref_str = "p1_selection_index" if game_state == "TEAM_SELECT_P1" else "p2_selection_index"
                    current_idx = globals()[idx_ref_str]
                    if event.key == pygame.K_LEFT: current_idx = (current_idx - 1 + len(NBA_TEAMS_LIST)) % len(NBA_TEAMS_LIST)
                    elif event.key == pygame.K_RIGHT: current_idx = (current_idx + 1) % len(NBA_TEAMS_LIST)
                    globals()[idx_ref_str] = current_idx
                    if game_state == "TEAM_SELECT_P1":
                        player1_team_data = NBA_TEAMS_LIST[p1_selection_index]
                    else:
                        player2_team_data = NBA_TEAMS_LIST[p2_selection_index]
                
                # Handle confirmation
                elif event.key == pygame.K_RETURN:
                    if game_state == "TEAM_SELECT_P1":
                        if game_mode == "1P":
                            game_state = "TEAM_SELECT_P2"
                            if p1_selection_index == p2_selection_index and len(NBA_TEAMS_LIST) > 1:
                                p2_selection_index = (p1_selection_index + 1) % len(NBA_TEAMS_LIST)
                                player2_team_data = NBA_TEAMS_LIST[p2_selection_index]
                        else: # 2P mode
                            game_state = "USERNAME_INPUT_P2"
                            player2_username = ""
                            username_input_active = True
                    elif game_state == "TEAM_SELECT_P2":
                        if not (game_mode == "2P" and p1_selection_index == p2_selection_index and len(NBA_TEAMS_LIST) > 1):
                            initialize_game_elements(full_reset=False) 
                            game_state = "GAMEPLAY"; game_paused_for_quarter_break = True
        
        elif game_state == "GAMEPLAY":
            if event.type == pygame.KEYDOWN:
                if game_over_flag:
                    if event.key == pygame.K_RETURN: 
                        initialize_game_elements(full_reset=False) 
                        game_state = "GAMEPLAY" 
                        reset_ball_gameplay() 
                    elif event.key == pygame.K_ESCAPE: 
                        initialize_game_elements(full_reset=True) 
                        game_state = "START_SCREEN"
                elif game_paused_for_quarter_break:
                    if event.key == pygame.K_RETURN: 
                        game_paused_for_quarter_break = False
                        reset_ball_gameplay() 
                elif not game_over_flag and not game_paused_for_quarter_break: 
                    if event.key == pygame.K_ESCAPE: 
                        initialize_game_elements(full_reset=True)
                        game_state = "START_SCREEN"

    is_menu_state = game_state in ("START_SCREEN", "USERNAME_INPUT", "USERNAME_INPUT_P2", 
                                  "DIFFICULTY_SELECT", "TEAM_SELECT_P1", "TEAM_SELECT_P2", 
                                  "LEADERBOARD_SCREEN")
    if music_loaded_successfully:
        if is_menu_state:
            if not pygame.mixer.music.get_busy(): pygame.mixer.music.play(-1) 
        else: 
            if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()

    screen.fill(DARK_DESATURATED_BLUE) 

    if game_state == "START_SCREEN":
        if start_screen_wallpaper: screen.blit(start_screen_wallpaper, (0,0))
        else: screen.fill(DARK_DESATURATED_BLUE) 

        title_text_surf = CUSTOM_TITLE_FONT.render("NBA RETRO PONG", True, WHITE)
        title_bg_height = title_text_surf.get_height() + 20
        title_bg_width = title_text_surf.get_width() + 40
        title_bg_surf = pygame.Surface((title_bg_width, title_bg_height), pygame.SRCALPHA)
        title_bg_surf.fill((0,0,0,150)) 
        screen.blit(title_bg_surf,(SCREEN_WIDTH//2 - title_bg_width//2, SCREEN_HEIGHT//4 - title_bg_height//2))
        draw_text_with_glow("NBA RETRO PONG", CUSTOM_TITLE_FONT, WHITE, (50,50,50), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        btn_w, btn_h = 400, 50
        btn_spacing = 20
        btn_y_start = SCREEN_HEIGHT // 2 + 30
        btn1_rect = pygame.Rect(SCREEN_WIDTH//2-btn_w//2, btn_y_start, btn_w, btn_h)
        btn2_rect = pygame.Rect(SCREEN_WIDTH//2-btn_w//2, btn_y_start + btn_h + btn_spacing, btn_w, btn_h)
        btn3_rect = pygame.Rect(SCREEN_WIDTH//2-btn_w//2, btn_y_start + 2*(btn_h + btn_spacing), btn_w, btn_h)

        pygame.draw.rect(screen,BUTTON_HOVER_COLOR if btn1_rect.collidepoint(mouse_pos) else BUTTON_COLOR,btn1_rect,0,10)
        draw_text("1 PLAYER vs CPU",RETRO_FONT_MEDIUM,BUTTON_TEXT_COLOR,screen,btn1_rect.centerx,btn1_rect.centery)
        pygame.draw.rect(screen,BUTTON_HOVER_COLOR if btn2_rect.collidepoint(mouse_pos) else BUTTON_COLOR,btn2_rect,0,10)
        draw_text("2 PLAYERS",RETRO_FONT_MEDIUM,BUTTON_TEXT_COLOR,screen,btn2_rect.centerx,btn2_rect.centery)
        pygame.draw.rect(screen,BUTTON_HOVER_COLOR if btn3_rect.collidepoint(mouse_pos) else BUTTON_COLOR,btn3_rect,0,10)
        draw_text("LEADERBOARD",RETRO_FONT_MEDIUM,BUTTON_TEXT_COLOR,screen,btn3_rect.centerx,btn3_rect.centery)

        if mouse_clicked:
            if btn1_rect.collidepoint(mouse_pos) or btn2_rect.collidepoint(mouse_pos):
                player1_username = ""; player2_username = "" 
            if btn1_rect.collidepoint(mouse_pos):
                game_mode = "1P"; game_state = "USERNAME_INPUT"; username_input_active = True
            elif btn2_rect.collidepoint(mouse_pos):
                game_mode = "2P"; selected_difficulty="NORMAL"; game_state = "USERNAME_INPUT"; username_input_active = True
            elif btn3_rect.collidepoint(mouse_pos):
                game_state = "LEADERBOARD_SCREEN"; leaderboard_view_mode = "1P" 
            if game_state != "START_SCREEN" and game_state != "LEADERBOARD_SCREEN":
                 initialize_game_elements(full_reset=False) 
                 p1_selection_index=0
                 player1_team_data = NBA_TEAMS_LIST[p1_selection_index] if NBA_TEAMS_LIST else None
                 p2_selection_index = 1 if len(NBA_TEAMS_LIST) > 1 else 0
                 player2_team_data = NBA_TEAMS_LIST[p2_selection_index] if len(NBA_TEAMS_LIST) > p2_selection_index else (NBA_TEAMS_LIST[0] if NBA_TEAMS_LIST else None)

    elif game_state == "USERNAME_INPUT" or game_state == "USERNAME_INPUT_P2":
        prompt_text = "ENTER PLAYER 1 USERNAME" if game_state == "USERNAME_INPUT" else "ENTER PLAYER 2 USERNAME"
        current_username = player1_username if game_state == "USERNAME_INPUT" else player2_username
        draw_text_with_glow(prompt_text, CUSTOM_TITLE_FONT, RETRO_GREEN_SCREEN, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box, border_radius=5) 
        pygame.draw.rect(screen, SELECTED_TEXT_COLOR if username_input_active else BLACK, input_box, 2, border_radius=5) 
        input_surface = INPUT_FONT.render(current_username, True, INPUT_TEXT_COLOR)
        screen.blit(input_surface, (input_box.x + 10, input_box.y + (input_box.height - input_surface.get_height()) // 2))
        if username_input_active and pygame.time.get_ticks() % 1000 < 500: 
            cursor_x = input_box.x + 10 + input_surface.get_width()
            cursor_y_start = input_box.y + 5; cursor_y_end = input_box.bottom - 5
            pygame.draw.line(screen, BLACK, (cursor_x, cursor_y_start), (cursor_x, cursor_y_end), 2)
        draw_text("Press ENTER to Confirm (Max 15 Chars)", RETRO_FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, input_box.bottom + 30)
        draw_text("Click box to activate input", RETRO_FONT_SMALL, (180,180,180), screen, SCREEN_WIDTH // 2, input_box.bottom + 55)

    elif game_state == "DIFFICULTY_SELECT":
        draw_text_with_glow("SELECT DIFFICULTY", CUSTOM_TITLE_FONT, RETRO_GREEN_SCREEN, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6)
        options = ["EASY", "NORMAL", "HARD", "EXTREME"]
        btn_w, btn_h = 250, 50
        total_height_of_buttons = len(options) * btn_h + (len(options) - 1) * 15 
        start_y = SCREEN_HEIGHT // 2 - total_height_of_buttons // 2
        for i, level in enumerate(options):
            rect = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, start_y + i * (btn_h + 15), btn_w, btn_h)
            is_hovered = rect.collidepoint(mouse_pos)
            color = DIFFICULTY_BUTTON_HOVER_COLORS[level] if is_hovered else DIFFICULTY_BUTTON_COLORS[level]
            pygame.draw.rect(screen, color, rect, 0, 10) 
            text_col = BLACK if level != "EXTREME" else WHITE 
            draw_text(level, RETRO_FONT_MEDIUM, text_col, screen, rect.centerx, rect.centery)
            if mouse_clicked and is_hovered:
                selected_difficulty = level; game_state = "TEAM_SELECT_P1"
                p1_selection_index = 0
                player1_team_data = NBA_TEAMS_LIST[p1_selection_index] if NBA_TEAMS_LIST else None
                p2_selection_index = 1 if len(NBA_TEAMS_LIST) > 1 else 0
                player2_team_data = NBA_TEAMS_LIST[p2_selection_index] if len(NBA_TEAMS_LIST) > p2_selection_index else (NBA_TEAMS_LIST[0] if NBA_TEAMS_LIST else None)
                break 

    elif game_state in ("TEAM_SELECT_P1", "TEAM_SELECT_P2"):
        title_y_pos = SCREEN_HEIGHT // 7
        player_title_text = "PLAYER 1 SELECT TEAM" if game_state == "TEAM_SELECT_P1" else \
                            (f"{player2_username.upper() if player2_username.strip() else 'PLAYER 2'} SELECT TEAM" if game_mode == "2P" else "CPU OPPONENT SELECT")
        draw_text_with_glow(player_title_text, CUSTOM_TITLE_FONT, RETRO_GREEN_SCREEN, BLACK, screen, SCREEN_WIDTH // 2, title_y_pos)
        current_selected_team = player1_team_data if game_state == "TEAM_SELECT_P1" else player2_team_data
        if current_selected_team and NBA_TEAMS_LIST: 
            team_name_display_y = title_y_pos + CUSTOM_TITLE_FONT.get_height() // 2 + 30
            team_name_rect = draw_text_with_glow(current_selected_team["name"], RETRO_FONT_LARGE, current_selected_team["primary"], WHITE, screen, SCREEN_WIDTH // 2, team_name_display_y, True, 2)
            logo_preview_center_y = team_name_rect.bottom + (LOGO_DISPLAY_MAX_DIM * 1.2) // 2 + 20
            paddle_preview_y = logo_preview_center_y + (LOGO_DISPLAY_MAX_DIM * 1.2) // 2 + 15
            if current_selected_team["name"] in team_select_logo_surfaces:
                logo_surf = team_select_logo_surfaces[current_selected_team["name"]]
                screen.blit(logo_surf, logo_surf.get_rect(center=(SCREEN_WIDTH // 2, logo_preview_center_y)))
            else: paddle_preview_y = team_name_rect.bottom + 20
            preview_paddle_width = PADDLE_WIDTH * 2.5
            preview_paddle_height = PADDLE_HEIGHT * 0.8 
            preview_paddle_rect = pygame.Rect(SCREEN_WIDTH // 2 - preview_paddle_width // 2, paddle_preview_y, preview_paddle_width, preview_paddle_height)
            pygame.draw.rect(screen, current_selected_team["primary"], preview_paddle_rect, 0, PADDLE_BORDER_RADIUS)
            pygame.draw.rect(screen, current_selected_team["secondary"], preview_paddle_rect, 5, PADDLE_BORDER_RADIUS) 
            instruction_y = preview_paddle_rect.bottom + 30
        else: 
            instruction_y = SCREEN_HEIGHT // 2
            draw_text("No teams available for selection.", MESSAGE_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        draw_text("< LEFT | RIGHT ARROWS TO CHANGE >", RETRO_FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, instruction_y)
        draw_text("PRESS ENTER OR CLICK CONFIRM", RETRO_FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, instruction_y + 25)
        confirm_button_y = instruction_y + 25 + 35
        confirm_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, confirm_button_y, 200, 50)
        is_confirm_hovered = confirm_button_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_confirm_hovered else BUTTON_COLOR, confirm_button_rect, 0, 10)
        draw_text("CONFIRM", RETRO_FONT_MEDIUM, BUTTON_TEXT_COLOR, screen, confirm_button_rect.centerx, confirm_button_rect.centery)
        
        if (mouse_clicked and is_confirm_hovered and NBA_TEAMS_LIST):
            if game_state == "TEAM_SELECT_P1":
                if game_mode == "1P":
                    game_state = "TEAM_SELECT_P2"
                    if p1_selection_index == p2_selection_index and len(NBA_TEAMS_LIST) > 1:
                        p2_selection_index = (p1_selection_index + 1) % len(NBA_TEAMS_LIST)
                        player2_team_data = NBA_TEAMS_LIST[p2_selection_index]
                else: # 2P mode
                    game_state = "USERNAME_INPUT_P2"
                    player2_username = ""
                    username_input_active = True
            elif game_state == "TEAM_SELECT_P2":
                if game_mode == "2P" and p1_selection_index == p2_selection_index and len(NBA_TEAMS_LIST) > 1:
                    msg_surf = MESSAGE_FONT.render(f"{player2_username.strip() if player2_username.strip() else 'Player 2'}, pick a different team!", True, (255,100,100))
                    msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH//2, confirm_button_rect.bottom + 30))
                    screen.blit(msg_surf, msg_rect); pygame.display.flip(); pygame.time.wait(1500) 
                else:
                    initialize_game_elements(full_reset=False) 
                    game_state = "GAMEPLAY"; game_paused_for_quarter_break = True 

    elif game_state == "GAMEPLAY":
        keys_pressed = pygame.key.get_pressed()
        if not game_over_flag and not game_paused_for_quarter_break:
            update_game_time(); move_paddles_gameplay(keys_pressed); move_ball_gameplay()
        draw_court(); draw_paddles_gameplay(); draw_ball()
        draw_on_fire_message(); draw_scores_and_names_gameplay(); draw_game_timer_and_quarter()
        if game_over_flag or game_paused_for_quarter_break:
            overlay_width = 600 if game_paused_for_quarter_break else 550
            overlay_height = 200 if game_paused_for_quarter_break else 250
            overlay_x = SCREEN_WIDTH // 2 - overlay_width // 2
            overlay_y = SCREEN_HEIGHT // 2 - overlay_height // 2
            overlay_surface = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
            overlay_surface.fill((0, 0, 0, 200)); screen.blit(overlay_surface, (overlay_x, overlay_y))
            pygame.draw.rect(screen, WHITE, (overlay_x, overlay_y, overlay_width, overlay_height), 3, 10) 
            if game_over_flag:
                draw_text_with_glow("GAME OVER", CUSTOM_TITLE_FONT, (255,0,0), BLACK, screen, SCREEN_WIDTH // 2, overlay_y + 50)
                draw_text(winner_message, MESSAGE_FONT, WHITE, screen, SCREEN_WIDTH // 2, overlay_y + 120)
                draw_text("ENTER: Play Again | ESC: Menu", RETRO_FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, overlay_y + 190)
            else: 
                prev_quarter_display = current_quarter -1; line1_text = ""
                if current_quarter == 1 and quarter_time_remaining_ms == QUARTER_DURATION_SECONDS * 1000 and player1_score == 0 and player2_score == 0:
                    line1_text = "GET READY!"
                elif prev_quarter_display == 0 : line1_text = "PREPARE FOR TIP-OFF!"
                else: line1_text = f"END OF QUARTER {prev_quarter_display}"
                draw_text(line1_text, MESSAGE_FONT, WHITE, screen, SCREEN_WIDTH // 2, overlay_y + 60)
                draw_text(f"PRESS ENTER TO START QUARTER {current_quarter}", MESSAGE_FONT, WHITE, screen, SCREEN_WIDTH // 2, overlay_y + 130)

    elif game_state == "LEADERBOARD_SCREEN":
        draw_text_with_glow("LEADERBOARD", CUSTOM_TITLE_FONT, RETRO_GREEN_SCREEN, BLACK, screen, SCREEN_WIDTH // 2, 40)
        toggle_button_w, toggle_button_h = 220, 35
        toggle_button_x = SCREEN_WIDTH - toggle_button_w - 20; toggle_button_y = 25
        leaderboard_toggle_rect = pygame.Rect(toggle_button_x, toggle_button_y, toggle_button_w, toggle_button_h)
        toggle_text = "View 2P Games" if leaderboard_view_mode == "1P" else "View 1P Games"
        is_toggle_hovered = leaderboard_toggle_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_toggle_hovered else BUTTON_COLOR, leaderboard_toggle_rect, 0, 8)
        draw_text(toggle_text, RETRO_FONT_SMALL, BUTTON_TEXT_COLOR, screen, leaderboard_toggle_rect.centerx, leaderboard_toggle_rect.centery)
        if mouse_clicked and is_toggle_hovered: leaderboard_view_mode = "2P" if leaderboard_view_mode == "1P" else "1P"
        header_y_pos = 90; filtered_data = []
        if leaderboard_view_mode == "1P":
            headers = ["Rank", "User", "Score", "CPU", "Team (P1)", "Difficulty"]
            col_x_positions = [30, 100, 240, 320, 420, 570] 
            filtered_data = [e for e in leaderboard_data if e.get("mode") == "1P"]
        else: 
            headers = ["Rank", "P1 User", "P2 User", "P1", "P2", "P1 Team", "P2 Team", "Date"]
            col_x_positions = [20, 80, 180, 280, 330, 390, 500, 610] 
            filtered_data = [e for e in leaderboard_data if e.get("mode") == "2P"]
        for i, header_text in enumerate(headers):
            draw_text(header_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[i], header_y_pos, center=False)
        line_start_x = col_x_positions[0]
        line_end_x = col_x_positions[-1] + LEADERBOARD_FONT.size(headers[-1])[0] + 10 
        pygame.draw.line(screen, WHITE, (line_start_x, header_y_pos + 25), (line_end_x , header_y_pos + 25), 1)
        for i, entry in enumerate(filtered_data[:15]): 
            y_pos = header_y_pos + 40 + (i * 25)
            if y_pos > SCREEN_HEIGHT - 80: break 
            rank_text = str(i + 1) + "." 
            draw_text(rank_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[0], y_pos, center=False)
            if leaderboard_view_mode == "1P":
                user_text = entry.get("username", "N/A")[:10]; p1_score_text = str(entry.get("p1_score", 0))
                cpu_score_text = str(entry.get("p2_score",0)); p1_team_text = entry.get("p1_team", "N/A")[:10]
                difficulty_text_val = entry.get("difficulty", "N/A")[:7]
                draw_text(user_text, LEADERBOARD_FONT, SELECTED_TEXT_COLOR, screen, col_x_positions[1], y_pos, center=False)
                draw_text(p1_score_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[2], y_pos, center=False)
                draw_text(cpu_score_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[3], y_pos, center=False)
                draw_text(p1_team_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[4], y_pos, center=False)
                draw_text(difficulty_text_val, LEADERBOARD_FONT, WHITE, screen, col_x_positions[5], y_pos, center=False)
            else: 
                p1_user_text = entry.get("username", "P1")[:10]; p2_user_text = entry.get("player2_username", "P2")[:10]
                p1_score_text = str(entry.get("p1_score", 0)); p2_score_text = str(entry.get("p2_score", 0))
                p1_team_text = entry.get("p1_team", "N/A")[:10]; p2_team_text = entry.get("p2_team", "N/A")[:10]
                date_text = datetime.strptime(entry.get("timestamp"), "%Y-%m-%d %H:%M:%S").strftime("%m/%d/%y") if entry.get("timestamp") else "N/A"
                draw_text(p1_user_text, LEADERBOARD_FONT, SELECTED_TEXT_COLOR, screen, col_x_positions[1], y_pos, center=False)
                draw_text(p2_user_text, LEADERBOARD_FONT, SELECTED_TEXT_COLOR, screen, col_x_positions[2], y_pos, center=False)
                draw_text(p1_score_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[3], y_pos, center=False)
                draw_text(p2_score_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[4], y_pos, center=False)
                draw_text(p1_team_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[5], y_pos, center=False)
                draw_text(p2_team_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[6], y_pos, center=False)
                draw_text(date_text, LEADERBOARD_FONT, WHITE, screen, col_x_positions[7], y_pos, center=False)
        back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 70, 150, 40)
        is_back_hovered = back_button_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_back_hovered else BUTTON_COLOR, back_button_rect, 0, 10)
        draw_text("BACK", RETRO_FONT_MEDIUM, BUTTON_TEXT_COLOR, screen, back_button_rect.centerx, back_button_rect.centery)
        if mouse_clicked and is_back_hovered: game_state = "START_SCREEN"
        elif any(e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE for e in events): game_state = "START_SCREEN"

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
