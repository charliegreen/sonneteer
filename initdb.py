#!/usr/bin/python

import sqlite3
import re

repeat = re.compile("[A-Z']*\\([0-9]+\\)")
whitespace = re.compile("\\s+")

def normalize_whitespace(line):
    tokens = filter(None, whitespace.split(line))
    return ' '.join(tokens)

def get_stress_pattern(p):
    nums = []
    for c in p:
        if c.isdigit():
            nums.append(1 if int(c)>0 else 0)
    return nums

def get_last_syll(p):
    lastSyll = ''
    for s in p.split(' '):
        for c in s:
            if c.isdigit():
                lastSyll = s[:-1]
                break
            else:
                lastSyll += c
    return lastSyll

# TODO
def get_commonness(word):
    return 0

if __name__ == "__main__":
    conn = sqlite3.connect("words.db")
    c = conn.cursor()

    try:
        c.execute('drop table words') # ERMAHGERD DRERP TERBLERS
    except sqlite3.OperationalError:
        pass                    # NERP, TERBLER NERT ERXERST

    c.execute('create table words (word text, rhyme text, sylls integer, '
              'stress text, commonness integer)')

    #values = []
    with open('cmudict.0.7a.txt', 'r') as f:
        for line in f:
            line = normalize_whitespace(line)

            if not line[0].isalpha() and line[0] != '\'':
                continue
            
            tokens = line.split(' ',1)
            word = tokens[0]
            pronunciation = tokens[1]

            if repeat.match(word):
                word = word[:word.index('(')]

            stress = ''.join(map(str,get_stress_pattern(pronunciation)))
            sylls  = len(stress)
            commonness = get_commonness(word)
            rhyme = get_last_syll(pronunciation)
            #values.append((word, rhyme, sylls, stress, commonness))
            c.execute('insert into words values (?,?,?,?,?)',
                      (word, rhyme, sylls, stress, commonness))
    
    #c.executemany('insert into words values (?,?,?,?,?)', values)
    conn.commit()
