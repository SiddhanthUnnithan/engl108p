# convenience script to end turn
# usage: bash end-turn.sh <client_name>

docker exec -it $1 curl localhost:8080/end_turn
