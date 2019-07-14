import math

class Operation():
    def __init__(self, operation, address, value=None):
        self.operation = operation
        self.address = address
        self.value = value

class Cache_Row():
    def __init__(self, index, word_1, word_2, valid=False, word_3=None, word_4=None):
        self.increment = 0
        self.dirty = False
        self.index = index
        self.valid = valid
        self.tag = None
        self.word_1 = word_1
        self.word_2 = word_2
        self.word_3 = word_3
        self.word_4 = word_4

class Cache_Set():
    def __init__(self, rows = {}):
        self.rows = rows

    def look_for_tag_in_rows(self, tag):
        for index, row in self.rows.items():
            if row.tag is not None and row.tag == tag:
                print('HIT')
                return True, row
        print('MISS')

        return False, -1

    def increment_all_rows(self):
        #remettre l'increment de la ligne utilisee  a 0
        for index, row in self.rows.items():
            if row.valid:
                row.increment += 1

    def get_next_row(self):
        current_max = -1
        next_row = None
        #find unoccupied row
        for index, row in self.rows.items():
            if row is not None and not row.valid:
                return row

        #find oldest row in occupied rows
        for row_index, row in self.rows.items():
            if row.increment > current_max:
                current_max = row.increment
                next_row = row
        return next_row

class Cache():
    def __init__(self, rows={}, number_of_blocks=4, block_size_in_words=2, number_of_sets=2, write_through=True):
        self.central_memory = Central_Memory()
        self.number_of_blocks = number_of_blocks
        self.block_size_in_words = block_size_in_words
        self.number_of_sets = number_of_sets
        self.sets = {}

        #self.sets[0] = Cache_Set({})
        #self.sets[1] = Cache_Set({})
        #for set_index, set in self.sets.items():
        #    set.rows[0] = Cache_Row(0, None, None, False, None, None)
        #    set.rows[1] = Cache_Row(1, None, None, False, None, None)
        #    set.rows[2] = Cache_Row(2, None, None, False, None, None)
        #    set.rows[3] = Cache_Row(3, None, None, False, None, None)

        for i in range(self.number_of_sets):
            #current_set = Cache_Set()
            self.sets[i] = Cache_Set({})
            #current_set  = self.sets[i]
            for j in range((self.number_of_blocks // self.number_of_sets)):
                self.sets[i].rows[j] = Cache_Row(j, None, None, False, None, None)

        self.number_of_index_bits = int(math.log(self.number_of_sets, 2))
        self.block_mask_size = int(math.log(self.block_size_in_words * 4, 2))
        self.write_through = write_through

    def get_row_index_from_tag(self, tag):
        for row in self.rows:
            if row.tag is not None and row.tag == tag:
                print('HIT')
                return row.index
        print('MISS')
        return -1

    def get_tag_from_address(self, address):
        binary_string = get_binary_string(address)
        tag = binary_string[:(32 - self.block_mask_size - self.number_of_index_bits)]
        return tag

    def get_block_address(self, address):
        for i in range(0, self.block_mask_size):
            address = set_bit(address, i, 0)
        return address

    def get_set_index(self, block_address):
        binary_string = get_binary_string(block_address)
        binary_string = binary_string[:-self.block_mask_size]
        binary_string = binary_string[-self.number_of_index_bits:]
        return int(binary_string,2)

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
        if row_index != -1:
            return True, row_index

        current_max = -1
        
        #find unoccupied row
        for row in self.rows:
            if row is not None and not row.valid:
                return False, row.index

        #find oldest row in occupied rows
        for row in self.rows:
            if row.increment > current_max:
                current_max = row.increment
                row_index = row.index

        return False, row_index

    def load_word(self, address):

        block_address = self.get_block_address(address)
        tag = self.get_tag_from_address(address)
        set_index = self.get_set_index(block_address)
        set = self.sets[set_index]
        hit, row = set.look_for_tag_in_rows(tag)
        if hit:
            row.increment = 0
            set.increment_all_rows()
            return
        else:
            row = set.get_next_row()


        if not self.write_through and row.dirty:
            print('Writing dirty row to central memory')
            block_address = self.build_back_address(row.tag, set_index)
            self.write_back(block_address, row)
            row.dirty = False

        if (self.block_size_in_words == 4):
            word_1 = self.central_memory.get_value_at_address(block_address)
            word_2 = self.central_memory.get_value_at_address(block_address + 4) #TODO change for actual number of words per block
            word_3 = self.central_memory.get_value_at_address(block_address + 8) #TODO change for actual number of words per block
            word_4 = self.central_memory.get_value_at_address(block_address + 12) #TODO change for actual number of words per block

            row.word_1 = word_1
            row.word_2 = word_2
            row.word_3 = word_3
            row.word_4 = word_4

        elif self.block_size_in_words == 2:
            word_1 = self.central_memory.get_value_at_address(block_address)
            word_2 = self.central_memory.get_value_at_address(block_address + 4) #TODO change for actual number of words per block

            row.word_1 = word_1
            row.word_2 = word_2

        elif self.block_size_in_words == 1:
            word_1 = self.central_memory.get_value_at_address(block_address)
            row.word_1 = word_1

        row.tag = tag

        #self.rows[index] = Cache_Row(index, 1, tag, word_1, word_2)

        row.valid = 1
        row.increment = 0
        set.increment_all_rows()

    def write_back(self, block_address, row):
        
        if self.block_size_in_words == 1:
            self.central_memory.write_to_address(block_address, row.word_1)
            
        elif self.block_size_in_words == 2:
            self.central_memory.write_to_address(block_address, row.word_1)
            self.central_memory.write_to_address(block_address + 4, row.word_2)
        elif self.block_size_in_words == 4:
            self.central_memory.write_to_address(block_address, row.word_1)
            self.central_memory.write_to_address(block_address + 4, row.word_2)
            self.central_memory.write_to_address(block_address + 8, row.word_3)
            self.central_memory.write_to_address(block_address + 12, row.word_4)

    def build_back_address(self, tag, index, index_in_set=0):
        block_address = tag + get_binary_string(index, self.number_of_index_bits)
        for i in range(self.block_mask_size):
            block_address += '0'
        print('built back address {:0X}'.format(int(block_address,2)))
        return int(block_address, 2)
        

    def store_word(self, address, value):
        block_address = self.get_block_address(address)
        tag = self.get_tag_from_address(address)
        index = self.get_set_index(block_address)
        set = self.sets[index]
        hit, row = set.look_for_tag_in_rows(tag)
        if not hit:
            self.load_word(address)
            hit, row = set.look_for_tag_in_rows(tag)
        else:
            row.increment=0
            set.increment_all_rows()
        word_index = self.get_word_index(address)


        if word_index == 1:
            row.word_1 = value
        elif word_index == 2:
            row.word_2 = value     
        elif word_index == 3:
            row.word_3 = value
        elif word_index == 4:
            row.word_4 = value
 
        if not self.write_through:
            row.dirty = True
        else:
            self.central_memory.write_to_address(address, value)

    def print_tag(self, tag):
        binary_string = tag
        number_of_bits = len(binary_string)
        number_of_bits_to_remove = number_of_bits % 4

        hex_bits = binary_string[:(number_of_bits - number_of_bits_to_remove)]
        last_bits = binary_string[number_of_bits - number_of_bits_to_remove:]
        result = ' tag {:08X} ( {} )'.format(int(hex_bits,2), last_bits)
        print(result, end = '')
        return result

    def print_words(self, row, number_of_words):
        if (number_of_words == 4):
            print(' word 1 {:08X} word 2 {:08X} word 3 {:08X} word 4 {:08X}'.format(row.word_1, row.word_2, row.word_3, row.word_4))     
        elif number_of_words == 2:
            print(' word 1 {:08X} word 2 {:08X} '.format(row.word_1, row.word_2))     
        elif number_of_words == 1:
            print(' word 1 {:08X}'.format(row.word_1))
            
            

    def print_cache_state(self):
        for set_index, set in self.sets.items():
            for row_index, row in set.rows.items():
                if (row.word_1 is not None  and row.tag is not None):
                    print('set index {} row index'.format(set_index, row_index), end = '')
                    self.print_tag(row.tag)
                    self.print_words(row, self.block_size_in_words)
                else:
                    print('increment {} valid {} dirty {} address None word 1 None word 2 None word 3 None word 4 None'.format(row.increment, row.valid, row.dirty)) 

            
                

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

def get_binary_format_string(number_of_bits):
    return '{:0' + str(number_of_bits) + 'b}'

def get_binary_string(number, number_of_bits = 32):
    binary_string = get_binary_format_string(number_of_bits).format(number)
    return binary_string

def get_n_first_bits(number, n):
    new_binary_string = get_n_first_bit_string(number, n)
    return int(new_binary_string, 2)

def get_n_first_bit_string(number, n):
    binary_string_wo_0b = get_binary_string(number)
    new_binary_string = binary_string_wo_0b[(len(binary_string_wo_0b) -2):len(binary_string_wo_0b)]
    return new_binary_string
    

#operations = [
#    Operation("lw", 0x1934EDD8),
#    Operation("lw", 0x8944EFA4),
#    Operation("sw", 0xAF70ADC8, 0x19887766),
#    Operation("lw", 0x0F58CC20),
#    Operation("lw", 0xBEADDEF0),
#    Operation("sw", 0x246EAF94, 0xAF7F7FF1),
#    Operation("lw", 0x19060908),
#    Operation("sw", 0x876D247C, 0x3003FFFF),
#    Operation("sw", 0x2823040C, 0x1010FFAF),
#    Operation("lw", 0x33444444),
#    Operation("lw", 0x21448808),
#    Operation("sw", 0x0ACCBEDC, 0x0ADD0001),
#    Operation("lw", 0x2144880C),
#    Operation("sw", 0x0ACCBED8, 0xCAFECAFE),
#    Operation("sw", 0x2144880C, 0xCCCCCCCC),
#    Operation("lw", 0x33444444),
#    Operation("lw", 0x2823040C)
#]

operations = [
    Operation("lw", 0x09448DDC),
    Operation("lw", 0x9934FF04 ),
    Operation("sw", 0xFF90ACC8, 0x99887766),
    Operation("lw", 0xFF88CC00 ),
    Operation("lw", 0xDEADBEF0 ),
    Operation("sw", 0x348EEF54, 0xFFFFFFF1 ),
    Operation("lw", 0x09090908 ),
    Operation("sw", 0x8761230C, 0x0003FFFF ),
    Operation("sw", 0x8883090C, 0x0010FFFF ),
    Operation("lw", 0x44444444 ),
    Operation("lw", 0x11448800 ),
    Operation("sw", 0xAACCEEDC, 0xAADD0000
)
]


#rows = [
#    Cache_Row(0, None, None),
#    Cache_Row(1, None, None),
#    Cache_Row(2, None, None),
#    Cache_Row(3, None, None),
#    Cache_Row(4, None, None),
#    Cache_Row(5, None, None),
#    Cache_Row(6, None, None),
#    Cache_Row(7, None, None),
#]

#rows = [
#    Cache_Row(0, None, None),
#    Cache_Row(1, None, None),
#    Cache_Row(2, None, None),
#    Cache_Row(3, None, None)
#]

#cache = Cache(number_of_blocks=8, block_size_in_words = 4, number_of_sets = 2, write_through = True)
cache = Cache(number_of_blocks=8, block_size_in_words = 1, number_of_sets = 4, write_through = False)


for operation in operations:
    
    if operation.operation == 'lw':
        print('{} {:08X}'.format(operation.operation, operation.address))
        cache.load_word(operation.address)
    elif operation.operation == 'sw':
        print('{} {:08X} {:08X}'.format(operation.operation, operation.address, operation.value))
        cache.store_word(operation.address, operation.value)
    cache.print_cache_state()
    print('----\n')


#print('CACHE ROWS -----')
#for row in cache.rows:
#    print('valid {} tag {:08X} word 1 {:08X} word 2 {:08X}'.format(row.valid, row.address, row.word_1, row.word_2))     

print('MODIFIED CENTRAL MEMORY ROWS ----')
for address,value in cache.central_memory.modified_words.items():
    print('address {:08X} value {:08X}'.format(address, value)) 