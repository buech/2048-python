def encode_row(row):
    '''
    Encodes a row in array representation to a row in bit representation
    '''
    return row[0] << 12 | row[1] << 8 | row[2] << 4 | row[3]

def encode(board):
    '''
    Encodes a row in array representation to a row in bit representation
    '''
    return (encode_row(board[0]) << 48 |
            encode_row(board[1]) << 32 |
            encode_row(board[2]) << 16 |
            encode_row(board[3]))

def decode_row(row):
    '''
    Decodes a row in bit representation to a row in array representation
    '''
    return ((row & 0xf000) >> 12,
            (row & 0x0f00) >> 8,
            (row & 0x00f0) >> 4,
            (row & 0x000f))

def decode(board):
    '''
    Decodes a board in bit representation to a board in array representation
    '''
    return (decode_row((board & 0xffff000000000000) >> 48),
            decode_row((board & 0x0000ffff00000000) >> 32),
            decode_row((board & 0x00000000ffff0000) >> 16),
            decode_row((board & 0x000000000000ffff)))

if __name__=='__main__':

    row = (15, 0, 10, 4)
    enc = encode_row(row)
    assert enc == 0xf0a4
    dec = decode_row(enc)
    assert row == dec

    board = ((5, 0, 1, 4),
             (3, 1, 2, 3),
             (1, 2, 3, 4),
             (0, 1, 0, 2))

    encb = encode(board)
    assert encb == 0x5014312312340102
    decb = decode(encb)
    assert board == decb
