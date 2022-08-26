# asteroids

import sys, time
from sprites import *

class Game:
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((WIDTH, HEIGHT))
        py.display.set_caption(TITLE)
        self.clock = py.time.Clock()
        self.ready_to_start = False
        
        # initialises local variables
        self.score = 0
        self.lives = 4
        self.difficulty = 0.01
        
        self.dead = False
        self.respawn = False
        
        self.time_dead = 0
        self.time_since_respawn = 0

    def new(self):
        # initialises sprites
        self.all_sprites = py.sprite.Group()
        self.bullets = py.sprite.Group()
        self.asteroids = py.sprite.Group()

        self.player = Player(self, (WIDTH / 32) / 2, (HEIGHT / 32) / 2)
        
    def new_asteroid(self):
        x = random.randint(1, (WIDTH/32) - 1)
        y = random.randint(1, (HEIGHT/32) - 1)
        
        # sets position for where the asteroids can spawn
        if 5 < x < 25:
            check = ((WIDTH / 32) - 1) - x
            # left side
            if check <= 16:
                x = random.randint(1, 4)
            # right side
            elif check > 16:
                x = random.randint(26, 29)
        
        if 3 < y < 14:
            check = ((HEIGHT / 32) - 1) - y
            # top
            if check <= 8:
                y = random.randint(1, 2)
            # bottom
            elif check > 8:
                y = random.randint(14, 15)
                
        choice = random.randint(1,3)
        self.asteroids.add(Asteroid(self, x, y, choice))
        
        # reduces time between asteroids spawning
        if self.difficulty < 3:
            self.difficulty -= 0.005
          
    def effect(self, object, speed):
        # creates explosion effect
        rot = random.randint(-180, 180)
        dir = vec(1, 0).rotate(rot)
        pos = object.pos + BARREL_OFFSET.rotate(rot)
        Bullet(self, pos, dir, speed)
       
    def update(self):
        # calls sprite's update functions
        self.all_sprites.update()
        self.bullets.update()
        self.asteroids.update()
        
        if self.dead:
            if self.respawn:
                self.player = Player(self, (WIDTH / 32) / 2, (HEIGHT / 32) / 2)
                self.all_sprites.add(self.player)
                
                self.dead = False
                self.respawn = False
        
        # player hit by asteroid
        else:
            if py.time.get_ticks() - self.time_since_respawn > 1750:
                collision = py.sprite.spritecollide(self.player, self.asteroids, False, False)
                if collision:
                    if self.lives == 1:
                        self.lives -= 1
                    self.dead = True
                    self.time_dead = py.time.get_ticks()
                    
                    self.all_sprites.empty()
                    py.sprite.Sprite.kill(self.player)

            # bullets on asteroids
            hits = py.sprite.groupcollide(self.asteroids, self.bullets, False, True)
            for hit in hits:
                hit.health -= 1
                if not hit.is_alive():
                    hit.explode()
                    self.score += hit.add_score()

    def run(self):
        self.new()
        self.playing = True
        self.start = time.time()
        
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.update()
            self.draw()
            self.events()
            
            # calls function to spawn new asteroid
            self.counter = time.time()
            if (self.counter - (5-self.difficulty)) >= self.start:
                self.new_asteroid()
                self.start = time.time()
                
    def update_interface(self):
        # updates information being rendered to the screen
        if self.lives > 0:
            lives = self.font.render("Lives: " + str(self.lives-1), 1, (255, 255, 255))
        else:
            lives = self.font.render("Lives: 0", 1, (255,255,255))
        self.screen.blit(lives, (50, 15))
            
        score = self.font.render("Score: " +  str(self.score), 1, (255, 255, 255))
        self.screen.blit(score, (150, 15))
        
        if self.lives == 0:
            if py.time.get_ticks() - self.time_dead > 2500:
                label = self.font.render("You lose. (ENTER) to continue", 1, (255,255,255))
                self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, (HEIGHT/2) - label.get_size()[1]))
        
        elif self.dead:
            if py.time.get_ticks() - self.time_dead > 2500:
                label = self.font.render("(ENTER) to respawn", 1, (255,255,255))
                self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, (HEIGHT/2) - label.get_size()[1]))
            
    def draw(self):
        # draws sprites and UI to the screen
        self.screen.blit(BACKGROUND_IMG, (0,0))
        self.update_interface()
        
        if self.dead:
            if not py.time.get_ticks() - self.time_dead > 250:
                self.effect(self.player, 50)
        
        for sprite in self.all_sprites:
            # centering rotations
            mx, my = sprite.pos.x, sprite.pos.y
            self.screen.blit(sprite.image, (mx - int(sprite.image.get_width() / 2), my - int(sprite.image.get_height() / 2)))
            
        for bullet in self.bullets:
            # centering rotations
            mx, my = bullet.pos.x, bullet.pos.y
            self.screen.blit(bullet.image, (mx - int(bullet.image.get_width() / 2), my - int(bullet.image.get_height() / 2)))
            
        for asteroid in self.asteroids:
            # centering rotations
            mx, my = asteroid.pos.x, asteroid.pos.y
            self.screen.blit(asteroid.image, (mx - int(asteroid.image.get_width() / 2), my - int(asteroid.image.get_height() / 2)))
            
        py.display.flip()

    def events(self):
        for event in py.event.get():
            # checks to see if user is wanting to quit the game
            if event.type == py.QUIT:
                self.quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_KP_ENTER or event.key == py.K_RETURN:
                    if self.lives == 0:
                        self.playing = False
                    elif self.dead:
                        # respawns the player
                        if py.time.get_ticks() - self.time_dead > 2500:
                            self.respawn = True
                            self.time_since_respawn = py.time.get_ticks()
                            self.lives -= 1
                    elif self.started == False:
                        self.started = True
                    elif self.chosen == False:
                        self.chosen = True
                
                # allows user to select letters for their name
                if not self.ready_to_start and self.started:
                    keys = py.key.get_pressed()
                    if keys[py.K_a] or keys[py.K_LEFT]:
                        if self.pointer != 0:
                            self.pointer -= 1
                        else:
                            self.pointer = 25
                    if keys[py.K_d] or keys[py.K_RIGHT]:
                        if self.pointer != 25:
                            self.pointer += 1
                        else:
                            self.pointer = 0

    def quit(self):
        py.quit()
        sys.exit()
        
    def start_screen(self):
        self.font = py.font.SysFont("impact", 25)
        self.font2 = py.font.SysFont("impact", 60)
        
        self.started = False
        
        # renders start screen
        while not self.started:
            self.screen.blit(BACKGROUND_IMG, (0,0))
            
            label = self.font2.render("ASTEROIDS", 1, (255,255,255))
            self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 200))
            
            label = self.font2.render("_____________", 1, (255,255,255))
            self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 205))
            
            label = self.font.render("1 coin 1 play. (ENTER)", 1, (255,255,255))
            self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 300))
                
            self.events()
            py.display.flip()
            
        if self.started:
            self.pointer = 0
            self.chosen = False
            
            self.name = ""
            letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
            
            # allows user to choose name
            while True:
                self.screen.blit(BACKGROUND_IMG, (0,0))

                label = self.font.render("Name: " + self.name, 1, (255,255,255))
                self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 175))
            
                # letter visual
                label = self.font.render("Choose 3 letters:  <  " + str(letters[self.pointer] + "  >"), 1, (255,255,255))
                self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 250))
                
                # selection
                if len(self.name) == 3:
                    self.ready_to_start = True
                    label = self.font.render("Press (ENTER) to play ASSTEROIDS", 1, (255,255,255))
                else:
                    label = self.font.render("Press (ENTER) to select", 1, (255,255,255))
                self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 325))

                self.events()
                
                # adding chosen letter
                if self.chosen:
                    if len(self.name) < 3:
                        self.name += letters[self.pointer]
                        self.chosen = False
                    else:
                        break
                    
                py.display.flip()
    
    def game_over(self):
        details = []
        overwrite = False
        matching = False
        
        # reads data for all highscores, looks up if player already has an entry
        with open("highscores.txt", "r") as f:
            for line in f.readlines():
                line = line.replace("\n", "").split(",")
                if self.name in line:
                    matching = True
                    if int(line[1]) < self.score:
                        line[0] = self.name
                        line[1] = str(self.score)
                        overwrite = True
                details.append(line)
        
        # if they don't have an entry, new data is written
        if not overwrite and not matching:
            line = self.name + "," + str(self.score)
            line = line.split(",")
            details.append(line)
        
        details = details[1:]
        details.sort(key=lambda details:int(details[1]), reverse=True)
        
        with open("highscores.txt", "w") as f:
                f.writelines("Name,Score" + "\n")
                for i in details:
                    f.writelines([i[0] + "," + i[1] + "\n"])

        # shows user rendered highscore
        self.initial_view = py.time.get_ticks()
        while not py.time.get_ticks() - self.initial_view > 7500:
            self.events()
            self.screen.blit(BACKGROUND_IMG, (0,0))
            
            label = self.font.render("Highscores ", 1, (255,255,255))
            self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 50))
            
            label = self.font.render("_____________________", 1, (255,255,255))
            self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 65))

            y = 127
            for i in range(10):
                try:
                    label = self.font.render(str(i+1) + "-  " + str(details[i][0]) + ": " + str(details[i][1]), 1, (255,255,255))
                    self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, y))
                    y += 27
                except:
                    pass
                
            label = self.font.render("_____________________", 1, (255,255,255))
            self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 410))
            
            label = self.font.render(str(self.name) + ": " + str(self.score), 1, (255,255,255))
            self.screen.blit(label, ((WIDTH/2) - label.get_size()[0]/2, 450))
                    
            py.display.flip()

# runs game loop
if __name__ == "__main__":
    while True:
        g = Game()
        g.start_screen()
        g.run()
        g.game_over()
    