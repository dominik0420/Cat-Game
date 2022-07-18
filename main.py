import pygame
import os
import random
#initialize pygame
pygame.init()


#global constants
#game will be ran at 720p
screen_height = 720
screen_width = 1280
screen = pygame.display.set_mode((screen_width, screen_height))

#loading images from assets
#actions:
action_run = [pygame.image.load(os.path.join("Assets/cat", "cat_run1.png")),
              pygame.image.load(os.path.join("Assets/cat", "cat_run2.png"))]
action_bounce = pygame.image.load(os.path.join("Assets/cat", "cat_bounce.png"))
action_dodge = pygame.image.load(os.path.join("Assets/cat", "cat_dodge.png"))
#obstacles:
obstacle_poop = [pygame.image.load(os.path.join("Assets/obstacle", "poop.png")),
                 pygame.image.load(os.path.join("Assets/obstacle", "double_poop.png"))]
obstacle_snake = [pygame.image.load(os.path.join("Assets/obstacle", "snake.png")),
                  pygame.image.load(os.path.join("Assets/obstacle", "snake2.png"))]
#flying objects
object_bird = [pygame.image.load(os.path.join("Assets/birds", "bird1.png")),
               pygame.image.load(os.path.join("Assets/birds", "bird2.png"))]
#backgrounds
bg_cloud = pygame.image.load(os.path.join("Assets/clouds", "cloud.png"))
bg_ground = pygame.image.load(os.path.join("Assets/ground", "ground.png"))


class Cat:
    #x and y position of the cat
    X = 80
    Y = 295
    Y_DODGE = 330
    BOUNCE_V = 8.5

    def __init__(self):
        #putting in the assets
        self.run_image = action_run
        self.bounce_image = action_bounce
        self.dodge_image = action_dodge

        #set everything but run to false so the cat won't be performing any actions other than running when the game starts
        self.cat_run = True
        self.cat_bounce = False
        self.cat_dodge = False

        #for animation of the cat
        self.step_index = 0
        self.bounce_v = self.BOUNCE_V

        #initialize image with a default running action
        self.image = self.run_image[0]

        #hit-box of the cat
        self.cat_rect = self.image.get_rect()
        self.cat_rect.x = self.X
        self.cat_rect.y = self.Y

    #update function on the cat status with userinput
    def update(self, userInput):
        #depending on the state of the cat, calling a corresponding function
        if self.cat_run:
            self.run()
        if self.cat_bounce:
            self.bounce()
        if self.cat_dodge:
            self.dodge()

        #resetting step_index every 10 secs
        if self.step_index >= 10:
            self.step_index = 0

        #set state of cat: if the button is pressed and cat is not performing the correct action
        if userInput[pygame.K_UP] and not self.cat_bounce:
            self.cat_run = False
            self.cat_bounce = True
            self.cat_dodge = False
        elif userInput[pygame.K_DOWN] and not self.cat_bounce:
            self.cat_run = False
            self.cat_bounce = False
            self.cat_dodge = True
        elif not (self.cat_bounce or userInput[pygame.K_DOWN]):
            self.cat_run = True
            self.cat_bounce = False
            self.cat_dodge = False

    #run function and getting the running animation
    def run(self):
        #from 1-4 of step_index displays image 1, after step index = 5 the image 2 is displayed
        #when step_index > 10 it would be reset (see line 69)
        self.image = self.run_image[self.step_index // 5]
        self.cat_rect = self.image.get_rect()
        self.cat_rect.x = self.X
        self.cat_rect.y = self.Y
        self.step_index += 1

    def bounce(self):
        self.image = self.bounce_image
        if self.cat_bounce:
            self.cat_rect.y -= self.bounce_v * 4
            self.bounce_v -= 0.8
        if self.bounce_v < - self.BOUNCE_V:
            self.cat_bounce = False
            self.bounce_v = self.BOUNCE_V

    def dodge(self):
        self.image = self.dodge_image
        self.cat_rect = self.image.get_rect()
        self.cat_rect.x = self.X
        self.cat_rect.y = self.Y_DODGE
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.image, (self.cat_rect.x, self.cat_rect.y))

class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = bg_cloud
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < - self.width:
            self.x = screen_width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x <- self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class Poop(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 345

class Snake(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 315

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0
        #override draw function

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1 # 0-4 bird1, 5-9 bird2, 10 reset


#defining main function
def main():
    global game_speed, x_bg, y_bg, score, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Cat()
    cloud = Cloud()
    game_speed = 20
    x_bg = 0
    y_bg = 380
    score = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def scoring():
        global score, game_speed
        score += 1
        if score % 100 == 0:
            game_speed += 2
        text = font.render("Your Score: " + str(score), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)

    def background():
        global x_bg, y_bg
        image_width = bg_ground.get_width()
        screen.blit(bg_ground, (x_bg, y_bg))
        screen.blit(bg_ground, (image_width + x_bg, y_bg))
        if x_bg <= -image_width:
            screen.blit(bg_ground, (image_width + x_bg, y_bg))
            x_bg = 0
        x_bg -= game_speed

    #while loop: condition to exit the game
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((182, 203, 214))
        userInput = pygame.key.get_pressed()

        #put the cat in
        player.draw(screen)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 1) == 0:
                obstacles.append(Poop(obstacle_poop))
            elif random.randint(0, 1) == 1:
                obstacles.append(Snake(obstacle_snake))
            elif random.randint(0, 1) == 2:
                obstacles.append(Bird(object_bird))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.cat_rect.colliderect(obstacle.rect):
                #pygame.draw.rect(screen, (255, 0, 0), player.cat_rect, 2) #hitbox turn red
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(screen)
        cloud.update()

        scoring()

        clock.tick(30)
        pygame.display.update()



#calling main function
#main()

def menu(death_count):
    global score
    run = True
    while run:
        screen.fill((182, 203, 214))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count ==0:
            text = font.render("Press any button to start THE PAIN :P", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("OHHH YOU DIED. Now, press any button to REstart PAIN HAHAHA", True, (0, 0, 0))
            display_score = font.render("Your previous score: " + str(score), True, (0, 0, 0))
            scoreRect = display_score.get_rect()
            scoreRect.center = (screen_width // 2, screen_height // 2 + 50)
            screen.blit(display_score, scoreRect)

        #position of text
        textRect = text.get_rect()
        textRect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text, textRect)
        screen.blit(action_run[0], (screen_width // 2 - 20, screen_height // 2 - 140))
        pygame.display.update()

        #quitting game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

#calling menu func and starting at 0 to start with the initial menu
menu(death_count = 0)