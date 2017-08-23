'''
1) Associate words with their grammatical counterparts. (e.g. "city" and "cities")
2) Calculate the occurrence of each word in the text.
3) Assign each word with points depending on their popularity.
4) Detect which periods represent the end of a sentence. (e.g "Mr." does not).
5) Split up the text into individual sentences.
6) Rank sentences by the sum of their words' points.
7) Return X of the most highly ranked sentences in chronological order.
'''

import codecs
import sys
import spacy

def main():
    args = sys.argv

    # Document name should be provided
    if len(args) < 2:
        print "Provide document"
        exit(1)

    filename = args[1]

    sentence_count = 3
    # Read number of sentences to output if provided
    if len(args) == 3:
        sentence_count = int(args[2])

    # Read file as utf-8
    document_file = codecs.open(filename, encoding='utf-8')
    contents = document_file.read()

    # Process file contents
    nlp = spacy.load('en')
    doc = nlp(contents)

    # 1, 2, 3
    occurrences = {}
    def fill_occurrences(word):
        word_lemma = lemma(word)
        count = occurrences.get(word_lemma, 0)
        count += 1
        occurrences[word_lemma] = count

    each_word(doc, fill_occurrences)

    # 4, 5, 6
    ranked = get_ranked(doc.sents, sentence_count, occurrences)

    # 7
    print " ".join([x['sentence'].text for x in ranked])

def each_word(words, func):
    for word in words:
        if word.pos_ is "PUNCT":
            continue

        func(word)

def get_ranked(sentences, sentence_count, occurrences):
    # Maintain ranked sentences for easy output
    ranked = []

    # Maintain the lowest score for easy removal
    lowest_score = -1
    lowest = 0

    for sent in sentences:
        # Fill ranked if not at capacity
        if len(ranked) < sentence_count:
            score = get_score(occurrences, sent)

            # Maintain lowest score
            if score < lowest_score or lowest_score is -1:
                lowest = len(ranked) + 1
                lowest_score = score

            ranked.append({'sentence': sent, 'score': score})
            continue

        score = get_score(occurrences, sent)
        # Insert if score is greater
        if score > lowest_score:
            # Maintain chronological order
            for i in xrange(lowest, len(ranked) - 1):
                ranked[i] = ranked[i+1]

            ranked[len(ranked) - 1] = {'sentence': sent, 'score': score}

            # Reset lowest_score
            lowest_score = ranked[0]['score']
            lowest = 0
            for i in xrange(0, len(ranked)):
                if ranked[i]['score'] < lowest_score:
                    lowest = i
                    lowest_score = ranked[i]['score']

    return ranked

def lemma(word):
    return word.lemma_

def get_score(occurrences, sentence):
    class Totaler:
        def __init__(self):
            self.score = 0
        def __call__(self, word):
            self.score += occurrences.get(lemma(word), 0)
        def total(self):
            # Should the score be divided by total words?
            return self.score

    totaler = Totaler()

    each_word(sentence, totaler)

    return totaler.total()

if __name__ == "__main__":
    main()
