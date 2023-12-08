from fastapi import FastAPI
from mangum import Mangum
import uuid
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from app.connections.dynamodb_conn import get_dynamodb_conn

app = FastAPI()
handler = Mangum(app)

ddb = get_dynamodb_conn()

table = ddb.Table('tbl_toDoItems')

# Set up CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def getAllTodos():
    response = table.scan()
    todos = response.get('Items', [])
    return {"todos": todos}

@app.get("/todo/{todo_id}")
async def get_todo(todo_id: str):
    response = table.get_item(Key={'id': todo_id})
    return response['Item']

@app.post("/todo")
async def create_todos(todo: dict):
    todo_id = str(uuid.uuid4())
    todo['id'] = todo_id
    table.put_item(Item=todo)
    return "New todo added"

@app.put("/todo/updateStatus")
async def update_todo(todo_object: dict):
    response = table.update_item(
        Key={'id': todo_object.get('id')},
        UpdateExpression="""
            set
                todo_item = :todo_item,
                active_item = :active_item,
                order_item = :order_item
        """,
        ExpressionAttributeValues={
            ':todo_item': todo_object.get('todo_item'),
            ':active_item': todo_object.get('active_item'),
            ':order_item': todo_object.get('order_item'),
            },
        ReturnValues="UPDATED_NEW"
    )
    return response

@app.put("/todo/updatePosition")
async def update_todo(todo_objects: List[dict]):
    responses = []
    for todo_object in todo_objects:
        response = table.update_item(
            Key={'id': todo_object.get('id')},
            UpdateExpression="""
                set
                    todo_item = :todo_item,
                    active_item = :active_item,
                    order_item = :order_item
            """,
            ExpressionAttributeValues={
                ':todo_item': todo_object.get('todo_item'),
                ':active_item': todo_object.get('active_item'),
                ':order_item': todo_object.get('order_item'),
            },
            ReturnValues="UPDATED_NEW"
        )
        responses.append(response)
    return responses

@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: str):
    response = table.delete_item(Key={'id': todo_id})
    return response
