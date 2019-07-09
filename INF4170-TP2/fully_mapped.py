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
    def __init__(self, index, word_1, word_2, valid=False, word_3=None, word_4=None):
        self.increment = 0
        self.index = index
        self.valid = valid
        self.address = address
        self.word_1 = word_1
        self.word_2 = word_2
        self.word_3 = word_3
        self.word_4 = word_4

class Cache():
    def __init__(self, rows={}, number_of_blocks=4, block_size_in_words=2, cache_type=Cache_Types.DIRECT_MAPPED, write_through=True):
        self.central_memory = Central_Memory()
        self.rows = rows
        self.number_of_blocks = number_of_blocks
        self.block_size_in_words = block_size_in_words
        self.type = cache_type 
        self.number_of_index_bits = int(math.log(self.number_of_blocks, 2))
        self.block_mask_size = int(math.log(self.block_size_in_words * 4, 2))
        self.write_through = write_through

    def get_row_index_from_address(self, address):
        for row in self.rows:
            if row.address is not None and row.address == address:
                print('HIT')
                return row.index
        print('MISS')
        return -1

    def get_tag_from_address(self, address):
        return address >> (self.number_of_index_bits + self.block_mask_size)

    def get_block_address(self, address):
        for i in range(0, self.block_mask_size):
            address = set_bit(address, i, 0)
        return address

    def get_word_index(self, address):
        last_4_bits = address & 0xf # peut etre 0, 4, 8 ou 12

        if self.block_size_in_words == 4:
            if last_4_bits == 0:
                return 1
            elif last_4_bits == 4:
                return 2
            elif last_4_bits == 8:
                return 3
            elif last_4_bits == 12:
                return 4
        elif self.block_size_in_words == 2:
            if last_4_bits == 0 or last_4_bits == 8:
                return 1
            elif last_4_bits == 4 or last_4_bits == 12:
                return 2
        elif self.block_size_in_words == 1:
            return 1
    
        block_size = (16 // self.block_size_in_words) 
        result = last_4_bits // block_size
        return result

    def add_cache_row(cache_row):
        self.rows[cache_row.index] = cache_row

    def get_next_row(self, address):
        row_index  = self.get_row_index_from_address(address)
        if row_index_from_address != -1:
            return row_index

        current_max = -1
        for row in self.rows:
            if row is not None and not row.valid:
                return row.index
        for row in self.rows:
            if row.increment > current_max:
                current_max = row.increment
                row_index = row.index
        return row_index

    def look_for_address_in_rows(self, address):
        for row in self.rows:
            if row.address is not None and row.address == address:
                return row.index
        return -1

    def increment_all_rows(self, index):
        #remettre l'increment de la ligne utilisee  a 0
        pass

    def load_word(self, address):

        row_index = self.get_next_row(address)
        row = self.rows[row_index]

        if row.valid == 1 and row.tag == tag:
            print('HIT')
            return row
        else:
            print('MISS')
            if not self.write_through and row.dirty:
                self.write_back(row)
                row.dirty = True
            word_1 = self.central_memory.get_value_at_address(address)
            word_2 = self.central_memory.get_value_at_address(address + 4) #TODO change for actual number of words per block
            self.rows[index] = Cache_Row(index, 1, tag, word_1, word_2)
        row.valid = 1

        self.increment_all_rows()

    def write_back(self, block_address, row):
        tag = row.tag
        index = row.index
        block_address = 0x0
        if self.block_size_in_words == 2:
            self.central_memory.write_to_address(block_address, row.word_1)
            self.central_memory.write_to_address(block_address + 4, row.word_2)
        elif self.block_size_in_words == 4:
            self.central_memory.write_to_address(block_address, row.word_1)
            self.central_memory.write_to_address(block_address + 4, row.word_2)
            self.central_memory.write_to_address(block_address + 8, row.word_3)
            self.central_memory.write_to_address(block_address + 12, row.word_4)

    def build_back_address(self, tag, index):
        #address >> (self.number_of_index_bits + 2)
        new_tag = tag << (self.number_of_index_bits + 2)
        new_index = None
        

    def store_word(self, address, value):

        row_index = self.get_row_index_from_address(address)

        if self.write_through:
            row.dirty = True
        
        if row.valid != 1 or row.tag != tag:
            print('MISS')
            self.load_word(address)
        elif row.valid == 1 and row.tag == tag:
            print('HIT')
        word_index = self.get_word_index(address)
        if word_index == 1:
            self.rows[index].word_1 = value
            if self.write_through:
                self.central_memory.write_to_address(address,value)
        elif word_index == 2:
            self.rows[index].word_2 = value
            if self.write_through:
                self.central_memory.write_to_address(address, value)

        self.increment_all_rows()

    def print_cache_state(self):
        for index, value in self.rows.items():
            if (value.word_1 is not None and value.word_2 is not None and value.tag is not None):
                print('index {} tag {:08X} word 1 {:08X} word 2 {:08X}'.format(index, value.tag, value.word_1, value.word_2))     
            else:
                print('index {} tag None word 1 None word 2 None'.format(index)) 

            
                

class Central_Memory():
    def __init__(self):
        self.modified_words = {}
    def get_value_at_address(self, address):
        if address in self.modified_words:
            print('Returning a modified value : central memory at address {:08X} is {:08X}'.format(address, self.modified_words[address]))
            return self.modified_words[address]
        else:
            print('Returning central memory at address {:08X} is {:08X}'.format(address, self.get_default_value_at_address(address)))
            return self.get_default_value_at_address(address)

    def write_to_address(self, address, value):
        self.modified_words[address] = value

    def get_default_value_at_address(self, address):
        if address <= 0x0FFFFFFF:
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
        elif address <= 0x8FFFFFFF:
            return 0x88888888
        elif address <= 0x9FFFFFFF:
            return 0x99999999
        elif address <= 0xAFFFFFFF:
            return 0xAAAAAAAA
        elif address <= 0xBFFFFFFF:
            return 0xBBBBBBBB
        elif address <= 0xCFFFFFFF:
            return 0xCCCCCCCC
        elif address <= 0xDFFFFFFF:
            return 0xDDDDDDDD
        elif address <= 0xEFFFFFFF:
            return 0xEEEEEEEE
        elif address <= 0xFFFFFFFF:
            return 0xFFFFFFFF 

def set_bit(v, index, x):
  """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
  mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
  v &= ~mask          # Clear the bit indicated by the mask (if x is False)
  if x:
    v |= mask         # If x was True, set the bit indicated by the mask.
  return v            # Return the result, we're done.

def get_n_first_bits(number, n):
    binary_string = bin(number)
    binary_string_wo_0b = binary_string[2:]
    new_binary_string = binary_string_wo_0b[(len(binary_string_wo_0b) -2):len(binary_string_wo_0b)]
    return int(new_binary_string, 2)
    

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

rows = [
    Cache_Row(0, None, None),
    Cache_Row(1, None, None),
    Cache_Row(2, None, None),
    Cache_Row(3, None, None)
]
cache = Cache(rows, number_of_blocks=8, block_size_in_words = 2, cache_type=Cache_Types.FULLY_ASSOCIATIVE)


for operation in operations:
    
    if operation.operation == 'lw':
        print('{} {:08X}'.format(operation.operation, operation.address))
        cache.load_word(operation.address)
    elif operation.operation == 'sw':
        print('{} {:08X} {:08X}'.format(operation.operation, operation.address, operation.value))
        cache.store_word(operation.address, operation.value)
    cache.print_cache_state()
    print('----\n')


print('CACHE ROWS -----')
for index, value in cache.rows.items():
    print('index {} tag {:08X} word 1 {:08X} word 2 {:08X}'.format(index, value.tag, value.word_1, value.word_2))     

print('MODIFIED CENTRAL MEMORY ROWS ----')
for address,value in cache.central_memory.modified_words.items():
    print('address {:08X} value {:08X}'.format(address, value)) 