from agents.agent import Agent
from game import Game


def train(agent: Agent, num_games: int):
    record = 0
    game = Game()
    state_old = game.get_current_state()
    for _ in range(num_games):
        move = agent.get_action(state_old)

        final_move = game.convert_move_to_direction(move)

        # perform move and get new state
        state_new, reward, game_over, score = game.play_step(final_move)

        # remember
        agent.remember(state_old, move, reward, state_new, game_over)
        state_old = state_new

        if game_over:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train()

            if score > record:
                record = score

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

if __name__ == '__main__':
    agent = Agent()
    num_games = 200
    train(agent, num_games)