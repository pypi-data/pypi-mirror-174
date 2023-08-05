import pandas as pd
import chardet
with open('represaliats.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large


pd.read_csv('represaliats.csv', encoding=result['encoding'])



