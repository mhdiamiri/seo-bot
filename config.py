# configure file
import os

PORT = 9150
HOST = "127.0.0.1"
CONTROLINIG_PORT = 9151

cwd = os.getcwd()
DRIVER_PATH = os.path.join(cwd, "chromedriver")

TARGET_HOST = "quera.org" # for test
SURF_PAGES = 100
WAITING_TIME = 1