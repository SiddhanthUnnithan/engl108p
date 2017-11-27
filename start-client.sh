# convenience script to start app server in client container
# usage: bash start-client.sh <container_name>

docker exec -it $1 python /App/client_server.py
