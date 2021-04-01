from pyalgo.basic_modules import default_functions, default_values
from pyalgo.basic_modules.algocryption_default_values import Simple_Columnar_Transposition_default_values
from . import functions_for_in_time_compile
from . import compiled_functions

import math
import time
import copy
import random
import hashlib

"""
sites used to create this encryption function:
---> I found some encryption algorithms from this site: https://www.thesslstore.com/blog/types-of-encryption-encryption-algorithms-how-to-choose-the-right-one/

-> I have found some information on RSA from those sites:
---> https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples

-> I have found some information on SHA256 from those sites:
---> https://www.youtube.com/watch?v=f9EbD6iY9zI&t=3s
---> https://qvault.io/cryptography/how-sha-2-works-step-by-step-sha-256/
"""





class pipeline:
    """this class can stack up a number of encryption methods at ones
    you can also add this function your own encryption class"""

    def __init__(self, algorithms: list, description: str = ""):
        ListType = default_values.ListType

        if not isinstance(algorithms, ListType):
            raise TypeError("'algorithms' should be a list type")
        self.algorithms = algorithms

        self.description = description

        for i in algorithms:
            self.check_if_algorithm_is_valid(i)

    def check_if_algorithm_is_valid(self, algorithm):
        if not ("encrypt" in dir(algorithm)):
            raise BrokenPipeError("all the functions should have an encrypt function")
        if not ("decrypt" in dir(algorithm)):
            raise BrokenPipeError("all the functions should have a decrypt function")
        if not ("save_key" in dir(algorithm)):
            raise BrokenPipeError("all the functions should have a save_key function")
        if not ("load_key" in dir(algorithm)):
            raise BrokenPipeError("all the functions should have a load_key function")
        if not ("clear_key" in dir(algorithm)):
            raise BrokenPipeError("all the functions should have a clear_key function")
        print(f"the class {algorithm} is valid")

    @property
    def keys(self):
        for i in range(len(self.algorithms)):
            if hasattr(i, "key"):
                print(i+1, "-->", self.algorithms[i].key)
            else:
                print(f"the cipher method number {i+1} has no key saved in it")
        return None

    def clear_keys(self):
        for i in self.algorithms:
            i.clear_key()

    def encrypt(self, msg_to_encrypt, key:dict = {1:None}):
        for i in key:
            if not key[i] == None:
                self.algorithms[i].key = key[i]

        for i in self.algorithms:
            msg_to_encrypt = i.encrypt(msg_to_encrypt)
            print(f"encrypted with {i} from {len(self.algorithms)} algorithms")

        return msg_to_encrypt

    def decrypt(self, msg_to_decrypt, key:dict = {1:None}):
        for i in key:
            if not key[i] == None:
                self.algorithms[i].key = key[i]

        for i in range(len(self.algorithms)):
            msg_to_decrypt = self.algorithms[-i - 1].decrypt(msg_to_decrypt)
            print(-i-1)

        return msg_to_decrypt







