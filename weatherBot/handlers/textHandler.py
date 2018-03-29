import nltk
import re
from nltk import Tree
nltk.download('maxent_ne_chunker')
nltk.download('words')


class TextHandler:
    '''
    Description: Tokenize the text
    :text: The text to be tokenized
    :tokens: The tokens after tokenizing
    '''
    def tokenize_text(self,text):
        tokens = nltk.word_tokenize(text)
        return tokens

    '''
    Description: Compute the POS tags
    :tokens: The to be tagged text
    :tagged: The tagged text
    '''
    def compute_pos(self,tokens):
        tagged = nltk.pos_tag(tokens)
        return tagged

    '''
    Description: Acquire all the NNP tags of the text
    :tagged: The tags
    :return: NNP tags
    '''
    def get_NNP(self,tagged):
        nnp_list = []
        for (word,tag) in tagged:
            if tag == "NNP":
                nnp_list.append(word)
        return nnp_list

    '''
    Description: Acquire all NN tags of the text
    :tagged: The tags
    :nn_list: All the NN tags
    '''
    def get_NN(self,tagged):
        nn_list = []
        for (word,tag) in tagged:
            if tag == "NN":
                nn_list.append(word)
        return nn_list

    '''
    Description: Regex for checking if the bot is greeted
    :return: true if greeted, false if not
    '''
    def is_hi(self,text):
        pattern = '^(he+y|hi|hello|yo+|good (day|morning|evening|afternoon))(\.|\!|,)*($| )'
        return bool(re.match(pattern,text,re.I))
        
    '''
    Description: Regex for checking if the user is saying goodbye
    :text: The text that is analyzed
    :return: true if goodbye, false if not
    '''
    def is_bye(self,text):
        pattern = '.*((good)?bye|farewell|take care|ciao|have a nice day|(see|talk to|speak) you( later)?)(\.|\!)*$'
        return bool(re.match(pattern,text,re.I))

    '''
    Description: checks whether the users wants to know the temperature
    :text: The text that is analyzed
    :return: true if the user needs the temperature, false if not
    '''
    def need_temp(self,text):
        pattern = '.*temperature.*'
        return bool(re.match(pattern,text,re.I))

    '''
    Description: regex for checking whether the user needs the weather status
    :text: The text that is analyzed
    :return: true if the user needs the weather status, false if not
    '''
    def need_status(self,text):
        pattern = '.*(status|type).*'
        return bool(re.match(pattern,text,re.I))

    '''
    Description: regex for checking whether the user wants a full weather forecast
    :text: The text that is analyzed
    :return: true if the user wants a full forecast, false if not
    '''
    def need_forecast(self,text):
        pattern = '.*forecast.*'
        return bool(re.match(pattern,text,re.I))        

    '''
    Description: regex for checking whether the user needs help
    :text: The text that is analyzed
    :return: true if the user needs help, false if not
    '''
    def need_help(self,text):
        pattern = '^help(\.|\!)*$'
        return bool(re.match(pattern,text,re.I))

    '''
    Description: Regex for checking whether the user would like to know the bot's mood
    :text: The text that is analyzed
    :return: true if the user would like to know the mood, false if not
    '''
    def mood(self,text):
        pattern = '((^How are you)|(^what(\'s| is) up)|.*mood).*'
        return bool(re.match(pattern,text,re.I))

    '''
    Description: Creates a parse tree to chunk the words in the text
    :text: The text that is analyzed
    :label: the target label
    :output: A list of the named entities
    '''
    def get_chunks(self,text,label):
        #get places by using label GPE
        chunked = nltk.chunk.ne_chunk(self.compute_pos(self.tokenize_text(text)))
        prev = None
        output = []
        current_chunk = []

        for subtree in chunked:
            if type(subtree) == Tree and subtree.label() == label:
                current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in output:
                    output.append(named_entity)
                    current_chunk = []
            else:
                continue

        return output

