from fastapi import FastAPI
from mangum import Mangum
import uuid
from app.connections.dynamodb_conn import get_dynamodb_conn

app = FastAPI()
handler = Mangum(app)

ddb = get_dynamodb_conn()

table = ddb.Table('tbl_toDoItems')

@app.get('/')
async def getAllTodos():
    response = table.scan()
    todos = response.get('Items', [])
    return {"todos": todos}

@app.get("/todo/{todo_id}")
async def get_todo(todo_id: str):
    response = table.get_item(Key={'id': todo_id})
    return response['Item']
