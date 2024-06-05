import environ
from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False)
)

FBT_MODULE_NAME = env.str('FBT_MODULE_NAME')

BASE_DIR = Path(__file__).resolve().parent