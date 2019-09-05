term_dict = {
    "fall": "03",
    "summer": "02",
    "spring": "01"
}

def translate_term_to_numerical(term):
    term_split = term.split(" ")
    try:
        return str(term_split[1] + term_dict[term_split[0]])
    except KeyError:
        raise Exception("Error parsing term")
