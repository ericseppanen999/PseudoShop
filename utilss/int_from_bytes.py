def int_from_bytes(byte_sequence):
        # convert byte sequence to int
        # assumes byte order is little endian
        if not isinstance(byte_sequence,(bytes, bytearray)):
            raise ValueError("invalid byte_sequence")
        byte_iter=reversed(byte_sequence)
        res=0
        for byte in byte_iter:
            res=res*256+byte
        return res