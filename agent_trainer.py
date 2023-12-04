from typing import Union

from agents import *
from game import Game


OneOfAgent = Union[SimpleAgent, ConvAgent, SimpleAgentExtended]


def train(agent: OneOfAgent, num_games: int):
    record = 0
    game = Game()
    state_old = agent.get_current_state(game)
    for _ in range(num_games):
        game_over = False
        while not game_over:
            move = agent.get_action(state_old)

            final_move = game.convert_move_to_direction(move)

            reward, game_over, score = game.play_step(final_move)
             
            state_new = agent.get_current_state(game)

            agent.remember(state_old, move, reward, state_new, game_over)
            state_old = state_new

            if game_over:
                game.reset()
                agent.n_games += 1
                agent.train()

                if score > record:
                    record = score

                print('Game', agent.n_games, 'Score', score, 'Record:', record)


if __name__ == '__main__':
    num_games = 300
    agent = SimpleAgent()
    # agent = SimpleAgentExtended()
    # agent = ConvAgent()
    train(agent, num_games)
    agent.save_model()