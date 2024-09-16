import pygame
import random
import math

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bicycle Runner")

# Configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)

# Configuración de la bicicleta
bike_width, bike_height = 50, 30
bike_x = WIDTH // 2 - bike_width // 2
bike_y = HEIGHT - 70
bike_speed = 5

# Configuración de los carriles
lane_width = WIDTH // 4

# Configuración de obstáculos
obstacle_radius = 25
obstacle_size = 50
obstacle_hex_size = 40
obstacles = []
obstacle_speed = 3
initial_obstacle_count = 10
obstacle_interval = 12
score = 0
side_moving_speed = 4

# Fuentes
font = pygame.font.SysFont(None, 35)

# Variables para la entrada del usuario
user_input = ""

# Función para reiniciar el juego
def reset_game():
    global score, obstacle_list, bike_x, bike_y, obstacle_speed, obstacle_interval, game_over
    score = 0
    obstacle_list.clear()  # Limpiar los obstáculos existentes
    bike_x = WIDTH // 2 - bike_width // 2
    bike_y = HEIGHT - 70
    obstacle_speed = 10
    obstacle_interval = 10
    game_over = False
    # Generar obstáculos iniciales
    for _ in range(initial_obstacle_count):
        obstacle_list.append(create_obstacle())

# Funciones para dibujar
def draw_bike(x, y):
    points = [
        (x + bike_width // 2, y),
        (x + bike_width, y + bike_height // 2),
        (x + bike_width // 2, y + bike_height),
        (x, y + bike_height // 2)
    ]
    pygame.draw.polygon(screen, YELLOW, points)

def draw_circle_obstacle(x, y):
    pygame.draw.circle(screen, RED, (x, y), obstacle_radius)

def draw_pentagon_obstacle(x, y):
    points = []
    for i in range(5):
        angle = math.radians(72 * i)
        point_x = x + obstacle_size * math.cos(angle)
        point_y = y + obstacle_size * math.sin(angle)
        points.append((point_x, point_y))
    pygame.draw.polygon(screen, BLUE, points)

def draw_triangle_obstacle(x, y):
    points = [
        (x, y - 30),
        (x + 30, y + 30),
        (x - 30, y + 30)
    ]
    pygame.draw.polygon(screen, PURPLE, points)

def draw_hexagon_obstacle(x, y):
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        point_x = x + obstacle_size * math.cos(angle)
        point_y = y + obstacle_size * math.sin(angle)
        points.append((point_x, point_y))
    pygame.draw.polygon(screen, GREEN, points)

def draw_obstacles(obs_list):
    for obs in obs_list:
        if obs['type'] == 'circle':
            draw_circle_obstacle(obs['rect'].centerx, obs['rect'].centery)
        elif obs['type'] == 'pentagon':
            draw_pentagon_obstacle(obs['rect'].centerx, obs['rect'].centery)
        elif obs['type'] == 'triangle':
            draw_triangle_obstacle(obs['rect'].centerx, obs['rect'].centery)
        elif obs['type'] == 'hexagon':
            draw_hexagon_obstacle(obs['rect'].centerx, obs['rect'].centery)

def draw_dividers_and_lines(offset):
    for i in range(1, 4):
        pygame.draw.line(screen, WHITE, (i * lane_width, 0), (i * lane_width, HEIGHT), 5)
    for i in range(0, WIDTH, lane_width):
        for j in range(0, HEIGHT, 60):
            pygame.draw.line(screen, YELLOW, (i + lane_width // 2, (j + offset) % HEIGHT), (i + lane_width // 2, (j + offset + 20) % HEIGHT), 5)

def create_obstacle():
    lane = random.randint(0, 3) * lane_width
    x_pos = random.randint(lane, lane + lane_width - obstacle_radius)
    obstacle_type = random.choice(['circle', 'pentagon'])
    
    # Introducir triángulos y hexágonos después de 300 y 600 puntos
    if score > 300:
        obstacle_type = random.choice(['circle', 'pentagon', 'triangle'])
    if score > 600:
        obstacle_type = random.choice(['circle', 'pentagon', 'triangle', 'hexagon'])

    return {
        'rect': pygame.Rect(x_pos, -obstacle_radius if obstacle_type == 'circle' else -obstacle_size,
                            obstacle_radius * 2,
                            obstacle_radius * 2 if obstacle_type == 'circle' else obstacle_size * 2),
        'type': obstacle_type,
        'direction': random.choice([-1, 1])
    }

def move_obstacles(obs_list):
    for obs in obs_list:
        obs['rect'].y += obstacle_speed
        if score > 500:
            obs['rect'].x += obs['direction'] * 2
            if obs['rect'].x <= (obs['rect'].left // lane_width) * lane_width:
                obs['direction'] = 1
            elif obs['rect'].x + (obstacle_radius * 2 if obs['type'] == 'circle' else obstacle_size) >= (obs['rect'].left // lane_width + 1) * lane_width:
                obs['direction'] = -1
    return [obs for obs in obs_list if obs['rect'].y < HEIGHT]

def check_collision(bike_rect, obs_list):
    for obs in obs_list:
        if bike_rect.colliderect(obs['rect']):
            return True
    return False

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def show_game_over():
    game_over_text = font.render("Game Over! Type AGAIN and press Enter", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
    user_input_text = font.render(user_input, True, WHITE)
    screen.blit(user_input_text, (WIDTH // 4, HEIGHT // 2 + 50))

# Bucle Principal del Juego
running = True
game_over = False
clock = pygame.time.Clock()
obstacle_timer = 0
obstacle_list = []
line_offset = 0

# Crear obstáculos iniciales
for _ in range(initial_obstacle_count):
    obstacle_list.append(create_obstacle())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]  # Borrar el último carácter del texto ingresado
                elif event.key == pygame.K_RETURN:  # Si se presiona Enter
                    if user_input.upper() == "AGAIN":  # Verificar si el texto ingresado es "AGAIN"
                        reset_game()  # Reiniciar el juego
                    user_input = ""  # Reiniciar el texto de entrada
                elif event.key == pygame.K_SPACE:
                    user_input += " "  # Añadir un espacio al texto ingresado
                else:
                    user_input += event.unicode  # Añadir el carácter ingresado al texto

    # Si el juego no ha terminado
    if not game_over:
        # Movimiento de la bicicleta
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            bike_x -= bike_speed
        if keys[pygame.K_RIGHT]:
            bike_x += bike_speed
        if keys[pygame.K_UP]:
            bike_y -= bike_speed
        if keys[pygame.K_DOWN]:
            bike_y += bike_speed

        # Limitar la bicicleta dentro de los carriles
        bike_x = max(lane_width // 2 - bike_width // 2, min(bike_x, WIDTH - lane_width // 2 - bike_width // 2))
        bike_y = max(0, min(bike_y, HEIGHT - bike_height))

        # Creación de obstáculos
        obstacle_timer += 1
        if obstacle_timer > obstacle_interval:
            obstacle_list.append(create_obstacle())
            obstacle_timer = 0

        # Aumentar el número de obstáculos después de un tiempo
        if score > 0 and score % 100 == 0:
            obstacle_interval = max(10, obstacle_interval - 1)

        # Movimiento de obstáculos y comprobación de colisiones
        obstacle_list = move_obstacles(obstacle_list)
        bike_rect = pygame.Rect(bike_x, bike_y, bike_width, bike_height)
        if check_collision(bike_rect, obstacle_list):
            game_over = True

        # Actualización del puntaje
        score += 1

        # Aumento de dificultad
        if score % 100 == 0:
            obstacle_speed += 1

        # Dibujo en pantalla
        screen.fill(BLACK)
        draw_dividers_and_lines(line_offset)
        draw_bike(bike_x, bike_y)
        draw_obstacles(obstacle_list)

        draw_score()

        # Actualizar el desplazamiento de las líneas discontinuas
        line_offset = (line_offset + obstacle_speed) % 60

    else:
        screen.fill(BLACK)  # Pantalla en negro cuando el juego termina
        show_game_over()
        # Renderizar el texto ingresado por el usuario
        user_input_text = font.render(user_input, True, WHITE)
        screen.blit(user_input_text, (WIDTH // 4, HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
