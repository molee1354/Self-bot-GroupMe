
#* for multiple line search requests
#if space turns to '+'
def spaceis_plus(search):
    l = list(search)
    for w in range(len(search)):
        if l[w] == ' ':
            l[w] = '+'

    gogo = ''.join(l)
    return gogo

#if space turns to '%20'
def spaceis_pcent(search):
    l = list(search)
    for w in range(len(search)):
        if l[w] == ' ':
            l[w] = '%20'

    gogo = ''.join(l)
    return gogo

#if space turns to '_'
def spaceis_underscore(search):
    l = list(search)
    for w in range(len(search)):
        if l[w] == ' ':
            l[w] = '_'

    gogo = ''.join(l)
    return gogo

#function to generate url. returns nothing if not correct website

def websearch(website, keyword_entry):

    #* var keyword_entry is the words that come after website : chatcommand[2:]

    if website == 'thesaurus':
        keyword = spaceis_pcent(keyword_entry)
    elif website == 'wiki':
        keyword = spaceis_underscore(keyword_entry)
    else:
        keyword = spaceis_plus(keyword_entry)

    match website:
        #google
        case 'google' | 'search':
            base = "https://www.google.com/search?q="

        #yt
        case 'youtube':
            base = "https://www.youtube.com/results?search_query="

        #wiki
        case 'wiki':
            base = "https://en.wikipedia.org/wiki/"

        #dictionary
        case 'dictionary':
            base = "https://www.dictionary.com/browse/"

        #thesaurus
        case 'thesaurus':
            base = "https://www.thesaurus.com/browse/"

        case _:  
            base = "https://www.google.com/search?q="

    return base + keyword
