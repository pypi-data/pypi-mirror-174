
"""
TODO document this
"""
def nomis_fetch_dataset(dataset, filters, encoding=None):
    from pandas import read_csv
    page = 1
    apiUrl = "https://www.nomisweb.co.uk/api/v01/dataset/" + dataset + ".data.csv?recordlimit=25000"

    for (attr, value) in filters.items():
        apiUrl = apiUrl + "&" + attr + "=" + value
    res = read_csv(apiUrl, header=0, encoding=encoding)
    frame = res
    while(len(res) == 25000):
        url = apiUrl+"&recordoffset=" + str(25000 * page)
        res = read_csv(url, header=0, encoding=encoding)
        page += 1
        frame = frame.append(res)
    return frame
