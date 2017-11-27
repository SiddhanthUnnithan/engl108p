# stop game and client containers
docker stop game-server
docker stop client-1
docker stop client-2

docker rm game-server
docker rm client-1
docker rm client-2

docker network rm game-network
