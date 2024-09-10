from time import time
from math import log2
from chess import pgn, Board
from util import to_binary_string



# Enter a file path and it returns a string of 1 or more PGNs that represent it

def encoder(file_path: str):
    start_time = time()

    # read binary of file
    print("reading file...")
    with open(file_path, "rb") as file:
        file_bytes = list(file.read())

    # record number of bits in file
    file_bits_count = len(file_bytes) * 8

    # convert file to chess moves
    print("\nencoding file...")
    output_pgns: list[str] = []
    file_bit_index = 0
    chess_board = Board()

    while True:
        legal_moves = list(chess_board.generate_legal_moves())
        move_bits = {legal_move.uci(): to_binary_string(index, min(int(log2(len(legal_moves))), file_bits_count - file_bit_index)) for index, legal_move in enumerate(legal_moves)}

        # take next binary chunk from the file
        file_chunk_pool = "".join([to_binary_string(byte, 8) for byte in file_bytes[file_bit_index // 8 : file_bit_index // 8 + 2]])
        next_file_chunk = file_chunk_pool[file_bit_index % 8 : file_bit_index % 8 + len(next(move_bits.values()))]

        # push chess move that corresponds with next chunk
        move_uci = next((move for move, binary in move_bits.items() if binary == next_file_chunk), None)
        if move_uci:
            chess_board.push_uci(move_uci)
            file_bit_index += len(move_bits[move_uci])
        else:
            break

        # check if the game is in a terminal state or EOF
        # if it is, convert it to a pgn and add to pgn list
        if (
            chess_board.legal_moves.count() <= 1
            or chess_board.is_insufficient_material()
            or chess_board.can_claim_draw()
            or file_bit_index >= file_bits_count
        ):
            pgn_board = pgn.Game()
            pgn_board.add_line(chess_board.move_stack)
            output_pgns.append(str(pgn_board))
            chess_board.reset()

        if file_bit_index >= file_bits_count: break

    print(
        f"\nsuccessfully converted file to pgn with "
        + f"{len(output_pgns)} game(s) "
        + f"({round(time() - start_time, 3)}s)."
    )

    # return pgn string
    return "\n\n".join(output_pgns)