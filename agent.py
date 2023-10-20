from collections import deque
import time

import torch
import random

from game import Game
from constants import Direction, Point
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 
        self.gamma = 0.9 
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(12, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game: Game):
        snake = game.snake
        head = snake.head
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = snake.direction == Direction.LEFT
        dir_r = snake.direction == Direction.RIGHT
        dir_u = snake.direction == Direction.UP
        dir_d = snake.direction == Direction.DOWN

        state = [
            # Danger up
            snake.is_collision(point_u),

            # Danger down
            snake.is_collision(point_d),

            # Danger right
            snake.is_collision(point_r),

            # Danger left
            snake.is_collision(point_l),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.apple.x < snake.head.x,  # food left
            game.apple.x > snake.head.x,  # food right
            game.apple.y < snake.head.y,  # food up
            game.apple.y > snake.head.y  # food down
            ]

        return torch.tensor(state, dtype=torch.float32).unsqueeze(0)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        state = torch.concat(states, axis=0)
        next_state = torch.cat(next_states, axis=0)
        action = torch.tensor(actions, dtype=torch.long)
        reward = torch.tensor(rewards, dtype=torch.float32)

        self.trainer.train_step(state, action, reward, next_state, game_overs)

    def train_short_memory(self, state: torch.Tensor, action: int, reward: int,
                           next_state: torch.Tensor, game_over: bool):
        action_t = torch.tensor(action, dtype=torch.long).unsqueeze(0)
        reward_t = torch.tensor(reward, dtype=torch.float32).unsqueeze(0)
        next_state_t = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)
        state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        game_over_t = (game_over,)
        
        self.trainer.train_step(state_t, action_t, reward_t, next_state_t, game_over_t)

    def get_action(self, state) -> int:
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        move = 0 # 0 - left, 1 - straight, 2 - right
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            prediction = self.model(state)
            move = torch.argmax(prediction).item()

        return int(move)


def train():
    record = 0
    agent = Agent()
    game = Game()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        move = agent.get_action(state_old)

        final_move = game.convert_move_to_direction(move)

        # perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move.value, reward, state_new, game_over)

        # remember
        agent.remember(state_old, final_move.value, reward, state_new, game_over)

        if game_over:
            # train long memory, plot result
            game = Game()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score

            print('Game', agent.n_games, 'Score', score, 'Record:', record)
            time.sleep(0.1)

if __name__ == '__main__':
    train()