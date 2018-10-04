import sys, os, json
import argparse
import unicodedata
from hunlp import HuNlp

nlp = HuNlp()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-m", "--model", required=True, help="The model representation as json str")
    required.add_argument("-c", "--config_param", help='The configuration file (or a string paramter). See the config format in the Readme.md')

    args = parser.parse_args()
    validate_arguments(args)

    return args.model, args.config_param

def validate_arguments(args):
    pass

def validate_config(config):
    pass

def read_config(config_param):
    if config_param is None:
        config = dict()
    elif type(config_param) is dict:
        # todo assert content
        config = config_param
    else:
        try:
            if os.path.isfile(config_param):
                with open(config_param, 'r') as f:
                    config = json.load(f)
            else:
                config = json.loads(config_param)
        except Exception as ex:
            # todo handle
            raise ex
        
    if "stop_words" not in config.keys():
        config["stop_words"] = []
    if "person_dictionary" not in config.keys():
        config["person_dictionary"] = {}
    
    return config

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def normalize(word):
    return strip_accents((word.lower()).strip())

def inspect(obj):
    for property, value in vars(obj).items():
        print(str(property) + ": " + str(value))

def lemmatize_persons(persons, lemma_dict):
    lemmatized_persons = []
    for person in persons:
        lemma_found = False
        for lemma, word_forms in lemma_dict.items():
            if person in word_forms:
                lemmatized_persons.append(lemma)
                lemma_found = True
                break
        if not lemma_found:
            lemmatized_persons.append(person)

    return lemmatized_persons

def extend_model(model, stop_words, lemma_dict):
    content = model['content']
    doc = nlp(content)
    lemmas = []
    persons = []
    person_candidate = ""
    for sent in doc:
        for tok in sent:
            if tok.lemma in stop_words:
                continue
            lemmas.append(normalize(tok.lemma))
            if tok.entity_type == "I-PER":
                person_candidate += tok.lemma + " "
            elif person_candidate != "":
                persons.append(normalize(person_candidate))
                person_candidate = ""
    model['lemmas'] = lemmas
    model['persons'] = lemmatize_persons(persons, lemma_dict)

    return model

def process(text, config_param):                                                                                                                        
    config = read_config(config_param)
    validate_config(config)
    model = json.loads(text)
    return json.dumps((extend_model(model, config["stop_words"], config["person_dictionary"])), ensure_ascii=False)
 

if __name__ == '__main__':
    (text, config_param) = parse_arguments()
    print(process(text, config_param))
