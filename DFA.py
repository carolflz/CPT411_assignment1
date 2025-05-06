import tkinter as tk
from tkinter import scrolledtext, font, ttk
from collections import defaultdict

# DFA Recognizer for the language L = {or, bad, and, blue, good, most, very, dirty, pretty, never}

# Define the DFA transitions as a dictionary of dictionaries
# each state maps input characters to the next state
dfa = {
    0: {'o': 1, 'b': 10, 'a': 20, 'g': 30, 'm': 40, 'v': 50, 'd': 60, 'p': 70, 'n': 80},
    
    # or
    1: {'r': 2}, 
    2: {},

    # bad / blue 
    10: {'a': 11, 'l': 13},
    11: {'d': 12},       
    12: {},

    13: {'u': 14},       
    14: {'e': 15},
    15: {},

    # and
    20: {'n': 21},
    21: {'d': 22},
    22: {},

    # good
    30: {'o': 31},
    31: {'o': 32},
    32: {'d': 33},
    33: {},

    # most
    40: {'o': 41},
    41: {'s': 42},
    42: {'t': 43},
    43: {},

    # very
    50: {'e': 51},
    51: {'r': 52},
    52: {'y': 53},
    53: {},

    # dirty
    60: {'i': 61},
    61: {'r': 62},
    62: {'t': 63},
    63: {'y': 64},
    64: {},

    # pretty
    70: {'r': 71},
    71: {'e': 72},
    72: {'t': 73},
    73: {'t': 74},
    74: {'y': 75},
    75: {},

    # never
    80: {'e': 81},
    81: {'v': 82},
    82: {'e': 83},
    83: {'r': 84},
    84: {},
}

# Define accepting states where valid words should end
accept_states = {2, 12, 15, 22, 33, 43, 53, 64, 75, 84}

# it traverse the each word through DFA
def simulate_dfa(input_str):
    current_state = 0
    for char in input_str:
        if char in dfa.get(current_state, {}):
            current_state = dfa[current_state][char]
        else:
            return False
    return current_state in accept_states
# Text highlighting using Tkinter Tags
def highlight_words(text_widget, input_text):
    # Configure tags
    text_widget.tag_configure("bold", font=('Arial', 10))
    # "accepted" words: green text with bold font (Arial Black)
    # "rejected" words: black text with normal font
    # "bold": defines a generic Arial font, but only applied with "accepted"
    text_widget.tag_configure("accepted", foreground='green', font=('Arial Black', 10))
    text_widget.tag_configure("rejected", foreground='black')
    
    # Clear previous content
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    
    # Split the input text into words
    words = input_text.split()
    word_stats = defaultdict(list)
    total_accepted = 0
    
    # perform text cleaning (remove punctuation and convert to lowercase)
    for position, word in enumerate(words, start=1):
        clean_word = ''.join(filter(str.isalpha, word)).lower()
        if simulate_dfa(clean_word):
            #insert the word into the text widget with the accepted tag
            text_widget.insert(tk.END, word + " ", ("bold", "accepted"))
            word_stats[clean_word].append(position)
            total_accepted += 1
        else:
            text_widget.insert(tk.END, word + " ", "rejected")
    
    text_widget.config(state=tk.DISABLED)
    return total_accepted, word_stats

def update_stats_table(word_stats):
    # Clear previous data
    for row in stats_tree.get_children():
        stats_tree.delete(row)
    
    # Add only words that appeared in the input text
    language_words = ['or', 'bad', 'and', 'blue', 'good', 'most', 'very', 'dirty', 'pretty', 'never']
    for word in language_words:
        if word in word_stats:
            positions = word_stats[word]
            status = "Accept"
            count = len(positions)
            pos_str = ", ".join(map(str, positions))
            stats_tree.insert("", "end", values=(word, status, count, pos_str))

