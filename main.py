from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange
import datetime

app = FastAPI()

#Its our model for database structure
class Player(BaseModel):
    name: str
    country: str
    live_rating : float
    age: int
    world_rank : int
    created_at: datetime.datetime = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M")
    rating_difference: float | None = None

#example of data
players = [{"id": 1, "name": "Magnus Carlsen", "country": "Norway", "live_rating": 2847, "age": 30, "world_rank": 1, "created_at": "2023-12-14-22.30",},
               {"id": 2, "name": "Fabiano Caruana", "country": "USA", "live_rating": 2820, "age": 28, "world_rank": 2, "created_at": "2023-12-14-22.31"},]

def find_player(id):
    for player in players:
        if player["id"] == id:
            return player



@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/players")  
def get_players():
    return {"data" : players}

@app.post("/players")
def create_players(player : Player):
    player_dict = player.model_dump()
    player_dict["id"] = randrange(1,100000)
    return {"player" :player_dict} #goes back to client as HTTP response

@app.get("/players/{id}")
def get_player(id : int):
    player = find_player(id)
    return {"player" : player}
