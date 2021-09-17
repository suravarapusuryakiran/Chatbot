

def get_link_from_tc(data):

    data = data.strip()

    if data == "CYTROPAC":
        return "my_cytropac_link"
    
    elif data.startswith("CYTROPAC"):
        # read xml file
        # check if typecode is in xml file
        # build link from xml file input
        # return link
        return "specific_cytropac_link"

    else:
        return None




