class Grid(list):
    """
        A Wrapper for a list of list of values (1,..,9 or None), representing Sudoku grid.
        Provides methods for compact URL-safe encoding of valid and invalid grids.

        Tip 1: Use encode_1() / decode_1() methods for valid grids.
        Tip 2: Use encode() / decode() as universal and safe methods.
    """

    B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-'
    FB64 = {c: i for i, c in enumerate(B64)}
    ALL_ALTS = tuple(range(10))
    ALL_ALTS_SET = frozenset(ALL_ALTS)

    @classmethod
    def from_str(cls, string):
        """
            Reads grid as a string of 81 values ("0" stands for a blank cell)
            given row by row, e.g.: "001003024020000056..."
        """
        return cls(
            [
                [int(x) if (x := string[j * 9 + i]) != '0' else None for i in range(9)]
                for j in range(9)
            ]
        )

    class Squares:
        """
            A representation of grid rows with two ways to get a set of 3x3 square values
            by i, j coordinates of one of its cells:
            > squares[i, j] - including the (i, j) cell,
            > squares(i, j) - excluding it.
        """
        def __init__(self, rows):
            self.rows = rows

        def __getitem__(self, ij):
            i, j = ij
            return set(self.rows[n][m] for n in range(i - i % 3, i - i % 3 + 3)
                       for m in range(j - j % 3, j - j % 3 + 3))

        def __call__(self, i, j):
            return set(self.rows[n][m] for n in range(i - i % 3, i - i % 3 + 3)
                       for m in range(j - j % 3, j - j % 3 + 3)
                       if (n, m) != (i, j))

    class Batch(list):
        """
            A representation of a grid row or column.
            > batch(i) - returns set of batch values except the one in position i.
        """
        def __call__(self, i):
            return set(self[j] for j in range(len(self)) if j != i)

    def __init__(self, seq=None):
        """
            Wraps sequence of lists of grid values.
        """
        if seq is None:
            seq = self.dummy()
        else:
            seq = [self.Batch(row) for row in seq]
        self.c = [self.Batch([seq[j][i] for j in range(9)]) for i in range(9)]
        self.s = self.Squares(self)
        super().__init__(seq)

    @classmethod
    def dummy(cls):
        """ Empty grid. """
        return cls([cls.Batch([None] * 9) for _ in range(9)])

    def alts(self, i, j) -> list:
        """ Sorted list of possible (according to sudoku rules) alternatives for the (i, j) cell """
        return sorted(self.ALL_ALTS_SET - self[i](j) - self.c[j](i) - self.s(i, j) | {0})

    def is_valid(self, *args):
        """
            is_valid(i, j) checks Sudoku rules for the (i, j) cell.
            is_valid()     checks all the cells.
        """
        if len(args) == 2:
            i, j = args
            return self[i][j] in self.alts(i, j)
        elif not args:
            return all(self.is_valid(i, j) for i in range(9) for j in range(9)
                       if self[i][j] is not None)
        else:
            raise Exception("0 or 2 args expected")

    def enumerate(self):
        return ((i, j, self[i][j]) for i in range(9) for j in range(9))

    @classmethod
    def bin_to_b64(cls, bin_code):
        """
            Encodes given string of binary code to string of symbols.
            Simply takes each next batch of 6 bits, converts to int
            and adds the symbol in corresponding position in B64 string:
            [000000][000001][000   ] <- adds zeros to match size of 6.
              is A    is B    is A   -> "ABA"
        """
        tail = len(bin_code) % 6
        if tail:
            bin_code += '0' * (6 - tail)
        return ''.join(cls.B64[int(bin_code[i * 6:(i + 1) * 6], 2)]
                       for i in range(len(bin_code) // 6))

    @classmethod
    def b64_to_bin(cls, string):
        """ Reverses bin_to_b64 """
        return ''.join(f'{cls.FB64[c]:06b}' for c in string)

    def encode_1(self, bin_prefix=""):
        """
            Encodes the grid by converting each number to up to 4 bit length binary code.
            Then applies bin_to_b64.
            Gives compact encoding for straight rows of blank cells.

            if grid.is_valid(), less bits needed for cell with less alternatives (grid.alts(i, j)),
            also more bit sequences stand for longer blank cell rows.

            The first bit in binary code stands for validation flag.

            Tip: Works well for grids with rare filled cells.
        """

        is_valid = self.is_valid()
        code = bin_prefix
        code += "1" if is_valid else "0"
        dub = self.dummy()
        z_alts = []
        for i, j, v in self.enumerate():

            alts = dub.alts(i, j) if is_valid else self.ALL_ALTS
            if not alts:
                raise Exception("Invalid grid for valid mode")

            v = 0 if v is None else v

            if v == 0:
                z_alts.append(alts)

            if z_alts:
                length = len(z_alts[0])
                cap = length.bit_length()
                unused = 2 ** cap - length
                if len(z_alts) - 1 == unused or v or i == j == 8:
                    code += f"{0 if len(z_alts) == 1 else (length + len(z_alts) - 2):0{cap}b}"
                    z_alts = []

            if v != 0:
                cap = len(alts).bit_length()
                code += f"{alts.index(v):0{cap}b}"

            dub[i][j] = self[i][j]

        return self.bin_to_b64(code)

    @classmethod
    def decode_1(cls, string=None, bin_code=None):
        """ The decoder for encode_1(). Returns list of list of values (or Nones) """
        if bin_code is None:
            bin_code = cls.b64_to_bin(string)
        grid = cls.dummy()
        is_valid, bin_code = int(bin_code[0]), bin_code[1:]
        zs = 0
        for i, j, _ in grid.enumerate():

            if zs:
                grid[i][j] = 0
                zs -= 1
                continue

            alts = grid.alts(i, j) if is_valid else cls.ALL_ALTS
            length = len(alts)
            cap = length.bit_length()

            pos, bin_code = int(bin_code[:cap], 2), bin_code[cap:]

            if pos < length:
                grid[i][j] = alts[pos]
            else:
                grid[i][j] = 0
                zs += pos - length + 1

        return [[grid[i][j] if grid[i][j] != 0 else None for j in range(9)] for i in range(9)]

    def encode_3(self, bin_prefix=""):
        """
            Encodes the grid by converting each next 3 digits ("0" stands for a blank cell)
            as a number to 10 bit length binary code. Then applies bin_to_b64.
            Gives compact encoding for straight rows of blank cells (up to 27 cells).

            Tip: Works well for well-filled grids (valid and invalid).
        """
        code = bin_prefix
        zs = 0
        num = ""
        for i, j, v in self.enumerate():

            v = 0 if v is None else v

            if zs:
                if v == 0 and zs < 27:
                    zs += 1
                    if not (i == j == 8):
                        continue
                code += f"{0 if zs == 3 else 996 + zs:010b}"
                zs = 0

            num += str(v)

            if len(num) == 3 or i == j == 8:
                if num == "000":
                    zs = 3
                else:
                    code += f"{int(f'{num:0<3}'):010b}"
                num = ""

        return self.bin_to_b64(code)

    @classmethod
    def decode_3(cls, string=None, *, bin_code=None):
        """ The decoder for encode_3(). Returns list of list of values (or Nones) """
        if bin_code is None:
            bin_code = cls.b64_to_bin(string)
        grid = cls.dummy()
        vs = iter(())
        for i, j, _ in grid.enumerate():

            if (v := next(vs, None)) is not None:
                grid[i][j] = v
                continue

            num, bin_code = int(bin_code[:10], 2), bin_code[10:]

            vs = (int(x) for x in f"{num:03d}") if num < 1000 else (0 for _ in range(num - 996))
            grid[i][j] = next(vs)

        return [[grid[i][j] if grid[i][j] != 0 else None for j in range(9)] for i in range(9)]

    def encode(self):
        """
            Encodes the grid by the method (encode_1 or encode_3) that gives most compact result.
            Adds distinguishing flag bits.
        """
        if self.is_valid():
            return self.encode_1()
        else:
            code_1 = self.encode_1(bin_prefix='0')
            code_3 = self.encode_3(bin_prefix='01')
            return min(code_1, code_3, key=len)

    @classmethod
    def decode(cls, string):
        """ The decoder for encode(). Returns list of list of values (or Nones) """
        bin_code = cls.b64_to_bin(string)
        if bin_code[0] == '1':
            return cls.decode_1(bin_code=bin_code)
        elif bin_code[:2] == '00':
            return cls.decode_1(bin_code=bin_code[1:])
        else:
            return cls.decode_3(bin_code=bin_code[2:])
