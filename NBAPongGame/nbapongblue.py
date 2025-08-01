import pygame
import random
import sys
import os

# Initialize Pygame
pygame.mixer.pre_init(44100, -16, 2, 512) # Initialize mixer with common parameters
pygame.init()


# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PADDLE_BORDER_RADIUS = 8

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COURT_LINE_COLOR = (220, 220, 220)
RETRO_GREEN_SCREEN = (20, 160, 50)
BUTTON_COLOR = (50, 50, 150)
BUTTON_HOVER_COLOR = (80, 80, 180)
BUTTON_TEXT_COLOR = WHITE
SELECTED_TEXT_COLOR = (255, 255, 0)
DIFFICULTY_BUTTON_COLORS = {
    "EASY": (60, 180, 75), "NORMAL": (255, 225, 25),
    "HARD": (245, 130, 48), "EXTREME": (230, 25, 75),
}
DIFFICULTY_BUTTON_HOVER_COLORS = {
    "EASY": (80, 200, 95), "NORMAL": (255, 235, 75),
    "HARD": (250, 150, 70), "EXTREME": (240, 50, 95),
}
DARK_DESATURATED_BLUE = (20, 30, 55)

BASKETBALL_ORANGE = (211, 84, 0)

# Paddle Properties
PADDLE_WIDTH = 15 # Standard paddle width
PADDLE_HEIGHT = 100 
PLAYER_PADDLE_SPEED = 7

BALL_RADIUS = 10
BASE_BALL_SPEED_X = 5
BASE_BALL_SPEED_Y = 5
actual_initial_ball_speed_x = BASE_BALL_SPEED_X
actual_initial_ball_speed_y = BASE_BALL_SPEED_Y

DIFFICULTY_SETTINGS = {
    "EASY":    {"ai_paddle_speed": 3, "ai_speed_factor": 0.30, "ball_speed_multiplier": 0.80},
    "NORMAL":  {"ai_paddle_speed": 4, "ai_speed_factor": 0.40, "ball_speed_multiplier": 1.10},
    "HARD":    {"ai_paddle_speed": 7, "ai_speed_factor": 0.70, "ball_speed_multiplier": 1.25},
    "EXTREME": {"ai_paddle_speed": 10, "ai_speed_factor": 1.00, "ball_speed_multiplier": 2.00},
}
selected_difficulty = "NORMAL"

NBA_TEAMS_LIST = [
    {"name": "LAKERS", "primary": (85, 37, 130), "secondary": (253, 185, 39)},
    {"name": "CELTICS", "primary": (0, 122, 51), "secondary": (139, 113, 73)},
    {"name": "KNICKS", "primary": (0, 107, 182), "secondary": (245, 132, 38)},
    {"name": "PACERS", "primary": (0, 45, 98), "secondary": (253, 187, 48)},
    {"name": "BULLS", "primary": (206, 17, 65), "secondary": (6, 25, 34)},
    {"name": "WARRIORS", "primary": (29, 66, 138), "secondary": (255, 199, 44)},
    {"name": "HEAT", "primary": (152, 0, 46), "secondary": (249, 160, 27)},
    {"name": "BUCKS", "primary": (0, 71, 27), "secondary": (240, 235, 210)},
    {"name": "76ERS", "primary": (0, 107, 182), "secondary": (237, 23, 76)},
    {"name": "SUNS", "primary": (29, 17, 96), "secondary": (229, 95, 32)},
    {"name": "NETS", "primary": (0, 0, 0), "secondary": (120, 120, 120)},
    {"name": "NUGGETS", "primary": (13, 34, 64), "secondary": (255, 198, 39)},
    {"name": "CLIPPERS", "primary": (200,16,46), "secondary": (29,66,138)},
    {"name": "MAVERICKS", "primary": (0,83,188), "secondary": (0,43,92)},
    {"name": "GRIZZLIES", "primary": (93,118,169), "secondary": (18,24,49)},
    {"name": "WIZARDS", "primary": (0, 43, 92), "secondary": (227, 24, 55)},
    {"name": "RAPTORS", "primary": (206, 17, 65), "secondary": (6, 25, 34)},
    {"name": "CAVALIERS", "primary": (134, 0, 56), "secondary": (253, 187, 48)},
    {"name": "PISTONS", "primary": (200, 16, 46), "secondary": (29, 66, 138)},
    {"name": "SPURS", "primary": (6, 25, 34), "secondary": (196, 206, 211)},
    {"name": "TIMBERWOLVES", "primary": (12, 35, 64), "secondary": (120, 190, 32)},
    {"name": "THUNDER", "primary": (0, 125, 195), "secondary": (239, 59, 36)},
    {"name": "TRAIL BLAZERS", "primary": (224, 58, 62), "secondary": (6, 25, 34)},
    {"name": "JAZZ", "primary": (0, 43, 92), "secondary": (249, 160, 27)},
    {"name": "KINGS", "primary": (91, 43, 130), "secondary": (99, 113, 122)},
    {"name": "HAWKS", "primary": (200, 16, 46), "secondary": (253, 185, 39)},
    {"name": "HORNETS", "primary": (29, 17, 96), "secondary": (0, 120, 140)},
    {"name": "MAGIC", "primary": (0, 125, 197), "secondary": (196, 206, 211)},
    {"name": "ROCKETS", "primary": (206, 17, 65), "secondary": (196, 206, 211)},
    {"name": "PELICANS", "primary": (0, 22, 65), "secondary": (180, 151, 90)},
]

