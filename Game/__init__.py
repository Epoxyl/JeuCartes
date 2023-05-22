import os
from gymnasium.envs.registration import register

game_directory = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

session = {}

# Prepare environments (only President for now)
register(
    id='President-v0',
    entry_point='Game.IA.PresidentEnvironment:PresidentEnv',            # todo: change PresidentEnvironment to Environments
    kwargs={'playersName': ['Alexandre', 'Antoine', 'Julien', 'Yohann'], 'maxScore': 100}     # change maxScore ?
)
