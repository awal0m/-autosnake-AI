"""贪吃🐍"""

import random
import sys
import time
import pygame
from pygame.locals import *
import collections             # 用于初始化🐍

SCREEN_WIDTH = 600      # 屏幕宽度
SCREEN_HEIGHT = 600     # 屏幕高度
SIZE = 20               # 小方格大小
LINE_WIDTH = 1          # 网格线宽度

# 游戏区域的坐标范围（格子区域）
SCOPE_X = [0, SCREEN_WIDTH // SIZE - 1]
SCOPE_Y = (3, SCREEN_HEIGHT // SIZE - 1)

# 三种食物的分值及颜色
FOOD_STYLE_LIST = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]


DARK = (200, 200, 200)      # 蛇的颜色
BLACK = (0, 0, 0)           # 网格线颜色
RED = (200, 30, 30)         # 红色，GAME OVER 的字体颜色
PINK = (255, 192, 203)
BGCOLOR = (255, 255, 255)      # 背景色


# 添加文字——速度/得分
def print_text(screen, font, x, y, text, fcolor=(0, 0, 0)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


# 初始化🐍
def init_snake():
    snake = collections.deque()        # 用双端队列创造
    snake.append((2, SCOPE_Y[0]))      # 🐍头
    snake.append((1, SCOPE_Y[0]))
    snake.append((0, SCOPE_Y[0]))      # 🐍尾
    return snake


# 生成食物
def create_food(snake):
    food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
    food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    while (food_x, food_y) in snake:
        # 如果食物出现在🐍身上，则重来
        food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    return food_x, food_y


# 随机地点生成三种食物
def get_food_style():
    return FOOD_STYLE_LIST[random.randint(0, 2)]


# 画背景
def background_fill(screen, chicken_2, count):
    # 填充背景图片
    # 如果没有背景图片可以填充只纯色
    screen.fill(BGCOLOR)    # 填充纯色
    num = 4
    # 背景图片
    if chicken_2 == 1:
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
        back_image = pygame.image.load('pt1.jpg')
    elif not chicken_2:
        back_image = pygame.image.load('back1.jpg')
    screen.blit(back_image, (0, 0))
    count += 1
    if count == num:
        count = 0
    # 画网格线 竖线
    for x in range(SIZE, SCREEN_WIDTH, SIZE):
        pygame.draw.line(screen, BLACK, (x, SCOPE_Y[0] * SIZE), (x, SCREEN_HEIGHT), LINE_WIDTH)
    # 画网格线 横线
    for y in range(SCOPE_Y[0] * SIZE, SCREEN_HEIGHT, SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)
    return count


# 自动🐍
def auto_snake(food, snake, b, pos):
    left = (-1, 0)
    right = (1, 0)
    up = (0, -1)
    down = (0, 1)
    # 1.🐍在食物左边：
    if snake[0][0] < food[0]:
        if b and pos[0] != -1:
            pos, b = snake_turn(snake, b, right)    # 向右转
        elif b and pos[0] == -1:                    # 🐍在向左
            pos, b = snake_u_turn(snake, food, b, pos)
        return pos, b

    # 2.🐍在食物右边
    elif snake[0][0] > food[0]:
        if b and pos[0] != 1:
            pos, b = snake_turn(snake, b, left)
        elif b and pos[0] == 1:
            pos, b = snake_u_turn(snake, food, b, pos)
        return pos, b

    # 3.🐍在食物上面
    elif snake[0][1] < food[1]:
        if b and pos[1] != -1:
            pos, b = snake_turn(snake, b, down)
        elif b and pos[1] == -1:
            pos, b = snake_u_turn(snake, food, b, pos)
        return pos, b

    # 4.🐍在食物下面
    elif snake[0][1] > food[1]:
        if b and pos[1] != 1:
            pos, b = snake_turn(snake, b, up)
        elif b and pos[1] == 1:
            pos, b = snake_u_turn(snake, food, b, pos)
        return pos, b


# 转向
def snake_turn(snake, b, pos):
    # 判断转向是否会撞到自己
    next_step = (snake[0][0] + pos[0], snake[0][1] + pos[1])
    if next_step in snake:  # 如果撞到自己,就换个方向
        pos, b = avoid_snake(snake, b, pos)
    b = False
    return pos, b


# 掉头,根据食物位置确定掉头方向
# 另外可设计函数根据重心位置确定掉头方向，这里我只采用食物导向
def snake_u_turn(snake, food, b, pos):
    pos_1 = pos
    if pos[0] and b:  # 🐍正在左右移动
        if snake[0][1] <= food[1] and b:    # 🐍在食物上边
            pos, b = avoid_one_step(snake, (0, 1), b)       # 向下
            if b:
                pos, b = avoid_one_step(snake, (0, -1), b)  # 向上
        if snake[0][1] >= food[1] and b:    # 🐍在食物下边
            pos, b = avoid_one_step(snake, (0, -1), b)      # 向上
            if b:
                pos, b = avoid_one_step(snake, (0, 1), b)   # 向下
        if b:
            pos = pos_1
            b = False
    elif pos[1] and b:
        if snake[0][0] <= food[0] and b:    # 🐍在食物左边
            pos, b = avoid_one_step(snake, (1, 0), b)       # 向右
            if b:
                pos, b = avoid_one_step(snake, (-1, 0), b)  # 向左
        if snake[0][0] >= food[0] and b:    # 🐍在食物右边
            pos, b = avoid_one_step(snake, (-1, 0), b)      # 向左
            if b:
                pos, b = avoid_one_step(snake, (1, 0), b)   # 向右
        if b:
            pos = pos_1
            b = False
    return pos, b


# 避让程序（当转向会撞到自己的身体）
# 两种情况：1.不转向即可躲过去 2.需要向别的方向转向
def avoid_snake(snake, b, pos):
    pos_1 = pos
    avoid = centre_of_snake(snake)
    if pos_1[0] and b:  # 🐍想向左右移动
        if avoid[1] >= 0 and b:     # 身体在蛇上方
            pos, b = avoid_one_step(snake, (0, 1), b)       # 向下
            if b:   # 向下不成功
                pos, b = avoid_one_step(snake, (0, -1), b)  # 向上
        if avoid[1] <= 0 and b:     # 身体在蛇下方
            pos, b = avoid_one_step(snake, (0, -1), b)      # 向上
            if b:
                pos, b = avoid_one_step(snake, (0, 1), b)   # 向下
        # 不能向上也不能向下
        if b:
            if pos_1[0] == 1:
                pos, b = avoid_one_step(snake, (-1, 0), b)  # 向左
            elif pos_1[0] == -1:
                pos, b = avoid_one_step(snake, (1, 0), b)   # 向右
            if b:
                pos = pos_1
        return pos, b
    elif pos_1[1] and b:  # 🐍想向上下移动
        if avoid[0] >= 0 and b:     # 身体在蛇左边
            pos, b = avoid_one_step(snake, (1, 0), b)       # 向右
            if b:
                pos, b = avoid_one_step(snake, (-1, 0), b)  # 向左
        if avoid[0] <= 0 and b:
            pos, b = avoid_one_step(snake, (-1, 0), b)      # 向左
            if b:
                pos, b = avoid_one_step(snake, (1, 0), b)   # 向右
        if b:
            if pos_1[1] == 1:
                pos, b = avoid_one_step(snake, (0, -1), b)  # 向上
            elif pos_1[1] == -1:
                pos, b = avoid_one_step(snake, (0, 1), b)   # 向下
            if b:
                pos = pos_1
        return pos, b


# 检测下一步并避让
# 如果可以转向则返回 b = False和pos，否则返回 b = True 以供继续转向
def avoid_one_step(snake, pos, b):
    next_step = (snake[0][0] + pos[0], snake[0][1] + pos[1])  # 判断可否向pos方向
    if SCOPE_X[0] <= next_step[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_step[1] <= SCOPE_Y[1] \
            and next_step not in snake:  # 可以向pos方向
        b = False
    else:
        b = True
    return pos, b


# 🐍的重心计算
# 返回🐍相对重心的位置
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
    avoid = (snake[0][0] - ct[0], snake[0][1] - ct[1])      # 蛇相对重心的位置
    return avoid


def main():
    pygame.init()                                                       # 初始化
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))     # 初始化背景窗口
    pygame.display.set_caption('小游戏贪吃蛇')                             # 窗口标题

    font1 = pygame.font.SysFont('KaiTi', 24)                    # 得分和速度的字体
    font2 = pygame.font.Font(None, 72)                          # GAME OVER 的字体
    font3 = pygame.font.SysFont('SimHei', 10, italic=True)      # 小组名的字体
    fwidth1, fheight1 = font2.size('GAME OVER')
    fwidth2, fheight2 = font2.size('GOOD')

    # b 是临界量，使一次循环（🐍前进一步）只能进行一种操作
    b = True
    # 蛇
    snake = init_snake()
    # 食物
    food = create_food(snake)
    food_style = get_food_style()
    # 方向
    pos = (1, 0)

    game_over = True
    start = False       # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
    score = 0           # 得分
    ori_speed = 0.1     # 原始速度
    speed = ori_speed
    last_move_time = None   # 上次移动的时间
    pause = False       # 暂停
    # 各种标识变量
    count_time = 0      # 用于显示得分庆祝
    cheat = 0           # 用于开关自动程序
    chicken_1 = 0       # 用于切换背景图片集
    chicken_2 = 0
    count = 0           # 用于动态显示背景图片
    # 游戏主循环
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:          # 用户关闭窗口
                sys.exit()                  # 用户关闭窗口则退出
            elif event.type == KEYDOWN:     # 用户按下键盘
                cheat = 0
                if event.key == K_RETURN:   # 用户按下return键开始游戏
                    if game_over:           # 如果刚开始游戏，则进行初始化，否则不变
                        start = True
                        game_over = False
                        b = True            # 初始时临界量可获得
                        snake = init_snake()
                        food = create_food(snake)
                        food_style = get_food_style()
                        pos = (1, 0)    # 🐍向右
                        # 得分
                        score = 0
                        last_move_time = time.time()    # 当前系统时间
                elif event.key == K_SPACE:              # 按下space暂停或继续游戏
                    if not game_over:
                        pause = not pause
                # 按下方向键控制🐍
                elif event.key == K_UP:
                    if b and not pos[1]:    # 当临界量可获得并且🐍没有向上向下
                        pos = (0, -1)       # 🐍向上
                        b = False           # 本次循环临界量不可获得，无法再进行方向操作
                elif event.key == K_DOWN:
                    if b and not pos[1]:
                        pos = (0, 1)        # 🐍向下
                        b = False
                elif event.key == K_LEFT:
                    if b and not pos[0]:
                        pos = (-1, 0)       # 🐍向左
                        b = False
                elif event.key == K_RIGHT:
                    if b and not pos[0]:
                        pos = (1, 0)        # 🐍向右
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
            curTime = time.time()    # 当前时间
            if curTime - last_move_time > speed:    # 根据速度使🐍移动
                if not pause:
                    b = True
                    last_move_time = curTime
                    print(pos)
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])    # 下一步🐍头的位置
                    if next_s == food:              # 吃到了食物
                        count_time = curTime
                        snake.appendleft(next_s)
                        score += food_style[0]
                        speed = 1.0/((score+1000) // 100)      # 🐍的速度随分数增加
                        food = create_food(snake)
                        food_style = get_food_style()
                    else:
                        if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] \
                                and next_s not in snake:    # 🐍没碰到边界且没碰到自己
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True
        # 好棒
        if chicken_2 == 2:
            if time.time() - count_time < 1:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth2) // 2, (SCREEN_HEIGHT - fheight2) // 2,
                           'GOOD', PINK)
        # 好棒
        else:
            if time.time() - count_time < 1:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth2) // 2, (SCREEN_HEIGHT - fheight2) // 2,
                           'GOOD', PINK)
        # 画背景
        if chicken_1 and not chicken_2:
            chicken_2 = 1
        elif chicken_1 and chicken_2:
            chicken_2 = 0
        chicken_1 = 0
        count = background_fill(screen, chicken_2, count)
        # 画食物
        pygame.draw.rect(screen, food_style[1], (food[0] * SIZE, food[1] * SIZE, SIZE, SIZE), 0)
        # 画蛇
        for s in snake:
            # 函数用法：pygame.draw.rect(表面，颜色，rect（左，上，宽，高），宽度）
            pygame.draw.rect(screen, BLACK, (s[0] * SIZE + LINE_WIDTH, s[1] * SIZE + LINE_WIDTH,
                                            SIZE - LINE_WIDTH, SIZE - LINE_WIDTH), 0)
        # 显示小组名
        print_text(screen, font3, 0, 0, f'李易韩，彭逸，白宇科小组', (0, 0, 0))
        print_text(screen, font3, 0, 8, f'————————————', (0, 0, 0))
        # 显示分数
        print_text(screen, font1, 10, 20, f'速度: {1+score//100}')
        print_text(screen, font1, 300, 20, f'得分: {score}')
        if chicken_2 == 2:
            if time.time() - count_time < 1:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth2) // 2, (SCREEN_HEIGHT - fheight2) // 2,
                           'GOOD', PINK)
        # 好棒
        else:
            if time.time() - count_time < 1:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth2) // 2, (SCREEN_HEIGHT - fheight2) // 2,
                           'GOOD', PINK)
        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth1) // 2, (SCREEN_HEIGHT - fheight1) // 2,
                           'GAME OVER', RED)
                speed = ori_speed    # 速度回正

        pygame.display.update()


if __name__ == '__main__':
    main()
