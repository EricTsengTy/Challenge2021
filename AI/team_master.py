import Const
from math import sqrt

class pathfinder():
    def __init__(self, AI):
        self.AI = AI
        self.helper = AI.helper
        self.pos = self._feet(self.helper.get_self_position())
        self.actionset = AI.actionset
        self.id = self.helper.get_self_id()

        self.n_layers = 4
        self.landing_points = [[] for _ in range(self.n_layers)]
        self.linking_points = [[] for _ in range(self.n_layers)]
        self.edge_points = [[] for _ in range(self.n_layers)] # edge linking points
        self.landing_point_set = set()

        self.resol = 16
        self.wall_offset = 6

        self.tick = 0.02
        self.split_prob = 0

        self.eps = 1e-4

        for i in range(self.n_layers):
            y = 160 + self.wall_offset + 200 * i
            for x in range(self.resol // 2, Const.ARENA_SIZE[0], self.resol):
                if self._in_wall(i, x):
                    self.landing_points[i].append((x, y))
                    self.landing_point_set.add((x, y))
                else:
                    self.linking_points[i].append((x, y))
                    if self._in_wall(i, x - self.resol) or self._in_wall(i, x + self.resol):
                        self.edge_points[i].append((x, y))

        self.want = ['FAN', 'THROW_COFFEE', 'THROW_BUG', 'DOS', 'DDOS', 'EXE', 'FIREWALL']
        # print(self._walking((954.0, 499.0), 2))

    def _move(self, tmp):
        if tmp[1] > 0:
            self.actionset['jump'] = True
        if tmp[0] > 0:
            self.actionset['right'] = True
        elif tmp[0] < 0:
            self.actionset['left'] = True

    def move(self):
        # find nearest want item
        print(self.pos)
        tmp = self.find_nearest_item()
        if tmp is not None:
            self._move(tmp)
        else: # find people
            tmp = self.find_nearest_player()
            if tmp is not None:
                self._move(tmp)
        

    def item_center(self, pos):
        return (pos[0] + Const.ITEM_WIDTH / 2, pos[1] + Const.ITEM_HEIGHT / 2)

    def find_nearest_player(self):
        d, best_move = 200000., None
        speed, jmp = self.helper.get_self_speed()[1], self.helper.get_remaining_jumps()
        player_list = self.helper.get_all_position()
        for i in range(player_list):
            if i != self.id:
                tmp_d, tmp_move = self.find(self.pos, self._feet(player_list[i]), speed, jmp)
                if tmp_d < d:
                    d, best_move = tmp_d, tmp_move
        return best_move

    def find_nearest_item(self):
        d, best_move, best_tar = 200000., None, None
        speed, jmp = self.helper.get_self_speed()[1], self.helper.get_remaining_jumps()
        for item in self.want:
            pos_list = self.helper.get_all_specific_item_position(item)
            for tar in pos_list:
                tmp_d, tmp_move = self.find(self.pos, self.item_center(tar), speed, jmp)
                if tmp_d < d:
                    d, best_move, best_tar = tmp_d, tmp_move, tar
        print(best_move, best_tar)
        print("est time:", d)
        return best_move

    def update(self):
        self.pos = self._feet(self.helper.get_self_position())
        self.actionset = self.AI.actionset ## not sure if nessesary

    def find(self, pos, tar, speed, jmp):
        # print("pos:", pos, "tar:", tar, "speed:", speed, "jmp:", jmp)
        path_candidate = self._find_all_reasonable_pathing(pos, tar, speed, jmp)
        # print(path_candidate)
        return self._search(pos, path_candidate, speed, jmp, tar)

    def _feet(self, pos):
        return (pos[0] + Const.PLAYER_WIDTH / 2, pos[1] + Const.PLAYER_HEIGHT - 1)

    def _in_wall(self, layer, x):
        if layer == 0:
            return 340 < x < 860 # 360 < x < 840
        elif layer == 1:
            return x < 420 or x > 780 # x < 400 or x > 800
        elif layer == 2:
            return 220 < x < 980 # 240 < x < 960
        else:
            return True # I think we won't use this

    def _layer(self, pos):
        # return (pos[1] + 40 + self.wall_offset) // 200
        return int(min(self.n_layers - 1, max(0, (pos[1] + 40 - self.wall_offset) // 200)))

    def _dist(self, pos1, pos2):
        return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def _find_closest_points(self, pos1, pos2, set_of_points, num = 2, x = None): 
        '''set_of_points have the same y coord, and they are sorted by x coords.'''
        y = set_of_points[0][1]
        if x is None:
            x = pos1[0] - (pos1[0] - pos2[0]) * (pos1[1] - y) / (pos1[1] - pos2[1])
        prev = set_of_points[0]
        now = set_of_points[0]
        for pt in set_of_points:
            prev, now = now, pt
            if pt[0] >= x:
                break
        if num == 1:
            if abs(prev[0] - x) < abs(now[0] - x):
                return [prev]
            else:
                return [now]
        return [prev, now]

    def _find_all_reasonable_pathing(self, pos, tar, speed = None, jmp = None): 
        '''return format: [[possible checkpoints]: layers]'''
        my_layer = self._layer(pos)
        tar_layer = self._layer(tar)
        # print("layer:", my_layer, tar_layer)
        if my_layer == tar_layer: 
            return [[tar]]
        elif my_layer < tar_layer:
            if not self._in_wall(my_layer, pos[0]):
                my_layer += 1
            ans = []
            for i in range(my_layer, tar_layer):
                if i <= tar_layer - 2:
                    ans.append(self.edge_points[i])
                else:
                    ans.append(self.linking_points[i])
            ans.append([tar])
            return ans
        else: # my_layer > tar_layer
            ans = []
            for i in range(my_layer, tar_layer, -1):
                ans.append(self._find_closest_points(pos, tar, self.landing_points[i - 1])) 
                # find two closest points to the line (pos, tar)
            if self._diff_y(pos[1], tar[1], speed, jmp) is not None:
                ans[0].append(tar)
            ans.append([tar])
            return ans

    def _walking(self, pos, jmp):
        l = self._layer(pos)
        if abs(pos[1] - (l * 200 + 160)) <= self.wall_offset \
            and jmp == 2 and self._in_wall(l, pos[1]):
                return True
        return False

    def _flyto(self, pos, tar, speed, jmp):
        '''return : (d, suggest method) or None'''
        tmp_x = self._diff_x(pos[0], tar[0])
        tmp_y = self._diff_y(pos[1], tar[1], speed, jmp, tar)
        # print("pos: ", pos, "tar: ", tar, "tmp_x & y: ", tmp_x, " ", tmp_y)
        if tmp_y is None:
            return None
        d = max(tmp_x, tmp_y)
        dir_x = 1 if tar[0] > pos[0] else -1
        dir_y = 0
        '''
        if speed > 0 and tar[1] < pos[1]:
            dir_y = 1
        '''
        if jmp > 0: # check if we need to jump
            if self._walking(pos, jmp):
                print("walking")
                if tmp_y > tmp_x and pos[1] > tar[1]:
                    dir_y = 1
            else:
                tmp_ynj = self.tick + self._diff_y(pos[1] + self.tick * (speed + .5 * Const.PLAYER_GRAVITY * self.tick), tar[1], speed + Const.PLAYER_GRAVITY * self.tick, jmp, tar)
                tmp_yj = self._diff_y(pos[1], tar[1], -Const.PLAYER_JUMP_SPEED, jmp - 1, tar)
                if tmp_y > self.tick * 2 and (tmp_ynj is None or tmp_ynj > d + self.eps) and\
                    (tmp_yj is not None and tmp_ynj > tmp_yj - self.eps): # lazy jumps
                    dir_y = 1
        if tar[1] < pos[1]: # if it is upwards, we don't need to care about speed
            speed = 0 
        else:
            if tmp_y > tmp_x: # you can jump over it
                speed = sqrt(speed ** 2 + 2 * (tar[1] - pos[1]) * Const.PLAYER_GRAVITY)
            else:
                speed = 0
        if self._dist(pos, tar) < 1: 
            dir_y = 0
        return d, (dir_x, dir_y), speed

    def _stat_jump(self, stat):
        return (stat[0], stat[1], - Const.PLAYER_JUMP_SPEED, stat[3] - 1, stat[4], stat[5])

    def _walkto(self, pos, tar):
        d = self._diff_x(pos[0], tar[0])
        dir_x = 1 if tar[0] > pos[0] else -1
        return d, (dir_x, 0), 0

    def _goto(self, stat, tar, checkpoints = None):
        '''
        with probability self.split_prob, it will try to jump
        return: list of "status", where status are in the form 
        stat: (cost, pos, speed, jmp, parent, how)
        the argument "checkpoint" is a reference
        '''
        cost, pos, speed, jmp, parent, how = stat
        ans = []
        # if self._walking(pos, jmp): #################
        #    tmp = self._walkto(pos, tar)
        # else:
        tmp = self._flyto(pos, tar, speed, jmp)
        # print("pos: ", pos, ", tar: ", tar, "how: ", tmp[1], ", cost: ", tmp[0])
        if tmp is not None:
            d, method, sp = tmp
            if tar in self.landing_point_set:
                speed, jmp = 0, 2 
            ans.append((cost + d, tar, sp, jmp, stat, method))
        return ans

    def _search(self, pos, checkpoints, speed, jmp, tar = None):
        n = len(checkpoints)
        # print("searching...")
        status = [[] for _ in range(n + 1)]
        status[0] = [(0, pos, speed, jmp, None, None)] # (cost, pos, speed, jmp, parent, how)
        for i in range(1, n + 1):
            for cp in checkpoints[i - 1]:
                for stat in status[i - 1]:
                    tmp = self._goto(stat, cp)
                    status[i] += tmp
        prev, bs, d = None, None, 100000. # find best d
        for stat in status[n]:
            if stat[0] < d:
                bs, d = stat, stat[0]
        
        '''
        for i in range(n + 1):
            print("================", i, "================")
            for j in status[i]:
                j = list(j)
                j[4] = "(parent)"
                print(j)
        '''
        
        if bs is None:
            # find nearest landing point and go to it
            tmp = self._find_closest_points(None, None, self.landing_points[self._layer(pos)], 1, tar[0])
            tmp_x = 1 if tmp[0][0] > pos[0] else -1
            return 100000., (tmp_x, 0)
        while bs[4] is not None:
            prev, bs = bs, bs[4]
        
        # print("pos:", pos)
        # print("target:", prev[1], "action: ", prev[5])
        return d, prev[5] # estimate cost & suggest action

    def _diff_y_ew0(self, pos_y, tar_y, speed, jmp):
        '''calculate the estimate time for one to "land" on this point.
        tar_y must < pos_y'''
        # print("hi")
        if speed > 0 and jmp > 0:
            speed, jmp = -Const.PLAYER_JUMP_SPEED, jmp - 1
        for i in range(jmp + 1):
            if self._diff_y_upwards(pos_y, tar_y, speed, i) is not None:
                leaked_gt_sqr = 0 if i == 0 else max(0, (speed ** 2 + Const.PLAYER_JUMP_SPEED ** 2 * jmp - Const.PLAYER_GRAVITY * 2 * (pos_y - tar_y)) / i)
                return (-speed + i * Const.PLAYER_JUMP_SPEED - sqrt(leaked_gt_sqr)) / Const.PLAYER_GRAVITY
        return None

    def _diff_x(self, pos_x, tar_x):
        return abs(pos_x - tar_x) / Const.PLAYER_SHIFT_SPEED

    def _diff_y(self, pos_y, tar_y, speed, jmp = 0, ref = None):
        if ref is not None and ref in self.landing_point_set:
            return self._diff_y_ew0(pos_y, tar_y, speed, jmp)
        return self._diff_y_downwards(pos_y, tar_y, speed, jmp) if pos_y <= tar_y else self._diff_y_upwards(pos_y, tar_y, speed, jmp)

    def _diff_y_downwards(self, pos_y, tar_y, speed, jmp = 0): # free fall
        tar_speed = sqrt(speed ** 2 + 2 * (tar_y - pos_y) * Const.PLAYER_GRAVITY)
        return (tar_speed - speed) / Const.PLAYER_GRAVITY

    def _diff_y_upwards(self, pos_y, tar_y, speed, jmp = 0):
        if jmp == 0:
            tmp = speed ** 2 - 2 * Const.PLAYER_GRAVITY * (pos_y - tar_y)
            if tmp < 0:
                return None
            else:
                return (-speed - sqrt(tmp)) / Const.PLAYER_GRAVITY
        if speed > 0:
            speed, jmp = -Const.PLAYER_JUMP_SPEED, jmp - 1
        '''
        leaked_t_sqr = (2 * (pos_y - tar_y) * Const.PLAYER_GRAVITY - speed ** 2 - jmp * (Const.PLAYER_JUMP_SPEED ** 2)) / (jmp + 1)
        print(leaked_t_sqr)
        '''
        c_sqr = (-2 * Const.PLAYER_GRAVITY * (pos_y - tar_y) + speed ** 2 + Const.PLAYER_JUMP_SPEED ** 2 * jmp) / (jmp + 1)
        if c_sqr < 0:
            return None
        if -speed < sqrt(c_sqr):
            return self._diff_y_upwards(pos_y, tar_y, -Const.PLAYER_JUMP_SPEED, jmp - 1)
        return ((-speed + Const.PLAYER_JUMP_SPEED * jmp) - (jmp + 1) * sqrt(c_sqr)) / Const.PLAYER_GRAVITY

class attacker():
    def __init__(self, AI):
        self.AI = AI
        self.helper = AI.helper
        self.eps = 0.01
        self.radius = 200
        self.id = self.helper.get_self_id()
        self.sp_delay = Const.PLAYER_SPECIAL_ATTACK_DELAY / Const.FPS
        self.thre = {'' : 0.25,
                     'FAN' : 0.1, 
                     'LIGHTNING' : -1, 
                     'THROW_COFFEE' : 0.3,
                     'THROW_BUG' : 0.3,
                     'DOS' : -1,
                     'DDOS' : -1,
                    }
        self.refresh = ['FAN', 'THROW_COFFEE', 'THROW_BUG', 'DOS', 'DDOS', 'LIGHTNING']
        self.pos = self.center(self.helper.get_self_position())
        self.actionset = self.AI.actionset
        self.stored_ability = None

    def update(self):
        self.pos = self.center(self.helper.get_self_position())
        self.actionset = self.AI.actionset ## not sure if nessesary

    def check_melee(self):
        if self.helper.get_if_player_in_attack_range():
            self.actionset['attack'] = True

    def redirect_sp_attack(self):
        if 0 <= self.helper.get_self_special_attack_delay() <= 1:
            tmp, tmp2 = self.ability_land_prob(self.stored_ability, 1), self.ability_land_prob(self.stored_ability, -1)
            if tmp > tmp2 + self.eps:
                self.actionset['right'] = True
                return True
            elif tmp2 > tmp + self.eps:
                self.actionset['left'] = True
                return True
        return False

    def check_going_to_get_item():
        if self.helper.get_can_use_special_attack():
            for item in self.refresh:
                pos_list = self.helper.get_all_specific_item_position(item)
                for pos in pos_list:
                    if self.dist(self.center_item(pos), self.center(self.pos)) < self.radius:
                        self.actionset['special_attack'] = True
                        self.stored_ability = self.helper.get_keep_item_type()

    def check_sp_attack(self):
        if self.helper.get_can_use_special_attack():
            my_item = self.helper.get_keep_item_type()
            if self.ability_land_prob(my_item) > self.thre[my_item]:
                self.actionset['special_attack'] = True
                self.stored_ability = my_item

    def center(self, pos):
        return (pos[0] + Const.PLAYER_WIDTH / 2, pos[1] + Const.PLAYER_HEIGHT / 2)

    def dist(self, xx, yy):
        return sqrt((xx[0] - yy[0]) ** 2 + (xx[1] - yy[1]) ** 2)

    def ability_land_prob(self, ability, face = None):
        tmp_pos = self.helper.get_all_position()
        cbs = self.helper.get_all_can_be_special_attacked()
        tmp_speed = self.helper.get_all_speed()
        pos = []
        phantom = [] # not used yet
        for i in range(4):
            if i != self.id and cbs[i]:
                pos.append(self.center(tmp_pos[i]))
                phantom.append(self.center((tmp_pos[i][0] + tmp_speed[i][0] * self.sp_delay\
                    , tmp_pos[i][1] + tmp_speed[i][1] * self.sp_delay)))
        if len(pos) == 0:
            return 0.
        land_prob = 0.
        def rangetest(pp, factor):
            if face == None: 
                return max(0, 1 - abs(pp[0] - self.pos[0]) / factor)
            else:
                if (pp[0] - self.pos[0]) * face >= 0:
                    return max(0, 1 - (pp[0] - self.pos[0]) / factor)
                else: 
                    return 0

        if ability == '':
            for p in pos:
                land_prob += max(0, 1 - abs(p[1] - self.pos[1]) / 200)\
                     * rangetest(p, 1600)
        elif ability == 'FAN':
            for p in pos:
                land_prob += max(0, 1 - abs(p[1] - self.pos[1]) / 450) * rangetest(p, 1600)  
        elif ability == 'LIGHTNING':
            for p in pos:
                if p[1] < self.pos[1] + 50:
                    land_prob += rangetest(p, 200)     
        elif ability == 'THROW_COFFEE':
            for p in pos:
                if p[1] < self.pos[1] + 50:
                    land_prob += 0.5 + 0.5 * rangetest(p, 500)
        elif ability == 'THROW_BUG':
            for p in pos:
                land_prob += min(1, 500 / max(1, self.dist(p, self.pos)))
        else:
            return 0
        return land_prob

class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.default_actionset = {'left' : False, 'right' : False, 'jump' : False, 'attack' : False, 'special_attack' : False}
        self.actionset = self.default_actionset.copy()

        self.attacker = attacker(self)
        self.pathfinder = pathfinder(self)

        self.time = 0

    def decide(self):
        # update info
        self.actionset = self.default_actionset.copy()
        self.attacker.update()
        # if auto attack can hit, land the hit
        self.attacker.check_melee()
        # if directed ability's land probability is good, do it
        self.attacker.check_sp_attack()
        # try redirect directed ability if needed
        if not self.attacker.redirect_sp_attack():
            # pathfinder
            self.pathfinder.update()
            self.pathfinder.move() 
        print("done")
        return self.actionset
