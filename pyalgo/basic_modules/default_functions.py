from . import default_values
import copy
import math
import random



def to_single_list(List):  # // needs to be optimized \\
                           # // may use a regression \\

    """
    This function takes a list and moving out the
    sub lists until there is no sub lists left

    example:
    before: [1, 2, [[1, 4], 2], 0]
    after: [1, 2, 1, 4, 2, 0]
    """

    List = copy.deepcopy(List)  # deep copy the list to not make a reference

    dumbList = []
    ListType = type(dumbList)

    if not isinstance(List, ListType): raise TypeError("You need to enter a list")

    is_single_list = True

    while is_single_list:
        for i in range(len(List)):
            if isinstance(List[i], ListType):

                is_single_list = False

                length = len(List[i])
                transferList = List[i]

                del List[i]

                for j in range(length):
                    List.insert(i, transferList[-1-j])

        is_single_list = not is_single_list

    return List


def print_list_arguments(List, Tag="-->", print_the_msg=True, return_msg=True):

    """
    This function takes a list and prints its arguments separated with the Tag first

    example:

    option number {the number of the argument}:  {Tag} {The arguments}

    :param List: this should be a list
    :param Tag: This should be a string
    :return: this function doesn't returns anything
    """

    msg = ""

    # // check that the type of the inputs are valid to this function \\
    if not isinstance(List, default_values.ListType):
        raise TypeError("'List' should be a list type")
    if not isinstance(Tag, default_values.StringType):
        raise TypeError("'Tag' should be a String type")


    for i in range(len(List)):
        if print_the_msg:
            print("option number {0}:  {1} {2}".format(i+1, Tag, List[i]))

        msg += "option number {0}:  {1} {2}".format(i+1, Tag, List[i])
        msg += "\n"

    if return_msg: return msg


def gcd(a, b):

    # this functions uses recursion and the euclidean algorithm to find the gcd of a, b

    """
    This function returns the greatest common divisor
    """

    if a < 0:  raise ValueError("'a' should be greater than 0")
    if b < 0:  raise ValueError("'b' should be greater than 0")

    if b == 0:
        return a

    return gcd(b, a % b)

greatest_common_divisor = gcd
euclidean_algorithm = gcd


def extended_euclidean_algorithm(a, b):
    """
    the euclidean algorithm find the gcd(greatest common divisor) of 'a' and 'b' by represent the problem to xa + yb
    the extended euclidean algorithm says the xa + yb = gcd(a, b)
    the extended euclidean algorithm helps to find 'x' and 'y' such that 'x' and 'y' are whole numbers
    """

    # /// uses s(i) = s(i-2) - q(i)*s(i-1) \\\
    # /// uses t(i) = t(i-2) - q(i)*t(i-1) \\\
    priv2_s, priv2_t = 1, 0
    priv_s, priv_t = 0, 1

    s, t = None, None

    q, r = a // b, a % b

    while b != 0:
        q, r = a // b, a % b
        a, b = b, a % b

        s, t = priv2_s - (q * priv_s), priv2_t - (q * priv_t)

        priv2_s, priv2_t = copy.deepcopy(priv_s), copy.deepcopy(priv_t)
        priv_s, priv_t = copy.deepcopy(s), copy.deepcopy(t)

    return (priv2_s, priv2_t)

eea = extended_euclidean_algorithm



def prime_check(n):
    """Primality test using 6k+-1 optimization."""

    if n <= 3:
        return n > 1

    if ((n%2 == 0) or (n%3 == 0)):
        return False

    i = 5
    while (i ** 2) <= n:
        if ((n%i == 0) or (n%(i+2) == 0)):
            return False

        i += 6
    return True




