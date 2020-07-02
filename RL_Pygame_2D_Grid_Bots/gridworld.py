import pygame
import numpy as np

class player():

    def __init__(self, x, y):

        # Initial Position - Episode Memory
        self.init_x = x
        self.init_y = y

        # Position Attributes
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.pos_x = 25*x
        self.pos_y = 25*y
        self.target_pos_x = 25*x
        self.target_pos_y = 25*y

        # Characteristic Attributes
        self.team = 1

    def decide_move(self):
        if self.x == self.target_x and self.y == self.target_y:
            diceroll = np.random.random(1)[0]
            if diceroll < 0.001:
                self.set_target(1, 0)
            if diceroll > 0.001 and diceroll < 0.002:
                self.set_target(-1, 0)
            if diceroll > 0.002 and diceroll < 0.003:
                self.set_target(0, 1)
            if diceroll > 0.003 and diceroll < 0.004:
                self.set_target(0, -1)

    def move(self):
        if (self.pos_x != self.target_pos_x or self.pos_y != self.target_pos_y):
            self.pos_x = self.pos_x + np.sign(self.target_pos_x - self.pos_x)
            self.pos_y = self.pos_y + np.sign(self.target_pos_y - self.pos_y)
        else:
            self.x = self.target_x
            self.y = self.target_y

    def set_target(self, dx, dy):
        self.target_pos_x = self.pos_x + 25 * dx
        self.target_x = self.x + 1 * dx

        self.target_pos_y = self.pos_y + 25 * dy
        self.target_y = self.y + 1 * dy

    def draw(self, window):
        pygame.draw.rect(window, (0,0,255), (self.pos_x, self.pos_y, 25, 25))

class goal():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos_x = 25*x
        self.pos_y = 25*y

    def draw(self, window):
        pygame.draw.rect(window, (50, 255, 50), (self.pos_x, self.pos_y, 25, 25))

class world():

    def __init__(self, w, h):

        # Dimensions of the board
        self.w = w
        self.h = h
        self.xsize = w/25
        self.ysize = h/25

        # Penalties and Rewards
        self.wall_collide_penalty = 0
        self.teammate_collide_penalty = 0
        self.opponent_collide_penalty = 0
        self.timestep_penalty = 0
        self.goal_reward = 0

        # Initialize Arrays
        self.players = []
        self.goals = []

    def define_state(self):
        state = np.zeros([self.xsize, self.ysize])
        for p in self.players:
            state[p.x][p.y] = p.team
        for g in self.goals:
            state[g.x][g.y] = -1
        return state

    def learn(self):
        for p in self.players:

            # Call Learning Function for Agent
            p.decide_move()

            # Wall Collision
            if p.target_x < 0 or p.target_x >= self.xsize:
                p.target_x = p.x
                p.target_pos_x = p.pos_x
            if p.target_y < 0 or p.target_y >= self.ysize:
                p.target_y = p.y
                p.target_pos_y = p.pos_y

            # Player Collision
            for pp in self.players:
                if pp != p and p.target_x == pp.x:
                    if p.team == pp.team:
                        pass # logic
                    else:
                        pass # logic
                    p.target_x = p.x
                    p.target_pos_x = p.pos_x
                if pp != p and p.target_y == pp.y:
                    if p.team == pp.team:
                        pass # logic
                    else:
                        pass # logic
                    p.target_y = p.y
                    p.target_pos_y = p.pos_y

            # Execute Action
            p.move()

    def draw(self, window):
        for p in self.players:
            p.draw(window)
        for g in self.goals:
            g.draw(window)

    def add_player(self, x, y):
        self.players.append(player(x, y))

    def add_goal(self, x, y):
        self.goals.append(goal(x, y))

    def set_wall_collide_penalty(self, val):
        self.wall_collide_penalty = val

    def set_teammate_collide_penalty(self, val):
        self.teammate_collide_penalty = val

    def set_opponent_collide_penalty(self, val):
        self.opponent_collide_penalty = val

    def set_timestep_penalty(self, val):
        self.timestep_penalty = val

    def set_goal_reward(self, val):
        self.goal_reward = val
