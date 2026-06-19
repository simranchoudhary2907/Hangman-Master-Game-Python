import random

# ==========================
# WORD CATEGORIES
# ==========================
WORD_BANK = {
    "Programming": [
        "python", "compiler", "function",
        "variable", "algorithm"
    ],

    "Technology": [
        "computer", "network", "database",
        "software", "hardware"
    ],

    "Cyber Security": [
        "security", "firewall",
        "encryption", "malware", "hacker"
    ]
}

# ==========================
# HANGMAN DRAWINGS
# ==========================
HANGMAN_PICS = [
"""
 +---+
 |   |
     |
     |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
     |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
 |   |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
/|   |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
/|\\  |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
/|\\  |
/    |
     |
=========
""",
"""
 +---+
 |   |
 O   |
/|\\ |
/ \\ |
     |
=========
"""
]

# ==========================
# DIFFICULTY
# ==========================
def get_difficulty():

    while True:

        print("\n===== Select Difficulty =====")
        print("1. Easy   (6 Lives, 2 Hints)")
        print("2. Medium (5 Lives, 1 Hint)")
        print("3. Hard   (4 Lives, 0 Hints)")

        choice = input("Enter choice (1/2/3): ")

        if choice == "1":
            return 6, 2 , "1"

        elif choice == "2":
            return 5, 1, "2"

        elif choice == "3":
            return 4, 0 , "3"

        else:
            print("Invalid choice. Try again.")


# ==========================
# DISPLAY WORD
# ==========================
def display_word(word, guessed_letters):

    display = []

    for letter in word:

        if letter in guessed_letters:
            display.append(letter)

        else:
            display.append("_")

    return " ".join(display)


# ==========================
# HINT FUNCTION
# ==========================
def give_hint(word, guessed_letters):

    remaining = []

    for letter in word:

        if letter not in guessed_letters:
            remaining.append(letter)

    if remaining:
        return random.choice(remaining)

    return None


# ==========================
# MAIN GAME
# ==========================

def get_initial_letters(word, difficulty):

    revealed = set()

    # Easy Mode -> Reveal 2 random letters
    if difficulty == "1":

        letters = random.sample(list(set(word)), min(2, len(set(word))))

        for letter in letters:
            revealed.add(letter)

    # Medium Mode -> Reveal first letter
    elif difficulty == "2":

        revealed.add(word[0])

    # Hard Mode -> Reveal nothing
    elif difficulty == "3":
        pass

    return revealed



def play_game():

    score = 0
    streak = 0
    best_streak = 0

    achievements = []

    print("""
========================================
           HANGMAN MASTER
========================================
Guess the hidden word
Earn achievements
Build winning streaks
========================================
""")

    while True:

        category = random.choice(list(WORD_BANK.keys()))
        secret_word = random.choice(WORD_BANK[category])

        lives, hints_left, difficulty = get_difficulty()

        original_hints = hints_left

        guessed_letters = get_initial_letters(
            secret_word,
            difficulty
        )

        print("\nGame Started!")
        print(f"Category: {category}")

        max_lives = lives

        while lives > 0:

            wrong_guesses = max_lives - lives

            if wrong_guesses > 6:
                wrong_guesses = 6

            print(HANGMAN_PICS[wrong_guesses])

            print(f"Category: {category}")
            print(f"Word: {display_word(secret_word, guessed_letters)}")
            print("Lives:", "❤️ " * lives)
            print(f"Hints Left: {hints_left}")

            if guessed_letters:
                print("Guessed Letters:",
                      ", ".join(sorted(guessed_letters)))
            else:
                print("Guessed Letters: None")

            guess = input(
                "\nEnter a letter (or type 'hint'): "
            ).lower().strip()

            # ------------------
            # Hint
            # ------------------
            if guess == "hint":

                if hints_left > 0:

                    hint_letter = give_hint(
                        secret_word,
                        guessed_letters
                    )

                    if hint_letter:
                        guessed_letters.add(hint_letter)
                        hints_left -= 1

                        print(
                            f"💡 Hint Revealed: {hint_letter}"
                        )

                else:
                    print("❌ No hints left!")

                continue

            # ------------------
            # Validation
            # ------------------
            if len(guess) != 1 or not guess.isalpha():
                print("Enter only one letter.")
                continue

            if guess in guessed_letters:
                print("Already guessed!")
                continue

            guessed_letters.add(guess)

            # ------------------
            # Correct Guess
            # ------------------
            if guess in secret_word:

                print("✅ Correct Guess!")

            else:

                lives -= 1

                print("❌ Wrong Guess!")

            # ------------------
            # Win Condition
            # ------------------
            if all(
                letter in guessed_letters
                for letter in secret_word
            ):

                print("\n🎉 CONGRATULATIONS!")
                print(f"You guessed the word: {secret_word}")

                score += 1

                streak += 1

                if streak > best_streak:
                    best_streak = streak

                # Achievements

                if "🏆 First Win" not in achievements:
                    achievements.append("🏆 First Win")

                if (
                    hints_left == original_hints
                    and
                    "🏆 Won Without Using Hint"
                    not in achievements
                ):
                    achievements.append(
                        "🏆 Won Without Using Hint"
                    )

                if (
                    score >= 5
                    and
                    "🏆 5 Wins Achieved"
                    not in achievements
                ):
                    achievements.append(
                        "🏆 5 Wins Achieved"
                    )

                break

        # ------------------
        # Lose Condition
        # ------------------
        else:

            print(HANGMAN_PICS[-1])

            print("\n💥 GAME OVER!")
            print(f"The word was: {secret_word}")

            streak = 0

        # ------------------
        # Stats
        # ------------------
        print("\n========== STATS ==========")

        print(f"Score: {score}")
        print(f"Current Streak: {streak}")
        print(f"Best Streak: {best_streak}")

        if achievements:

            print("\nAchievements Unlocked:")

            for achievement in achievements:
                print(achievement)

        print("===========================")

        # ------------------
        # Play Again
        # ------------------
        play_again = input(
            "\nDo you want to play again? (yes/no): "
        ).lower().strip()

        if play_again not in ["yes", "y"]:

            print("\nThanks for Playing!")

            print(f"Final Score: {score}")
            print(f"Best Streak: {best_streak}")

            break


# ==========================
# START GAME
# ==========================
if __name__ == "__main__":
    play_game()



