
"""
TODO document this
"""
def extract_data_from_excel(spreadsheet, sheet, header):
    from pandas import read_excel

    frame = read_excel(spreadsheet, sheet_name=sheet)
    frame = frame.filter(regex=header + "\.?(%d)?")
    frame = frame.dropna()
    headers = frame.iloc[0]
    frame = frame[1:]
    frame.columns = headers
    return frame