class hashing_algorithms:
    def __init__(self):  pass


    @staticmethod
    def sha256(msg):
        # // check if the msg entered is valid \\
        StringType = default_values.StringType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if not (isinstance(msg, StringType) or
                isinstance(msg, ByteType) or
                isinstance(msg, ByteArrayType)):
            raise TypeError("'msg' should be a String type, a Bytes type or a ByteArrayType")

        # // constants \\
        WORD_SIZE = 32
        MAX_WORDS = 64
        BLOCK_SIZE = 512

        a = 0
        b = 1
        c = 2
        d = 3
        e = 4
        f = 5
        g = 6
        h = 7

        K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
             0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
             0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
             0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
             0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
             0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
             0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
             0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2, ]

        FIRST_HASH_VLUES = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB,
                            0x5BE0CD19]

        initial_hash = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB,
                        0x5BE0CD19]

        # // transfer the constants into binary \\
        for i in range(len(K)):
            K[i] = str(bin(K[i]))[2:].zfill(32)
        for i in range(len(FIRST_HASH_VLUES)):
            FIRST_HASH_VLUES[i] = str(bin(FIRST_HASH_VLUES[i]))[2:].zfill(32)
        for i in range(len(initial_hash)):
            initial_hash[i] = str(bin(initial_hash[i]))[2:].zfill(32)

        # // initializing some basic operations \\
        def shift_right(bits, shiftNum):
            bits = ("0" * shiftNum) + bits
            return bits[:(len(bits)-shiftNum)]

        def rotate_right(bits, rotateNum):
            rotateNum = rotateNum % len(bits)
            if rotateNum == 0:
                return bits
            bits = bits[-rotateNum:] + bits
            return bits[:-rotateNum]

        def add(a, b):
            """
            this function takes 2 binary numbers add them together
            and then return the modulo 2^32 binary number
            """
            a = int(a, 2)
            b = int(b, 2)
            #result = (a+b)%(2**32)
            result = str(bin(a+b))[2:]
            return result[-32:].zfill(WORD_SIZE)

        # // initializing some functions \\
        def lower_sigma0(bits):
            x1 = int(rotate_right(bits, 7), 2)
            x2 = int(rotate_right(bits, 18), 2)
            x3 = int(shift_right(bits, 3), 2)

            return str(bin(x1 ^ x2 ^ x3))[2:].zfill(WORD_SIZE)


        def lower_sigma1(bits):
            x1 = int(rotate_right(bits, 17), 2)
            x2 = int(rotate_right(bits, 19), 2)
            x3 = int(shift_right(bits, 10), 2)

            return str(bin(x1 ^ x2 ^ x3))[2:].zfill(WORD_SIZE)


        def upper_sigma0(bits):
            x1 = int(rotate_right(bits, 2), 2)
            x2 = int(rotate_right(bits, 13), 2)
            x3 = int(rotate_right(bits, 22), 2)

            return str(bin(x1 ^ x2 ^ x3))[2:].zfill(WORD_SIZE)

        def upper_sigma1(bits):
            x1 = int(rotate_right(bits, 6), 2)
            x2 = int(rotate_right(bits, 11), 2)
            x3 = int(rotate_right(bits, 25), 2)

            return str(bin(x1 ^ x2 ^ x3))[2:].zfill(WORD_SIZE)

        def choice(x, y, z):
            result = ""
            for i in range(len(x)):
                if x[i] == "1":
                    result += y[i]
                elif x[i] == "0":
                    result += z[i]
            return result.zfill(WORD_SIZE)

        def majority(x, y, z):
            result = ""
            temp = None
            for i in range(len(x)):
                temp = int(x[i]) + int(y[i]) + int(z[i])
                if temp >= 2:
                    result += "1"
                else:
                    result += "0"
            return result.zfill(WORD_SIZE)


        # // transferring the msg to bytes if it is a string \\
        if isinstance(msg, StringType):
            msg = msg.encode()


        # // transferring to binary according to the ascci table \\
        msg = default_functions.values_to_single_number.bytes_to_single_num(msg)
        str_msg = str(bin(msg))[3:]
        msg = str(bin(msg))[3:]

        if len(msg) > int("1"*64, 2):
            raise ValueError(f"the input msg should be less than {int('1'*64, 2)}")

        ##############for i in range(len(str_msg)):
        ##############    if i % 8 == 0:
        ##############        print(" ", end="")
        ##############    print(str_msg[i], end="")
        ##############print("")

        #// adds a single '1' at the end of the binary string \\
        str_msg += "1"
        ##############for i in range(len(str_msg)):
        ##############    if i % 8 == 0:
        ##############        print(" ", end="")
        ##############    print(str_msg[i], end="")
        ##############print("")

        #// padding with zeros \\
        number_of_chunks = math.ceil(len(str_msg) / BLOCK_SIZE)
        if ((number_of_chunks * BLOCK_SIZE) - 64) < len(str_msg):
            number_of_chunks += 1
        num_of_zeros_padding = (number_of_chunks*BLOCK_SIZE)-64-len(str_msg)
        ##############print("num_of_zeros_padding =", num_of_zeros_padding)
        str_msg = str_msg+"0"*num_of_zeros_padding
        ##############print("padded msg =", str_msg)

        #// adding the last 64 bits that tells the input size in binary \\
        msg_size_final_64_padding = str(bin(len(msg)))[2:].zfill(64)
        ##############print("msg_size_final_64_padding =", msg_size_final_64_padding)
        str_msg += msg_size_final_64_padding
        ##############print("str_msg =", str_msg)
        ##############print("number_of_chunks =", number_of_chunks)

        ##############print(msg_size_final_64_padding)

        # // creating the message schedule for each block\\
        ##############print("\n")
        for i in range(int(number_of_chunks)):

            FIRST_HASH_VLUES = copy.deepcopy(initial_hash)

            message_schedule = []
            # we first append the first 16 words of 32 bits
            for j in range(int(BLOCK_SIZE / WORD_SIZE)):
                message_schedule.append(str_msg[(j * WORD_SIZE) + i*BLOCK_SIZE : ((j+1) * WORD_SIZE) + i*BLOCK_SIZE])


            # we complete the 'message_schedule' to be in a fixed length of 64 elements
            word_to_add = int(BLOCK_SIZE / WORD_SIZE)
            for j in range(int(MAX_WORDS - (BLOCK_SIZE / WORD_SIZE))):
                result = add(lower_sigma1(message_schedule[word_to_add-2]), message_schedule[word_to_add-7])
                result = add(result, lower_sigma0(message_schedule[word_to_add-15]))
                result = add(result, message_schedule[word_to_add-16])
                message_schedule.append(result)
                word_to_add += 1

                #print(j + int(BLOCK_SIZE / WORD_SIZE), result)

            ##############print("\n\n")
            ##############
            ##############for j in range(len(message_schedule)):
            ##############    print(i+1, str(j).zfill(2), message_schedule[j])


            # // compression \\

            for j in range(len(message_schedule)):
                T1 = add(upper_sigma1(initial_hash[e]), choice(initial_hash[e], initial_hash[f], initial_hash[g]))
                T1 = add(T1, initial_hash[h])
                T1 = add(T1, K[j])
                T1 = add(T1, message_schedule[j])

                T2 = add(upper_sigma0(initial_hash[a]), majority(initial_hash[a], initial_hash[b], initial_hash[c]))

                #print("")
                #print("T1 =", T1)
                #print("T2 =", T2)

                for k in range(len(initial_hash)):
                    initial_hash[len(initial_hash) - k - 1] = initial_hash[len(initial_hash) - k - 2]
                initial_hash[a] = add(T1, T2)
                initial_hash[e] = add(initial_hash[e], T1)

            ##############for k in range(len(initial_hash)):
            ##############    print(initial_hash[k], initial_hash[k] == FIRST_HASH_VLUES[k])
            ##############input(":")

            # // Final Hash Value \\
            ##############print("\n")
            for k in range(len(initial_hash)):
                initial_hash[k] = add(initial_hash[k], FIRST_HASH_VLUES[k])
                #initial_hash[k] = str(hex(int(initial_hash[k], 2)))[2:].zfill(8)

        for k in range(len(initial_hash)):
            initial_hash[k] = str(hex(int(initial_hash[k], 2)))[2:].zfill(8)

        return ''.join(initial_hash)
        #return hashlib.sha256(msg).digest()






