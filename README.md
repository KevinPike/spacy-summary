# spacy-smmry

This is an implementation of [SMMRY](http://smmry.com/about) using [spacy.io](https://spacy.io/).

## Usage

To get started with `spacy-smmry`, install the dependencies:

```bash
# A virtualenv is recommended
virtualenv .env
source .env/bin/activate

# Install python libraries
pip install -r requirements.txt
python -m spacy download en
```

The program takes the text file to summarize and the number of sentences to include in the summary:
```python
# Reads and summarizes document.txt in 3 sentences
python main.py document.txt 3
```