# convenience script to start application server in game container
# usage: bash start-gs.sh

docker exec -it game-server python /App/game_server.py
