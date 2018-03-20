import nltk

#Used to extract location names from the text string;
#POS-tag the text
#Extract all NNP tags from the text
#Assume adjacent NNP tags belong to the same location (e.g. New York = 1 location instead of 2)
#Assume all parsed NNP tags are a location
def ner_parse(text):
    #Download the required nltk packages if they are not installed:
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')

        
    text = nltk.word_tokenize(text)
    locs = list()
    tags = nltk.pos_tag(text)

    #Tag the first word of the sentence seperately
    #e.g. 'Could' as first word received NNP tag due to the capital C
    tags = nltk.tag.pos_tag(nltk.word_tokenize(text[0])) + tags[1:]

    idx = 0
    while idx < len(tags):
        name = ''
        if tags[idx][1] == 'NNP':
            name = name + tags[idx][0]
            while idx+1 < len(tags) and tags[idx+1][1] == 'NNP':
                name = name + ' '
                idx += 1
                name = name + tags[idx][0]
                
            
            locs.append(name)
            name = ''

                    
        idx += 1
    print(locs)
    return locs
    
exampletext = 'Could you give me the weather forecasts of the places New York, New Amsterdam, New Jersey and Sydney?'
ner_parse(exampletext)