class XOR_Cipher:
    def __init__(self, key, description: str = ""):
        self.check_if_key_is_valid(key)

        self.key = key

        self.description = description

    def encrypt(self, msg_to_encrypt, key=None):
        StringType = default_values.StringType
        ListType = default_values.ListType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        # // check if the input type is in the correct type: string, list, byte or bytearray \\
        if not (isinstance(msg_to_encrypt, StringType) or isinstance(msg_to_encrypt, ListType)
                or isinstance(msg_to_encrypt, ByteType) or isinstance(msg_to_encrypt, ByteArrayType)):
            raise TypeError("'bytes' needs to be: string, list, bytes or btrearray")

        if key == None:
            key = self.key
        else:
            self.check_if_key_is_valid(key)

        # // this sections transform the input type into bytearray \\
        if isinstance(msg_to_encrypt, StringType):  # transfer string to bytearray
            msg_to_encrypt = bytearray([ord(i) for i in msg_to_encrypt])
        if isinstance(msg_to_encrypt, ListType):
            msg_to_encrypt = bytearray([ord(i) for i in msg_to_encrypt])
        if isinstance(msg_to_encrypt, ByteType):  # transfer to bytes
            msg_to_encrypt = bytearray(msg_to_encrypt)

        print(type(msg_to_encrypt))

        for i, value in enumerate(msg_to_encrypt):
            if isinstance(key, default_values.IntType):
                msg_to_encrypt[i] = key ^ value
            else:
                msg_to_encrypt[i] = key[i % len(key)] ^ value

            if (i+1) % 5000000 == 0:
                print(f"successfully encrypted {i+1} \\ {len(msg_to_encrypt)}")

        return msg_to_encrypt

    def decrypt(self, msg_to_decrypt, key=None):
        StringType = default_values.StringType
        ListType = default_values.ListType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if not (isinstance(msg_to_decrypt, StringType) or isinstance(msg_to_decrypt, ListType)
                or isinstance(msg_to_decrypt, ByteType) or isinstance(msg_to_decrypt, ByteArrayType)):
            raise TypeError("'bytes' needs to be byte type or bytearray type")

        if key == None:
            key = self.key
        else:
            self.check_if_key_is_valid(key)

        if isinstance(msg_to_decrypt, StringType):  # transfer string to bytearray
            msg_to_decrypt = bytearray([ord(i) for i in msg_to_decrypt])
        if isinstance(msg_to_decrypt, ListType):
            msg_to_decrypt = bytearray([ord(i) for i in msg_to_decrypt])
        if isinstance(msg_to_decrypt, ByteType):
            msg_to_decrypt = bytearray(msg_to_decrypt)

        for i, value in enumerate(msg_to_decrypt):
            if isinstance(key, default_values.IntType):
                msg_to_decrypt[i] = key ^ value
            else:
                msg_to_decrypt[i] = key[i % len(key)] ^ value

            if (i + 1) % 5000000 == 0:
                print(f"successfully encrypted {i + 1} \\ {len(msg_to_decrypt)}")

        return msg_to_decrypt

    def save_key(self, key_to_save=None, dir=None, filename="xor.key"):
        if key_to_save == None:  key_to_save = self.key

        self.check_if_key_is_valid(key_to_save)

        if not dir == None:
            dir += "\\" + str(filename)
        else:
            dir = str(filename)

        key_to_save_str = ""
        if isinstance(key_to_save, default_values.IntType):
            key_to_save_str = str(key_to_save)
        else:
            for i in key_to_save:
                key_to_save_str += str(i) + "\n"

        print(dir)
        file = open(dir, "w")
        file.write(key_to_save_str)
        file.close()

    def load_key(self, dir):
        try:
            with open(dir, "r") as file:
                content = file.readlines()
        except:
            content = dir.split()

        key = []

        for i in content:
            key.append(int(i))
        if len(key) == 1:
            key = key[0]

        self.key = key

    def clear_key(self):
        del self.key

    @staticmethod
    def check_if_key_is_valid(key):
        IntType, ListType = default_values.IntType, default_values.ListType

        if not (isinstance(key, IntType) or isinstance(key, ListType)):  # checks if key is an int or a list
            raise TypeError("'key' can be an int type or a list type")

        if isinstance(key, IntType):  # checks if the key is in the range of 0 -> 255 and key is an int
            if key >= 256:
                raise ValueError("'key' cannot be bigger than 255")
            if key < 0:
                raise ValueError("'key' cannot be smaller than 0")
        elif isinstance(key, ListType):  # checks if the key is in the range of 0 -> 255 and key is a list
            for i in key:
                if i >= 256:
                    raise ValueError("any number in 'key' cannot be bigger than 255")

                if i < 0:
                    raise ValueError("any number in 'key' cannot be smaller than 0")




