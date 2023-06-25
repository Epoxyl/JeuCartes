import gymnasium as gym

players = ['Alexandre', 'Antoine', 'Julien']
agent_list = [0, 0, 0, 0]
MAX_SCORE = 100
env = gym.make("President-v0")

def main():
    """
    Main program
    :return:
    """
    env.__init__(players, MAX_SCORE)


