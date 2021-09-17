from actions.validation import validation
import pandas as pd
df = pd.read_excel('actions/All_Products.xlsx')

def get_languages(name): # in case of datasheet

  languages = []
            
  product_name = df['baureihe'].tolist()

  # product_info = df[df["product"] == name]

  # if product_info:
  #   languages = product_info[]

  for n in product_name:
    if str(n) in name:
      index = df.index[df['baureihe'] == n]
      if df['german'][index].to_string(index=False) != 'NaN':
        languages.append('german')
      if df['english'][index].to_string(index=False) != 'NaN':
        languages.append('english')
      if df['italian'][index].to_string(index=False) != 'NaN':
        languages.append('italian')
      if df['spanish'][index].to_string(index=False) != 'NaN':
        languages.append('spanish')
      if df['french'][index].to_string(index=False) != 'NaN':
        languages.append('french')
    
  return languages


def check_product(code):
  product_name = df['baureihe'].tolist()

  if code in product_name:          # in case of datasheet
    product_existance = True
    return product_existance, code   
  else:                             # incase of CAD                 
    typecode = validation(code)      
    if not bool(typecode):
      product_existance = False
      return product_existance
    else:
      product_existance = True
      return product_existance, typecode  
