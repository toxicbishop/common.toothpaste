"""
Preview a name as GitHub contribution-graph art (7 rows x 52 cols).
Uses a 3x5 pixel font. Letter cells are filled squares on a 7-row grid.
"""

FONT = {
    'a': ['.X.', 'X.X', 'XXX', 'X.X', 'X.X'],
    'b': ['XX.', 'X.X', 'XX.', 'X.X', 'XX.'],
    'c': ['.XX', 'X..', 'X..', 'X..', '.XX'],
    'd': ['XX.', 'X.X', 'X.X', 'X.X', 'XX.'],
    'e': ['XXX', 'X..', 'XX.', 'X..', 'XXX'],
    'f': ['XXX', 'X..', 'XX.', 'X..', 'X..'],
    'g': ['.XX', 'X..', 'X.X', 'X.X', '.XX'],
    'h': ['X.X', 'X.X', 'XXX', 'X.X', 'X.X'],
    'i': ['XXX', '.X.', '.X.', '.X.', 'XXX'],
    'j': ['..X', '..X', '..X', 'X.X', '.X.'],
    'k': ['X.X', 'X.X', 'XX.', 'X.X', 'X.X'],
    'l': ['X..', 'X..', 'X..', 'X..', 'XXX'],
    'm': ['X.X', 'XXX', 'XXX', 'X.X', 'X.X'],
    'n': ['X.X', 'XXX', 'XXX', 'XXX', 'X.X'],
    'o': ['XXX', 'X.X', 'X.X', 'X.X', 'XXX'],
    'p': ['XX.', 'X.X', 'XX.', 'X..', 'X..'],
    'q': ['.X.', 'X.X', 'X.X', 'XX.', '..X'],
    'r': ['XX.', 'X.X', 'XX.', 'X.X', 'X.X'],
    's': ['.XX', 'X..', '.X.', '..X', 'XX.'],
    't': ['XXX', '.X.', '.X.', '.X.', '.X.'],
    'u': ['X.X', 'X.X', 'X.X', 'X.X', 'XXX'],
    'v': ['X.X', 'X.X', 'X.X', 'X.X', '.X.'],
    'w': ['X.X', 'X.X', 'XXX', 'XXX', 'X.X'],
    'x': ['X.X', 'X.X', '.X.', 'X.X', 'X.X'],
    'y': ['X.X', 'X.X', '.X.', '.X.', '.X.'],
    'z': ['XXX', '..X', '.X.', 'X..', 'XXX'],
    '0': ['XXX', 'X.X', 'X.X', 'X.X', 'XXX'],
    '1': ['.X.', 'XX.', '.X.', '.X.', 'XXX'],
    '2': ['XXX', '..X', 'XXX', 'X..', 'XXX'],
    '3': ['XXX', '..X', 'XXX', '..X', 'XXX'],
    '4': ['X.X', 'X.X', 'XXX', '..X', '..X'],
    '5': ['XXX', 'X..', 'XXX', '..X', 'XXX'],
    '6': ['XXX', 'X..', 'XXX', 'X.X', 'XXX'],
    '7': ['XXX', '..X', '..X', '..X', '..X'],
    '8': ['XXX', 'X.X', 'XXX', 'X.X', 'XXX'],
    '9': ['XXX', 'X.X', 'XXX', '..X', 'XXX'],
    ' ': ['...', '...', '...', '...', '...'],
}

ROWS = 7
COLS = 52
LETTER_W = 3
GAP = 1
TOP_PAD = 1  # letter rendered in rows 1..5, leaves top/bottom row blank

FILLED = '#'
EMPTY = '.'


def render(name: str):
    name = name.lower()
    unknown = [c for c in name if c not in FONT]
    if unknown:
        raise ValueError(f"Unsupported chars: {unknown!r}. Allowed: a-z, 0-9, space.")

    width = len(name) * (LETTER_W + GAP) - GAP
    if width > COLS:
        raise ValueError(f"Name too wide: {width} cols, max {COLS}. Drop a char or two.")

    grid = [[0] * COLS for _ in range(ROWS)]
    x = (COLS - width) // 2  # center horizontally

    for ch in name:
        glyph = FONT[ch]
        for r in range(5):
            for c in range(LETTER_W):
                if glyph[r][c] == 'X':
                    grid[TOP_PAD + r][x + c] = 1
        x += LETTER_W + GAP

    return grid


def print_grid(grid):
    for row in grid:
        print(' '.join(FILLED if v else EMPTY for v in row))


def main():
    name = input("Enter name (a-z, 0-9, spaces): ").strip()
    if not name:
        print("No input.")
        return
    try:
        grid = render(name)
    except ValueError as e:
        print(f"Error: {e}")
        return
    print(f"\nPreview ({ROWS} rows x {COLS} cols — matches GitHub graph):\n")
    print_grid(grid)


if __name__ == "__main__":
    main()
