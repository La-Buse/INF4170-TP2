class Cache_Row():
    def __init__(self, index, valid, tag, word_1, word_2):
        self.index = index
        self.valid = valid
        self.tag = tag
        self.word_1 = word_1
        self.word_2 = word_2

class Cache():
    def __init__(self, rows=[]):
        self.central_memory = central_memory
        self.rows = rows

    def add_cache_row(cache_row):
        self.rows.append(cache_row)

    def load_word(self, address):
        pass
initial_value = 0x00000000

class Central_Memory():
    def __init__():
        self.modified_words = {}
    def get_value_at_address(self, address):
        if address in self.modified_words:
            return self.modified_words[address]
        else:
            return self.get_default_value_at_address(address)

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
        

for i in range(0,16):
    if (i != 0):
        initial_value += 0x11111111
    print('{:08X}'.format(initial_value))
