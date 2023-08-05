from decimal import Decimal  # 解决浮点数精度问题

_author = 'Xinre<ancdngding@qq.com>'
_version = '0.0.3'


def add(nums, *args) -> float or int:
    """
    计算多个数字的和
    例如：
    >>> add(12, 12, 12)
    36
    >>> add([12, 11, 10])
    33
    """
    result = 0
    if type(nums) != list:
        for i in args:
            nums += i
        return nums
    else:
        for i in nums:
            result += i
        return result


def multiply(nums, *args) -> float or int:
    """
    计算多个数字的乘积
    """
    for i in args:
        nums *= i
    return nums


def div(nums, *args) -> float or int:
    """
    计算数字之间的商
    """
    for i in args:
        nums /= i
    return nums


def power(n, ex) -> float:
    """
    计算数字的多次幂
    例如:
    >>> power(2, 2)
    4.0
    >>> power(1.1, 2)
    1.21
    >>> power(-2, 3)
    -8.0
    """
    result = Decimal('1.0')
    for i in range(ex):
        result *= Decimal(str(n))
    return float(result)


def average(nums, *args) -> float:
    """
    计算平均数
    例如:
    >>> average(1, 3, 5)
    3.0
    >>> average([1, 2, 3])
    2.0
    """
    if type(nums) == list:
        return add(nums) / len(nums)
    else:
        return add(list(tuple([nums]) + args)) / (len(args) + 1)


def median(nums: list) -> float or int:
    """
    求一组数据中的中位数
    例如:
    >>> median([1, 2, 5, 3, 4])
    3
    >>> median([1, 2, 3, 4])
    2.5
    """
    nums.sort()
    if len(nums) % 2 == 0:
        return (nums[int(len(nums) / 2) - 1] + nums[int(len(nums) / 2)]) / 2
    else:
        return nums[int(len(nums) / 2)]


def mid(text: str, first: int, lenth: int) -> str:
    """
    截取字符串的指定范围的内容
    起始位置first为需要截取内容的起始位置（不同于下标）, 截取长度lenth为整数
    例如:
    >>> mid("Mingrui", 5, 3)
    'rui'
    """
    if type(text) == str and type(first) == int and type(lenth) == int:
        return text[first - 1:first - 1 + lenth]
    # 简单的异常处理
    elif type(text) != str:
        raise TypeError("The agrument 'text' should be string.")
    elif type(first) != int:
        raise TypeError("The agrument 'first' should be interger.")
    elif type(lenth) != int:
        raise TypeError("The agrument 'lenth' should be interger.")


def mode(nums: list):
    num_count = {}
    for i in nums:
        if i not in num_count:
            num_count[i] = 1
        else:
            num_count[i] += 1
    print(num_count)


def delta(nums: list) -> float:
    """
    求方差
    例如:
    >>> delta([1, 2, 3, 4, 5])
    2.0
    """
    l = []
    for i in nums:
        l.append(power(i - average(nums), 2))
    return add(l) / len(nums)


def wac(nums: dict) -> float:
    """
    求加权平均数
    例如:
    >>> wac({10: 1, 20: 2, 30: 1})
    20.0
    """
    n1, n2 = Decimal(), Decimal()
    for k, v in nums.items():
        n1 += k * v
        n2 += v
    return float(n1 / n2)


def XE(source: str, m=2) -> str:
    """
    全称: XEncryption
    用于加密文本(Unicode)
    示例:
    >>> XE("XEncryption")
    '.`9ob;z:8vu9'
    >>> XE("China")
    'c2v5rb'
    """
    
    def _(num: int) -> str:
        res = ""
        if num >= 64: res += '1'; num -= 64
        else: res += '0'
        if num >= 32: res += '1'; num -= 32
        else: res += '0'
        if num >= 16: res += '1'; num -= 16
        else: res += '0'
        if num >= 8: res += '1'; num -= 8
        else: res += '0'
        if num >= 4: res += '1'; num -= 4
        else: res += '0'
        if num >= 2: res += '1'; num -= 2
        else: res += '0'
        if num == 1: return res + '1'
        else: return res + '0'
    k = lambda x: str(sum([int(x[i]) * 2 ** (len(x) - 1 - i) for i in range(len(x))]))
        
    l = [_(ord(i)) for i in source]
    
    l_ = [i[-1] + i[0:6] if i[-1] != '0' else 'x' + i[0:6] for i in l]
    res = "".join([chr(int(k(str(i)))) if 'x' not in i else chr(int(k(str(i)[1:]))) for i in l_])
    r = [chr(ord(res[i]) - m) if i % 2 == 1 else
                chr(ord(res[i]) + m) for i in range(len(res))]
    r.insert(len(r) ** 2 % 9, chr(96 + m))
    
    return "".join(r)
        

def XD(source: str) -> str:
    """
    全称: XDecryption
    用于解密XE生成的文本
    示例:
    >>> XE(".`9ob;z:8vu9")
    'XEncryption'
    >>> XE("c2v5rb")
    'China'
    """
    
    def _(num: int) -> str:
        res = ""
        if num >= 64: res += '1'; num -= 64
        else: pass
        if num >= 32: res += '1'; num -= 32
        else: res += '0'
        if num >= 16: res += '1'; num -= 16
        else: res += '0'
        if num >= 8: res += '1'; num -= 8
        else: res += '0'
        if num >= 4: res += '1'; num -= 4
        else: res += '0'
        if num >= 2: res += '1'; num -= 2
        else: res += '0'
        if num == 1: return res + '1'
        else: return res + '0'
    k = lambda x: str(sum([int(x[i]) * 2 ** (len(x) - 1 - i) for i in range(len(x))]))

    s = list(source)
    try:
        m = ord(s.pop((len(s) - 1) ** 2 % 9)) - 96
    except:
        m = ord(s.pop(-1)) - 96
    l = [chr(ord(s[i]) + m) if i % 2 == 1 else
         chr(ord(s[i]) - m) for i in range(len(s))]
    l = [_(ord(i)) for i in l]
    l = [i[1:7] + i[0] if len(i) == 7 else
         i + '0' for i in l]
    return "".join([chr(int(k(i))) for i in l])
