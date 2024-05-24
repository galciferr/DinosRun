import pygame
import os
import random
pygame.init()

# Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUN = [pygame.image.load(os.path.join("Images/Dinos", "DinosRun_1.png")),
           pygame.image.load(os.path.join("Images/Dinos", "DinosRun_2.png"))]
JUMP = pygame.image.load(os.path.join("Images/Dinos", "DinosJump.png"))
CROUCH = [pygame.image.load(os.path.join("Images/Dinos", "DinosCrouch_1.png")),
          pygame.image.load(os.path.join("Images/Dinos", "DinosCrouch_2.png"))]
DEAD = pygame.image.load(os.path.join("Images/Dinos", "DinosDead.png"))

BIRD = [pygame.image.load(os.path.join("Images/Bird", "Bird_1.png")),
        pygame.image.load(os.path.join("Images/Bird", "Bird_2.png"))]

CLOUD = pygame.image.load(os.path.join("Images/Other", "Cloud.png"))

ROAD = pygame.image.load(os.path.join("Images/Other", "Road.png"))

GAME_OVER = pygame.image.load(os.path.join("Images/Other", "GameOver.png"))

BIG_CACTUS = [pygame.image.load(os.path.join("Images/Cactus", "BigCactus_1.png")),
              pygame.image.load(os.path.join("Images/Cactus", "BigCactus_2.png")),
              pygame.image.load(os.path.join("Images/Cactus", "BigCactus_3.png"))]
SMALL_CACTUS = [pygame.image.load(os.path.join("Images/Cactus", "SmallCactus_1.png")),
                pygame.image.load(os.path.join("Images/Cactus", "SmallCactus_2.png")),
                pygame.image.load(os.path.join("Images/Cactus", "SmallCactus_3.png"))]


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_CROUCH = 340
    JUMP_SPEED = 8.5

    def __init__(self):
        self.crouch_img = CROUCH
        self.run_img = RUN
        self.jump_img = JUMP
        self.dead_img = DEAD

        self.dinos_crouch = False
        self.dinos_jump = False
        self.dinos_run = True
        self.dinos_dead = False

        self.step_count = 0
        self.jump_speed = self.JUMP_SPEED
        self.image = self.run_img[0]
        self.dinos_rect = self.image.get_rect()
        self.dinos_rect.x = self.X_POS
        self.dinos_rect.y = self.Y_POS

    def run(self):
        self.image = self.run_img[self.step_count // 5]
        self.dinos_rect = self.image.get_rect()
        self.dinos_rect.x = self.X_POS
        self.dinos_rect.y = self.Y_POS
        self.step_count += 1

    def jump(self):
        self.image = self.jump_img
        if self.dinos_jump:
            self.dinos_rect.y -= self.jump_speed * 4
            self.jump_speed -= 0.8
        if self.jump_speed < - self.JUMP_SPEED:
            self.dinos_jump = False
            self.jump_speed = self.JUMP_SPEED

    def crouch(self):
        self.image = self.crouch_img[self.step_count // 5]
        self.dinos_rect = self.image.get_rect()
        self.dinos_rect.x = self.X_POS
        self.dinos_rect.y = self.Y_POS_CROUCH
        self.step_count += 1

    def dead(self):
        self.image = self.dead_img
        self.dinos_rect = self.image.get_rect()
        self.dinos_rect.x = self.X_POS
        self.dinos_rect.y = self.Y_POS

    def update(self, userInput, death_count):

        if self.step_count >= 10:
            self.step_count = 0

        if death_count > 0:
            self.dinos_dead = True
            self.dinos_crouch = False
            self.dinos_run = False
            self.dinos_jump = False
        elif userInput[pygame.K_DOWN] and not self.dinos_jump:
            self.dinos_crouch = True
            self.dinos_run = False
            self.dinos_jump = False
        elif userInput[pygame.K_UP] and not self.dinos_jump:
            self.dinos_crouch = False
            self.dinos_run = False
            self.dinos_jump = True
        elif not (self.dinos_jump or userInput[pygame.K_DOWN]):
            self.dinos_crouch = False
            self.dinos_run = True
            self.dinos_jump = False

        if self.dinos_crouch:
            self.crouch()
        if self.dinos_run:
            self.run()
        if self.dinos_jump:
            self.jump()
        if self.dinos_dead:
            self.dead()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dinos_rect.x, self.dinos_rect.y))

class Enemy:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            enemys.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class Bird(Enemy):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class SmallCactus(Enemy):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class BigCactus(Enemy):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < - self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


def main():
    global game_speed, x_pos_road, y_pos_road, points, enemys
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_road = 0
    y_pos_road = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    enemys = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points - " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_road, y_pos_road
        image_width = ROAD.get_width()
        SCREEN.blit(ROAD, (x_pos_road, y_pos_road))
        SCREEN.blit(ROAD, (image_width + x_pos_road, y_pos_road))
        if x_pos_road <= -image_width:
            SCREEN.blit(ROAD, (image_width + x_pos_road, y_pos_road))
            x_pos_road = 0
        x_pos_road -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()



        if len(enemys) == 0:
            if random.randint(0, 2) == 0:
                enemys.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                enemys.append(BigCactus(BIG_CACTUS))
            elif random.randint(0, 2) == 2:
                enemys.append(Bird(BIRD))

        for enemy in enemys:
            enemy.draw(SCREEN)
            enemy.update()
            if player.dinos_rect.colliderect(enemy.rect):
                death_count += 1
                player.update(userInput, death_count)
                SCREEN.blit(GAME_OVER, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 140))

        player.draw(SCREEN)
        player.update(userInput, death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

        if death_count > 0:
            pygame.time.delay(2000)
            menu(death_count)

def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score - " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUN[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count = 0)
