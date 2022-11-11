import os


class EnvModeChoices:
    prod = 'prod'
    dev = 'dev'
    local = 'local'


class Reaction:
    positive = 'pos'
    negative = 'neg'


ENV_MODE = os.getenv('PROD_DEV_MODE', EnvModeChoices.local)
