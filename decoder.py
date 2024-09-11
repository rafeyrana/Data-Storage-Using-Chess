from time import time
from math import log2
from chess import pgn, Board
from utils import get_pgn_games


def decoder(pgn_string: str, output_file_path: str):
    start_time = time()
    total_move_count = 0

    # Load PGN games from the string
    games: list[pgn.Game] = get_pgn_games(pgn_string)

    # Initialize output file and clear its contents
    with open(output_file_path, "wb") as output_file:
        pass  # Empty the file by opening it in write-binary mode

    output_data = ""

    with open(output_file_path, "ab") as output_file:
        for game_index, game in enumerate(games):
            chess_board = Board()
            game_moves = list(game.mainline_moves())
            total_move_count += len(game_moves)

            for move_index, move in enumerate(game_moves):
                # Generate UCI for legal moves in current position
                legal_moves = list(chess_board.generate_legal_moves())
                legal_move_ucis = [legal_move.uci() for legal_move in legal_moves]

                # Get the binary representation of the played move based on its index
                move_index_in_legal_moves = legal_move_ucis.index(move.uci())
                move_binary = bin(move_index_in_legal_moves)[2:]  # Convert to binary

                # Calculate the max binary length based on the number of legal moves
                max_binary_length = int(log2(len(legal_move_ucis)))

                # If it's the last move of the last game, adjust binary length to fit byte alignment
                is_last_move_of_last_game = (
                    game_index == len(games) - 1 and move_index == len(game_moves) - 1
                )
                if is_last_move_of_last_game:
                    max_binary_length = min(max_binary_length, 8 - (len(output_data) % 8))

                # Pad the binary representation to fit the maximum binary length
                move_binary = move_binary.zfill(max_binary_length)

                # Play the move on the board
                chess_board.push_uci(move.uci())

                # Append the move binary to the output data string
                output_data += move_binary

                # If the output data is a multiple of 8 bits, flush it to the output file
                if len(output_data) % 8 == 0:
                    output_file.write(
                        bytes(
                            int(output_data[i * 8 : i * 8 + 8], 2)
                            for i in range(len(output_data) // 8)
                        )
                    )
                    output_data = ""  # Reset the output data buffer

    elapsed_time = round(time() - start_time, 3)
    print(f"\nSuccessfully decoded {len(games)} PGN game(s) with {total_move_count} move(s) in {elapsed_time} seconds.")
