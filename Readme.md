# Introduction

This scripts is aimed to help my thesis that about to analyzing the hungarian social media. I have a pipeline that contains scraping -> parsing -> morphologic analysis -> analyzers for social graphs and other aspects.

Find other elements in the following locations:
1. Scrapers: https://github.com/tbalogh/online-media-scrapers 
2. Parsers: https://github.com/tbalogh/online-media-article-parsers
3. Morphologic analyer: this project

Util tools:
1. https://github.com/tbalogh/python-processor-executors

# Setup

This project is heavily depends on hungarian morphological analyzers. Thanks for the authors and contributors.

1. pip install https://github.com/oroszgy/hunlp/releases/download/0.2/hunlp-0.2.0.tar.gz
2. docker pull oroszgy/hunlp
3. docker run -it -m 8G -p 9090:9090 oroszgy/hunlp  (wait until the server started inside the container: [Thread-1] INFO org.eclipse.jetty.server.Server - Started)

This steps is extracted from the following nlp project (that this scripts depends on): https://github.com/oroszgy/hunlp

# Usage

This scripts takes the model representation of articles (created by the parsers) and extend it with morphologic information such as: lemmas and named entities.

Article model

```json
"{
    "id": "",
    "portal": "",
    "url": "",
    "published_time": "",
    "title": "",
    "content": "",
    "description": "", #optional
    "author": [], #optional
    "category": "...", #optional
    "tags": [], #optional
    "description": "..." #optional
}"
```

```json
"{
    "id": "",
    "portal": "",
    "url": "",
    "published_time": "",
    "title": "",
    "content": "",
    "description": "", #optional
    "author": [], #optional
    "category": "...", #optional
    "tags": [], #optional
    "description": "..." #optional

    "lemmas": [], # NEW INFO
    "persons": [] # NEW INFO
}"
```

# Example:

Without configuration:

```bash
python morph_analyzer.py -m '{"content": "Donald Trump, az amerikai elnök tárgyalt Vladimir Putinnal. Trump nem értett egyet Putinnal."}'
```

With stop_words:

```bash
python morph_analyzer.py -m '{"content": "Donald Trump, az amerikai elnök tárgyalt Vladimir Putinnal. Trump nem értett egyet Putinnal."}' -c '{"stop_words": ["az", ",", "."]}'
```

With person_dictionary:
```bash
python morph_analyzer.py -m '{"content": "Donald Trump, az amerikai elnök tárgyalt Vladimir Putinnal. Trump nem értett egyet Putinnal."}' -c '{"person_dictionary": {"vladimir putin": ["putin"], "donald trump": ["trump"]} }'
```

# Configuration

You can pass the followings into the configuration:

* stop words: this will filter out the unnecessery lemmas, eg.: punctuations
* person dictionary: this will "lemmatize" the different form of the same person, eg.: putin, putyin, vlagyimir putyin, vladimir putin -> vladimir putin

If no configuration given than it won't filter or change anything.

## Format

```json
{
    "stop_words": ["word1", "word2"],
    "person_dictionary": {
        "person1": ["form1_of_person1", "form2_of_person1"],
        "person2": ["form1_of_person2", "form2_of_person2", "form3_of_person2"] 
        //...
    }
}
```


# Known issues

The Named Entity Recognition does not work perfectly cause it does not provide all the information to decide the border of the named entities so some named entities will be mixed together (see the example below).


This works:
```bash
python morph_analyzer.py -m '{"content": "Donald Trump, az amerikai elnök tárgyalt Vladimir Putinnal."}'
```

This does not work:
```bash
python morph_analyzer.py -m '{"content": "Az amerikai elnök, Donald Trump Vladimir Putinnal tárgyalt."}'
```
