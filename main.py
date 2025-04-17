from fastapi import FastAPI
from typing import Optional
app = FastAPI()
@app.get('/')
async def read_root():
    return {"message": "hello world"}
@app.get('/message')
async def read_message():
    return "I am the message"
@app.get('/greeting')
async def showGreeting(name:str,age:int)-> dict:
    return {"message": "hello "+name,"age":age,}
@app.get('/items/{item_no}')
async def showGreeting(item_no: int):
    return {"item":item_no}
@app.get('/users/me')
async def getCurrentUser():
    return {"Current User": 'current User'}
@app.get('/users/{user_id}')
async def getCurrentUserId(user_id):
    return {"UserId":user_id}
 
from enum import Enum
class ModelName(str, Enum): # ModelName is a subclass that inherits from Enum and str 
    # why string == to behave like a string
    # why enum == so that we can define a fixed number of choices. no need for manually checking
    Shahid ='Shahid'
    Khaista = 'Khaista'
    Imad = "Imad"
@app.get('/models/{model_name}')
async def getModel(model_name: ModelName):
    if(model_name is ModelName.Imad):
        return ModelName.Imad
    if(model_name is ModelName.Khaista):
        return ModelName.Khaista
    if(model_name is ModelName.Shahid):
        return ModelName.Shahid
@app.get('/active')
async def getActiveUser(name: Optional[str]= 'shahid', age:int = 34)->dict:
    return {"message": "hello "+name, "age": age}
    
# this is queryparams, if we give it a value it will print otherwise it will shift to the default values.

#QUERY PARAMS TYPE CONVERSION
@app.get('/items_id/{item_id}')
async def getItemNumber(item_id: str, q: Optional[str]= None)-> dict:
    if q:
        print('The q value is '+q)
        return {"item_id": item_id, "q": q}
        
    return {"item_id": item_id}
@app.get('/shortexample/{item_id}')
async def readItem(item_id: str, q: Optional[str]= None, short: bool = False):
    item_id = {"item_id": item_id}
    if q:
        item_id.update({"q": q})
    if not short:
        item_id.update({"description": "this is an amazing item."})
    return item_id
from pydantic import BaseModel
class Item(BaseModel):
    name: str
    description: Optional[str]= None
    price: Optional[float]= None
    tax: Optional[float]= None
@app.post('/postitem/')
async def postItem(item: Item):
    item_dict = item.model_dump()
    if(item.tax is not None):
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
from fastapi import Query,Path
from typing import Annotated
@app.get('/annotated/')
# > becomes %3E

  #  $ becomes %24
async def annotatedExample(q: Annotated[str | None, Query(min_length=10,max_length=50)]= None):
    result = {"item": [{"item_id:" "Foo"}, {"item_id": "Bar"}]}
    if q and q.startswith("hi") and q.endswith("$"):
        result.update({"q": q})
    return result
@app.get('/list/')
async def recieveList(q: Annotated[list[str] |None, Query(title="Query String",min_length=1,deprecated=True)] = {"foo","bar"}):
    q_items = {"item": q}
    return q_items
# PATH PARAMETER AND NUMERIC VALIDATION
@app.get('/usingpath/{item_id}')
async def usePath(item_id: Annotated[str|None, Path(title='this example is path parameter')],q:Annotated[str | None,Query(alias='query-parameter')]= None):
    result = {"item_id": item_id}
    if q:
        result.update({"q":q})
    return result
@app.get('/ensuring/{item_id}')
async def esure(q: str, item_id: Annotated[int, Path(title= 'the id of item to get')]):
    result = {"item_id": item_id}
    if q:
        result.update({"q":q})
    return result
    

    




 
    
