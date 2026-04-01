import pandas as pd


def aggregation(df):
    string_cols = ['marketplace', 'product_name', 'status']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)


    numeric_cols = ['quantity', 'price', 'cost_price']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce') 
            df[col] = df[col].fillna(0).astype(int)  


    if 'sold_at' in df.columns:

        df['sold_at'] = pd.to_datetime(df['sold_at'], errors='coerce').dt.strftime('%Y-%m-%d')
        df['sold_at'] = df['sold_at'].fillna('')

    result = df.to_dict('records')
    return result


