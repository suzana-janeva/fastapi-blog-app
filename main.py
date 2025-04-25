from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Blog App!"}

@app.get("/posts/{post_id}")
def read_post(post_id: int):
    return {"post_id": post_id, "title": f"Post {post_id}", "content": "This is a sample post content."}