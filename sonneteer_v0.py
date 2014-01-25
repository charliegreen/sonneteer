#!/usr/bin/python

import re
import sys
import random

global word_pronunciations
# This is a dict that contains the pronounciation of all words in the CMU
# Pronunciation Dictionary. It maps a string (the word, case insensitive)
# to a list of strings (the pronunciation strings). These pronunciation
# strings are to be individually processed when needed.

repeat = re.compile("[A-Z']*\\([0-9]+\\)")
whitespace = re.compile("\\s+")

def load_dict():
    global word_pronunciations
    word_pronunciations = {}
    with open('cmudict.0.7a.txt','r') as f:
        for line in f:
            line = normalize_whitespace(line)

            # Note that this also skips comments in cmudict
            if not line[0].isalpha() and line[0] != '\'':
                continue

            tokens = line.split(' ', 1)
            word = tokens[0]
            pronunciation = tokens[1]

            if repeat.match(word):
                word = word[:word.index('(')]
                try:
                    word_pronunciations[word].append(pronunciation)
                except KeyError:
                    word_pronunciations[word] = [pronunciation]
            else:
                word_pronunciations[word] = [pronunciation]

def normalize_whitespace(line):
    tokens = filter(None, whitespace.split(line))
    return ' '.join(tokens)

def get_pronunciations(word):
    return word_pronunciations[word.upper()]

def get_stress_pattern(p):
    nums = []
    for c in p:
        if c.isdigit():
            nums.append(1 if int(c)>0 else 0)
    return nums

if __name__ == "__main__":
    load_dict()
    rhymeScheme = "ABABCDCDEFEFGG"
    rhymes = dict()
    
    for lineno in xrange(len(rhymeScheme)):
        line = ""
        lastSyllableStressed = True
        numSyllables = 0
        currentRhyme = rhymeScheme[lineno]

        while numSyllables < 10:
            word = random.choice(word_pronunciations.keys())
            ps = get_pronunciations(word)

            for p in ps:
#                print "%d %s %s" % (numSyllables, word, p)

                nums = [1 if lastSyllableStressed else 0]
                nums += get_stress_pattern(p)

                bad = False
                if len(nums)-1 + numSyllables > 10: # deal with lengthy words
                    bad = True

                for i in xrange(len(nums)-1): # verify stress patterns
                    if nums[i] == nums[i+1]:
                        bad = True
                        break

                if len(nums)-1 + numSyllables == 10:
                    lastSyll = ""
                    for s in p.split(" "):
                        for c in s:
                            if c.isdigit():
                                lastSyll = s[:-1]
                                break
                            else:
                                lastSyll += c

                    try:            # get rhyme for current line
                        if lastSyll != rhymes[currentRhyme]:
                            bad = True
                    except KeyError: # carry on, and mark this as our rhyme
                        if not bad:
                            rhymes[currentRhyme] = lastSyll
                            
                if bad:
                    continue
                    
                line += word+" "
                lastSyllableStressed = nums[-1] == 1
                numSyllables += len(nums)-1
                
                break

            else:
                continue
        print line
                                
                                    
