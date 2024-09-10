from chess import pgn
from io import StringIO


def to_binary_string(num: int, bits: int):
    return format(num, f'0{bits}b')


def get_pgn_games(pgn_string: str):
    games = []
    pgn_stream = StringIO(pgn_string)
    while game := pgn.read_game(pgn_stream):
        games.append(game)
    return games