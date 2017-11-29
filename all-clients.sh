# convenience script to execute all_clients command on game server (guardian)
# usage: bash all-clients.sh

docker exec -it game-server curl -XPOST localhost:8080/all_clients
