class ivec2:
    __slots__ = ("x", "y")

    def __init__(self, x=0, y=None):
        if y is None:
            # ivec2(ivec2) 또는 ivec2((x, y)) 허용
            if isinstance(x, ivec2):
                self.x, self.y = x.x, x.y
            elif isinstance(x, (tuple, list)) and len(x) == 2:
                self.x, self.y = x
            else:
                self.x = self.y = x
        else:
            self.x = x
            self.y = y

    def __repr__(self):
        return f"ivec2({self.x}, {self.y})"

    # ───────── 연산자 ─────────
    def __eq__(self, other):
        ox, oy = self._unpack(other)
        return (self.x, self.y) == (ox, oy)

    def __add__(self, other):
        ox, oy = self._unpack(other)
        return ivec2(self.x + ox, self.y + oy)

    def __sub__(self, other):
        ox, oy = self._unpack(other)
        return ivec2(self.x - ox, self.y - oy)

    def __mul__(self, other):
        ox, oy = self._unpack(other)
        return ivec2(self.x * ox, self.y * oy)

    def __mod__(self, other):
        ox, oy = self._unpack(other)
        return ivec2(self.x % ox, self.y % oy)

    def __gt__(self, other):
        ox, oy = self._unpack(other)
        return ivec2(self.x > ox, self.y > oy)
    def __ge__(self, other):
        ox, oy = self._unpack(other)
        return ivec2(self.x >= ox, self.y >= oy)
    def __lt__(self, other):
        ox, oy = self._unpack(other)
        return ivec2(self.x < ox, self.y < oy)
    def __le__(self, other):
        ox, oy = self._unpack(other)
        return ivec2(self.x <= ox, self.y <= oy)

    # ───────── 내부 헬퍼 ─────────
    def _unpack(self, other):
        """ivec2, tuple, list, int 모두 지원"""
        if isinstance(other, ivec2):
            return other.x, other.y
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            return other[0], other[1]
        elif isinstance(other, (int, float)):
            return other, other
        else:
            raise TypeError(f"Unsupported operand type: {type(other)}")

    # ───────── 시퀀스 인터페이스 ─────────
    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, i):
        if i == 0: return self.x
        elif i == 1: return self.y
        raise IndexError("ivec2 index out of range")

    def __len__(self): return 2

    # ───────── 인덱스 변환 ─────────
    def toIndex(self) -> int:
        return int(self.x + self.y * 8)

    def __index__(self): return self.toIndex()
    def __int__(self): return self.toIndex()

    # ───────── 정적 반복 ─────────
    @staticmethod
    def range(width, height):
        for y in range(height):
            for x in range(width):
                yield ivec2(x, y)
