from numpy import floor, uint8

def acid_normalize_cdf(cdf):
        # acid normalization
        # helper function in autolevels
        # see report for explanation
        return floor((cdf-cdf.min()*255/cdf.max()-cdf.min())).astype(uint8)

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

def normalize_cdf(cdf):
    # normalize cdf
    # helper function for auto levels
    cdf_min=cdf.min()
    cdf_max=cdf.max()
    if cdf_max!=cdf_min:
        cdf_range=cdf_max-cdf_min
    else:
        cdf_range=1
    normalized_cdf=floor((cdf-cdf_min)*255/cdf_range).astype(uint8)
    return normalized_cdf

def normalize(value,value_min,value_max):
        # normalize range
        if value_max>value_min:
            new_value=int((value-value_min)/(value_max-value_min)*255)
        else:
            new_value=value
        new_value=max(0,min(255,new_value))
        return new_value

def scaler(g,lower_bound,upper_bound):
        # helper function to scale a value between a lower and upper bound
        return max(lower_bound,min(upper_bound,g))