# convenience script to execute send_turn command against client
# usage: bash send-turn.sh <client_name> <card_index>

docker exec -it $1 python /App/shell_helpers/send-turn.py $1 $2

docker exec -it $1 curl localhost:8080/get_hand
