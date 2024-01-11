import re

def cleanCity(workplace):
    # Replace "cedex" with an empty string
    workplace = workplace.replace("cedex", '')
    workplace = workplace.replace("CEDEX", '')
    workplace = workplace.replace("\u2026","")
    # Remove digits
    workplace = re.sub(r'\d+', '', workplace)

    # Replace '\s+er\s+' with ' '
    workplace = re.sub(r'\s+er\s+', ' ', workplace)

    # Replace '\s+-\s+' with ' '
    workplace = re.sub(r'\s+-\s+', ' ', workplace)

    # Replace '\s+e\s+' with ' '
    workplace = re.sub(r'\s+e\s+', ' ', workplace)

    # Replace 'La Défense' with 'Paris '
    workplace = workplace.replace('La Défense', 'Paris ')

    # Replace 'Lyon Paris er' with 'Paris '
    workplace = workplace.replace('Lyon Paris er', 'Paris ')

    # Split by '·' and take the first part
    workplace = workplace.split('·')[0]

    return workplace.strip()