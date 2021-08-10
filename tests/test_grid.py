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