def _8chunk_to_7chunk(binNum) -> bytes:
    number_of_bytes_added = 0
    if  (len(str(binNum))/7 == len(str(binNum))//7):
        number_of_bytes_added = 0
    else:
        number_of_bytes_added = 7 - (len(str(binNum))%7)

    #print("number_of_bytes_added =", number_of_bytes_added)

    binNum = ("0" * number_of_bytes_added) + str(binNum)

    binList = []
    for i in range(len(binNum) // 7):
        binList.append("0" + binNum[i*7:(i+1)*7])
        #print(binNum[i*7:(i+1)*7])

    binList.insert(0, bin(random.randint(128, 255))[2:])
    #binList.insert(0, bin(131)[2:])

    #print("binList =", binList)
    binNum = bytes([int(i, 2) for i in binList])
    #print("binNum =", binNum)
    return binNum


def _7chunk_to_8chunk(Bytes:bytes) -> int:
    binList = list(Bytes)  # transfer bytes to list of numbers
    binList = [str(bin(i))[2:].zfill(8) for i in binList]  # transfer the number in the list to binary

    binList = [i[1:] for i in binList]  # remove the first bit in each binary number

    binNum = ''.join(binList)

    binNum = int(binNum, 2)

    return binNum


class values_to_single_number:

    """
    -this function takes a String, a List, a ByteArray or a bytes and return a single number that represent this group of values
    -this function is reversible
    -each set of values have a distinguish number

    - this function takes the info and convert it into bytes
    then the function takes those bytes and represent them as a binary number
    and finally the function takes the binary number and convert it into a decimal number
    """

    def __init__(self):
        pass

    @classmethod
    def to_whole_number(cls, msg):

        StringType = default_values.StringType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if not (isinstance(msg, StringType) or
                isinstance(msg, ByteType) or
                isinstance(msg, ByteArrayType)):
            raise TypeError("you can only convert a String, a Bytes or a ByteArray into a whole number")



        # convert 'msg' into bytes
        if isinstance(msg, StringType):
            msg = msg.encode()
        if isinstance(msg, ByteType):
            pass
        if isinstance(msg, ByteArrayType):
            msg = bytes(msg)


        msg = list(msg)
        msg = cls.list_of_numbers_to_bytes(msg)
        msg = cls.bytes_to_single_num(msg)
        return (msg)

    @classmethod
    def list_of_numbers_to_bytes(cls, List):

        b = bytes()
        for i in List:
            if not i == 0:
                num_of_bytes = math.floor(math.log(i, 2) / 8 + 1)
            else:
                num_of_bytes = 1
            b += (i.to_bytes(num_of_bytes, 'little'))

        return (b)

    @classmethod
    def bytes_to_single_num(cls, N):

        N = list(N)
        binary_nums_str = ""
        for i in N:
            # print("binary_nums_str =", binary_nums_str)
            # print("i =", i, "   bin(i) =", bin(i))
            # binary_nums_str += str(bin(i))[2:].ljust(8, '0')
            binary_nums_str += str(bin(i))[2:].zfill(8)

        binary_nums_str = "1" + binary_nums_str
        return int(binary_nums_str, 2)




    """
    this section converts a number into a string or any other given type
    """
    @classmethod
    def from_whole_num(cls, num, type_to_return="String"):
        num = cls.nums_to_list_of_bytes_values(num)
        #print(num)
        num = bytes(num)
        num = cls.bytes_to_nums(num)
        #print(num)
        if type_to_return == "String":
            num = bytes(num).decode()
        elif type_to_return == "Bytes":
            bytes(num)
        elif type_to_return == "ByteArray":
            bytearray(num)
        return num

    @staticmethod
    def nums_to_list_of_bytes_values(N):
        N = str(bin(N))
        N = N[2:]

        # print(N)
        # input(":")

        N = str(N)
        N = N[1:]
        nums_in_N = int(len(N) / 8)
        b = []

        for i in range(nums_in_N):
            # print(i, N, N[i*8:(i+1)*8], int(N[i*8:(i+1)*8], 2))
            b.append(int(N[i * 8:(i + 1) * 8], 2))

        return (b)

    @staticmethod
    def bytes_to_nums(Bytes):
        numbers = []
        for i in range(len(Bytes)):
            # print(Bytes[i])
            numbers.append(bytes())
            numbers[-1] += bytes([Bytes[i]])

        #print("\n\n\n\n")
        return [int.from_bytes(i, 'little') for i in numbers]