# --- Fonts ---
try:
    RETRO_FONT_LARGE = pygame.font.SysFont("monospace", 50, bold=True)
    RETRO_FONT_MEDIUM = pygame.font.SysFont("monospace", 35, bold=True)
    RETRO_FONT_SMALL = pygame.font.SysFont("monospace", 25)
    SCORE_FONT = pygame.font.SysFont("monospace", 36, bold=True)
    TEAM_NAME_FONT = pygame.font.SysFont("monospace", 20, bold=True)
    GAME_CLOCK_FONT = pygame.font.SysFont("monospace", 48, bold=True)
    QUARTER_DISPLAY_FONT = pygame.font.SysFont("monospace", 24, bold=True)
    MESSAGE_FONT = pygame.font.SysFont("monospace", 30, bold=True)
except pygame.error:
    print("Warning: Monospace font not found. Using system default.")
    RETRO_FONT_LARGE = pygame.font.Font(None, 70)
    RETRO_FONT_MEDIUM = pygame.font.Font(None, 50)
    RETRO_FONT_SMALL = pygame.font.Font(None, 35)
    SCORE_FONT = pygame.font.Font(None, 50)
    TEAM_NAME_FONT = pygame.font.Font(None, 30)
    GAME_CLOCK_FONT = pygame.font.Font(None, 60)
    QUARTER_DISPLAY_FONT = pygame.font.Font(None, 30)
    MESSAGE_FONT = pygame.font.Font(None, 40)


# --- Setup Screen ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NBA Retro Pong")
clock = pygame.time.Clock()

# --- Load Assets ---
start_screen_wallpaper = None
ball_bounce_sound = None 
cheering_sound = None 

