## 0926
## week1 assignment spell checker by claire

import re
from collections import Counter
import streamlit as st

def words(text): return re.findall(r"[^\d\W]+\'*[^\d\W]+", text.lower())
## match all words without numbers
## include ' if there's any

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) | known(edits1(word)) or known(edits2(word)) or [word])
    
def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = "abcdefghijklmnopqrstuvwxyz'"
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

## Evaluation



#### spelltest(Testset(open('spell-testset1.txt'))) # Development set


## App

st.title("Spell Checker Demo")

origin = st.sidebar.checkbox("Show original word", value=False, key=None, help=None)

input1  = ""
input1 = st.selectbox("Choose a word", ['love','happy', 'teecher'])


input2 = ""
input2 = st.text_input("Key in a word:")

    
test_input = ""
if (input1 != ""):
    test_input = input1
if (input2 != ""):
    test_input = input2
    
if (test_input != ""):
    if (origin):
        st.text(correction(test_input))
        
    if (test_input == correction(test_input)):
        st.success("Correct!", icon="✅")
        st.balloons()
        test_input = ""
        input2 = ""
        input1 = ""
    else:
        st.error("Wrong", icon="🚨")
        test_input = ""
        input2 = ""
        input1 = ""