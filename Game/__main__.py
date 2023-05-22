import gymnasium as gym

players = ['Alexandre', 'Antoine', 'Julien']
agent_list = [0, 0, 0, 0]
MAX_SCORE = 100

def main():
    """
    Main program
    :return:
    """

    env = gym.make("President-v0")
    env.__init__(players, MAX_SCORE)


