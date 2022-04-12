import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:pity", host="0.0.0.0", port=7777, reload=False)
