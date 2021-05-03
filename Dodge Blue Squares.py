from typing import List
import pygame
import random
import sys

lines = [line.rstrip() for line in open('High Scores.txt')]
# Reads the text file line by line
high_scores_names = []  # Creates a list for the names of people with high scores
high_scores = []  # Creates a list for the high scores

for i in range(0, 9, 2):  # Puts the names of the people with high scores in a list
    high_scores_names.append(lines[i])

for i in range(1, 10, 2):  # Puts the high scores in a list
    high_scores.append(int(lines[i]))

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3')  # Load background music
pygame.mixer.music.set_volume(0.5)  # Sets the volume of the music (0-1.0)

font = pygame.font.SysFont("monospace", 35)
font2 = pygame.font.SysFont("times new roman", 40, True)
HEIGHT = 600  # Dimensions of screen
WIDTH = 800

draw_line = False
horizontal_line = (HEIGHT // 2) + 50

RED = (255, 0, 0)  # Colours
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

player_size = 50
player_pos = [WIDTH//2, HEIGHT-2*player_size]
# If you want player exactly in middle: WIDTH/2 - player_size/2

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), 100]  # position of first blue box
enemy_list = [enemy_pos]

SPEED = 7
score = 60  # should be 0
num_enemies = 5
level = 1  # should be 1
screen = pygame.display.set_mode((WIDTH, HEIGHT))

counter = 0
counter2 = 0
right_side = True  # Used to put player on the right side of the screen at the start of level 4
game_over = False
clock = pygame.time.Clock()


def set_level(score: int, player_pos: List[int, int]) -> int:
    """
    Change SPEED, number of blue boxes, and level as required.
    :param score: current score
    :param player_pos: position of the player
    :return: updated SPEED
    """
    global num_enemies, level, WIDTH, enemy_size, screen, draw_line, HEIGHT, player_size, counter, right_side
    if score < 20:
        SPEED = 7
        num_enemies = 8
        level = 1
    elif score < 40:
        SPEED = 10
        num_enemies = 11
        level = 2
    elif score < 60:
        SPEED = 14
        num_enemies = 14
        level = 3
    elif score < 100:
        SPEED = 16
        WIDTH = 600
        level = 4
        if player_pos[0] >= 600 and right_side:
            player_pos[0] = 600-player_size
            right_side = False
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    else:  # if score >= 100
        draw_line = True
        if player_pos[1] <= horizontal_line:
            draw_line = False
            HEIGHT = 600 // 2 + 50 + (3 * player_size)  # Change height of screen
        player_size = 40
        SPEED = 19
        num_enemies = 16
        WIDTH = 600
        if player_pos[1] > horizontal_line:
            player_pos[1] -= 1
        if player_pos[0] >= WIDTH:
            # if the player is near the right side of the screen, don't cut them off the screen
            player_pos[0] = WIDTH-player_size
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        level = 5
    return SPEED


def scores() -> None:
    """
    Print new scores. Update 'High Scores.txt' if needed.
    """
    if score < high_scores[4]:  # IF user is not in the top 5
        same_scores = True
    else:
        same_scores = False
        if score >= high_scores[4]:  # If the user is now in the top 5
            name = str(input("Enter your name: "))  # Prompts user to enter their name
            if score > high_scores[0]:  # If the user is now in first place
                for i in range(4, 0, -1):  # Drops everyone in the standings down by 1
                    high_scores[i] = high_scores[i - 1]
                high_scores[0] = score

                for i in range(4, 0, -1):  # Drops everyone in the standings down by 1
                    high_scores_names[i] = high_scores_names[i - 1]
                high_scores_names[0] = name

            elif high_scores[1] <= score < high_scores[0]:  # If the user is now in second place
                # high_scores[0] remains the same
                for i in range(4, 1, -1):  # Drops everyone in the standings down by 1
                    high_scores[i] = high_scores[i - 1]
                for i in range(4, 1, -1):  # Drops everyone in the standings down by 1
                    high_scores_names[i] = high_scores_names[i - 1]
                high_scores[1] = score
                high_scores_names[1] = name

            elif high_scores[2] <= score < high_scores[1]:  # If the user is now in third place
                for i in range(4, 2, -1):  # Drops everyone in the standings down by 1
                    high_scores[i] = high_scores[i - 1]
                for i in range(4, 2, -1):  # Drops everyone in the standings down by 1
                    high_scores_names[i] = high_scores_names[i - 1]
                high_scores[2] = score
                high_scores_names[2] = name

            elif high_scores[3] <= score < high_scores[2]:  # If the user is now in fourth place
                for i in range(4, 3, -1):  # Drops everyone in the standings down by 1
                    high_scores[i] = high_scores[i - 1]
                for i in range(4, 3, -1):  # Drops everyone in the standings down by 1
                    high_scores_names[i] = high_scores_names[i - 1]
                high_scores[3] = score
                high_scores_names[3] = name
            elif high_scores[4] <= score < high_scores[3]:  # If the user is now in fifth place
                high_scores[4] = score
                high_scores_names[4] = name

        open("High Scores.txt", "w").close()  # Delete everything in the text file
        updated_lines = ['a', 1, 'b', 2, 'c', 3, 'd', 4, 'e', 5]  # Creates list with 10 elements
        updated_lines[0] = high_scores_names[0]  # Update the high scores information
        updated_lines[1] = str(high_scores[0])
        updated_lines[2] = high_scores_names[1]
        updated_lines[3] = str(high_scores[1])
        updated_lines[4] = high_scores_names[2]
        updated_lines[5] = str(high_scores[2])
        updated_lines[6] = high_scores_names[3]
        updated_lines[7] = str(high_scores[3])
        updated_lines[8] = high_scores_names[4]
        updated_lines[9] = str(high_scores[4])

        counter = 0  # See for loop below
        with open('High Scores.txt', 'w') as file:  # Writes information to the text file
            for i in updated_lines:
                counter += 1
                file.write(i)
                if counter <= 9:  # This prevents making an extra line at the end of the file
                    file.write('\n')

    longest_name = len(max(high_scores_names, key=len))  # Gets the length of the longest name

    print ('')
    print ('Your score: ', score)
    if same_scores:  # If the high scores remained the same
        print ('')
        print ('The high scores did not change.')
        print ('')
        print (' HIGH SCORES')
    else:
        print ('')
        print('NEW HIGH SCORES')

    for i in range(0, 5, 1):
        # print (high_scores_names[i], high_scores[i])  # Prints the new high scores
        print(high_scores_names[i].ljust(longest_name + 1, ' '),
              str(high_scores[i]).ljust(20, ' '))  # Prints the high scores