class RSA():
    #you can see the following websites for more information:
    # -> https://cryptobook.nakov.com/asymmetric-key-ciphers/rsa-encrypt-decrypt-examples


    def __init__(self, p, q, e, description: str = ""):
        self.p = p
        self.q = q
        self.e = e

        self.Phi = ((self.p - 1) * (self.q - 1))
        self.N = p * q  # compute N

        self.description = description

        self.check_if_key_is_valid()



    def check_if_key_is_valid(self, e=None, p=None, q=None, d=None, N=None, Phi=None):
        if e == None:  e = self.e
        if p == None:  p = self.p
        if q == None:  q = self.q
        if N == None:  N = self.N
        if Phi == None:  Phi = self.Phi

        if not (p*q == N):  raise ValueError("'N' should be p * q (N = p*q)")
        if not (((p-1) * (q-1)) == Phi):  raise ValueError("'Phi' should be as follows (Phi = ((p - 1) * (q - 1)))")
        if e >= self.Phi:  raise ValueError(f"'e' cannot be bigger than phi({self.Phi} = (p-1) * (q-1))")

        #if not (default_functions.gcd(e, self.Phi) == 1):
        if (Phi % e == 0):
            raise ValueError("'e' should be co-prime with φ(p, q)")

        #if not default_functions.prime_check(p):  raise ValueError("'p' should be a prime number")
        #if not default_functions.prime_check(q):  raise ValueError("'q' should be a prime number")
        #if not default_functions.prime_check(e):  raise ValueError("'e' should be a prime number")

        if not hasattr(self, "d"):
            self.find_private_key()

        if d == None:  d = self.d
        if not ((d * e) % Phi == 1):  raise ValueError("'d' should have the following rule: (e*d) % Phi == 1")



    def find_private_key(self):
        self.d = default_functions.eea(self.e, self.Phi)[0]
        if self.d < 0:
            self.d += self.Phi

    def create_signature(self, msg_to_sign, d=None, N=None, apply_hashing=True, hashing_algorithm=None):
        if N == None: n = self.N
        if d == None: d = self.d

        StringType = default_values.StringType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if not (isinstance(msg_to_sign, StringType) or
                isinstance(msg_to_sign, ByteType) or
                isinstance(msg_to_sign, ByteArrayType)):
            raise TypeError("'msg_to_sign' need to be a string type, a bytes type or an bytearray type")

        if not isinstance(apply_hashing, default_values.BoolType):
            raise TypeError("'apply_hashing' needs to by a bool type (True or False)")

        if apply_hashing:
            if hashing_algorithm == None:
                msg_to_sign = hashing_algorithms.sha256(msg_to_sign)
            else:
                msg_to_sign = hashing_algorithm(msg_to_sign)

        return self.encrypt(msg_to_sign, N=N, e=d)

    def validate_signature(self, signature, msg, N=None, e=None, apply_hashing=True, hashing_algorithm=None):
        if N == None: n = self.N
        if e == None: e = self.e

        StringType = default_values.StringType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if not (isinstance(signature, StringType) or
                isinstance(signature, ByteType) or
                isinstance(signature, ByteArrayType)):
            raise TypeError("'signature' need to be a string type, a bytes type or an bytearray type")

        if not (isinstance(msg, StringType) or
                isinstance(msg, ByteType) or
                isinstance(msg, ByteArrayType)):
            raise TypeError("'msg' need to be a string type, a bytes type or an bytearray type")

        if apply_hashing:
            if hashing_algorithm == None:
                msg = hashing_algorithms.sha256(msg)
            else:
                msg = hashing_algorithm(msg)

        if isinstance(msg, StringType):
            return msg.encode() == self.decrypt(signature, N=N, d=e)
        return bytes(msg) == self.decrypt(signature, N=N, d=e)





    def encrypt(self, msg_to_encrypt, N = None, e = None, type_to_return="ByteArray"):

        StringType = default_values.StringType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if N == None:  N = self.N
        if e == None:  e = self.e

        if not (isinstance(msg_to_encrypt, StringType) or
                isinstance(msg_to_encrypt, ByteType) or
                isinstance(msg_to_encrypt, ByteArrayType)):
            raise TypeError("'msg_to_encrypt(M)' must be a string, a bytes or a bytearray")

        is_chunk_jump_correct = False
        chunk_jump = 1

        #// checking the jump value for faster encryption \\
        while not is_chunk_jump_correct:
            try:
                if chunk_jump == len(msg_to_encrypt):
                    chunk_jump -= 1
                    is_chunk_jump_correct = True

                encrypted_text = bytes()
                #(math.ceil(len(msg_to_encrypt) / chunk_jump))
                pre_encrypted_chunk = msg_to_encrypt[0 * chunk_jump:1 * chunk_jump]
                self.basic_encrypt(pre_encrypted_chunk)
                chunk_jump += 1
                print(f"chunk_jump is now {chunk_jump}")
            except:
                chunk_jump -= 1
                #print(f"chunk_jump is {chunk_jump}")
                is_chunk_jump_correct = True

        print("chunk jump =", chunk_jump)
        for i in range(math.ceil(len(msg_to_encrypt) / chunk_jump)):
            pre_encrypted_chunk = msg_to_encrypt[i * chunk_jump:(i + 1) * chunk_jump]

            encrypted_chunk = self.basic_encrypt(pre_encrypted_chunk)
            encrypted_chunk = int.from_bytes(encrypted_chunk, 'little')
            encrypted_chunk = str(bin(encrypted_chunk))[2:]
            encrypted_chunk = int(encrypted_chunk)
            encrypted_chunk = default_functions._8chunk_to_7chunk(encrypted_chunk)

            encrypted_text += encrypted_chunk

            print(f"chunk {i+1} \\ {math.ceil(len(msg_to_encrypt) / chunk_jump)} has been encrypted successfully")

        encrypted_text += bytes([random.randint(128, 255)])
        return encrypted_text


    def decrypt(self, msg_to_decrypt, N = None, d = None):
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if not hasattr(self, "d"):
            self.find_private_key()

        if N == None:  N = self.N
        if d == None:  d = self.d

        if not (isinstance(msg_to_decrypt, ByteType) or
                isinstance(msg_to_decrypt, ByteArrayType)):
            raise TypeError("'msg_to_decrypt(C)' should be a Bytes or a bytearray,   this function do not get a String")

        stop_read_number = True
        decrypted_text = bytearray()
        pre_decrypted_chunk = bytes()
        chunk_number = 1
        for i in range(len(msg_to_decrypt)):
            if msg_to_decrypt[i] >= 128:
                stop_read_number = True
            if not stop_read_number:
                pre_decrypted_chunk += bytes([msg_to_decrypt[i]])
            if stop_read_number:
                if not list(pre_decrypted_chunk) == []:
                    decrypted_chunk = default_functions._7chunk_to_8chunk(pre_decrypted_chunk)
                    num_of_bytes = math.floor(math.log(decrypted_chunk, 2) / 8 + 1)
                    decrypted_chunk = decrypted_chunk.to_bytes(num_of_bytes, "little")
                    decrypted_chunk = self.basic_decrypt(decrypted_chunk)
                    decrypted_text += decrypted_chunk
                    print(f"chunk {chunk_number} has been decrypted successfully")
                    chunk_number += 1

                pre_decrypted_chunk = bytes()
                stop_read_number = False
        return decrypted_text



    def basic_encrypt(self, msg_to_encrypt, N = None, e = None, type_to_return="ByteArray"):

        StringType = default_values.StringType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if N == None:  N = self.N
        if e == None:  e = self.e

        if not (isinstance(msg_to_encrypt, StringType) or
                isinstance(msg_to_encrypt, ByteType) or
                isinstance(msg_to_encrypt, ByteArrayType)):
            raise TypeError("'msg_to_encrypt(M)' must be a string, a bytes or a bytearray")

        # transfer into bytes
        if isinstance(msg_to_encrypt, StringType):
            msg_to_encrypt = [ord(char) for char in msg_to_encrypt]
        if isinstance(msg_to_encrypt, ByteArrayType):
            msg_to_encrypt = bytes(msg_to_encrypt)

        msg_to_encrypt = default_functions.values_to_single_number.to_whole_number(bytes(msg_to_encrypt))

        if msg_to_encrypt >= N:
            raise ValueError(f"the plain text is too long {msg_to_encrypt} > {N}")

        msg_to_encrypt = pow(msg_to_encrypt, e, N)

        #return pow(msg_to_encrypt, e, N)

        if type_to_return == "ByteArray":
            num_of_bytes = math.floor(math.log(msg_to_encrypt, 2) / 8 + 1)
            encrypted_msg = msg_to_encrypt.to_bytes(num_of_bytes, "little")
            return encrypted_msg

    def basic_decrypt(self, msg_to_decrypt, key: list =[None, None]):
        N, d = key[0], key[1]
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if not hasattr(self, "d"):
            self.find_private_key()


        if N == None:  N = self.N
        if d == None:  d = self.d

        if not (isinstance(msg_to_decrypt, ByteType) or
                isinstance(msg_to_decrypt, ByteArrayType)):
            raise TypeError("'msg_to_decrypt(C)' should be a Bytes or a bytearray,   this function do not get a String")



        msg_to_decrypt = int.from_bytes(msg_to_decrypt, "little")

        msg_to_decrypt = pow(msg_to_decrypt, d, N)

        M = default_functions.values_to_single_number.from_whole_num(msg_to_decrypt, type_to_return="Bytes")

        return bytearray(M)

    @property
    def private_key(self):
        return {"d": self.d, "e": self.e}

    @property
    def public_key(self):
        return {"N": self.N, "e": self.e}

    @property
    def key(self):
        if not hasattr(self, "d"):
            self.find_private_key()

        try:
            return {"N": self.N, "d": self.d, "e": self.e, "p":self.p, "q":self.q}
        except AttributeError:
            raise ValueError("there is no key saved in this class")

    @key.setter
    def key(self, key):
        for i in key:
            if i == "N":
                self.N = key["N"]
            elif i == "e":
                self.e = key["e"]
            elif i == "d":
                self.d = key["d"]
            elif i == "p":
                self.p = key["p"]
            elif i == "q":
                self.q = key["q"]
            elif i == "Phi":
                self.Phi = key["Phi"]
            else:
                raise ValueError("the dictionary keys should be 'N', 'e', 'd', 'p' or 'q'")

        self.check_if_key_is_valid()

    def save_key(self, key=None, dir=None, filename="rsa.key"):
        dictionaryType = default_values.DictionatyType
        if (not (key == None)):
            if not isinstance(key, dictionaryType):
                print("'key_to_save' needs to be a dictionary type")
        else:
            key = self.key

        if dir == None:
            dir = str(filename)
        else:
            dir += "\\" + str(filename)

        content = ""
        for i in key:
            content += "{}{} \n".format(i, self.key[i])

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")

    def save_public_key(self, dir=None, filename="rsa.pubkey"):

        dir += "\\" + str(filename)

        content = ""
        for i in self.public_key:
            content += "{}{} \n".format(i, self.key[i])

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")

    def save_private_key(self, dir=None, filename="rsa.privkey"):

        dir += "\\" + str(filename)

        content = ""
        for i in self.private_key:
            content += "{}{} \n".format(i, self.key[i])

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")

    def load_key(self, dir):
        try:
            with open(dir) as file:
                content = file.readlines()
        except:
            content = dir.split()

        for i in content:
            if i[0] == "e":
                self.e = int(i[1:])
            elif i[0] == "d":
                self.d = int(i[1:])
            elif i[0] == "N":
                self.N = int(i[1:])
            elif i[0] == "p":
                self.p = int(i[1:])
            elif i[0] == "q":
                self.q = int(i[1:])
            else:
                raise ValueError(f"the key is corrupted, '{i[0]}' is not a value for RSA")

        print("loaded")

    def clear_key(self):
        del self.e
        del self.d
        del self.N

    def print_public_key(self):
        print(f"N = {self.N}")
        print(f"e = {self.e}")

    def print_private_key(self):
        print(f"N = {self.N}")
        print(f"d = {self.d}")

    def print_key(self):
        print(f"N = {self.N}")
        print(f"e = {self.e}")
        print(f"d = {self.d}")





