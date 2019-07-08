import math

class Cache_Types:
    DIRECT_MAPPED = 1
    FULLY_ASSOCIATIVE = 2

class Operation():
    def __init__(self, operation, address, value=None):
        self.operation = operation
        self.address = address
        self.value = value

class Cache_Row():
    def __init__(self, index, valid=0, tag=None, word_1=None, word_2=None):
        self.index = index
        self.valid = valid
        self.tag = tag
        self.word_1 = word_1
        self.word_2 = word_2

class Cache():
    def __init__(self, rows={}, number_of_blocks=4, block_size_in_words=2, type=Cache_Types.DIRECT_MAPPED, write_through=True):
        self.central_memory = Central_Memory()
        self.rows = rows
        self.number_of_blocks = number_of_blocks
        self.block_size_in_words = block_size_in_words
        self.type = type 
        self.number_of_index_bits = int(math.log(self.number_of_blocks, 2))
        self.block_mask_size = int(math.log(self.block_size_in_words, 2))

    def get_index_from_address(self, address):
        mask = (1 << (self.number_of_index_bits + 2)) - 1
        index = address & mask
        index = index >> 2
        print('calculated index:', bin(index))
        return index

    def get_tag_from_address(self, address):
        return address >> (self.number_of_index_bits + 2)

    def get_block_address(self, address):
        for i in range(0, self.block_mask_size):
            address = set_bit(address, i, 0)
        return address

    def get_word_index(self, address):
        last_4_bits = address & 0xf # peut etre 0, 4, 8 ou 12
        block_size = (16 // self.block_size_in_words) 
        result = last_4_bits // block_size
        return result + 1

    def add_cache_row(cache_row):
        self.rows[cache_row.index] = cache_row

    def load_word(self, address):

        index = self.get_index_from_address(address)
        tag = self.get_tag_from_address(address)
        print('calculated tag {:08X}'.format(tag))
        row = self.rows[index]
        if row.valid == 1 and row.tag == tag:
            print('HIT')
            return row
        else:
            print('MISS')
            word_1 = self.central_memory.get_value_at_address(address)
            word_2 = self.central_memory.get_value_at_address(address + 4)
            self.rows[index] = Cache_Row(index, 1, tag, word_1, word_2)

    def store_word(self, address, value):

        index = self.get_index_from_address(address)
        tag = self.get_tag_from_address
        row = self.rows[index]
        if row.valid != 1 or row.tag == tag:
            print('MISS')
            self.load_word(address)
        elif row.valid == 1 and row.tag == tag:
            print('HIT')
        word_index = self.get_word_index(address)
        if word_index == 1:
            self.rows[index].word_1 = address
            self.central_memory.write_to_address(address,value)
        elif word_index == 2:
            self.rows[index].word_2 == address
            self.central_memory.write_to_address(address, value)
                

class Central_Memory():
    def __init__(self):
        self.modified_words = {}
    def get_value_at_address(self, address):
        if address in self.modified_words:
            return self.modified_words[address]
        else:
            return self.get_default_value_at_address(address)

    def write_to_address(self, address, value):
        self.modified_words[address] = value

    def get_default_value_at_address(self, address):
        if address <= 0x0FFFFFF:
            return 0x00000000
        elif address <= 0x1FFFFFFF:
            return 0x11111111
        elif address <= 0x2FFFFFFF:
            return 0x22222222
        elif address <= 0x3FFFFFFF:
            return 0x33333333
        elif address <= 0x4FFFFFFF:
            return 0x44444444
        elif address <= 0x5FFFFFFF:
            return 0x55555555
        elif address <= 0x6FFFFFFF:
            return 0x66666666
        elif address <= 0x7FFFFFFF:
            return 0x77777777
        elif address <= 0x8FFFFFFFF:
            return 0x88888888
        elif address <= 0x9FFFFFFF:
            return 0x99999999
        elif address <= 0xAFFFFFFF:
            return 0xAAAAAAAA
        elif address <= 0xBFFFFFFF:
            return 0xBBBBBBBB
        elif address <= 0xCFFFFFFF:
            return 0xCCCCCCCC
        elif address <= 0xDFFFFFFFF:
            return 0xDDDDDDDD
        elif address <= 0xEFFFFFFFF:
            return 0xEEEEEEEE
        elif address <= 0xFFFFFFFFF:
            return 0xFFFFFFFF 

def set_bit(v, index, x):
  """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
  mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
  v &= ~mask          # Clear the bit indicated by the mask (if x is False)
  if x:
    v |= mask         # If x was True, set the bit indicated by the mask.
  return v            # Return the result, we're done.

#hex_value = 0x12345678
#mask = (1 << 5) - 1
#print(bin(hex_value))
#var = hex_value & mask
#print(bin(var))
#print(bin(var >> 2))
#print('{:08X}'.format(var))
        
#print('{:08X}'.format((0x12345678 >> 4) & 0xf)) 
#print('{:08X}'.format((0x12345678 >> 4))) 

#for i in range(0,16):
#    if (i != 0):
#        initial_value += 0x11111111
#    print('{:08X}'.format(initial_value))

operations = [
    Operation("lw", 0x1934EDD8),
    Operation("lw", 0x8944EFA4),
    Operation("sw", 0xAF70ADC8, 0x19887766),
    Operation("lw", 0x0F58CC20),
    Operation("lw", 0xBEADDEF0),
    Operation("sw", 0x246EAF94, 0xAF7F7FF1),
    Operation("lw", 0x19060908),
    Operation("sw", 0x876D247C, 0x3003FFFF),
    Operation("sw", 0x2823040C, 0x1010FFAF),
    Operation("lw", 0x33444444),
    Operation("lw", 0x21448808),
    Operation("sw", 0x0ACCBEDC, 0x0ADD0001),
    Operation("lw", 0x2144880C),
    Operation("sw", 0x0ACCBED8, 0xCAFECAFE),
    Operation("sw", 0x2144880C, 0xCCCCCCCC),
    Operation("lw", 0x33444444),
    Operation("lw", 0x2823040C)
]

rows = {
    0: Cache_Row(0),
    1: Cache_Row(1),
    2: Cache_Row(2),
    3: Cache_Row(3)
}
cache = Cache(rows)

for operation in operations:
    
    if operation.operation == 'lw':
        print('{} {:08X}'.format(operation.operation, operation.address))
        cache.load_word(operation.address)
    elif operation.operation == 'sw':
        print('{} {:08X} {:08X}'.format(operation.operation, operation.address, operation.value))
        cache.store_word(operation.address, operation.value)
    print('----\n')


print('CACHE ROWS -----')
for index, value in cache.rows.items():
    print('index {} tag {:08X} word 1 {:08X} word 2 {:08X}'.format(index, value.tag, value.word_1, value.word_2))     

print('MODIFIED CENTRAL MEMORY ROWS ----')
for address,value in cache.central_memory.modified_words.items():
    print('address {:08X} value {:08X}'.format(address, value)) 