def drop_enemies(enemy_list: List[List[int, int]]) -> None:
    """
    Append to <enemy_list> if there are not enough blue boxes on the screen.
    :param enemy_list: List of blue boxes
    :return: None
    """
    delay = random.random()
    if len(enemy_list) < num_enemies and delay < 0.1:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list: List[List[int, int]]):
    """
    Draw the blue boxes to the screen
    :param enemy_list: List of blue boxes
    :return: None
    """
    if level <= 4:
        for enemy_pos in enemy_list:
            pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    else:
        for enemy_pos in enemy_list:
            pygame.draw.rect(screen, WHITE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_positions(enemy_list: List[List[int, int]]) -> int:
    """
    Update the positions of the blue boxes. If a blue box goes past the player,
    increment the score by 1.
    :param enemy_list: List of blue boxes
    :return: the updated score
    """
    # Updates position of enemy
    global score
    for idx, enemy_pos in enumerate(enemy_list):
        if 0 <= enemy_pos[1] <= HEIGHT:  # If enemy block is still in game
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
        if level >= 4:
            diagonal = random.random()
            if diagonal <= 0.5: # About 50% of the enemies will go diagonally
                enemy_pos[0] += 3
    return score


def collision_check(enemy_list: List[List[int, int]], player_pos: List[int, int]) -> bool:
    """
    :param enemy_list: List of blue boxes
    :param player_pos: Position of the player
    :return: True iff the player is touching a blue box.
    """
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False


def detect_collision(player_pos: List[int, int], enemy_pos: List[int, int]) -> bool:
    """
    :param player_pos: Position of the player
    :param enemy_pos: Position of a blue box
    :return: True iff <player_pos> and <enemy_pos> are touching/colliding.
    """
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (p_x < e_x < p_x + player_size) or (e_x < p_x < e_x + enemy_size):
        if (p_y < e_y < p_y + player_size) or (e_y < p_y < e_y + enemy_size):
            return True
    return False


def ready() -> None:
    """
    The screen before the game starts.
    Exit this function when the user presses any key.
    """
    screen.fill(BLACK)
    text3 = "Press any key to start the game."
    label3 = font.render(text3, 1, WHITE)
    screen.blit(label3, (60, 40))
    pygame.display.update()
    while True:
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN:
                pygame.mixer.music.play(-1, 0)  # Plays the background music
                return None


ready()


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and x >= player_size:
                x -= player_size  # move left
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and x < WIDTH - player_size:
                x += player_size  # move right

            player_pos = [x, y]

    screen.fill(BLACK)
    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list)
    SPEED = set_level(score, player_pos)

    text = "Score: " + str(score)
    label = font.render(text, 1, YELLOW)  # Display score
    text2 = "Level: " + str(level)
    label2 = font.render(text2, 1, RED)  # Display Label
    screen.blit(label2, (10, HEIGHT - 40))
    screen.blit(label, (WIDTH - 210, HEIGHT - 40))

    if collision_check(enemy_list, player_pos):
        draw_enemies(enemy_list)
        scores()  # Updates the new high scores
        game_over = True

    draw_enemies(enemy_list)  # Draws enemies
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))  # draw player
    if draw_line:
        pygame.draw.line(screen, WHITE, (0, horizontal_line), (WIDTH, horizontal_line), 2)  # Horizontal line
    if level == 5:
        clock.tick(35)  # 35 frames per second
    else:
        clock.tick(30)

    pygame.display.update()  # Update screen

