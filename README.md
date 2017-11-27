# engl108p
HP-themed President with Exploding Snap cards.

Instead of introducing the complexity of a persistent socket connection and dealing with multiple clients, we can instantiate a single  game server and multiple client 'servers' that send HTTP requests to the game server, which is monitored by a game guardian (someone that facilitates start/end of the game).

## Game Server
- Flask
- Global Variables
    - valid clients
        - maps client name to _secret_ key identifier
    - turns (cyclical queue)
        - initial random generation
    - current game state (last observed card)
        - nature of this data structure is dependent on the game mechanics (e.g. might want to store last three cards for President runs)
- Routes
    - JOIN
        - returns client identifier
    - ALL CLIENTS JOINED
        - sent by *guardian*
        - sends notifications to all clients
    - SEND TURN
        - initiated from interface, sent through client server
    - GET CURRENT GAME state 
    - QUIT
        - delete all game state

## Guardian Client
- Assumption: all clients are running on the same machine
    - Instantiates 'x' docker containers corresponding to each client
    - Provides unique incrementing identifier for each client container

## Client Interface
- Persistent I/O stream which a user interacts with via the terminal
- Key-based commands

## Client Server
- Proxy which stores client state
- Sends requests to game server depending on client interface _request_
- No requests made from external _machines_
- Global Variables
    - Client hand
    - Client identifier
- Routes
    - SEND TURN
        - strictly used for forwarding to the game server
        - randomly determines whether a card should explode prior to it being sent
            - if card explodes; end turn but don't alter turn queue
    - GET HAND
        - returns current client hand
        - randomly determines whether a card should explode from the hand before being returned
            - randomly selected card across the entire hand
        - order of the cards is fixed
        - only applicable to games
