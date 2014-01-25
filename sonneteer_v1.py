#!/usr/bin/python

import re
import sys
import random
import sqlite3

global wordlist
repeat = re.compile("[A-Z']*\\([0-9]+\\)")
whitespace = re.compile("\\s+")

def normalize_whitespace(line):
    tokens = filter(None, whitespace.split(line))
    return ' '.join(tokens)

def init_wordlist():
    global wordlist
    wordlist = []
    with open('cmudict.0.7a.txt','r') as f:
        for line in f:
            line = normalize_whitespace(line)

            # Note that this also skips comments in cmudict
            if not line[0].isalpha() and line[0] != '\'':
                continue

            tokens = line.split(' ', 1)
            word = tokens[0]
            if repeat.match(word):
                #word = word[:word.index('(')]
                continue

            #if word not in wordlist:
            wordlist.append(word)

def verify_iambic_pentameter(lastStressed, stress):
    nums = [1 if lastStressed else 0]
    for c in stress:
        nums.append(int(c))
        
    bad = False
    for i in xrange(len(nums)-1):
        if nums[i] == nums[i+1]:
            bad = True
            break
    return not bad

if __name__ == "__main__":
    init_wordlist()

    connection = sqlite3.connect('words.db')
    c = connection.cursor()

    rhymeScheme = "AABB"
    rhymes = dict()

    for lineno in xrange(len(rhymeScheme)):
        line = ""
        lastSyllableStressed = True
        numSyllables = 0
        currentRhyme = rhymeScheme[lineno]

        while numSyllables < 10:
            word = random.choice(wordlist)
            matching = c.execute("select * from words where word=?",
                                 (word,)).fetchall()
            
            for match in matching:
                _, rhym, syls, strs, cmmn = match
                
                if syls+numSyllables > 10:
                    # This pronunciation is too long. Skip.
                    continue

                # Verify stress patterns
                if not verify_iambic_pentameter(lastSyllableStressed,strs):
                    continue

                if syls+numSyllables == 10:
                    # We get the last word in this! Deal with rhymes
                    try:
                        if rhym != rhymes[currentRhyme]:
                            continue
                    except KeyError:
                        rhymes[currentRhyme] = rhym
                        
                line += word+" "
                lastSyllableStressed = strs[-1] == '1'
                numSyllables += syls
                break

        print line
