import pygame as pg
from pygame import transform
import Const
from pygame.math import Vector2
from math import pi, sqrt, tan
from Model.GameObject.basic_game_object import Basic_Game_Object
from EventManager.EventManager import *
import random

class Basic_Attack_Object(Basic_Game_Object):
    def __init__(self, model, attacker_id, position, width, height, speed):
        super().__init__(model, position.x, position.y, width, height)
        self.speed = speed
        self.name = ""
        self.damage = 0
        self.disappear_hit_player = False
        self.immune = [False for _ in range(Const.PLAYER_NUMBER)]
        self.immune[attacker_id] = True
        self.timer = 0
        self.attacker = self.model.players[attacker_id]

    def collide_player(self, player):
        pass

    def basic_tick(self):
        if self.obey_gravity:
            self.speed.y += Const.PLAYER_GRAVITY/Const.FPS
        self.position += self.speed / Const.FPS
        if self.x > Const.ARENA_SIZE[0] or self.x < 0: 
            self.kill()
        

    def tick(self):
        self.basic_tick()
        self.timer += 1
        for player in self.model.players:
            if (not self.immune[player.player_id]) and player.can_be_special_attacked() and self.collide_player(player):
                player.be_special_attacked(self)
                self.immune[player.player_id] = True
                if self.disappear_hit_player:
                    self.kill()
            if self.attacker.player_id != player.player_id and self.collide_player(player):
                self.model.ev_manager.post(EventBeAttacked(player.player_id))

class Basic_Attack_Object_No_Vanish(Basic_Game_Object):
    def __init__(self, model, attacker_id, position, direction, damage, name, width = 1, height = 1, speed = Const.ARROW_SPEED):
        super().__init__(model, position.x, position.y, width, height)
        self.name = name
        self.attacker_id = attacker_id
        self.speed = direction.normalize() * speed
        self.damage = damage
        self.immune = [False for _ in range(Const.PLAYER_NUMBER)]
        self.immune[attacker_id] = True
        self.attacker = self.model.players[attacker_id]

    def check_col(self, recta):
        # should be override
        return False

    def basic_tick(self):
        self.position += self.speed / Const.FPS # since this ignores terrains
        if self.x > Const.ARENA_SIZE[0] or self.x < 0: 
            self.kill()

    def tick(self):
        self.basic_tick()
        for player in self.model.players:
            if not self.immune[player.player_id] and self.check_col(player):
                player.be_special_attacked(self)
                self.immune[player.player_id] = True
            if self.attacker.player_id != player.player_id and self.check_col(player):
                self.model.ev_manager.post(EventBeAttacked(player.player_id))

class Arrow(Basic_Attack_Object):
    def __init__(self, model, attacker_id, position, speed, Arrow_type):
        super().__init__(model, attacker_id, position, 1, 1, speed)
        self.name = 'Arrow'
        if Arrow_type == 'Ddos': self.damage = Const.DDOS_DAMAGE
        else: self.damage = Const.DOS_DAMAGE
        self.disappear_hit_player = True

    def collide_player(self, player):
        return player.rect.collidepoint(self.center.x, self.center.y)

class Bug(Basic_Attack_Object):
    def __init__(self, model, attacker_id, position, speed):
        super().__init__(model, attacker_id, position, Const.BUG_WIDTH, Const.BUG_HEIGHT, speed)
        self.name = 'Bug'
        self.damage = Const.BUG_DAMAGE
        self.disappear_hit_player = True
        self.obey_gravity = False
        self.state_timer = 0
        self.state = 'straight'
        self.track = []

    def basic_tick(self):
        self.state_timer += 1
        if self.state == 'straight':
            self.position += self.speed
            if self.state_timer == Const.BUG_STRAIGHT_TIMER:
                self.state = 'random'
        elif self.state == 'random':
            self.position += self.speed
            if self.state_timer % Const.BUG_RANDOM_PERIOD == 0:
               self.speed = self.speed.rotate(random.randint(-90, 90))
            if self.state_timer == Const.BUG_RANDOM_TIMER:
                self.kill()

    def tick(self):
        self.basic_tick()
        
        if( (self.state_timer-1) == 0 ): self.track = [self.position]*50
        else: self.track[ (self.state_timer-1) %50 ] = self.position
        
        for player in self.model.players:
            if (not self.immune[player.player_id]) and player.can_be_special_attacked() and self.collide_player(player):
                player.be_special_attacked(self)
                self.immune[player.player_id] = True
                if self.disappear_hit_player:
                    self.kill()
            if self.attacker.player_id != player.player_id and self.collide_player(player):
                self.model.ev_manager.post(EventBeAttacked(player.player_id))

    def collide_player(self, player):
        return player.rect.collidepoint(self.center.x, self.center.y)