try:
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "NBAPongLogo.png")
    start_screen_wallpaper_original = pygame.image.load(image_path)
    start_screen_wallpaper = pygame.transform.scale(start_screen_wallpaper_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error loading start screen wallpaper: {e}")
    start_screen_wallpaper = None

try:
    sound_path_bounce = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BallBounce.wav")
    ball_bounce_sound = pygame.mixer.Sound(sound_path_bounce)
except pygame.error as e:
    print(f"Error loading sound 'BallBounce.wav': {e}")
    ball_bounce_sound = None

try:
    sound_path_cheer = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Cheering.wav")
    cheering_sound = pygame.mixer.Sound(sound_path_cheer)
except pygame.error as e:
    print(f"Error loading sound 'Cheering.wav': {e}")
    cheering_sound = None


# --- Game State Variables ---
game_state = "START_SCREEN" # START_SCREEN, DIFFICULTY_SELECT, TEAM_SELECT_P1, TEAM_SELECT_P2, GAMEPLAY
game_mode = None 

player1_team_data = NBA_TEAMS_LIST[0]
player2_team_data = NBA_TEAMS_LIST[1]
home_court_team_data = None
p1_selection_index = 0
p2_selection_index = 1

# --- Game Objects ---
paddle1_rect = None
paddle2_rect = None
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_speed = [0,0]
player1_score = 0
player2_score = 0

# --- Timekeeping ---
QUARTER_DURATION_SECONDS = 60
current_quarter = 1
quarter_time_remaining_ms = QUARTER_DURATION_SECONDS * 1000
game_paused_for_quarter_break = False
game_over_flag = False
winner_message = ""

# --- UI Helper ---
def draw_text_with_glow(text, font, main_color, glow_color, surface, x, y, center=True, glow_offset=1):
    glow_surfs = []
    offsets = [
        (-glow_offset, -glow_offset), (0, -glow_offset), (glow_offset, -glow_offset),
        (-glow_offset, 0),                           (glow_offset, 0),
        (-glow_offset, glow_offset), (0, glow_offset), (glow_offset, glow_offset),
    ]
    for off_x, off_y in offsets:
        glow_surfs.append(font.render(text, True, glow_color))
    text_surf = font.render(text, True, main_color)
    text_rect = text_surf.get_rect()
    if center: text_rect.center = (x, y)
    else: text_rect.topleft = (x,y)
    for i, glow_surf in enumerate(glow_surfs):
        glow_rect = glow_surf.get_rect(center=(text_rect.centerx + offsets[i][0], text_rect.centery + offsets[i][1]))
        surface.blit(glow_surf, glow_rect)
    surface.blit(text_surf, text_rect)
    return text_rect

def draw_text(text, font, color, surface, x, y, center=True):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center: textrect.center = (x, y)
    else: textrect.topleft = (x,y)
    surface.blit(textobj, textrect)
    return textrect


# --- Game Initialization ---
def initialize_game_elements():
    global paddle1_rect, paddle2_rect, ball_pos, ball_speed, player1_score, player2_score, home_court_team_data
    global actual_initial_ball_speed_x, actual_initial_ball_speed_y
    global current_quarter, quarter_time_remaining_ms, game_paused_for_quarter_break, game_over_flag, winner_message

    paddle1_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddle2_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

    paddle1_rect = pygame.Rect(50, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT) # Use standard PADDLE_WIDTH
    paddle2_rect = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT) # Use standard PADDLE_WIDTH

    if game_mode == "1P":
        multiplier = DIFFICULTY_SETTINGS[selected_difficulty]["ball_speed_multiplier"]
    else:
        multiplier = DIFFICULTY_SETTINGS["NORMAL"]["ball_speed_multiplier"]
        
    actual_initial_ball_speed_x = BASE_BALL_SPEED_X * multiplier
    actual_initial_ball_speed_y = BASE_BALL_SPEED_Y * multiplier

    reset_ball_gameplay()
    player1_score = 0
    player2_score = 0

    if player1_team_data and player2_team_data:
        home_court_team_data = random.choice([player1_team_data, player2_team_data])
    else:
        home_court_team_data = NBA_TEAMS_LIST[0]

    current_quarter = 1
    quarter_time_remaining_ms = QUARTER_DURATION_SECONDS * 1000
    game_paused_for_quarter_break = False
    game_over_flag = False
    winner_message = ""

# --- Gameplay Functions ---
def draw_court():
    if home_court_team_data:
        screen.fill(home_court_team_data["primary"])
        line_color = home_court_team_data["secondary"]
        r1, g1, b1 = home_court_team_data["primary"]
        r2, g2, b2 = home_court_team_data["secondary"]
        brightness1 = r1 + g1 + b1
        brightness2 = r2 + g2 + b2
        color_diff = abs(brightness1 - brightness2)
        if color_diff < 150: 
            line_color = WHITE 
        pygame.draw.line(screen, line_color, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 3)
    else:
        screen.fill(BLACK) 
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 3)

