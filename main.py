import pygame, math, random, os

pygame.init()
W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 40, True)
big = pygame.font.SysFont("Arial", 100, True)

# =====================
# СОСТОЯНИЯ
# =====================
state = "menu"
difficulty = 1  # 1 easy, 2 normal, 3 hard

# =====================
# ИГРОК
# =====================
p_pos = [W//2, H//2]
hp = 5

# =====================
# ДЖОЙСТИКИ
# =====================
j_rad = 120
j_base = [200, H-200]
j_move = list(j_base)
j_on = False

j_base_shoot = [W-200, H-200]
j_shoot = list(j_base_shoot)
j_shoot_on = False

# =====================
# ДУЭЛЬ
# =====================
enemy = {"pos":[W//2,200], "hp":5}

# =====================
# ИГРА
# =====================
bullets = []
enemies = []
score = 0
last_shot = 0
last_spawn = 0

def draw(text,x,y,f=font):
    screen.blit(f.render(text,True,(255,255,255)),(x,y))

run = True
while run:
    screen.fill((20,20,30))
    now = pygame.time.get_ticks()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()

            if state=="menu":
                if 400<mx<800 and 300<my<380:
                    state="lobby"
                if 400<mx<800 and 420<my<500:
                    state="duel"

            elif state=="lobby":
                if 400<mx<800 and 300<my<380:
                    difficulty=1; state="game"
                if 400<mx<800 and 420<my<500:
                    difficulty=2; state="game"
                if 400<mx<800 and 540<my<620:
                    difficulty=3; state="game"

            elif state=="duel":
                if mx < W//2:
                    j_on=True
                else:
                    j_shoot_on=True

        if e.type == pygame.MOUSEBUTTONUP:
            j_on=False
            j_shoot_on=False
            j_move=list(j_base)
            j_shoot=list(j_base_shoot)

    # ================= MENU =================
    if state=="menu":
        draw("BULLET KNIGHT",300,120,big)

        pygame.draw.rect(screen,(0,200,100),(400,300,400,80))
        draw("START",520,310)

        pygame.draw.rect(screen,(200,50,50),(400,420,400,80))
        draw("DUEL",540,430)

        pygame.display.flip(); clock.tick(60); continue

    # ================= LOBBY =================
    if state=="lobby":
        draw("SELECT DIFFICULTY",300,150)

        pygame.draw.rect(screen,(50,200,50),(400,300,400,80))
        draw("EASY",540,310)

        pygame.draw.rect(screen,(200,200,50),(400,420,400,80))
        draw("NORMAL",510,430)

        pygame.draw.rect(screen,(200,50,50),(400,540,400,80))
        draw("HARD",540,550)

        pygame.display.flip(); clock.tick(60); continue

    # ================= DUEL =================
    if state=="duel":

        if j_on:
            mx,my=pygame.mouse.get_pos()
            ang=math.atan2(my-j_base[1],mx-j_base[0])
            p_pos[0]+=math.cos(ang)*6
            p_pos[1]+=math.sin(ang)*6

        if j_shoot_on and now-last_shot>200:
            mx,my=pygame.mouse.get_pos()
            ang=math.atan2(my-j_base_shoot[1],mx-j_base_shoot[0])
            bullets.append([list(p_pos),ang])
            last_shot=now

        for b in bullets[:]:
            b[0][0]+=math.cos(b[1])*10
            b[0][1]+=math.sin(b[1])*10

            pygame.draw.circle(screen,(255,255,0),(int(b[0][0]),int(b[0][1])),8)

            if math.hypot(b[0][0]-enemy["pos"][0],b[0][1]-enemy["pos"][1])<30:
                enemy["hp"]-=1
                bullets.remove(b)

        pygame.draw.rect(screen,(255,50,50),(*enemy["pos"],50,50))
        pygame.draw.rect(screen,(0,200,255),(*p_pos,50,50))

        pygame.draw.circle(screen,(100,100,100),j_base,j_rad,3)
        pygame.draw.circle(screen,(200,200,200),j_move,40)

        pygame.draw.circle(screen,(100,100,100),j_base_shoot,j_rad,3)
        pygame.draw.circle(screen,(255,100,100),j_shoot,40)

        draw(f"ENEMY HP: {enemy['hp']}",50,50)

        if enemy["hp"]<=0:
            draw("YOU WIN",450,300,big)

        pygame.display.flip(); clock.tick(60); continue

    # ================= GAME =================
    if state=="game":

        # сложность
        spawn_delay = 2000 // difficulty
        speed_mul = 1 + (difficulty-1)*0.5

        # автоатака (оставили!)
        if now-last_shot>400:
            if enemies:
                t=min(enemies,key=lambda e: math.hypot(e[0]-p_pos[0],e[1]-p_pos[1]))
                ang=math.atan2(t[1]-p_pos[1],t[0]-p_pos[0])
                bullets.append([list(p_pos),ang])
                last_shot=now

        # спавн
        if now-last_spawn>spawn_delay:
            enemies.append([random.randint(50,W-50),50,1])
            last_spawn=now

        # движение (один джойстик)
        if j_on:
            mx,my=pygame.mouse.get_pos()
            ang=math.atan2(my-j_base[1],mx-j_base[0])
            p_pos[0]+=math.cos(ang)*6
            p_pos[1]+=math.sin(ang)*6

        # пули
        for b in bullets[:]:
            b[0][0]+=math.cos(b[1])*10
            b[0][1]+=math.sin(b[1])*10
            pygame.draw.circle(screen,(255,255,0),(int(b[0][0]),int(b[0][1])),8)

            for e in enemies[:]:
                if math.hypot(b[0][0]-e[0],b[0][1]-e[1])<25:
                    enemies.remove(e)
                    bullets.remove(b)
                    score+=10
                    break

        # враги
        for e in enemies:
            dx=p_pos[0]-e[0]
            dy=p_pos[1]-e[1]
            d=math.hypot(dx,dy)
            if d!=0:
                e[0]+=dx/d*2*speed_mul
                e[1]+=dy/d*2*speed_mul

            pygame.draw.rect(screen,(255,0,0),(e[0],e[1],40,40))

            if d<30:
                hp-=1
                enemies.clear()

        pygame.draw.rect(screen,(0,200,255),(*p_pos,50,50))

        draw(f"SCORE: {score}",40,40)
        draw(f"HP: {hp}",40,90)

        if hp<=0:
            state="menu"
            hp=5
            score=0
            enemies.clear()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