class Coffee(Basic_Attack_Object):
    def __init__(self, model, attacker_id, position, speed):
        super().__init__(model, attacker_id, position, Const.COFFEE_WIDTH, Const.COFFEE_HEIGHT, speed)
        self.name = 'Coffee'
        self.damage = Const.COFFEE_DAMAGE
        self.disappear_hit_player = True
        self.obey_gravity = True
        self.gravity = Const.COFFEE_GRAVITY
        self.track = []

    def tick(self):
        self.basic_tick()
        if( (self.timer) == 0 ): self.track = [self.position]*20
        else: self.track[ (self.timer) %20 ] = self.position

        self.timer += 1
        for player in self.model.players:
            if (not self.immune[player.player_id]) and player.can_be_special_attacked() and self.collide_player(player):
                player.be_special_attacked(self)
                self.immune[player.player_id] = True
                if self.disappear_hit_player:
                    self.kill()
            if self.attacker.player_id != player.player_id and self.collide_player(player):
                self.model.ev_manager.post(EventBeAttacked(player.player_id))

    def collide_player(self, player):
        return player.rect.collidepoint(self.center.x, self.center.y)

class Fireball(Basic_Attack_Object):
    # this is a ball-shaped obj, hence only the position matters, it represents the center of fireball
    def __init__(self, model, attacker_id, position, speed):
        super().__init__(model, attacker_id, position, 1, 1, speed)
        self.name = 'Fireball'
        self.damage = self.attacker.enhance_fireball_damage
        self.radius = Const.FIREBALL_RADIUS
        self.disappear_hit_player = False
        self.immune = [False for _ in range(Const.PLAYER_NUMBER)]
        self.immune[attacker_id] = True

    def collide_player(self, player): # check if a rectangle collide with a ball (self)
        rxl = player.x
        rxr = rxl + Const.PLAYER_WIDTH
        ryu = player.y
        ryb = ryu + Const.PLAYER_HEIGHT
        tmpx = -1
        tmpy = -1
        if self.x > rxr:
            tmpx = 1
        elif self.x > rxl:
            tmpx = 0
        if self.y > ryb:
            tmpy = 1
        elif self.y > ryu:
            tmpy = 0
        if tmpx == 0:
            if tmpy == 1:
                return self.y - ryb < self.radius
            elif tmpy == -1:
                return ryu - self.y < self.radius
            else: # 0
                return True
        if tmpy == 0:
            if tmpx == 1:
                return self.x - rxr < self.radius
            elif tmpx == -1:
                return rxl - self.x < self.radius
        corx = rxl if tmpx == -1 else rxr
        cory = ryu if tmpy == -1 else ryb
        return (self.x - corx) ** 2 + (self.y - cory) ** 2 < self.radius ** 2
    
class Tornado(Basic_Attack_Object):
    def __init__(self, model, attacker_id, position, speed):
        super().__init__(model, attacker_id, position, Const.TORNADO_WIDTH, Const.TORNADO_HEIGHT, speed)
        self.name = 'Tornado'
        self.damage = Const.TORNADO_DAMAGE
        self.disappear_hit_player = False
        
    def collide_player(self, player):
        return player.rect.colliderect(self.rect)

class Lightning(Basic_Attack_Object):
    def __init__(self, model, attacker_id, position, speed, destination):
        super().__init__(model, attacker_id, position, Const.LIGHTNING_WIDTH, destination + 100, speed)
        self.name = 'Lightning'
        self.damage = Const.LIGHTNING_DAMAGE
        self.disappear_hit_player = False
        self.destination = destination # the final y position
        self.timer = Const.LIGHTNING_TIMER
        
    def collide_player(self, player):
        return player.rect.colliderect(self.rect)

    def tick(self):
        self.timer -= 1
        for player in self.model.players:
            if (not self.immune[player.player_id]) and player.can_be_special_attacked() and self.collide_player(player):
                player.be_special_attacked(self)
                self.immune[player.player_id] = True
                if self.disappear_hit_player:
                    self.kill()
            if self.attacker.player_id != player.player_id and self.collide_player(player):
                self.model.ev_manager.post(EventBeAttacked(player.player_id))
        if self.timer <= 0:
            self.kill()

