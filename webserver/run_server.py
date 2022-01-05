import uvicorn, sys
from . import config

if __name__ == "__main__":
    sys.path.append("..")
    uvicorn.run("webserver.main:app", **config.UVICORN_CONFIG)