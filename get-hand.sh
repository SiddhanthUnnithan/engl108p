# convenience script to run get_hand command
# usage: bash get-hand.sh <client_name>

docker exec -it $1 curl localhost:8080/get_hand
