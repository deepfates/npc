import argparse
from npc.game import Game

# Now let's run the game
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--game_file', type=str, default='./zork1.z5')
    parser.add_argument('--max_steps', type=int, default=10)
    args = parser.parse_args()
    game_file = args.game_file
    max_steps = args.max_steps
    
    game = Game(game_file=game_file, max_steps=max_steps)#, agent_turns=5)
    game.run()
