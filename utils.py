def translate_term_to_numerical(term):
    term_split = term.split(" ")
    if term_split[0] == "fall":
        term_num = "03"
    elif term_split[0] == "summer":
        term_num= "02"
    elif term_split[0] == "spring":
        term_num = "01"
    else:
        raise Exception("Error parsing term")
    return str(term_split[1] + term_num)
