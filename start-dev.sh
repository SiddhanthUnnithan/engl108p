# script to run 1 game server, 2 client containers in DEV mode
# usage: bash start-dev.sh

# build docker network for cross-container communication
docker network create game-network

# port mapping not needed as all communication is happening internally
docker run -d -it -v $PWD:/App --name game-server --network game-network game-server

docker run -d -it -v $PWD:/App -e CLIENT_HOSTNAME=client-1 -e GAME_SERVER_HOSTNAME=game-server -e DEV_FLAG=true --name client-1 --network game-network game-client

docker run -d -it -v $PWD:/App -e CLIENT_HOSTNAME=client-2 -e GAME_SERVER_HOSTNAME=game-server -e DEV_FLAG=true --name client-2 --network game-network game-client
