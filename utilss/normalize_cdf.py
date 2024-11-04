from numpy import floor, uint8

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