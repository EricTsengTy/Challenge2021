import Const
from math import sqrt
import heapq as heap
from collections import defaultdict

class A_star():
    def __init__(self):
        self.max_x = Const.ARENA_SIZE[0]
        self.max_y = Const.ARENA_SIZE[1]
        self.resol = 10
        self.x, self.y = self.max_x // self.resol, self.max_y // self.resol 
        self.default_graph = self.build_init_graph()
        self.land_padding_height = 20 // self.resol
        self.land_padding_width = 50 // self.resol
        self.jmp_limit = 360 / self.resol

        self._1dir = {(-1, 0) : 2 , (1, 0) : 2 , (-1, -1) : 3, (1, -1) : 3, (0, -1) : 3}
        self._0dir = {(-1, 0) : 2 , (1, 0) : 2 , (-1, -1) : 3, (1, -1) : 3, (0, -1) : 3,
                      (-1, 1) : 6 , (0, 1) : 6 , ( 1,  1) : 6}

    def build_init_graph(self):
        tmp = [[0 for i in range(self.y)] for _ in range(self.x)]
        for floor in Const.GROUND_POSITION:
            left, top, width, height = floor
            left //= self.resol
            top //= self.resol
            width //= self.resol
            height //= self.resol
            for i in range(left - 1, left + width + 1): # padding
                if i < 0 or i >= self.x:
                    continue
                for j in range(top, top + height):
                    tmp[i][j] = -1  # wall
                tmp[i][top - 1] = 1 # ground

        return tmp

    def estimate(self, x, y):
        est = abs(x[0] - y[0])
        if x[1] > y[1]:
            if x[1] - y[1] < self.jmp_limit:
                est += (x[1] - y[1]) * 1.2
            else:
                est += 80
        else:
            est += (y[1] - x[1]) * 2
        return est

    def neighbor(self, x):
        ans = [] # (v, dist_v)
        if self.default_graph[x[0]][x[1]] == 1:
            using = self._1dir
        else:
            using = self._0dir

        for v_dir, dist_v in using.items():
            pos = (x[0] + v_dir[0], x[1] + v_dir[1])
            if pos[0] >= self.x or pos[0] < 0 or pos[1] >= self.y or pos[1] < 0:
                continue
            ans.append((pos, dist_v))
        return ans

    def find_path(self, source, goal):
        return self.find((int(source[0] / self.resol), int(source[1] / self.resol - 0.5)),\
                         (int(goal[0] / self.resol + Const.ITEM_WIDTH / 2 / self.resol),\
                          int(goal[1] / self.resol + Const.ITEM_HEIGHT / 2 / self.resol)))

    def find(self, source, goal):
        g_score = {source : 0}
        h_score = {source : self.estimate(source, goal)}
        f_score = {source : h_score[source]}
        open_set, closed_set = [(h_score[source], source)], set()
        parent = {}
        
        def best_move(): # backtracking
            prev, now = goal, parent[goal]
            while now != source:
                prev, now = parent[prev], parent[now]
            return (prev[0] - source[0], prev[1] - source[1])

        while len(open_set) > 0:
            _ , x = heap.heappop(open_set)

            if x == goal:
                return (best_move(), g_score[x])
            if x in closed_set:
                continue

            closed_set.add(x)
            for y, dist_y in self.neighbor(x):
                if y in closed_set:
                    continue
                tentative_gscore = g_score[x] + dist_y
                if (y not in g_score) or (tentative_gscore < g_score[y]):
                    parent[y] = x
                    g_score[y] = tentative_gscore
                    h_score[y] = self.estimate(y, goal)
                    f_score[y] = g_score[y] + h_score[y]
                    heap.heappush(open_set, (f_score[y], y))
        return None








class TeamAI():
    def __init__(self, helper):
        self.helper = helper
        self.default_actionset = {'left' : False, 'right' : False, 'jump' : False, 'attack' : False, 'special_attack' : False}
        self.atk_only = {'left' : False, 'right' : False, 'jump' : False, 'attack' : True, 'special_attack' : False}
        self.actionset = self.default_actionset
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
        self.want = ['FAN', 'THROW_COFFEE', 'THROW_BUG', 'DOS', 'DDOS', 'EXE', 'FIREWALL']
        self.refresh = ['FAN', 'THROW_COFFEE', 'THROW_BUG', 'DOS', 'DDOS', 'LIGHTNING']
        self.stored_ability = None
        self.eps = 0.01
        self.pos = self.center(self.helper.get_self_position())
        self.pathfinder = A_star()
        self.dont_jmp = 0
        self.jmp_delay = 8
        self.A_star_timer = 0
        self.A_star_delay = 12
        self.stored_move = None
        self.want_item = None
        self.radius = 120

    def decide(self):
        if self.A_star_timer > 0:
            self.A_star_timer -= 1
        if self.dont_jmp > 0:
            self.dont_jmp -= 1
        if self.helper.get_in_folder():
            return self.atk_only

        self.actionset = self.default_actionset.copy()
        self.pos = self.center(self.helper.get_self_position())
        # if auto attack can hit, land the hit
        self.check_melee()
        # if directed ability's land probability is good, do it
        self.check_sp_attack()
        # try redirect directed ability if needed
        if not self.redirect_sp_attack():
            self.move() # find the nearest useful item, and go to it
        
        # if "is going to get a new item", use current item
        #self.check_going_to_get_item()

        if self.dont_jmp > 0:
            self.actionset['jump'] = False
        if self.actionset['jump']:
            self.dont_jmp = self.jmp_delay

        # print(self.pos[1])
        # print(self.stored_move, self.want_item)
        return self.actionset

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

    def move(self):
        if self.A_star_timer == 0:
            self.A_star_timer = self.A_star_delay
            nearest, best_move, self.want_item = 10000, None, None
            for item in self.want:
                pos_list = self.helper.get_all_specific_item_position(item)
                for pos in pos_list:
                    tmp = self.pathfinder.find_path(self.feet(), pos)
                    if tmp is not None:
                        tmp_move, d = tmp
                        if d < nearest:
                            nearest, best_move, self.want_item = d, tmp_move, item
            self.stored_move = best_move

        if self.stored_move[0] == 1:
            self.actionset['right'] = True
        elif self.stored_move[0] == -1:
            self.actionset['left'] = True

        if self.stored_move[1] == -1:
            if self.helper.get_self_speed()[1] > - self.eps:
                self.actionset['jump'] = True
        # print(self.stored_move, self.want_item)
    
    def feet(self):
        return (self.pos[0], self.pos[1] + Const.PLAYER_HEIGHT / 2 - 1)

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


















    def center(self, pos):
        return (pos[0] + Const.PLAYER_WIDTH / 2, pos[1] + Const.PLAYER_HEIGHT / 2)

    def center_item(self, pos):
        return (pos[0] + Const.ITEM_WIDTH / 2, pos[1] + Const.ITEM_HEIGHT / 2)

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







