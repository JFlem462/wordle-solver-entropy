import os
import sys
import subprocess
from pathlib import Path
import csv
import numpy as np
import math
from collections import Counter

#Intitialized Arrays, letters, probabilities, and morse code
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

#Define probabilities for each letter. (in text.) ("W" = 2.4-0.119 because the probabilities must sum to 1.)
probabilities = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 2.4, 6.7, 7.5, 1.9, 0.095, 6.0, 6.3, 9.1, 2.8, 0.98, 2.281, 0.15, 2.0, 0.074]

p=[values /100 for values in probabilities]

# Designing a Wordle Solver with Shannon Entropy: 
# Algorithms and Performance Analysis

def makeWordList(file_path):
    with open(file_path, 'r') as file:
        # Read each line and strip newline characters
        words = [line.strip() for line in file]

    return words


def compute_word_stats(wordList, letters, p):
    result = []

    for word in wordList:
        # compute probability score
        prob_sum = round((1/len(wordList)),4)

        # compute entropy score
        # NEW METHOD FOR ENTROPY SUM
        wordEntropy = compute_entropy(word, wordList)

        # append [word, entropy, probability]
        result.append([word, round(wordEntropy,4), round(prob_sum, 4)])

    
    sorted_result = sorted(result, reverse=True, key=lambda x: x[1])
    return sorted_result

def wordle_pattern(guess, secret):
    # Simplified Wordle feedback generator
    result = []
    secret_counts = Counter(secret)

    # First pass: greens
    for i, ch in enumerate(guess):
        if secret[i] == ch:
            result.append('G')
            secret_counts[ch] -= 1
        else:
            result.append(None)

    # Second pass: yellows and blacks
    for i, ch in enumerate(guess):
        if result[i] is None:
            if secret_counts[ch] > 0:
                result[i] = 'Y'
                secret_counts[ch] -= 1
            else:
                result[i] = 'B'
    return ''.join(result)

def compute_entropy(guess, possible_answers):
    N = len(possible_answers)
    pattern_counts = Counter(wordle_pattern(guess, secret) for secret in possible_answers)

    entropy = 0.0
    for count in pattern_counts.values():
        p = count / N
        entropy -= p * math.log2(p)
    return entropy

def compute_entropy_guess(info):
    entropyGuess = 0.0
    for i in range(len(info)):
        if info[i][1] == 1 or info[i][1] == 2:
            entropyGuess = entropyGuess + (p[letters.index(info[i][0])] * -math.log2(p[letters.index(info[i][0])]))
    return entropyGuess
    
        

def opening_guesses(wordList, n, letters, p):
    stats = compute_word_stats(wordList, letters, p)
    TotalPos = 0.0
    for i in range (len(wordList)):
        TotalPos = TotalPos + (-(1/len(wordList)) * math.log2((1/len(wordList))))
    print(f"Total Possibilities: {len(wordList)}, {round(TotalPos,2)} bits")
    print("Word   H[word]  P(word]")
    for item in stats[:n]:
        print(item)


def guess_information(guess):
    print("Enter the following information for each letter in your guess")
    print("0 = letter not in answer. (GRAY)")
    print("1 = letter in answer. (YELLOW)")
    print("2 = letter in answer. Correct position. (GREEN)")
    guessLetters = list(guess)
    InfoCombo = []
    for l in range(len(guessLetters)):
        infoLetter = int(input(f"Enter the information for {guessLetters[l]}: "))
        if infoLetter > 2 or infoLetter < 0:
            raise ValueError("Information must be either 0, 1, or 2.")
        else:
            InfoCombo.append([guessLetters[l], infoLetter])
    print(InfoCombo)
    print(f"{guess}: {compute_entropy_guess(InfoCombo)} bits")
    return InfoCombo
        

def removing_letters(info):
    #Looks at the letters entered and the information about the guess.
    #Info, 0= letter not in answer, 1= letter in answer, 2=letter in answer, correct position
    eliminated_letters = []
    for x in range(len(info)):
        letterCheck = info[x][0]
        if info[x][1] == 0:
            eliminated_letters.append(letterCheck)
    print(eliminated_letters)
    return eliminated_letters

def update_probabilities(letters, probs, eliminated_letters):
    # Step 1: Filter out eliminated letters
    new_letters = []
    new_probs = []
    
    for letter, p in zip(letters, probs):
        if letter not in eliminated_letters:
            new_letters.append(letter)
            new_probs.append(p)

    # Step 2: Renormalize so probabilities sum to 1
    total = sum(new_probs)
    new_probs = [p / total for p in new_probs]

    return new_letters, new_probs

def update_word_list(word_list, guess_feedback):
    new_list = []
    guess = ''.join([ch for ch, _ in guess_feedback])  # reconstruct guess word

    for word in word_list:
        valid = True
        for i, (ch, fb) in enumerate(guess_feedback):
            if fb == 0:
                # Letter not in answer at all
                if ch in word:
                    valid = False
                    break
            elif fb == 1:
                # Letter must be in word but not at this position
                if ch not in word or word[i] == ch:
                    valid = False
                    break
            elif fb == 2:
                # Letter must be in correct position
                if word[i] != ch:
                    valid = False
                    break
        if valid:
            new_list.append(word)
    return new_list


def playGame(word_list):
    global letters, p      # ensure you're modifying globals
    
    playGame = True
    tries = 0

    print("=====WORDLE SOLVER=====")

    while playGame and (tries < 6):
        opening_guesses(word_list, 10, letters, p)
        word_input = input("Enter a five letter word: ")

        if word_input not in word_list:
            print(f"{word_input} is not a valid word.")
            continue

        info = guess_information(word_input)
        elimLetters = removing_letters(info)

        # Update probabilities correctly
        letters, p = update_probabilities(letters, p, elimLetters)

        # Update candidate word list
        word_list = update_word_list(word_list, info)

        tries += 1

            
    
if __name__ == "__main__":
    current_dir = Path(__file__).parent
    word_list_file = current_dir / 'wordle_words_large.txt'
    
    if not makeWordList:
        print(f"Word list file not found: {word_list_file}")
        sys.exit(1)
    
    word_list = makeWordList(word_list_file)
    print(f"Loaded {len(word_list)} words from the word list.")
    playGame(word_list)

        
        
            
            
        
