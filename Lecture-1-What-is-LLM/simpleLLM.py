# A slightly more advanced conceptual model of an LLM,
# inspired by the idea of an LSTM.

# -----------------------------------------------------------------------------------
## 1. The "Training Data"
# This time, our "knowledge" will be based on *phrases*, not just single words.
# This helps our "LLM" remember the context.
# Key is a tuple (a sequence of words), and value is a list of possible next words.

training_data = {
    # Sholay Dialogue
    ("kitne", "aadmi"): ["the?"],
    ("kitne", "aadmi", "the?"): ["Sardar", "do", "the."],
    
    # Om Shanti Om Dialogue
    ("ek", "chutki", "sindoor"): ["ki"],
    ("sindoor", "ki", "keemat"): ["tum", "kya", "jaano"],
    ("tum", "kya", "jaano"): ["Ramesh", "Babu."],
    
    # DDLJ Dialogue
    ("bade", "bade", "deshon"): ["mein"],
    ("deshon", "mein", "aisi"): ["choti"],
    ("aisi", "choti", "choti"): ["baatein"],
    ("choti", "choti", "baatein"): ["hoti", "rehti", "hai", "Senorita."],
    
    # 3 Idiots Dialogue
    ("all", "izz"): ["well!"],
    ("dost", "fail"): ["ho"],
    ("dost", "fail", "ho"): ["jaye"],
    ("jaye", "toh"): ["dukh"],
    ("dukh", "hota"): ["hai."],
    
    # More general phrases
    ("pani", "puri"): ["khana"],
    ("chai", "garam"): ["hai"],
    ("mera", "naam"): ["Amit", "Rohan"],
    ("mera", "naam", "hai"): ["Amit", "Rohan"]
}

# -----------------------------------------------------------------------------------
## 2. The "LLM" (A more sophisticated class)
# This class mimics the "sequence memory" of an LSTM.
# It doesn't just look at the last word; it looks at the last *few* words
# to make a better prediction.

import random

class SequenceLLM:
    """
    A conceptual model with 'sequence memory'.
    It uses a history of words to make more contextual predictions.
    """
    def __init__(self, training_data, history_size=3):
        self.training_data = training_data
        self.history_size = history_size

    def generate_text(self, starting_text, max_length=15):
        """
        Generates text by predicting the next word based on a sequence.
        """
        # Start the sequence with the user's input, converting to a list of words
        sequence = starting_text.lower().replace('.', '').replace('?', '').split()
        
        # Loop to generate new words
        for _ in range(max_length):
            # Get the most recent words to use for prediction
            # This is our 'memory' or 'context'
            context = tuple(sequence[-self.history_size:])
            
            # Try to find this context phrase in our "training data"
            if context in self.training_data:
                # If found, get the list of possible next words
                possible_next_words = self.training_data[context]
                
                # Randomly pick the next word
                next_word = random.choice(possible_next_words)
                
                # Add the predicted word to our sequence
                sequence.append(next_word)
            else:
                # If the current sequence is not in our data, we fall back to a smaller context
                # This is a simple form of "attention"
                context = tuple(sequence[-1:])
                if context in self.training_data:
                    next_word = random.choice(self.training_data[context])
                    sequence.append(next_word)
                else:
                    # If we can't find any context, we stop.
                    print("\n--- [I'm stuck! My knowledge is limited.] ---")
                    break
        
        # Join the list back into a sentence
        return " ".join(sequence)

# -----------------------------------------------------------------------------------
## 3. The Interactive Demonstration for Students

# Let's create our "LLM brain"  
my_llm = SequenceLLM(training_data)

print("नमस्ते! Let's play a game. I'll start a famous dialogue, and you'll guess what comes next.")
print("Then, we'll see how my simple 'LLM brain' completes it, using a bit of 'memory'.\n")

print("---------------------------------------------------------------------------------")
# Example 1: Sholay Dialogue
input_dialogue = "Kitne aadmi"
print(f"**Your Turn!** What comes after '{input_dialogue}'?")
print("Wait for the 'LLM' to respond...")
output_text = my_llm.generate_text(input_dialogue, max_length=5)
print(f"My LLM says: '{output_text}'")
print("-" * 75)

# Example 2: DDLJ Dialogue
input_dialogue = "Bade bade deshon mein"
print(f"**Your Turn!** What comes after '{input_dialogue}'?")
print("Wait for the 'LLM' to respond...")
output_text = my_llm.generate_text(input_dialogue, max_length=10)
print(f"My LLM says: '{output_text}'")
print("-" * 75)

# Example 3: General phrase, to show it's not just dialogues
input_dialogue = "chai"
print(f"**Your Turn!** What comes after '{input_dialogue}'?")
print("Wait for the 'LLM' to respond...")
output_text = my_llm.generate_text(input_dialogue, max_length=5)
print(f"My LLM says: '{output_text}'")
print("-" * 75)