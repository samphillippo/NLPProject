import pandas as pd
from dateutil import parser
import datetime
import re


def generate_citation(data):
    '''
    Generate an IEEE citation for a given row of data
    '''
    data_array = data
    authors = data_array['authors']
    citation = ""
    if authors != None:
        citation += _parseAuthors(authors)
    title = data_array['title']
    if title == None:
        citation += "UNKNOWN TITLE, "
    else:
        citation += "\"" + str(title) + "\", "
    publisher = data_array['publisher']
    if publisher != None:
        citation += str(publisher) + ", "
    date = data_array['datePublished']
    if date != None:
        try:
            citation += _convert_date(str(date)) + ", "
        except:
            # print("Date Error... {}".format(date))
            pass
    doi = data_array['doi']
    if doi == None:
        citation += _convert_oai_to_doi(str(doi))
    else:
        citation += str(doi) + "."
    return citation


# Given single date, parse into IEEE format (Month Year)
def _convert_date(date):
    parsed_date = parser.parse(date, default=datetime.datetime(1,1,1))
    if parsed_date.month ==  1 and len(date) == 4:
        return parsed_date.strftime("%Y")
    else:
        return parsed_date.strftime("%B %Y")

# If no DOI is provided, convert OAI to DOI
def _convert_oai_to_doi(oai):
    rest_call = "https://oai.core.ac.uk/"
    return rest_call + oai

#parses a string into a first name representation (John Joseph Flynn -> J.J. Flynn)
def _parseFirstName(firstName):
    firstNames = re.split(r'\s+|-|\.', firstName)
    parsedName = ""
    for name in firstNames:
        if len(name) > 0:
            parsedName += re.sub(r'[^a-zA-Z]', '', name)[0:1].upper() + "."
    return parsedName

#given a single author, parses it down to a IEEE usable format
def _parseAuthor(author):
    names = author.split(",")
    names = [name for name in names if len(name) > 0]
    if len(names) > 2:
        if len(names) == 3 and '.' in names[2]:
            return _parseFirstName(names[1]) + _parseFirstName(names[2]) + " " + names[0] + ", "
        return ''.join(names)
    if len(names) == 2:
        return _parseFirstName(names[1]) + " " + names[0] + ", "
    if len(names) == 1:
        sub_names = names[0].split(" ")
        if len(sub_names) == 2:
            return _parseFirstName(sub_names[0]) + " " + sub_names[1] + ", "
        return names[0] + ", "
    return ""

#given an array of authors, gets the IEEE formatted string to be used in citation "{authors}, "
def _parseAuthors(authors):
    parsedAuthorString = ""
    if len(authors) <= 3:
        for author in authors:
            parsedAuthorString += _parseAuthor(author)
    else:
        for author in authors[:3]:
            parsedAuthorString += _parseAuthor(author)
        parsedAuthorString += "et al., "
    return parsedAuthorString


def test():
    # Test _convert_date:
    assert _convert_date('2020-01-01') == 'January 2020'
    assert _convert_date('2020-01') == 'January 2020'
    assert _convert_date('2020') == '2020'
    assert _convert_date('2020-01-01T00:00:00Z') == 'January 2020'

    # Test _convert_oai_to_doi:
    assert _convert_oai_to_doi('oai:core.ac.uk:123456') == 'https://oai.core.ac.uk/oai:core.ac.uk:123456'

    # Test _parseFirstName:
    assert _parseFirstName('John Joseph Flynn') == 'J.J.F.'
    assert _parseFirstName('John') == 'J.'
    assert _parseFirstName('John  Joseph') == 'J.J.'
    assert _parseFirstName('John-Joseph') == 'J.J.'
    assert _parseFirstName('donkey kong') == 'D.K.'

    # Test _parseAuthor:
    assert _parseAuthor('Flynn, John Joseph') == 'J.J. Flynn, '
    assert _parseAuthor('Flynn') == 'Flynn, '
    assert _parseAuthor('Flynn, John') == 'J. Flynn, '

    # Test _parseAuthors:
    assert _parseAuthors(['Flynn, John Joseph', 'Doe, Jane']) == 'J.J. Flynn, J. Doe, '
    assert _parseAuthors(['Flynn, John Joseph', 'Doe, Jane', 'Smith, John']) == 'J.J. Flynn, J. Doe, J. Smith, '
    assert _parseAuthors(['Flynn, John Joseph', 'Doe, Jane', 'Smith, John', 'Doe, Jim']) == 'J.J. Flynn, J. Doe, J. Smith, et al., '

    print('All CitationGenetator tests passed!')
