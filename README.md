# Live Chat Service

This project implements a live chat service that supports both UDP and TCP protocols. Users can create and join chat rooms to communicate in real-time.

## Features
- Support for UDP and TCP protocols: Choose between UDP for faster, connectionless communication and TCP for reliable, connection-oriented communication.
- Chat rooms: Users can create and join multiple chat rooms.
- Real-time messaging: Messages are delivered in real-time within the chat rooms.

## ScreenShot
![Network](https://github.com/Ahmed-Ehab20/Chat/assets/102390696/78c39b88-22f5-4d25-9739-82d3f7e4c305)

## How To Run
1. Open a terminal and navigate to the project directory.
2. Run the following program
   ```sh
    python TCPserver.py
    ```
   or
   ```sh
    python UDPserver.py
    ```
3. Then Run the Client
   ```sh
    python TCPclient.py
    ```
   or
   ```sh
    python UDPclient.py
    ```
