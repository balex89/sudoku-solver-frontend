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

    grid, mask = Grid.decode_locked("hGOsvL8D1EeIEooxA86ULJw6IHBwfw~gyRLFDAsaEEVIA")

    assert grid == [[_, 8, _, _, _, _, _, 7, 5],
                    [_, _, 7, _, _, 8, _, _, _],
                    [1, _, _, 6, _, 5, 4, _, _],
                    [_, 2, _, 5, _, _, _, _, 3],
                    [9, _, _, _, _, _, _, 5, _],
                    [8, 5, _, _, _, 4, 9, _, 2],
                    [_, _, _, _, 9, _, _, _, _],
                    [_, 3, _, _, _, 2, _, 9, _],
                    [4, _, _, 1, _, _, _, _, _]]

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

    code = Grid.from_str("0L800000L7L500L700L8000L100L60L5L4000L20L50000L3L9000"
                         "000L50L8L5000L4L90L20000L900000L3000L20L90L400L100000").encode_locked()

    assert code == "hGOsvL8D1EeIEooxA86ULJw6IHBwfw~gyRLFDAsaEEVIA"
