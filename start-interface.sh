# convenience script to instantiate client interface
# usage: bash start-interface.sh <client_name>

docker exec -it $1 python /App/client_interface.py
