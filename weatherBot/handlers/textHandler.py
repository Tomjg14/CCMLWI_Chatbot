import nltk
import re
from nltk import Tree
nltk.download('maxent_ne_chunker')
nltk.download('words')


class TextHandler:

    def tokenize_text(self,text):
        tokens = nltk.word_tokenize(text)
        return tokens

    def compute_pos(self,tokens):
        tagged = nltk.pos_tag(tokens)
        return tagged

    def get_NNP(self,tagged):
        nnp_list = []
        for (word,tag) in tagged:
            if tag == "NNP":
                nnp_list.append(word)
        return nnp_list

    def get_NN(self,tagged):
        nn_list = []
        for (word,tag) in tagged:
            if tag == "NN":
                nn_list.append(word)
        return nn_list

    def is_hi(self,text):
        pattern = '^(he+y|hi|hello|yo+|good (day|morning|evening|afternoon))(\.|\!|,)*($| )'
        return bool(re.match(pattern,text,re.I))
        

    def is_bye(self,text):
        pattern = '.*((good)?bye|farewell|take care|ciao|have a nice day|(see|talk to|speak) you( later)?)(\.|\!)*$'
        return bool(re.match(pattern,text,re.I))

    def need_help(self,text):
        pattern = '^help(\.|\!)*$'
        return bool(re.match(pattern,text,re.I))

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

