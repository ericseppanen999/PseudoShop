from numpy import floor, uint8

def acid_normalize_cdf(self,cdf):
        # acid normalization
        # helper function in autolevels
        # see report for explanation
        return floor((cdf-cdf.min()*255/cdf.max()-cdf.min())).astype(uint8)
