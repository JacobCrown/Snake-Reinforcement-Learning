import torch
import random
import numpy as np

from game import Game
from constants import Direction, Point
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 100
LR = 0.001

class Agent:
    def __init__(self, input_dim: int = 12):
        self.n_games = 0
        self.epsilon = 0 
        self.gamma = 0.9 
        self.model = Linear_QNet(12, 512, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma, batch_size=BATCH_SIZE)
        self.mem_cntr = 0

        self.state_memory = np.zeros((MAX_MEMORY, input_dim), dtype=np.float32)
        self.new_state_memory = np.zeros((MAX_MEMORY, input_dim), dtype=np.float32)
        self.action_memory = np.zeros((MAX_MEMORY), dtype=np.int32)
        self.reward_memory = np.zeros((MAX_MEMORY), dtype=np.float32)
        self.terminal_memory = np.zeros((MAX_MEMORY), dtype=bool)


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
            game.apple.x < head.x,  # food left
            game.apple.x > head.x,  # food right
            game.apple.y < head.y,  # food up
            game.apple.y > head.y  # food down
            ]

        return np.array(state, dtype=np.float32)

    def remember(self, state, action, reward, next_state, game_over):
        idx = self.mem_cntr % MAX_MEMORY
        self.state_memory[idx] = state
        self.action_memory[idx] = action
        self.reward_memory[idx] = reward
        self.new_state_memory[idx] = next_state
        self.terminal_memory[idx] = game_over

        self.mem_cntr += 1

    def train_long_memory(self):
        if self.mem_cntr < BATCH_SIZE:
            return

        max_mem = min(self.mem_cntr, MAX_MEMORY)
        batch = np.random.choice(max_mem, BATCH_SIZE, replace=False)

        state_batch = torch.tensor(self.state_memory[batch])
        next_state_batch = torch.tensor(self.new_state_memory[batch])
        action_batch = torch.tensor(self.action_memory[batch])
        reward_batch = torch.tensor(self.reward_memory[batch])
        terminal_batch = torch.tensor(self.terminal_memory[batch])

        self.trainer.train_step(state_batch, action_batch, reward_batch, \
                                next_state_batch, terminal_batch)

    def get_action(self, state) -> int:
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 120 - self.n_games
        move = 0 # 0 - left, 1 - straight, 2 - right
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            state_t = torch.tensor(state, dtype=torch.float32)
            prediction = self.model(state_t.unsqueeze(0))
            move = int(torch.argmax(prediction).item())

        return move


def train():
    record = 0
    agent = Agent()
    game = Game()
    state_old = agent.get_state(game)
    while True:
        move = agent.get_action(state_old)

        final_move = game.convert_move_to_direction(move)

        # perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # remember
        agent.remember(state_old, move, reward, state_new, game_over)
        state_old = state_new

        if game_over:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

if __name__ == '__main__':
    train()