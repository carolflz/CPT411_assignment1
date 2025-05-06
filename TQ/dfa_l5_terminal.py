import re

# Define patterns
pattern = ["and", "or", "very", "never", "good", "bad", "pretty", "dirty", "blue", "most"]
start_state = "q0"
accept_states = ["q3", "q7", "q11", "q14", "q20", "q25", "q28", "q30", "q34", "q39"]
alphabets = list("abcdefghijklmnopqrstuvwxyz")

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

# Main DFA processing function
def analyze_text(text):
    sentences = re.split(r'[.\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    total_occurrence_count = {p: 0 for p in pattern}

    for sentence in sentences:
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
        
        # Debug output to check words after splitting
        print(f"Final Words: {words}")

        substrings_found = find_substring_from_words(words)

        if substrings_found:
            status = "Accepted"
            occurrences = calc_occurrence_count(substrings_found, sentence)
            positions = find_position_index(sentence)
            for word, count in occurrences.items():
                total_occurrence_count[word] += count
        else:
            status = "Rejected"
            occurrences = {}
            positions = {}

        print(f"\nSentence: {sentence}")
        print(f"Status: {status}")
        print(f"Matched Patterns: {substrings_found}")
        print(f"Occurrences: {occurrences}")
        print(f"Positions: {positions}")
        print("-" * 50)

    print("\n=== TOTAL OCCURRENCES ===")
    for word, count in total_occurrence_count.items():
        print(f"{word}: {count}")

# File selector interface
if __name__ == "__main__":
    print("Choose the file to analyze:")
    print("1. sample_text1.txt")
    print("2. sample_text2.txt")
    choice = input("Enter 1 or 2: ")

    file_path = ""
    if choice == "1":
        file_path = "sample_text1.txt"
    elif choice == "2":
        file_path = "sample_text2.txt"
    else:
        print("Invalid choice.")
        exit()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        analyze_text(text)
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Make sure it is in the same folder as this script.")
