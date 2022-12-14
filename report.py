"""è´ªåð"""

import random
import sys
import time
import pygame
from pygame.locals import *
import collections             # ç¨äºåå§åð

SCREEN_WIDTH = 600      # å±å¹å®½åº¦
SCREEN_HEIGHT = 600     # å±å¹é«åº¦
SIZE = 20               # å°æ¹æ ¼å¤§å°
LINE_WIDTH = 1          # ç½æ ¼çº¿å®½åº¦

# æ¸¸æåºåçåæ èå´ï¼æ ¼å­åºåï¼
SCOPE_X = [0, SCREEN_WIDTH // SIZE - 1]
SCOPE_Y = (3, SCREEN_HEIGHT // SIZE - 1)

# ä¸ç§é£ç©çåå¼åé¢è²
FOOD_STYLE_LIST = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]


DARK = (200, 200, 200)      # èçé¢è²
BLACK = (0, 0, 0)           # ç½æ ¼çº¿é¢è²
RED = (200, 30, 30)         # çº¢è²ï¼GAME OVER çå­ä½é¢è²
PINK = (255, 192, 203)
BGCOLOR = (255, 255, 255)      # èæ¯è²


# æ·»å æå­ââéåº¦/å¾å
def print_text(screen, font, x, y, text, fcolor=(0, 0, 0)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


# åå§åð
def init_snake():
    snake = collections.deque()        # ç¨åç«¯éååé 
    snake.append((2, SCOPE_Y[0]))      # ðå¤´
    snake.append((1, SCOPE_Y[0]))
    snake.append((0, SCOPE_Y[0]))      # ðå°¾
    return snake


# çæé£ç©
def create_food(snake):
    food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
    food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    while (food_x, food_y) in snake:
        # å¦æé£ç©åºç°å¨ðèº«ä¸ï¼åéæ¥
        food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    return food_x, food_y


# éæºå°ç¹çæä¸ç§é£ç©
def get_food_style():
    return FOOD_STYLE_LIST[random.randint(0, 2)]


# ç»èæ¯
def background_fill(screen, chicken_2, count):
    # å¡«åèæ¯å¾ç
    # å¦ææ²¡æèæ¯å¾çå¯ä»¥å¡«ååªçº¯è²
    screen.fill(BGCOLOR)    # å¡«åçº¯è²
    num = 4
    # èæ¯å¾ç
    '''if chicken_2 == 1:
        if count == 0:
            back_image = pygame.image.load('pt2.jpg')
        elif count == 1:
            back_image = pygame.image.load('pt3.jpg')
        elif count == 2:
            back_image = pygame.image.load('pt4.jpg')
        elif count == 3:
            back_image = pygame.image.load('pt5.jpg')
        elif count == 4:
            back_image = pygame.image.load('pt6.jpg')
        elif count == 5:
            back_image = pygame.image.load('pt7.jpg')
        elif count == 6:
            back_image = pygame.image.load('pt8.jpg')
    elif chicken_2 == 2:
        back_image = pygame.image.load('pt1.jpg')'''
    elif not chicken_2:
        back_image = pygame.image.load('back1.jpg')
    screen.blit(back_image, (0, 0))
    count += 1
    if count == num:
        count = 0
    # ç»ç½æ ¼çº¿ ç«çº¿
    for x in range(SIZE, SCREEN_WIDTH, SIZE):
        pygame.draw.line(screen, BLACK, (x, SCOPE_Y[0] * SIZE), (x, SCREEN_HEIGHT), LINE_WIDTH)
    # ç»ç½æ ¼çº¿ æ¨ªçº¿
    for y in range(SCOPE_Y[0] * SIZE, SCREEN_HEIGHT, SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)
    return count


# èªå¨ð
def auto_snake(food, snake, b, pos):
    left = (-1, 0)
    right = (1, 0)
    up = (0, -1)
    down = (0, 1)
    # 1.ðå¨é£ç©å·¦è¾¹ï¼
    if snake[0][0] < food[0]:
        if b and pos[0] != -1:
            pos, b = snake_turn(snake, b, right)    # åå³è½¬
        elif b and pos[0] == -1:                    # ðå¨åå·¦
            pos, b = snake_u_turn(snake, food, b, pos)
        return pos, b

    # 2.ðå¨é£ç©å³è¾¹
    elif snake[0][0] > food[0]:
        if b and pos[0] != 1:
            pos, b = snake_turn(snake, b, left)
        elif b and pos[0] == 1:
            pos, b = snake_u_turn(snake, food, b, pos)
        return pos, b

    # 3.ðå¨é£ç©ä¸é¢
    elif snake[0][1] < food[1]:
        if b and pos[1] != -1:
            pos, b = snake_turn(snake, b, down)
        elif b and pos[1] == -1:
            pos, b = snake_u_turn(snake, food, b, pos)
        return pos, b

    # 4.ðå¨é£ç©ä¸é¢
    elif snake[0][1] > food[1]:
        if b and pos[1] != 1:
            pos, b = snake_turn(snake, b, up)
        elif b and pos[1] == 1:
            pos, b = snake_u_turn(snake, food, b, pos)
        return pos, b


# è½¬å
def snake_turn(snake, b, pos):
    # å¤æ­è½¬åæ¯å¦ä¼æå°èªå·±
    next_step = (snake[0][0] + pos[0], snake[0][1] + pos[1])
    if next_step in snake:  # å¦ææå°èªå·±,å°±æ¢ä¸ªæ¹å
        pos, b = avoid_snake(snake, b, pos)
    b = False
    return pos, b


# æå¤´,æ ¹æ®é£ç©ä½ç½®ç¡®å®æå¤´æ¹å
# å¦å¤å¯è®¾è®¡å½æ°æ ¹æ®éå¿ä½ç½®ç¡®å®æå¤´æ¹åï¼è¿éæåªéç¨é£ç©å¯¼å
def snake_u_turn(snake, food, b, pos):
    pos_1 = pos
    if pos[0] and b:  # ðæ­£å¨å·¦å³ç§»å¨
        if snake[0][1] <= food[1] and b:    # ðå¨é£ç©ä¸è¾¹
            pos, b = avoid_one_step(snake, (0, 1), b)       # åä¸
            if b:
                pos, b = avoid_one_step(snake, (0, -1), b)  # åä¸
        if snake[0][1] >= food[1] and b:    # ðå¨é£ç©ä¸è¾¹
            pos, b = avoid_one_step(snake, (0, -1), b)      # åä¸
            if b:
                pos, b = avoid_one_step(snake, (0, 1), b)   # åä¸
        if b:
            pos = pos_1
            b = False
    elif pos[1] and b:
        if snake[0][0] <= food[0] and b:    # ðå¨é£ç©å·¦è¾¹
            pos, b = avoid_one_step(snake, (1, 0), b)       # åå³
            if b:
                pos, b = avoid_one_step(snake, (-1, 0), b)  # åå·¦
        if snake[0][0] >= food[0] and b:    # ðå¨é£ç©å³è¾¹
            pos, b = avoid_one_step(snake, (-1, 0), b)      # åå·¦
            if b:
                pos, b = avoid_one_step(snake, (1, 0), b)   # åå³
        if b:
            pos = pos_1
            b = False
    return pos, b


# é¿è®©ç¨åºï¼å½è½¬åä¼æå°èªå·±çèº«ä½ï¼
# ä¸¤ç§æåµï¼1.ä¸è½¬åå³å¯èº²è¿å» 2.éè¦åå«çæ¹åè½¬å
def avoid_snake(snake, b, pos):
    pos_1 = pos
    avoid = centre_of_snake(snake)
    if pos_1[0] and b:  # ðæ³åå·¦å³ç§»å¨
        if avoid[1] >= 0 and b:     # èº«ä½å¨èä¸æ¹
            pos, b = avoid_one_step(snake, (0, 1), b)       # åä¸
            if b:   # åä¸ä¸æå
                pos, b = avoid_one_step(snake, (0, -1), b)  # åä¸
        if avoid[1] <= 0 and b:     # èº«ä½å¨èä¸æ¹
            pos, b = avoid_one_step(snake, (0, -1), b)      # åä¸
            if b:
                pos, b = avoid_one_step(snake, (0, 1), b)   # åä¸
        # ä¸è½åä¸ä¹ä¸è½åä¸
        if b:
            if pos_1[0] == 1:
                pos, b = avoid_one_step(snake, (-1, 0), b)  # åå·¦
            elif pos_1[0] == -1:
                pos, b = avoid_one_step(snake, (1, 0), b)   # åå³
            if b:
                pos = pos_1
        return pos, b
    elif pos_1[1] and b:  # ðæ³åä¸ä¸ç§»å¨
        if avoid[0] >= 0 and b:     # èº«ä½å¨èå·¦è¾¹
            pos, b = avoid_one_step(snake, (1, 0), b)       # åå³
            if b:
                pos, b = avoid_one_step(snake, (-1, 0), b)  # åå·¦
        if avoid[0] <= 0 and b:
            pos, b = avoid_one_step(snake, (-1, 0), b)      # åå·¦
            if b:
                pos, b = avoid_one_step(snake, (1, 0), b)   # åå³
        if b:
            if pos_1[1] == 1:
                pos, b = avoid_one_step(snake, (0, -1), b)  # åä¸
            elif pos_1[1] == -1:
                pos, b = avoid_one_step(snake, (0, 1), b)   # åä¸
            if b:
                pos = pos_1
        return pos, b


# æ£æµä¸ä¸æ­¥å¹¶é¿è®©
# å¦æå¯ä»¥è½¬ååè¿å b = Falseåposï¼å¦åè¿å b = True ä»¥ä¾ç»§ç»­è½¬å
def avoid_one_step(snake, pos, b):
    next_step = (snake[0][0] + pos[0], snake[0][1] + pos[1])  # å¤æ­å¯å¦åposæ¹å
    if SCOPE_X[0] <= next_step[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_step[1] <= SCOPE_Y[1] \
            and next_step not in snake:  # å¯ä»¥åposæ¹å
        b = False
    else:
        b = True
    return pos, b


# ðçéå¿è®¡ç®
# è¿åðç¸å¯¹éå¿çä½ç½®
def centre_of_snake(snake):
    x_centre = y_centre = 0
    count = 0
    for s in snake:
        if count < 10:
            count += 1
            x_centre += s[0]
            y_centre += s[1]
        else:
            break
    ct = (x_centre/10, y_centre/10)
    avoid = (snake[0][0] - ct[0], snake[0][1] - ct[1])      # èç¸å¯¹éå¿çä½ç½®
    return avoid


def main():
    pygame.init()                                                       # åå§å
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # åå§åèæ¯çªå£
    pygame.display.set_caption('å°æ¸¸æè´ªåè')                             # çªå£æ é¢

    font1 = pygame.font.SysFont('KaiTi', 24)                    # å¾ååéåº¦çå­ä½
    font2 = pygame.font.Font(None, 72)                          # GAME OVER çå­ä½
    font3 = pygame.font.SysFont('SimHei', 10, italic=True)      # å°ç»åçå­ä½
    fwidth1, fheight1 = font2.size('GAME OVER')
    fwidth2, fheight2 = font2.size('GOOD')

    # b æ¯ä¸´çéï¼ä½¿ä¸æ¬¡å¾ªç¯ï¼ðåè¿ä¸æ­¥ï¼åªè½è¿è¡ä¸ç§æä½
    b = True
    # è
    snake = init_snake()
    # é£ç©
    food = create_food(snake)
    food_style = get_food_style()
    # æ¹å
    pos = (1, 0)

    game_over = True
    start = False       # æ¯å¦å¼å§ï¼å½start = Trueï¼game_over = True æ¶ï¼ææ¾ç¤º GAME OVER
    score = 0           # å¾å
    ori_speed = 0.1     # åå§éåº¦
    speed = ori_speed
    last_move_time = None   # ä¸æ¬¡ç§»å¨çæ¶é´
    pause = False       # æå
    # åç§æ è¯åé
    count_time = 0      # ç¨äºæ¾ç¤ºå¾ååºç¥
    cheat = 0           # ç¨äºå¼å³èªå¨ç¨åº
    chicken_1 = 0       # ç¨äºåæ¢èæ¯å¾çé
    chicken_2 = 0
    count = 0           # ç¨äºå¨ææ¾ç¤ºèæ¯å¾ç
    # æ¸¸æä¸»å¾ªç¯
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:          # ç¨æ·å³é­çªå£
                sys.exit()                  # ç¨æ·å³é­çªå£åéåº
            elif event.type == KEYDOWN:     # ç¨æ·æä¸é®ç
                cheat = 0
                if event.key == K_RETURN:   # ç¨æ·æä¸returné®å¼å§æ¸¸æ
                    if game_over:           # å¦æåå¼å§æ¸¸æï¼åè¿è¡åå§åï¼å¦åä¸å
                        start = True
                        game_over = False
                        b = True            # åå§æ¶ä¸´çéå¯è·å¾
                        snake = init_snake()
                        food = create_food(snake)
                        food_style = get_food_style()
                        pos = (1, 0)    # ðåå³
                        # å¾å
                        score = 0
                        last_move_time = time.time()    # å½åç³»ç»æ¶é´
                elif event.key == K_SPACE:              # æä¸spaceæåæç»§ç»­æ¸¸æ
                    if not game_over:
                        pause = not pause
                # æä¸æ¹åé®æ§å¶ð
                elif event.key == K_UP:
                    if b and not pos[1]:    # å½ä¸´çéå¯è·å¾å¹¶ä¸ðæ²¡æåä¸åä¸
                        pos = (0, -1)       # ðåä¸
                        b = False           # æ¬æ¬¡å¾ªç¯ä¸´çéä¸å¯è·å¾ï¼æ æ³åè¿è¡æ¹åæä½
                elif event.key == K_DOWN:
                    if b and not pos[1]:
                        pos = (0, 1)        # ðåä¸
                        b = False
                elif event.key == K_LEFT:
                    if b and not pos[0]:
                        pos = (-1, 0)       # ðåå·¦
                        b = False
                elif event.key == K_RIGHT:
                    if b and not pos[0]:
                        pos = (1, 0)        # ðåå³
                        b = False
                elif event.key == K_q:
                    cheat = 1
                if event.key == K_j:
                    cheat = 1
                    chicken_1 = 1
                if event.key == K_k:
                    cheat = 1
                    chicken_2 = 2
        if not game_over:
            if cheat:
                pos, b = auto_snake(food, snake, b, pos)
            curTime = time.time()    # å½åæ¶é´
            if curTime - last_move_time > speed:    # æ ¹æ®éåº¦ä½¿ðç§»å¨
                if not pause:
                    b = True
                    last_move_time = curTime
                    print(pos)
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])    # ä¸ä¸æ­¥ðå¤´çä½ç½®
                    if next_s == food:              # åå°äºé£ç©
                        count_time = curTime
                        snake.appendleft(next_s)
                        score += food_style[0]
                        speed = 1.0/((score+1000) // 100)      # ðçéåº¦éåæ°å¢å 
                        food = create_food(snake)
                        food_style = get_food_style()
                    else:
                        if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] \
                                and next_s not in snake:    # ðæ²¡ç¢°å°è¾¹çä¸æ²¡ç¢°å°èªå·±
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True
        # å¥½æ£
        if chicken_2 == 2:
            if time.time() - count_time < 1:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth2) // 2, (SCREEN_HEIGHT - fheight2) // 2,
                           'GOOD', PINK)
        # å¥½æ£
        else:
            if time.time() - count_time < 1:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth2) // 2, (SCREEN_HEIGHT - fheight2) // 2,
                           'GOOD', PINK)
        # ç»èæ¯
        if chicken_1 and not chicken_2:
            chicken_2 = 1
        elif chicken_1 and chicken_2:
            chicken_2 = 0
        chicken_1 = 0
        count = background_fill(screen, chicken_2, count)
        # ç»é£ç©
        pygame.draw.rect(screen, food_style[1], (food[0] * SIZE, food[1] * SIZE, SIZE, SIZE), 0)
        # ç»è
        for s in snake:
            # å½æ°ç¨æ³ï¼pygame.draw.rect(è¡¨é¢ï¼é¢è²ï¼rectï¼å·¦ï¼ä¸ï¼å®½ï¼é«ï¼ï¼å®½åº¦ï¼
            pygame.draw.rect(screen, BLACK, (s[0] * SIZE + LINE_WIDTH, s[1] * SIZE + LINE_WIDTH,
                                            SIZE - LINE_WIDTH, SIZE - LINE_WIDTH), 0)
        # æ¾ç¤ºå°ç»å
        print_text(screen, font3, 0, 0, f'ææé©ï¼å½­é¸ï¼ç½å®ç§å°ç»', (0, 0, 0))
        print_text(screen, font3, 0, 8, f'ââââââââââââ', (0, 0, 0))
        # æ¾ç¤ºåæ°
        print_text(screen, font1, 10, 20, f'éåº¦: {1+score//100}')
        print_text(screen, font1, 300, 20, f'å¾å: {score}')
        if chicken_2 == 2:
            if time.time() - count_time < 1:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth2) // 2, (SCREEN_HEIGHT - fheight2) // 2,
                           'GOOD', PINK)
        # å¥½æ£
        else:
            if time.time() - count_time < 1:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth2) // 2, (SCREEN_HEIGHT - fheight2) // 2,
                           'GOOD', PINK)
        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth1) // 2, (SCREEN_HEIGHT - fheight1) // 2,
                           'GAME OVER', RED)
                speed = ori_speed    # éåº¦åæ­£

        pygame.display.update()


if __name__ == '__main__':
    main()
