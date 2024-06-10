import environ
from pathlib import Path


env = environ.Env(
    DEBUG=(bool, False)
)

FBT_MODULE_NAME = env.str('FBT_MODULE_NAME')

REDIS_PASSWORD = env.str('REDIS_PASSWORD', "")
REDIS_PORT = env.int('REDIS_PORT', 6379)

WS_SERVER_PORT = env.int('WS_SERVER_PORT', 8001) 

BASE_DIR = Path(__file__).resolve().parent

# Complementary filter parameters
TAU = 0.98
DT  = 0.004 
