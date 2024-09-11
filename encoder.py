from time import time
from math import log2
from chess import pgn, Board
from utils import to_binary_string


def encoder(file_path: str) -> str:
    start_time = time()

    # Read file as bytes
    print("Reading file...")
    with open(file_path, "rb") as file:
        file_bytes = list(file.read())

    total_bits = len(file_bytes) * 8  # Total number of bits in the file
    print("\nEncoding file...")

    output_pgns: list[str] = []
    bit_index = 0
    chess_board = Board()

    while True:
        legal_moves = list(chess_board.generate_legal_moves())

        # Calculate the maximum number of bits needed to represent a move
        max_bits_for_move = min(
            int(log2(len(legal_moves))),
            total_bits - bit_index
        )

        # Map legal moves to binary strings
        move_to_bits = {
            move.uci(): to_binary_string(i, max_bits_for_move)
            for i, move in enumerate(legal_moves)
        }

        # Get the next chunk of bits from the file
        byte_start_index = bit_index // 8
        file_chunk_pool = "".join(
            to_binary_string(byte, 8) for byte in file_bytes[byte_start_index : byte_start_index + 2]
        )
        next_chunk = file_chunk_pool[bit_index % 8 : bit_index % 8 + max_bits_for_move]

        # Find and apply the corresponding move
        for move_uci, move_bits in move_to_bits.items():
            if move_bits == next_chunk:
                chess_board.push_uci(move_uci)
                break

        # Move the pointer forward by the chunk size
        bit_index += max_bits_for_move

        # Check for terminal game state or EOF
        eof_reached = bit_index >= total_bits
        game_over = (
            chess_board.legal_moves.count() <= 1
            or chess_board.is_insufficient_material()
            or chess_board.can_claim_draw()
            or eof_reached
        )

        if game_over:
            game = pgn.Game()
            game.add_line(chess_board.move_stack)
            output_pgns.append(str(game))

            chess_board.reset()  # Reset the board for the next game

        if eof_reached:
            break

    elapsed_time = round(time() - start_time, 3)
    print(f"\nSuccessfully converted file to {len(output_pgns)} PGN game(s) in {elapsed_time} seconds.")

    return "\n\n".join(output_pgns)
