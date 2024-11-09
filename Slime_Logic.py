class Slime(object):
    """
    模拟随机生成机制，提供种子初始化、整数范围校验和随机数生成。
   """

    def __init__(self):
        """初始化Slime对象，设置seed、x和z为None。"""
        self.seed = None
        self.x = None
        self.z = None

    @staticmethod
    def java_int(val):
        """将val限制在Java int范围内。"""
        limit = 2147483647
        if not (-1 * limit) - 1 <= val <= limit:
            val = (val + (limit + 1)) % (2 * (limit + 1)) - limit - 1
        return val

    @staticmethod
    def java_long(val):
        """将val限制在Java long范围内。"""
        limit = 9223372036854775807
        if not (-1 * limit) - 1 <= val <= limit:
            val = (val + (limit + 1)) % (2 * (limit + 1)) - limit - 1
        return val

    def rng_seed(self):
        """根据seed、x和z计算随机种子值。"""
        a = self.java_long(self.java_int((self.x ** 2) * 0x4c1906))
        b = self.java_long(self.java_int(self.x * 0x5ac0db))
        c = self.java_long(self.java_int(self.z ** 2) * 0x4307a7)
        d = self.java_long(self.java_int(self.z * 0x5f24f))
        return self.java_long(((self.seed + a + b + c + d) ^ 0x3ad8025f))

    def check(self, seed, x, z):
        """检查seed、x和z是否满足特定条件。"""
        self.seed = seed
        self.x = x
        self.z = z
        rng = self.rng_seed()
        obj = JavaRandom()
        obj.set_seed(rng)
        rtn = obj.next_int(10)
        return rtn == 0


class JavaRandom(object):
    """
   模拟Java随机数生成器，提供种子设置和随机数生成。
   """

    def __init__(self):
        """初始化JavaRandom对象，设置seed为None。"""
        self.seed = None

    def set_seed(self, seed):
        """设置随机数生成器的种子值。"""
        self.seed = (seed ^ 0x5deece66d) & ((1 << 48) - 1)

    def next(self, bits):
        """生成指定位数的随机数。"""
        if bits < 1:
            bits = 1
        elif bits > 32:
            bits = 32
        self.seed = (self.seed * 0x5deece66d + 0xb) & ((1 << 48) - 1)
        retval = self.seed >> (48 - bits)
        if retval & (1 << 31):
            retval -= (1 << 32)
        return retval

    def next_int(self, n):
        """生成一个在指定范围内的随机整数。"""
        if n > 1:
            if not (n & (n - 1)):
                return (n * self.next(31)) >> 31
            bits = self.next(31)
            val = bits % n
            while (bits - val + n - 1) < 0:
                bits = self.next(31)
                val = bits % n
            return val
