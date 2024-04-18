import os

# Easy to use for relative paths a cross the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(ROOT_DIR, "../output")

APP_DATA_DIR = os.getenv('LOCALAPPDATA')

DEFAULT_PLAYER_INSTANCE = "/World/audio2face/Player"
DEFAULT_SOLVER_INSTANCE = "/World/audio2face/BlendshapeSolve"
DEFAULT_A2E_INSTANCE = "/World/audio2face/CoreFullface"