def draw_paddles_gameplay():
    # Always draw paddles as team-colored rectangles
    pygame.draw.rect(screen, player1_team_data["primary"], paddle1_rect, border_radius=PADDLE_BORDER_RADIUS)
    pygame.draw.rect(screen, player1_team_data["secondary"], paddle1_rect, 3, border_radius=PADDLE_BORDER_RADIUS)
    pygame.draw.rect(screen, player2_team_data["primary"], paddle2_rect, border_radius=PADDLE_BORDER_RADIUS)
    pygame.draw.rect(screen, player2_team_data["secondary"], paddle2_rect, 3, border_radius=PADDLE_BORDER_RADIUS)

def draw_ball():
    pygame.draw.circle(screen, BASKETBALL_ORANGE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
    pygame.draw.arc(screen, BLACK, (int(ball_pos[0]) - BALL_RADIUS, int(ball_pos[1]) - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2), 0, 3.14, 1) 
    pygame.draw.arc(screen, BLACK, (int(ball_pos[0]) - BALL_RADIUS, int(ball_pos[1]) - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2), 3.14, 6.28, 1)


def draw_scores_and_names_gameplay():
    text_color_p1 = WHITE if sum(home_court_team_data["primary"]) < 382 else BLACK
    text_color_p2 = WHITE if sum(home_court_team_data["primary"]) < 382 else BLACK

    p1_score_text = SCORE_FONT.render(str(player1_score), True, text_color_p1)
    p1_score_bg = pygame.Surface((p1_score_text.get_width() + 20, p1_score_text.get_height() + 10), pygame.SRCALPHA)
    p1_score_bg.fill((0,0,0,120)) 
    screen.blit(p1_score_bg, (SCREEN_WIDTH // 4 - p1_score_bg.get_width() // 2, 15))
    screen.blit(p1_score_text, (SCREEN_WIDTH // 4 - p1_score_text.get_width() // 2, 20))

    p2_score_text = SCORE_FONT.render(str(player2_score), True, text_color_p2)
    p2_score_bg = pygame.Surface((p2_score_text.get_width() + 20, p2_score_text.get_height() + 10), pygame.SRCALPHA)
    p2_score_bg.fill((0,0,0,120)) 
    screen.blit(p2_score_bg, (SCREEN_WIDTH * 3 // 4 - p2_score_bg.get_width() // 2, 15))
    screen.blit(p2_score_text, (SCREEN_WIDTH * 3 // 4 - p2_score_text.get_width() // 2, 20))
    
    # Always display team names
    draw_text_with_glow(player1_team_data["name"], TEAM_NAME_FONT, player1_team_data["primary"], WHITE, screen, SCREEN_WIDTH // 4, 60, center=True, glow_offset=1 )
    draw_text_with_glow(player2_team_data["name"], TEAM_NAME_FONT, player2_team_data["primary"], WHITE, screen, SCREEN_WIDTH * 3 // 4, 60, center=True, glow_offset=1 )

def draw_game_timer_and_quarter():
    timer_bg_width = 200 
    timer_bg_height = 75 
    timer_bg_x = SCREEN_WIDTH // 2 - timer_bg_width // 2
    timer_bg_y = 15      

    timer_bg_surface = pygame.Surface((timer_bg_width, timer_bg_height), pygame.SRCALPHA)
    timer_bg_surface.fill((0, 0, 0, 180)) 
    screen.blit(timer_bg_surface, (timer_bg_x, timer_bg_y))
    pygame.draw.rect(screen, (200,0,0), (timer_bg_x, timer_bg_y, timer_bg_width, timer_bg_height), 3, border_radius=5)

    display_time_ms = max(0, quarter_time_remaining_ms) 
    seconds_total = display_time_ms // 1000
    minutes = seconds_total // 60
    seconds = seconds_total % 60
    time_str = f"{minutes:02}:{seconds:02}"

    time_surf = GAME_CLOCK_FONT.render(time_str, True, (255, 0, 0)) 
    time_rect = time_surf.get_rect(center=(SCREEN_WIDTH // 2, timer_bg_y + timer_bg_height * 0.40))
    screen.blit(time_surf, time_rect)

    qtr_str = f"QTR: {current_quarter}"
    qtr_surf = QUARTER_DISPLAY_FONT.render(qtr_str, True, WHITE) 
    qtr_rect = qtr_surf.get_rect(center=(SCREEN_WIDTH // 2, timer_bg_y + timer_bg_height * 0.78))
    screen.blit(qtr_surf, qtr_rect)

def reset_ball_gameplay():
    global ball_pos, ball_speed  
    ball_pos[0] = SCREEN_WIDTH // 2
    ball_pos[1] = SCREEN_HEIGHT // 2
    ball_speed[0] = random.choice([actual_initial_ball_speed_x, -actual_initial_ball_speed_x])
    ball_speed[1] = random.choice([actual_initial_ball_speed_y, -actual_initial_ball_speed_y])

def move_ball_gameplay():
    global player1_score, player2_score, ball_pos, ball_speed  

    if game_paused_for_quarter_break or game_over_flag:
        return

    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= SCREEN_HEIGHT:
        ball_speed[1] *= -1

    ball_rect_obj = pygame.Rect(ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

    if paddle1_rect and ball_rect_obj.colliderect(paddle1_rect): 
        ball_speed[0] *= -1
        ball_pos[0] = paddle1_rect.right + BALL_RADIUS  
        delta_y = ball_pos[1] - paddle1_rect.centery
        ball_speed[1] = delta_y * 0.1 + ball_speed[1] * 0.5
        ball_speed[1] = max(-actual_initial_ball_speed_y*1.5, min(actual_initial_ball_speed_y*1.5, ball_speed[1]))
        if ball_bounce_sound: ball_bounce_sound.play() 

    if paddle2_rect and ball_rect_obj.colliderect(paddle2_rect): 
        ball_speed[0] *= -1
        ball_pos[0] = paddle2_rect.left - BALL_RADIUS  
        delta_y = ball_pos[1] - paddle2_rect.centery
        ball_speed[1] = delta_y * 0.1 + ball_speed[1] * 0.5
        ball_speed[1] = max(-actual_initial_ball_speed_y*1.5, min(actual_initial_ball_speed_y*1.5, ball_speed[1]))
        if ball_bounce_sound: ball_bounce_sound.play() 

    if ball_pos[0] - BALL_RADIUS <= 0:  
        player2_score += 1
        if cheering_sound: cheering_sound.play() 
        reset_ball_gameplay()
    elif ball_pos[0] + BALL_RADIUS >= SCREEN_WIDTH:  
        player1_score += 1
        if cheering_sound: cheering_sound.play() 
        reset_ball_gameplay()


def move_paddles_gameplay(keys_pressed):
    if game_paused_for_quarter_break or game_over_flag:
        return
    
    if not paddle1_rect or not paddle2_rect: 
        return

    if keys_pressed[pygame.K_w] and paddle1_rect.top > 0:
        paddle1_rect.y -= PLAYER_PADDLE_SPEED
    if keys_pressed[pygame.K_s] and paddle1_rect.bottom < SCREEN_HEIGHT:
        paddle1_rect.y += PLAYER_PADDLE_SPEED

    if game_mode == "2P":  
        if keys_pressed[pygame.K_UP] and paddle2_rect.top > 0:
            paddle2_rect.y -= PLAYER_PADDLE_SPEED
        if keys_pressed[pygame.K_DOWN] and paddle2_rect.bottom < SCREEN_HEIGHT:
            paddle2_rect.y += PLAYER_PADDLE_SPEED
    else:  
        ai_current_paddle_speed = DIFFICULTY_SETTINGS[selected_difficulty]["ai_paddle_speed"]
        ai_current_speed_factor = DIFFICULTY_SETTINGS[selected_difficulty]["ai_speed_factor"]
        
        target_y = ball_pos[1]
        movement = (target_y - paddle2_rect.centery) * ai_current_speed_factor
        movement = max(-ai_current_paddle_speed, min(ai_current_paddle_speed, movement)) 
        paddle2_rect.y += movement
    
    paddle1_rect.clamp_ip(screen.get_rect())
    paddle2_rect.clamp_ip(screen.get_rect())

def update_game_time():
    global quarter_time_remaining_ms, current_quarter, game_paused_for_quarter_break, game_over_flag, winner_message, ball_speed

    if game_over_flag or game_paused_for_quarter_break:
        return

    delta_ms = clock.get_time()  
    quarter_time_remaining_ms -= delta_ms

    if quarter_time_remaining_ms <= 0:
        quarter_time_remaining_ms = 0  
        ball_speed = [0, 0]  

        if current_quarter < 4:  
            current_quarter += 1
            quarter_time_remaining_ms = QUARTER_DURATION_SECONDS * 1000  
            game_paused_for_quarter_break = True
        else:  
            game_over_flag = True
            if player1_score > player2_score:
                winner_message = f"{player1_team_data['name']} WINS!" # Always use team name now
            elif player2_score > player1_score:
                winner_message = f"{player2_team_data['name']} WINS!" # Always use team name now
            else:
                winner_message = "IT'S A TIE!"


# --- Main Loop ---
running = True
while running:
    mouse_clicked = False
    mouse_pos = pygame.mouse.get_pos()
    keys_pressed_event_frame = pygame.key.get_pressed() 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                mouse_clicked = True
        if event.type == pygame.KEYDOWN:
            if game_state == "TEAM_SELECT_P1" or game_state == "TEAM_SELECT_P2":
                current_selection_index = p1_selection_index if game_state == "TEAM_SELECT_P1" else p2_selection_index
                if event.key == pygame.K_LEFT:
                    current_selection_index = (current_selection_index - 1 + len(NBA_TEAMS_LIST)) % len(NBA_TEAMS_LIST)
                elif event.key == pygame.K_RIGHT:
                    current_selection_index = (current_selection_index + 1) % len(NBA_TEAMS_LIST)
                
                if game_state == "TEAM_SELECT_P1":
                    p1_selection_index = current_selection_index
                    player1_team_data = NBA_TEAMS_LIST[p1_selection_index]
                else:
                    p2_selection_index = current_selection_index
                    player2_team_data = NBA_TEAMS_LIST[p2_selection_index]
            
            elif game_state == "GAMEPLAY":
                if game_over_flag:
                    if event.key == pygame.K_RETURN: initialize_game_elements()
                    elif event.key == pygame.K_ESCAPE: 
                        initialize_game_elements()
                        game_state = "START_SCREEN"
                elif game_paused_for_quarter_break:
                    if event.key == pygame.K_RETURN: 
                        game_paused_for_quarter_break = False
                        reset_ball_gameplay()
                elif not game_over_flag and not game_paused_for_quarter_break:
                    if event.key == pygame.K_ESCAPE:
                        initialize_game_elements()
                        game_state = "START_SCREEN"

    # --- Game State Logic & Drawing ---
    if game_state == "START_SCREEN":
        if start_screen_wallpaper:
            screen.blit(start_screen_wallpaper, (0,0))
        else:
            screen.fill(DARK_DESATURATED_BLUE) 

        title_bg_surf = pygame.Surface((SCREEN_WIDTH - 100, 80), pygame.SRCALPHA)  
        title_bg_surf.fill((0,0,0, 150))  
        screen.blit(title_bg_surf, (50, SCREEN_HEIGHT // 4 - 40))
        draw_text("NBA RETRO PONG", RETRO_FONT_LARGE, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        button_width = 400
        button_height = 50
        button_1p_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 50, button_width, button_height)
        button_2p_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 50 + button_height + 20, button_width, button_height)

        pygame.draw.rect(screen, BUTTON_COLOR if not button_1p_rect.collidepoint(mouse_pos) else BUTTON_HOVER_COLOR, button_1p_rect, border_radius=10)
        draw_text("1 PLAYER vs CPU", RETRO_FONT_MEDIUM, BUTTON_TEXT_COLOR, screen, button_1p_rect.centerx, button_1p_rect.centery)

        pygame.draw.rect(screen, BUTTON_COLOR if not button_2p_rect.collidepoint(mouse_pos) else BUTTON_HOVER_COLOR, button_2p_rect, border_radius=10)
        draw_text("2 PLAYERS", RETRO_FONT_MEDIUM, BUTTON_TEXT_COLOR, screen, button_2p_rect.centerx, button_2p_rect.centery)

        if mouse_clicked:
            if button_1p_rect.collidepoint(mouse_pos):
                game_mode = "1P"
                game_state = "DIFFICULTY_SELECT" # Directly to difficulty for 1P
            elif button_2p_rect.collidepoint(mouse_pos):
                game_mode = "2P"
                selected_difficulty = "NORMAL" 
                game_state = "TEAM_SELECT_P1" # Directly to team select for 2P
    
    elif game_state == "DIFFICULTY_SELECT": # This state is now only for 1P mode
        screen.fill(DARK_DESATURATED_BLUE) 
        draw_text("SELECT DIFFICULTY", RETRO_FONT_LARGE, RETRO_GREEN_SCREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6)
        
        difficulty_options = ["EASY", "NORMAL", "HARD", "EXTREME"]
        button_width = 250
        button_height = 50
        total_button_height = len(difficulty_options) * button_height + (len(difficulty_options) - 1) * 15
        start_y = SCREEN_HEIGHT // 2 - total_button_height // 2

        for i, diff_level in enumerate(difficulty_options):
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, start_y + i * (button_height + 15), button_width, button_height)
            
            color = DIFFICULTY_BUTTON_COLORS[diff_level]
            hover_color = DIFFICULTY_BUTTON_HOVER_COLORS[diff_level]

            pygame.draw.rect(screen, color if not button_rect.collidepoint(mouse_pos) else hover_color, button_rect, border_radius=10)
            text_col = BLACK 
            draw_text(diff_level, RETRO_FONT_MEDIUM, text_col, screen, button_rect.centerx, button_rect.centery)

            if mouse_clicked and button_rect.collidepoint(mouse_pos):
                selected_difficulty = diff_level
                game_state = "TEAM_SELECT_P1" 
                break 

    elif game_state == "TEAM_SELECT_P1" or game_state == "TEAM_SELECT_P2":
        screen.fill(DARK_DESATURATED_BLUE) 
        player_title_text = "PLAYER 1 SELECT TEAM" if game_state == "TEAM_SELECT_P1" else "PLAYER 2 SELECT TEAM"
        if game_mode == "1P" and game_state == "TEAM_SELECT_P2":
            player_title_text = "CPU OPPONENT SELECT"

        draw_text(player_title_text, RETRO_FONT_LARGE, RETRO_GREEN_SCREEN, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)
        current_team_data = player1_team_data if game_state == "TEAM_SELECT_P1" else player2_team_data
        
        team_name_rect = draw_text_with_glow( # Always use glow for team names on select screen
            current_team_data["name"], RETRO_FONT_MEDIUM, current_team_data["primary"], WHITE,
            screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True, glow_offset=2 
        )

        preview_width = PADDLE_WIDTH * 1.5 # Preview for standard paddles
        preview_height = PADDLE_HEIGHT * 0.8 
        preview_rect = pygame.Rect(SCREEN_WIDTH // 2 - preview_width // 2, team_name_rect.bottom + 30, preview_width, preview_height)

        pygame.draw.rect(screen, current_team_data["primary"], preview_rect, border_radius=PADDLE_BORDER_RADIUS)
        pygame.draw.rect(screen, current_team_data["secondary"], preview_rect, 5, border_radius=PADDLE_BORDER_RADIUS)

        draw_text("< LEFT | RIGHT ARROWS TO CHANGE >", RETRO_FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, preview_rect.bottom + 50)
        draw_text("ENTER OR CLICK CONFIRM", RETRO_FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, preview_rect.bottom + 80)

        confirm_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT * 3 // 4 + 20, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR if not confirm_button_rect.collidepoint(mouse_pos) else BUTTON_HOVER_COLOR, confirm_button_rect, border_radius=10)
        draw_text("CONFIRM", RETRO_FONT_MEDIUM, BUTTON_TEXT_COLOR, screen, confirm_button_rect.centerx, confirm_button_rect.centery)

        confirm_action = mouse_clicked and confirm_button_rect.collidepoint(mouse_pos)
        if keys_pressed_event_frame[pygame.K_RETURN]:
            confirm_action = True
            pygame.time.wait(200)

        if confirm_action:
            if game_state == "TEAM_SELECT_P1":
                game_state = "TEAM_SELECT_P2"
                if p1_selection_index == p2_selection_index:
                    p2_selection_index = (p1_selection_index + 1) % len(NBA_TEAMS_LIST)
                player2_team_data = NBA_TEAMS_LIST[p2_selection_index]
            elif game_state == "TEAM_SELECT_P2":
                if game_mode == "2P" and p1_selection_index == p2_selection_index:
                    draw_text("Player 2, pick a different team!", RETRO_FONT_SMALL, (255,100,100), screen, SCREEN_WIDTH // 2, confirm_button_rect.bottom + 30)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                else:
                    initialize_game_elements()
                    game_state = "GAMEPLAY"

    elif game_state == "GAMEPLAY":
        keys_pressed_gameplay = pygame.key.get_pressed() 

        if game_over_flag:
            pass 
        elif game_paused_for_quarter_break:
            pass 
        else:  
            update_game_time()  
            move_paddles_gameplay(keys_pressed_gameplay) 
            move_ball_gameplay()  

        draw_court()
        draw_paddles_gameplay()
        draw_ball()  
        draw_scores_and_names_gameplay()
        draw_game_timer_and_quarter()
        
        if game_over_flag:
            msg_box_width = 550  
            msg_box_height = 250
            msg_box_x = SCREEN_WIDTH // 2 - msg_box_width // 2
            msg_box_y = SCREEN_HEIGHT // 2 - msg_box_height // 2
            
            msg_bg_surf = pygame.Surface((msg_box_width, msg_box_height), pygame.SRCALPHA)
            msg_bg_surf.fill((0, 0, 0, 200))  
            screen.blit(msg_bg_surf, (msg_box_x, msg_box_y))
            pygame.draw.rect(screen, WHITE, (msg_box_x, msg_box_y, msg_box_width, msg_box_height), 3, border_radius=10)  

            draw_text("GAME OVER", RETRO_FONT_LARGE, (255,0,0), screen, SCREEN_WIDTH // 2, msg_box_y + 50)
            draw_text(winner_message, MESSAGE_FONT, WHITE, screen, SCREEN_WIDTH // 2, msg_box_y + 120)
            draw_text("ENTER: Play Again | ESC: Menu", RETRO_FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, msg_box_y + 190)

        elif game_paused_for_quarter_break:
            msg_box_width = 600
            msg_box_height = 200
            msg_box_x = SCREEN_WIDTH // 2 - msg_box_width // 2
            msg_box_y = SCREEN_HEIGHT // 2 - msg_box_height // 2

            msg_bg_surf = pygame.Surface((msg_box_width, msg_box_height), pygame.SRCALPHA)
            msg_bg_surf.fill((0, 0, 0, 200))
            screen.blit(msg_bg_surf, (msg_box_x, msg_box_y))
            pygame.draw.rect(screen, WHITE, (msg_box_x, msg_box_y, msg_box_width, msg_box_height), 3, border_radius=10)

            prev_qtr_display = current_quarter -1 if current_quarter > 1 else 4 
            draw_text(f"END OF QUARTER {prev_qtr_display}", MESSAGE_FONT, WHITE, screen, SCREEN_WIDTH // 2, msg_box_y + 60)
            draw_text(f"PRESS ENTER TO START QUARTER {current_quarter}", MESSAGE_FONT, WHITE, screen, SCREEN_WIDTH // 2, msg_box_y + 130)
            
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
