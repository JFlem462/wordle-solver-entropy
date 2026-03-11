# wordle-solver-entropy
A Wordle solver program made in Python that calculates the entropy, or uncertainty, or each word and decreases the possible word list to find the best answer.

# Wordle Solver Using Shannon Entropy  
*A computational approach to optimal guessing strategies in Wordle*

## Overview
This project implements a entropy-based algorithm designed to choose guesses that maximize information gain and minimize the number of attempts needed to find the secret word.

The solver uses probability distributions, pattern analysis, and entropy calculations to intelligently narrow down the search space after each guess.

The program supports:
- Entropy‑based ranking of optimal opening guesses  
- Interactive feedback entry (Green = 2/Yellow = 1/Gray = 0)  
- Dynamic pruning of the candidate word list  
- Probability updates based on eliminated letters  
- A full Wordle gameplay loop with up to six attempts  

---

## How It Works

### **1. Entropy‑Driven Guess Selection**
For each possible guess, the solver:
- Computes all possible feedback patterns against remaining candidate words  
- Calculates the Shannon entropy of the distribution  
- Ranks guesses by expected information gain  

This ensures each guess reduces uncertainty as efficiently as possible.

### **2. Wordle Pattern Simulation**
The function `wordle_pattern(guess, secret)` generates Wordle‑style feedback:
- **2** = Green (correct letter, correct position)  
- **1** = Yellow (correct letter, wrong position)  
- **0** = Black/Gray (letter not in word)  

### **3. Candidate Filtering**
After each guess, the solver removes words that cannot match the feedback pattern using `update_word_list()`.

### **4. Probability Updates**
Letters marked as absent (Gray) are removed from the probability distribution, and remaining probabilities are renormalized.

---

## 📂 Project Structure

```
final_wordle/
│── final_wordle.py
│── wordle_words_large.txt
│── README.md  ← (this file)
```

---

## 🚀 Features

- **Entropy‑based optimal guessing**
- **Interactive gameplay**
- **Automatic elimination of impossible words**
- **Dynamic probability updates**
- **Top‑N recommended opening guesses**
- **Modular, readable Python code**

---

## 🛠️ Technologies Used

- **Python**
- **NumPy**
- **math / log2 entropy calculations**
- **Counter from collections**
- **CSV and file handling utilities**

---

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wordle-entropy-solver.git
   cd wordle-entropy-solver
   ```

2. Ensure the word list file `wordle_words_large.txt` is in the same directory.

3. Run the solver:
   ```bash
   python final_wordle.py
   ```

4. Follow the on‑screen prompts:
   - Enter your guess  
   - Enter feedback for each letter (0 = Gray, 1 = Yellow, 2 = Green)  
   - Receive updated entropy scores and recommended guesses  

---

## 📊 Example Output

```
=====WORDLE SOLVER=====
Total Possibilities: 2315, 11.18 bits
Word   H[word]  P(word]
['raise', 5.42, 0.0004]
['slate', 5.40, 0.0004]
['crate', 5.38, 0.0004]
...
Enter a five letter word:
```

---

## What I Learned
This project strengthened several core computational and mathematical skills:
Information Theory in Practice
I applied Shannon entropy to evaluate how much information each guess provides. This helped me understand entropy not just as a formula, but as a practical tool for decision‑making.

### Algorithm Design & Optimization
Building the solver required:
- Designing efficient pattern‑matching logic
- Reducing the search space intelligently
- Ranking guesses based on expected information gain
This deepened my understanding of algorithmic efficiency and search strategies.

### Probability Modeling
I implemented dynamic probability updates by removing eliminated letters and renormalizing distributions. This reinforced concepts in probability, uncertainty, and Bayesian‑style updating.
Data Structures & Python Engineering
Working with:
- Counter for pattern frequencies
- List comprehensions
- Modular function design
- File handling and word‑list processing helped me write cleaner, more maintainable code.

### Human‑Computer Interaction
The interactive feedback loop required designing a user‑friendly interface for entering Wordle clues, validating input, and presenting results clearly.

---

## 📚 Future Improvements

- Add GUI interface  
- Add simulation mode for automated testing  
- Visualize entropy reduction across guesses  
- Integrate alternative scoring heuristics  
- Add support for hard mode constraints  

---

## 🤝 Acknowledgments
This project was developed as part of an Independent Study about Entropy and information theory. 
