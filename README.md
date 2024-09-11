# Data-Storage-Using-Chess
## Chess Move Encoding and Decoding Scheme

## Overview

This project implements a novel encoding and decoding scheme that converts any file in raw binary format into equivalent chess moves. These chess moves can then be simulated on platforms like [Lichess](https://lichess.org/), allowing for effective online storage of files. The core idea is to assign binary numbers to chess moves, enabling each move to represent a small part of the file through encoding.

## Key Features

- **Binary to Chess Moves**: Converts binary data from files into a sequence of chess moves.
- **Efficient Storage**: Utilizes a unique combination of 3 bits per move, allowing for more efficient encoding compared to a simple 1 bit per move.
- **Game Management**: Automatically starts a new game upon reaching a terminal state (checkmate, draw, or insufficient material).
- **Flexible Encoding**: Supports encoding of various file types by mapping binary data to chess moves based on their order in the chess library.

## How It Works

1. **Encoding**: The `encoder` function reads a binary file and converts it into a series of chess moves. Each legal move is assigned a unique binary representation based on its index.
2. **Decoding**: The `decode` function takes a PGN (Portable Game Notation) string and converts it back into binary data, reconstructing the original file.
3. **Game State Management**: The encoding process recognizes when a game ends (either through checkmate, draw, or a position with only one legal move) and starts a new game accordingly.