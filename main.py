from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#Its our model for database structure
class Player(BaseModel):
    name: str
    country: str
    live_rating : float
    world_rank : int

#example of data
players = [{"name": "Magnus Carlsen", "country": "Norway", "live_rating": 2847,  "world_rank": 1, "id": 1},
           {"name": "Fabiano Caruana", "country": "USA", "live_rating": 2820,  "world_rank": 2, "id": 2}]

def find_player(id):
    for player in players:
        if player["id"] == id:
            return player
        
def find_index_player(id):
    for index, player in enumerate(players):
        if player['id'] == id:
            return index
    return None



@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/players")  
def get_players():
    return {"data" : players}

@app.post("/players")
def create_players(player : Player, status_code= status.HTTP_201_CREATED):
    player_dict = player.model_dump()
    player_dict["id"] = randrange(1,100000)
    players.append(player_dict)
    return {"player" :player_dict} #goes back to client as HTTP response

@app.get("/players/{id}")
def get_player(id : int):
    player = find_player(id)
    if player is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"player with id: {id} was not found")
    return {"player" : player}

@app.delete("/players/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(id : int):
    index = find_index_player(id)
    if index is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"player with id: {id} was not found")
    players.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/players/{id}")
def update_player(id : int, player : Player):
    index = find_index_player(id)
    if index is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"player with id: {id} was not found")
    player_dict = player.model_dump()
    player_dict["id"] = id
    players[index] = player_dict
    return {"player" : player_dict}

