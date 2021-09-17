import pandas as pd
all_products = pd.read_excel(r'actions/All_Products.xlsx')

def product_info(code): # called only for datasheet to series includes image URL, 
    product_family_name = all_products['baureihe'].tolist()
    for family_index in range(len(product_family_name)):
        if str(product_family_name[family_index]).upper() in code:
            index = family_index
            break   
    product_details = all_products.iloc[index]
    
    return product_details
