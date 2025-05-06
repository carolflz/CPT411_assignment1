from flask import Flask, render_template, request
import re

app = Flask(__name__)
app.secret_key = "super secret key"

pattern = ["and", "or", "very", "never", "good", "bad", "pretty", "dirty", "blue", "most"]
states = ["q"+str(i) for i in range(40)]
alphabets = list("abcdefghijklmnopqrstuvwxyz")
start_state = "q0"
accept_states = ["q3", "q7", "q11", "q14", "q20", "q25", "q28", "q30", "q34", "q39"]

# DFA transitions
transition = {
    ('q0', 'a'): 'q1', ('q1', 'n'): 'q2', ('q2', 'd'): 'q3',
    ('q0', 'm'): 'q4', ('q4', 'o'): 'q5', ('q5', 's'): 'q6', ('q6', 't'): 'q7',
    ('q0', 'g'): 'q8', ('q8', 'o'): 'q9', ('q9', 'o'): 'q10', ('q10', 'd'): 'q11',
    ('q0', 'b'): 'q12', ('q12', 'a'): 'q13', ('q13', 'd'): 'q14',
    ('q12', 'l'): 'q26', ('q26', 'u'): 'q27', ('q27', 'e'): 'q28',
    ('q0', 'p'): 'q15', ('q15', 'r'): 'q16', ('q16', 'e'): 'q17',
    ('q17', 't'): 'q18', ('q18', 't'): 'q19', ('q19', 'y'): 'q20',
    ('q0', 'd'): 'q21', ('q21', 'i'): 'q22', ('q22', 'r'): 'q23',
    ('q23', 't'): 'q24', ('q24', 'y'): 'q25',
    ('q0', 'o'): 'q29', ('q29', 'r'): 'q30',
    ('q0', 'v'): 'q31', ('q31', 'e'): 'q32', ('q32', 'r'): 'q33', ('q33', 'y'): 'q34',
    ('q0', 'n'): 'q35', ('q35', 'e'): 'q36', ('q36', 'v'): 'q37',
    ('q37', 'e'): 'q38', ('q38', 'r'): 'q39'
}

# Add space transitions to reset to q0 after word completion
for state in set(transition.values()):
    transition[(state, ' ')] = 'q0'

# Add trap state to catch all undefined transitions
trap_state = "qX"

# Fill missing transitions with trap state
for state in set(transition.values()).union({start_state}):
    for char in alphabets:
        if (state, char) not in transition:
            transition[(state, char)] = trap_state

# Loop trap state to itself
for char in alphabets:
    transition[(trap_state, char)] = trap_state

# Helper: find words in pattern
def find_substring_from_words(words):
    return set([word for word in words if word in pattern])

# Helper: accurate word-boundary count
def calc_occurrence_count(substrings_found, sentence):
    return {
        s: len(re.findall(r'\b' + re.escape(s) + r'\b', sentence, re.IGNORECASE))
        for s in substrings_found
    }

# Helper: position index of matched words
def find_position_index(sentence):
    return {
        p: [m.start() for m in re.finditer(r'\b' + re.escape(p) + r'\b', sentence, re.IGNORECASE)]
        for p in pattern if p in sentence.lower()
    }

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.args.get('generatebtn'):
        text = request.args.get('text')
        sentences_string = re.split(r'[.\n]+', text)
        clean_sentences = [s.strip() for s in sentences_string if s.strip()]
        total_occurrence_count = {p: 0 for p in pattern}
        sentences_data = []

        for sentence in clean_sentences:
            current_state = start_state
            words = []
            word = ""

            for char in sentence.lower():
                # Check for non-alphabetic characters (punctuation, spaces)
                if char not in alphabets:
                    # If there is a word formed, add it
                    if word:
                        words.append(word)
                        word = ""
                    # Reset DFA to start state if punctuation/space is encountered
                    current_state = start_state
                    continue

                if (current_state, char) in transition:
                    # Continue DFA transitions
                    current_state = transition[(current_state, char)]
                    word += char
                else:
                    # When no valid transition is found, reset and start a new word
                    if word:
                        words.append(word)
                        word = ""
                    current_state = start_state  # Reset DFA to start state

            # After loop ends, ensure the last word is added
            if word:
                words.append(word)

            substrings_found = find_substring_from_words(words)

            if substrings_found:
                status = 'Accepted'
                occurrence_count = calc_occurrence_count(substrings_found, sentence)
                positions = find_position_index(sentence)
                for p, c in occurrence_count.items():
                    total_occurrence_count[p] += c
            else:
                status = 'Rejected'
                occurrence_count = {}
                positions = {}

            sentences_data.append({
                'sentence': sentence,
                'words': words,
                'substrings_found': substrings_found,
                'status': status,
                'occurrence_count': occurrence_count,
                'position': positions
            })

        return render_template('index.html',
                               pattern=pattern,
                               states=states,
                               alphabets=alphabets,
                               start_state=start_state,
                               accept_states=accept_states,
                               sentences_string=clean_sentences,
                               sentences_data=sentences_data,
                               total_occurrence_count=total_occurrence_count,
                               transition=transition)

    return render_template('index.html',
                           pattern=pattern,
                           states=states,
                           alphabets=alphabets,
                           start_state=start_state,
                           accept_states=accept_states)

if __name__ == "__main__":
    app.run(debug=True)