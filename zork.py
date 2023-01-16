# Setup environment
import textworld
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from time import sleep

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

load_dotenv()
llm = OpenAI(model_name="text-davinci-003", temperature=0.0, max_tokens=50, stop=["\n",">","Game:"])





# Let the environment know what information we want as part of the game state.
infos = textworld.EnvInfos(
    feedback=True,    # Response from the game after typing a text command.
    description=True, # Text describing the room the player is currently in.
    inventory=True,    # Text describing the player's inventory.
    max_score=True,   # Maximum score obtainable in the game.
    score=True,       # Score obtained so far.
    
)
env = textworld.start('./zork1.z5', infos=infos)


def go(env, func, max_steps=10, interactive=False, secs=1):
    game_state = env.reset()
    try:
        done = False
        i = 0
        while not done:
            i += 1
            print("#"*60, i)
            description = "" if game_state.description == game_state.feedback else f"{game_state.description}"
            scene = f"""{description}{game_state.feedback}
(Score: {game_state.score}/{game_state.max_score}, Moves: {game_state.moves}, DONE: {done})
"""
            if interactive:
                print(scene)
                command = input(">")
            else:
                command = func(scene)
                print(">",command)
            game_state, score, done = env.step(command)
            sleep(secs)
            if i >= max_steps:
                break
        env.render()  # Final message.
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

    print("Played {} steps, scoring {} points.".format(game_state.moves, game_state.score))
    understood_commmands = game_state.moves / i
    print("Percentage of commands understood: {:.2f}%".format(* understood_commmands))

if __name__ == "__main__":
    go(env, lambda x: "look", interactive=True)













