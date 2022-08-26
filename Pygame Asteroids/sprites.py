
import random
from settings import *

class Player(py.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        py.sprite.Sprite.__init__(self, self.groups)
        
        # initialises local variables
        self.game = game
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 90
        self.last_shot = 0

    def get_keys(self):
        self.left = False
        self.right = False
        self.throttle = False
        self.shoot = False
        keys = py.key.get_pressed()

        # gets user inputs
        if keys[py.K_a] or keys[py.K_LEFT]:
            self.left = True

        if keys[py.K_d] or keys[py.K_RIGHT]:
            self.right = True

        if keys[py.K_w] or keys[py.K_UP]:
            self.throttle = True

        if keys[py.K_SPACE]:
            self.shoot = True

    def movement(self):
        self.rot_speed = 0
        self.acc = vec(0,0)

        # uses user inputs to apply physics
        if self.left is True:
            self.rot_speed = ROT_SPEED

        if self.right is True:
            self.rot_speed = -ROT_SPEED

        if self.throttle is True:
            self.acc = vec(-PLAYER_ACC / 2, 0).rotate(-self.rot + 180)
            if self.left is True:
                self.rot_speed = SLOW_TURNING
            elif self.right is True:
                self.rot_speed = -SLOW_TURNING

    def shooting(self):
        # initialises a bullet
        if self.shoot is True:
            now = py.time.get_ticks()
            if now - self.last_shot >= BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir, BULLET_SPEED)

    def boundaries(self):
        # checks to see if player has suprassed screen parameters
        # right
        if self.pos.x > WIDTH:
            self.pos.x = 0
        # left
        elif self.pos.x < 0:
            self.pos.x = WIDTH
        # top
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        # bottom
        elif self.pos.y < 0:
            self.pos.y = HEIGHT

    def values_to_update(self):
        # updates local variables
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = py.transform.rotate(PLAYER_IMG, self.rot)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos.x, self.pos.y)
        
        self.rect.width = 20; self.rect.height = 20
        
        if self.acc.x != 0 and self.acc.y != 0:
            self.acc *= 0.7071

        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)

    def update(self):
        # runs all functions
        self.get_keys()
        self.movement()
        self.shooting()
        self.values_to_update()
        self.boundaries()


class Bullet(py.sprite.Sprite):
    def __init__(self, game, pos, dir, speed):
        self.groups = game.bullets
        py.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = BULLET_IMG
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * speed
        self.spawn_time = py.time.get_ticks()

    def update(self):
        # adds direction and velocity to bullet
        self.pos += (self.vel * self.game.dt)
        self.rect.center = self.pos
        if py.time.get_ticks() - self.spawn_time > BULLET_LIFE:
            self.kill()
            
            
class Asteroid(py.sprite.Sprite):
    def __init__(self, game, x, y, choice):
        self.groups = game.asteroids
        py.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        # decides what image should be loaded depending on type of asteroid
        if choice == 1:
            self.image = SMALL
            self.type = "S"
            self.health = 2
        elif choice == 2:
            self.image = MEDIUM
            self.type = "M"
            self.health = 4
        else:
            self.image = LARGE
            self.type = "L"
            self.health = 6
            
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        
        self.rot = random.randint(-180, 180) % 360
        self.speed = random.randint(3, 15) / 10
        
        self.image = py.transform.rotate(self.image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def is_alive(self):
        # checks asteroid health
        if self.health == 0:
            return False
        else:
            return True
    
    def explode(self):
        # spawns in children asteroids if size is large enough
        if self.type == "L" or self.type == "M":
            pos = self.pos
            x = (pos[0] / 32)
            y = (pos[1] / 32)
            
            if self.type == "L":
                for i in range(3):
                    dir = vec(1, 0).rotate(random.randint(-180, 180))
                    self.game.asteroids.add(Asteroid(self.game, x, y, 2))
                    self.rot = dir
            elif self.type == "M":
                for i in range(5):
                    dir = vec(1, 0).rotate(random.randint(-180, 180))
                    self.game.asteroids.add(Asteroid(self.game, x, y, 1))
                    self.rot = dir
        self.kill()
        
    def add_score(self):
        # adds score when asteroid is destroyed
        if self.type == "L":
            return BASE_SCORE * 1
        elif self.type == "M":
            return BASE_SCORE * 2
        else:
            return BASE_SCORE * 3
        
    def movement(self):
        # applies direction and correct hitbox information
        self.pos += self.vel
        self.vel = vec(-self.speed / 2, 0).rotate(-self.rot)
        self.pos += self.vel

        self.rect.center = self.pos
        
    def boundaries(self):
        # checks to see if asteroid has suprassed screen parameters
        # right
        if self.pos.x > WIDTH:
            self.pos.x = 0
        # left
        elif self.pos.x < 0:
            self.pos.x = WIDTH
        # top
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        # bottom
        elif self.pos.y < 0:
            self.pos.y = HEIGHT
            
    def update(self):
        # calls functions
        self.movement()
        self.boundaries()
