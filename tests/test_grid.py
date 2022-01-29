from app.grid import Grid

_ = None

GRID = [
    [_, 8, _, _, _, 2, _, 4, _],
    [_, _, _, _, 3, _, 5, _, 1],
    [_, _, 2, _, 7, 9, 8, _, _],
    [2, 7, _, _, _, _, _, _, _],
    [_, _, 4, _, _, _, _, _, _],
    [5, _, _, 3, 4, _, _, _, _],
    [8, _, 3, 7, 5, _, _, _, _],
    [_, 1, 7, _, _, _, _, _, _],
    [9, _, _, 2, 1, _, _, _, 4]
]

INVALID_GRID = [
    [_, 8, _, _, _, 2, _, 4, _],
    [_, _, _, _, 3, _, 5, _, 1],
    [_, _, 2, _, 7, 9, 8, _, _],
    [2, 7, _, _, _, _, _, _, _],
    [_, _, 4, _, _, _, _, _, _],
    [5, _, _, 3, 4, _, _, _, 4],  # <- error here
    [8, _, 3, 7, 5, _, _, _, _],
    [_, 1, 7, _, _, _, _, _, _],
    [9, _, _, 2, 1, _, _, _, 4]
]


def test_encode():

    code = Grid(GRID).encode()

    assert code == "hFEB_iAwZIFzybz14z-gDafDf4tRy"
    assert Grid.decode(code) == GRID

    assert Grid.decode(Grid(INVALID_GRID).encode()) == INVALID_GRID


def test_decode_locked():

    grid, mask = Grid.decode_locked("BjBdQFwGKEQFhVKEhWxOdFRhaFJErGcE6EhkUAR0~JVSpSVVU")

    assert grid == [[1, 8, _, _, _, _, 1, 7, 5],
                    [_, 1, 7, _, 1, 8, _, _, 1],
                    [1, _, 1, 6, 1, 5, 4, _, _],
                    [1, 2, 1, 5, _, _, _, 1, 3],
                    [9, _, _, _, _, _, 1, 5, 1],
                    [8, 5, _, _, 1, 4, 9, 1, 2],
                    [_, _, _, 1, 9, _, _, _, _],
                    [1, 3, _, _, 1, 2, 1, 9, 1],
                    [4, _, 1, 1, _, _, _, _, _]]

    assert mask == [[1, 0, 0, 0, 0, 0, 1, 1, 0],
                    [0, 1, 0, 0, 1, 0, 0, 0, 1],
                    [0, 0, 1, 0, 1, 1, 0, 0, 0],
                    [1, 0, 1, 0, 0, 0, 0, 1, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0, 1],
                    [1, 0, 0, 0, 1, 1, 0, 1, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 1, 0, 1, 0, 1],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0]]


def test_encode_locked():

    code = Grid.from_str("1L800001L7L501L701L8001L101L61L5L4001L21L50001L3L9000"
                         "001L51L8L5001L4L91L20001L900001L3001L21L91L401L100000").encode_locked()

    assert code == "BjBdQFwGKEQFhVKEhWxOdFRhaFJErGcE6EhkUAR0~JVSpSVVU"
