import uvicorn, sys

if __name__ == "__main__":
    sys.path.append("..")
    uvicorn.run("webserver.main:app", reload=True)