### Description
This project implements a Deterministic Finite Automaton (DFA) in Python to recognize specific English conjunctions, adverbs, and adjectives within a given text. The DFA simulates a state machine that processes input one character at a time, from left to right, to determine whether predefined patterns exist in the text.

The DFA is complete and deterministic, with transitions defined for each state and input symbol from the specified alphabet (Σ). The program terminates early if a trap state is entered. The system is capable of recognizing and locating the following words:

Recognized Patterns (Language L)
Conjunctions: and, or
Adverbs: very, never
Adjectives: good, bad, pretty, dirty, blue, most
Input Alphabet (Σ)
{a, b, d, e, g, i, l, m, n, o, p, r, s, t, u, v, y}

How It Works
The DFA is defined using a dictionary of states and transitions.
Input text is tokenized and each word is checked against the DFA.
Recognized words are highlighted and recorded with positions.
A statistics table displays occurrences of each accepted word.
