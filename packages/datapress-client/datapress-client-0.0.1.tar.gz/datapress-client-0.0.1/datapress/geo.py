import os

# datapress_client directory
DIRNAME = os.path.dirname(os.path.abspath(__file__))

"""
List the LSOAs in a given header region (as numpy array)
"""
def get_lsoas_in(place):
    from pandas import read_csv
    filename = os.path.join(DIRNAME, 'static', 'lsoa_lookup.csv')
    frame = read_csv(filename)
    frame = frame[frame['UTLA19NM'] == place]
    return frame['LSOA11CD'].to_numpy()