class Dos(Basic_Game_Object):
    def __init__(self, model, attacker, target):
        super().__init__(model, attacker.center.x, attacker.center.y, 1, 1)
        self.name = 'Dos'
        self.attacker = attacker
        self.direction = target.center-self.position
        if self.direction.length() == 0: self.direction = pg.Vector2(1, 0)
        self.timer = 0
        self.rounds = Const.DOS_ACTIVE_LIMIT

    def tick(self):
        self.basic_tick()
        if self.timer<=0:
            self.timer = Const.DOS_TIMER
            self.rounds -=1
            self.model.attacks.append(Arrow(self.model, self.attacker.player_id, self.position, 
                                            self.direction.normalize() * Const.ARROW_SPEED, 'Dos'))
        self.timer -= 1
        if self.rounds<=0:
            self.kill()

class Ddos(Basic_Game_Object):
    def __init__(self, model, attacker, target):
        super().__init__(model, target.center.x, target.center.y, 1, 1)
        self.name = 'Ddos'
        self.attacker = attacker
        self.direction = Vector2(0,1) * Const.DDOS_RADIUS
        self.timer = 0
        self.rounds = Const.DDOS_ACTIVE_LIMIT

    def tick(self):
        self.basic_tick()
        if self.timer<=0:
            self.timer = Const.DDOS_TIMER
            self.rounds -= 1
            for _ in range(5):
                From = self.position - self.direction
                self.model.attacks.append(Arrow(self.model, self.attacker.player_id, From, 
                                                self.direction.normalize() * Const.ARROW_SPEED, 'Ddos'))
                self.direction.rotate_ip(72)
        self.timer -= 1
        if self.rounds<=0:
            self.kill()

class Throw_Bug(Basic_Game_Object):
    def __init__(self, model, attacker, target):
        super().__init__(model, attacker.center.x, attacker.center.y, 1, 1)
        self.name = 'Throw_Bug'
        for deg in range(0, 360, 60): 
            self.model.attacks.append(Bug(model,attacker.player_id, self.position, 
                                      Vector2(1, 0).rotate(deg) * Const.BUG_THROW_SPEED))
        self.kill()

class Throw_Coffee(Basic_Game_Object):
    def __init__(self, model, attacker, target):
        super().__init__(model, attacker.center.x, attacker.center.y, 1, 1)
        self.name = 'Throw_Coffee'
        # 30, 40, 55 degree
        self.model.attacks.append(Coffee(model,attacker.player_id, self.position, 
                                         (attacker.face + Vector2(0,-tan(30/180*pi))).normalize() * Const.COFFEE_THROW_SPEED))
        self.model.attacks.append(Coffee(model,attacker.player_id, self.position, 
                                         (attacker.face + Vector2(0,-tan(40/180*pi))).normalize() * Const.COFFEE_THROW_SPEED))
        self.model.attacks.append(Coffee(model,attacker.player_id, self.position, 
                                         (attacker.face + Vector2(0,-tan(55/180*pi))).normalize() * Const.COFFEE_THROW_SPEED))
        self.kill()
        
class Cast_Fireball(Basic_Game_Object):
    def __init__(self, model, attacker):
        super().__init__(model, attacker.center.x, attacker.center.y, 1, 1)
        self.name = "Cast_Fireball"
        self.model.attacks.append(Fireball(model, attacker.player_id, self.position, 
                                           attacker.face.normalize() * Const.FIREBALL_SPEED))
        self.kill()

class Cast_Tornado(Basic_Game_Object):
    def __init__(self, model, attacker):
        super().__init__(model, attacker.rect.x + Const.PLAYER_WIDTH, attacker.rect.y + Const.PLAYER_HEIGHT - Const.TORNADO_HEIGHT, 1, 1)
        self.name = 'Cast_Tornado'
        self.model.attacks.append(Tornado(model,attacker.player_id, self.position, 
                                          attacker.face.normalize() * Const.TORNADO_SPEED))
        self.kill()

class Cast_Lightning(Basic_Game_Object):
    def __init__(self, model, attacker):
        super().__init__(model, attacker.rect.x + Const.PLAYER_WIDTH / 2 - Const.LIGHTNING_WIDTH / 2, -100, 1, 1)
        self.name = 'Cast_Lightning'
        self.model.attacks.append(Lightning(model, attacker.player_id, self.position, Vector2(0,0),
                                            attacker.rect.y + Const.PLAYER_HEIGHT - Const.LIGHTNING_HEIGHT))
        self.kill()