class Simple_Columnar_Transposition:
    # I used the following sites to help me build this function:
    # http://www.crypto-it.net/eng/simple/columnar-transposition.html
    # https: // www.boxentriq.com / code - breaking / columnar - transposition - cipher


    chars_values = {"a": 1,
                    "b": 2,
                    "c": 3,
                    "d": 4,
                    "e": 5,
                    "f": 6,
                    "g": 7,
                    "h": 8,
                    "i": 9,
                    "j": 10,
                    "k": 11,
                    "l": 12,
                    "m": 13,
                    "n": 14,
                    "o": 15,
                    "p": 16,
                    "q": 17,
                    "r": 18,
                    "s": 19,
                    "t": 20,
                    "u": 21,
                    "v": 22,
                    "w": 23,
                    "x": 24,
                    "y": 25,
                    "z": 26}


    def __init__(self, key=5, chunk_size:int = 25):
        """
        key is the key used to encrypt the msg
        the length of the key will determine the number of columns
        if the key is a number then the columns would be read from left from right

        if the key is a list then each chunk should be encrypted be the corresponding key


        the chunk_size is the number of letters that will be entered to the table
        the chunk_size is an independent hyperparameter to the key size

        if chunk_size is set to 'All' then the program will encrypt all of the plain-text like one chunk
        if you want that the program will encrypt all of the plain-text as one chunk you can set 'chunk_size' to 'All' or -1
        """

        self.key = key
        self.chunk_size = chunk_size

        self.check_if_key_is_valid()

    def check_if_key_is_valid(self, key=None, chunk_size=None):
        if key == None:  key = self.key
        if chunk_size == None:  chunk_size = self.chunk_size

        StringType = default_values.StringType
        IntType = default_values.IntType
        ListType = default_values.ListType

        if not (isinstance(key, IntType) or isinstance(key, StringType) or isinstance(key, ListType)):
            raise ValueError("'key' should be an int, n string or a List")
        if not isinstance(chunk_size, IntType) or isinstance(chunk_size, StringType):
            raise ValueError("'chunk_size' should be an Int or a String")

        if isinstance(key, IntType) and key <= 0:
            raise ValueError("'key' needs to be bigger that zero(0)")
        if isinstance(chunk_size, IntType):
            if (chunk_size < -1):
                raise ValueError("'chunk_size' needs to be bigger that zero(0) or -1")

        if isinstance(chunk_size, StringType) and (not (chunk_size == "All")):
            raise ValueError("if 'chunk_size' is a string type then it should be set to 'All'")


    def encrypt(self, msg_to_encrypt, key=None, chunk_size=None, type_to_return="ByteArray"):
        if not type_to_return in Simple_Columnar_Transposition_default_values.encrypt_type_to_return_default_values:
            raise ValueError(f"'type_to_return' can be from the following list: {Simple_Columnar_Transposition_default_values.encrypt_type_to_return_default_values}")

        if key == None:  key = self.key
        if chunk_size == None:  chunk_size = self.chunk_size

        StringType = default_values.StringType
        ListType = default_values.ListType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if (chunk_size > len(msg_to_encrypt)) or (chunk_size == -1) or (chunk_size == "All"):
            chunk_size = len(msg_to_encrypt)

        self.check_if_key_is_valid(key=key, chunk_size=chunk_size)


        if not (isinstance(msg_to_encrypt, StringType) or
                isinstance(msg_to_encrypt, ListType) or
                isinstance(msg_to_encrypt, ByteType) or
                isinstance(msg_to_encrypt, ByteArrayType)):
            raise TypeError("'msg_to_encrypt' should be a String, a List, a Bytes or a Bytearray")

        # transfer msg_to_encrypt to a List that separate the elements of msg_to_encrypt
        if isinstance(msg_to_encrypt, StringType):
            msg_to_encrypt = [i for i in msg_to_encrypt]
        if isinstance(msg_to_encrypt, ByteType):
            msg_to_encrypt = list(bytearray(msg_to_encrypt))
        if isinstance(msg_to_encrypt, ByteArrayType):
            msg_to_encrypt = list(msg_to_encrypt)


        chunks_per_msg_to_encrypt = len(msg_to_encrypt)//chunk_size + (len(msg_to_encrypt)%chunk_size != 0)

        encrypted_list = []
        for chunk_number in range(chunks_per_msg_to_encrypt):
            chunk = msg_to_encrypt[chunk_number*chunk_size:(chunk_number+1)*chunk_size]
            if isinstance(key, default_values.IntType):
                chunk = self.encrypt_chunk(chunk, key)
            if isinstance(key, StringType):
                chunk = self.encrypt_chunk(chunk, key)
            if isinstance(key, ListType):
                chunk = self.encrypt_chunk(chunk, key[chunk_number%len(key)])

            encrypted_list.append(chunk)

            print("chunk_number =", chunk_number + 1, "  ", chunk)

        encrypted_list = default_functions.to_single_list(encrypted_list)


        if type_to_return == "String":
            return (''.join(encrypted_list))
        if type_to_return == "List":
            return encrypted_list
        if type_to_return == "Bytes":
            if isinstance(encrypted_list[0], StringType):
                a = ''.join(encrypted_list)
                return bytes(a, 'utf-8')
            if isinstance(encrypted_list[0], default_values.IntType):
                return bytes(encrypted_list)
        if type_to_return == "ByteArray":
            if isinstance(encrypted_list[0], StringType):
                a = ''.join(encrypted_list)
                return bytearray(a, 'utf-8')
            if isinstance(encrypted_list[0], default_values.IntType):
                return bytearray(encrypted_list)





    def decrypt(self, msg_to_decrypt, key=None, chunk_size=None, type_to_return="ByteArray"):

        if not type_to_return in Simple_Columnar_Transposition_default_values.encrypt_type_to_return_default_values:
            raise ValueError(f"'type_to_return' can be from the following list: {Simple_Columnar_Transposition_default_values.encrypt_type_to_return_default_values}")

        if key == None:  key = self.key
        if chunk_size == None:  chunk_size = self.chunk_size

        StringType = default_values.StringType
        ListType = default_values.ListType
        ByteType = default_values.ByteType
        ByteArrayType = default_values.ByteArrayType

        if (chunk_size > len(msg_to_decrypt)) or (chunk_size == -1) or (chunk_size == "All"):
            chunk_size = len(msg_to_decrypt)

        self.check_if_key_is_valid(key=key, chunk_size=chunk_size)

        if not (isinstance(msg_to_decrypt, StringType) or
                isinstance(msg_to_decrypt, ListType) or
                isinstance(msg_to_decrypt, ByteType) or
                isinstance(msg_to_decrypt, ByteArrayType)):
            raise TypeError("'msg_to_encrypt' should be a String, a List, a Bytes or a Bytearray")

        # transfer msg_to_decrypt to a List that separate the elements of msg_to_encrypt
        if isinstance(msg_to_decrypt, StringType):
            msg_to_decrypt = [i for i in msg_to_decrypt]
        if isinstance(msg_to_decrypt, ByteType):
            msg_to_decrypt = list(bytearray(msg_to_decrypt))
        if isinstance(msg_to_decrypt, ByteArrayType):
            msg_to_decrypt = list(msg_to_decrypt)

        chunks_per_msg_to_decrypt = len(msg_to_decrypt) // chunk_size + (len(msg_to_decrypt) % chunk_size != 0)

        decrypted_list = []
        for chunk_number in range(chunks_per_msg_to_decrypt):
            chunk = msg_to_decrypt[chunk_number * chunk_size:(chunk_number + 1) * chunk_size]
            if isinstance(key, default_values.IntType):
                chunk = self.decrypt_chunk(chunk, key)
            if isinstance(key, StringType):
                chunk = self.decrypt_chunk(chunk, key)
            if isinstance(key, ListType):
                chunk = self.decrypt_chunk(chunk, key[chunk_number % len(key)])

            decrypted_list.append(chunk)

            #print("chunk_number =", chunk_number + 1, "  ", chunk)

        decrypted_list = default_functions.to_single_list(decrypted_list)

        if type_to_return == "String":
            return (''.join(decrypted_list))
        if type_to_return == "List":
            return decrypted_list
        if type_to_return == "Bytes":
            if isinstance(decrypted_list[0], StringType):
                a = ''.join(decrypted_list)
                return bytes(a, 'utf-8')
            if isinstance(decrypted_list[0], default_values.IntType):
                return bytes(decrypted_list)
        if type_to_return == "ByteArray":
            if isinstance(decrypted_list[0], StringType):
                a = ''.join(decrypted_list)
                return bytearray(a, 'utf-8')
            if isinstance(decrypted_list[0], default_values.IntType):
                return bytearray(decrypted_list)

        #return ''.join(default_functions.to_single_list(decrypted_list))

    def encrypt_chunk(self, chunk, key=None):
        """
        :param chunk: this should be a list of elements to encrypt
        :param key: this is the key used to encrypt the chunk. if the key is not provided, then the
                    program will encrypt the chunk with the key saved in the class
        :return: this function should retrun a list of encrypted data
        """

        if key == None: key = self.key
        if isinstance(key, default_values.ListType):
            key = key[0]


        if isinstance(key, default_values.IntType):
            if key > len(chunk):
                key = len(chunk)
        if isinstance(key, default_values.StringType):
            if len(key) > len(chunk):
                key = key[:len(chunk)]
        if isinstance(key, default_values.ListType):
            if len(key) > len(chunk):
                key = key[:len(chunk)]

        StringType = default_values.StringType
        chunk_size = len(chunk)


        if (isinstance(key, StringType)):
            key_length = len(key)
        if isinstance(key, default_values.IntType):
            key_length = copy.deepcopy(key)

        #rows_per_chunk = chunk_size // key_length + (chunk_size % key_length != 0)
        rows_per_chunk = math.ceil(chunk_size / key_length)


        pre_encrypted_list = []
        for row_number in range(rows_per_chunk):
            pre_encrypted_list.append(chunk[row_number * key_length:(row_number + 1) * key_length])

            if not len(pre_encrypted_list) == 1:
                encrypted_list = list(map(list, zip(*pre_encrypted_list[:-1])))
                for j in range(len(encrypted_list)):
                    try:
                        encrypted_list[j].append(pre_encrypted_list[-1][j])
                    except: pass
            else:
                #encrypted_list = copy.deepcopy(pre_encrypted_list)
                encrypted_list = [i for i in pre_encrypted_list[0]]

        #print(encrypted_list)
        if isinstance(key, StringType):
            key_order = []
            for i in key:
                key_order.append(self.chars_values[i]-1)

            final_encrypted_list = []
            for i in range(len(key_order)):
                final_encrypted_list.append(encrypted_list[key_order.index(min(key_order))])
                key_order[key_order.index(min(key_order))] = (max(key_order)+1)
        else:
            final_encrypted_list = encrypted_list.copy()

        return default_functions.to_single_list(final_encrypted_list)

    def decrypt_chunk(self, chunk, key=None):
        """
                :param chunk: this should be a list of elements to decrypt
                :param key: this is the key used to encrypt the chunk. if the key is not provided, then the
                            program will encrypt the chunk with the key saved in the class
                :return: this function should retrun a list of decrypted data
                """

        if key == None: key = self.key
        if isinstance(key, default_values.ListType):
            key = key[0]

        if isinstance(key, default_values.IntType):
            if key > len(chunk):
                key = len(chunk)
        if isinstance(key, default_values.StringType):
            if len(key) > len(chunk):
                key = key[:len(chunk)]

        StringType = default_values.StringType
        chunk_size = len(chunk)

        if (isinstance(key, StringType)):
            key_length = len(key)
        if isinstance(key, default_values.IntType):
            key_length = copy.deepcopy(key)

        rows_per_chunk = math.ceil(chunk_size/key_length)

        # creating a blank matrix
        matrix = []
        total = 1
        for row in range(rows_per_chunk):
            matrix.append([])
            for column in range(key_length):
                if total <= chunk_size:
                    matrix[row].append('')
                total += 1


        if isinstance(key, StringType):
            #creatin the key order
            key_order = []
            for i in key:
                key_order.append(self.chars_values[i])
            key_order_pos = copy.deepcopy(key_order)
            pos = 1
            for i in key_order:
                key_order_pos[key_order.index(min(key_order))] = pos
                key_order[key_order.index(min(key_order))] = max(key_order)+1
                pos += 1
            key_order = copy.deepcopy(key_order_pos)


        pos = 0
        for i in range(key_length):
            if isinstance(key, StringType):
                column = key_order.index(i+1)
            else:
                column = i

            row = 0

            while (row < len(matrix)) and (len(matrix[row]) > column):
                matrix[row][column] = (chunk[pos])
                row += 1
                pos += 1
        return default_functions.to_single_list(matrix)

    def clear_key(self):
        del self.key
        del self.chunk_size

    def save_key(self, key=[None, None], dir=None, filename='sct.key'):
        ListType = default_values.ListType

        if not isinstance(key, ListType):
            raise TypeError("'key' needs to be a list as following: [key, chunk_size]")

        key, chunk_size = key[0], key[1]
        if key == None:  key = self.key
        if chunk_size == None:  chunk_size = self.chunk_size

        self.check_if_key_is_valid(key=key, chunk_size=chunk_size)

        if dir == None:
            dir = str(filename)
        else:
            dir += "\\" + str(filename)

        content = ""

        content += "[chunk_size]"
        if isinstance(chunk_size, ListType):
            for i in chunk_size:
                content += "\n"
                content += f"{i}"
        else:
            content += "\n"
            content += f"{chunk_size}"

        content += "\n"
        content += "[key]"
        for i in key:
            content += "\n"
            content += f"{i}"

        file = open(dir, "w")
        file.write(content)
        file.close()

        print("saved")


    def load_key(self, dir):
        try:
            with open(dir) as file:
                content = file.readlines()
        except:
            content = dir.split()


        chunk_size = None
        key = []

        chunk_phase = False
        key_phase = False
        for i in content:
            a = i[:-1]
            b = not i[0] == "["
            0==0
            if i[:-1] == "[chunk_size]":
                key_phase = False
                chunk_phase = True
            if i[:-1] == "[key]":
                key_phase = True
                chunk_phase = False

            if not i[0] == "[":
                if chunk_phase:
                    chunk_size = int(i)
                elif key_phase:
                    try:
                        key.append(int(i))
                    except:
                        if i[-1] == "\n":
                            key.append(i[:-1])
                        else:
                            key.append(i)

        if len(key) == 1:
            key = key[0]

        self.key = key
        self.chunk_size = chunk_size

    def clear_key(self):
        del self.key
        del self.chunk_size