def clear_all():
    input_textbox.delete('1.0', tk.END)
    output_textbox.config(state=tk.NORMAL)
    output_textbox.delete('1.0', tk.END)
    output_textbox.config(state=tk.DISABLED)
    count_label.config(text="Total accepted words: 0")
    status_label.config(text="Status: ")
    for row in stats_tree.get_children():
        stats_tree.delete(row)

def process_text():
    input_text = input_textbox.get("1.0", tk.END).strip()
    if not input_text:
        output_textbox.config(state=tk.NORMAL)
        output_textbox.delete("1.0", tk.END)
        output_textbox.insert(tk.END, "Error: Input cannot be empty.")
        output_textbox.config(state=tk.DISABLED)
        count_label.config(text="Total accepted words: 0")
        status_label.config(text="Status: ")
        for row in stats_tree.get_children():
            stats_tree.delete(row)
        return
    
    total_accepted, word_stats = highlight_words(output_textbox, input_text)
    count_label.config(text=f"Total accepted words: {total_accepted}")
    
    status = "Accepted" if total_accepted > 0 else "Rejected"
    status_label.config(text=f"Status: {status}")
    
    update_stats_table(word_stats)

# Create the main window
root = tk.Tk()
root.title("DFA Word Recognizer")
root.geometry("1000x700")

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Title Label
title_label = tk.Label(main_frame, 
                     text="DFA Recognizer for L = {or, bad, and, blue, good, most, very, dirty, pretty, never}", 
                     font=("Arial", 10, "bold"))
title_label.pack(pady=10)

# Input frame
input_frame = tk.Frame(main_frame)
input_frame.pack(fill=tk.X, pady=5)

input_label = tk.Label(input_frame, text="Enter your text below:", font=("Arial", 9))
input_label.pack(anchor=tk.W)

input_textbox = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=8, font=("Arial", 10))
input_textbox.pack(fill=tk.X, padx=5, pady=5)

# Button frame
button_frame = tk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=5)

process_button = tk.Button(button_frame, text="Run Analysis", command=process_text, bg="#4CAF50", fg="white")
process_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_all, bg="#f44336", fg="white")
clear_button.pack(side=tk.RIGHT, padx=5)

# Output frame
output_frame = tk.Frame(main_frame)
output_frame.pack(fill=tk.BOTH, expand=True, pady=5)

output_header_frame = tk.Frame(output_frame)
output_header_frame.pack(anchor=tk.W)

output_label = tk.Label(output_header_frame, text="Output", font=("Arial", 9))
output_label.pack(side=tk.LEFT)

status_label = tk.Label(output_header_frame, text="Status: ", font=("Arial", 9))
status_label.pack(side=tk.LEFT, padx=10)

output_textbox = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=2, font=("Arial", 10))
output_textbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

count_label = tk.Label(output_frame, text="Total accepted words: 0", font=("Arial", 9))
count_label.pack(anchor=tk.W, pady=5)

# Statistics frame
stats_frame = tk.Frame(main_frame)
stats_frame.pack(fill=tk.BOTH, expand=True, pady=5)

stats_label = tk.Label(stats_frame, text="Word Statistics (Positions in text):", font=("Arial", 9, "bold"))
stats_label.pack(anchor=tk.W)

stats_tree = ttk.Treeview(stats_frame, columns=("Word", "Status", "Count", "Positions"), show="headings", height=8)
stats_tree.heading("Word", text="Word")
stats_tree.heading("Status", text="Status")
stats_tree.heading("Count", text="Count")
stats_tree.heading("Positions", text="Positions")
stats_tree.column("Word", width=100, anchor=tk.W)
stats_tree.column("Status", width=100, anchor=tk.CENTER)
stats_tree.column("Count", width=50, anchor=tk.CENTER)
stats_tree.column("Positions", width=200, anchor=tk.CENTER)
stats_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

scrollbar = ttk.Scrollbar(stats_tree, orient="vertical", command=stats_tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
stats_tree.configure(yscrollcommand=scrollbar.set)

# Initialize stats table
update_stats_table({})

root.mainloop()