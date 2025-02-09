#Name:Alakhdeep Sandhu
#Date:27th November, 2024
#POCO LOCO GAME


import random
#importing time module to  allow pauses
import time 

# Function to display the rules
def rules_list_display():
    print("\n" + "*"*52)
    print("*" + " " * 50 + "*")
    print("*{:^50}*".format("POCO LOCO"))
    print("*" + " " * 50 + "*")
    print("*" + "*"*50 + "*")
    print("Rules of the Game:")
    print("- The game is played with chips. Each \
player starts with the same number of chips.")
    print("- The goal is to lose all your chips as quickly as possible.")
    print("- Players take turns rolling three dice. \
You can roll up to three times in a turn.")
    print("- Dice rolls are scored as follows:")
    print("  > PoCo! (4, 5, 6): Highest score, \
gives 4 chips to the loser of the round.")
    print("  > Three-of-a-kind (e.g., 6, 6, 6 or 5,5,5): \
Second highest, gives 3 chips to the loser.")
    print("  > Loco! (1, 2, 3): Third highest, \
gives 2 chips to the loser.")
    print("  > Other rolls are scored based on the \
dice values (e.g., 1 = 100 points, 2 = 2 points, "
          "3 = 3 points, 4 = 4 points, 5 = 5 points, 6 = 60 points).")
    print("- If there is a tie for the \
lowest score, one of the tied players is chosen randomly as the loser.")
    print("- Opponents (computer players) use \
strategy to decide how many times to roll.")
    print("- The next player in a round cannot \
roll more times than the previous player.")
    print("- The game ends when a player loses \
all their chips. The first player to do so wins!")
    print("- Recommendation: I recommend using low \
number of starting chips as the game can be quite long, e.g., 5 or 10.")
    print("- Enjoy the game!\n")

# Function to roll three dice
def roll_dice():
    return [random.randint(1, 6) for i in range(3)]

# Function to draw dice
def draw_dice(dice):
    dice_faces = {
        1: [" ----- ", "|     |", "|  o  |", "|     |", " ----- "],
        2: [" ----- ", "|o    |", "|     |", "|    o|", " ----- "],
        3: [" ----- ", "|o    |", "|  o  |", "|    o|", " ----- "],
        4: [" ----- ", "|o   o|", "|     |", "|o   o|", " ----- "],
        5: [" ----- ", "|o   o|", "|  o  |", "|o   o|", " ----- "],
        6: [" ----- ", "|o   o|", "|o   o|", "|o   o|", " ----- "]
    }
# Print dice numbers for clarity
    print(f"Dice rolled: {dice}")
    lines = [""] * 5
    for die in dice:
        face = dice_faces[die]
        for i in range(5):
            lines[i] += face[i] + "  "
    for line in lines:
        print(line)

# Function to calculate the score of a roll
# Note: The first three cases don't have actual "scores",
# These are numbers that have been assigned to refer to our three special cases
# which will allow us to give chips to losing players
def calculate_score(roll):
    roll.sort()
# PoCo!
    if roll == [4, 5, 6]:
        return 1000
# Three-of-a-kind
    elif roll[0] == roll[1] == roll[2]:
        return 900 + roll[0]
# Loco!
    elif roll == [1, 2, 3]:
        return 800
    else:
#For the other dice combinations we calculate the score by summing dice values.
        return sum(
            (100 if die == 1 else 2 if die == 2 else 3 if die == 3 else
             4 if die == 4 else 5 if die == 5 else 60)
            for die in roll
        )

# Function to play a turn
def play_turn(player_name, is_player, max_rolls):
    rolls = []
# Maximum rolls determined by previous player
    for i in range(1, max_rolls + 1):
        roll = roll_dice()
        print(f"{player_name} rolled:")
# Display dice with ASCII art and numbers
        draw_dice(roll)
# Pause after each dice roll for clarity
        time.sleep(3)
        rolls.append(roll)
        if i < max_rolls:
            if is_player:
# Ensure the player enters only 'y' or 'n'
                while True:
                    choice = input(f"{player_name}, do you \
want to roll again? (y/n): ").lower()
                    if choice in ["y", "n"]:
                        break
                    else:
                        print("Invalid input. Please \
enter 'y' for yes or 'n' for no.")
                if choice != "y":
                    break
            else:
# Opponent strategy
                current_score = calculate_score(roll)
# High score, stop rolling
                if current_score >= 700:
                    break
# Low score after 2 rolls, take a risk
                elif i == 2 and current_score < 200:
                    continue
# Random decision for other cases
                else:  
                    if random.choice([True, False]):
                        break
    return calculate_score(rolls[-1]), len(rolls)

# Function to resolve a round
def resolve_round(players, scores):
# Find the lowest score
    lowest_score = min(scores.values())
    tied_players = [player for player, \
                    score in scores.items() if score == lowest_score]

# Resolve tie by choosing a random player from the tied players
    if len(tied_players) > 1:
        print(f"Tie for the lowest \
score between: {', '.join(tied_players)}")
        loser = random.choice(tied_players)
        print(f"{loser} is randomly chosen as the loser.")
    else:
        loser = tied_players[0]

# Find the highest score
    highest_player = max(scores, key=scores.get)
    highest_score = scores[highest_player]

# Determine chips to give based on the highest "score"
#(refer to earlier Note)
    if highest_score == 1000:
        chips_to_give = 4
    elif 900 <= highest_score < 1000:
        chips_to_give = 3
    elif highest_score == 800:
        chips_to_give = 2
    else:
        chips_to_give = 1

# Update chip counts
    for player in players:
        if player != loser:
            players[player] -= chips_to_give
            players[loser] += chips_to_give
# Return winner and loser of the round
    return highest_player, loser

# Main game loop
def start_game():
    rules_list_display()
    player_name = input("Enter your name: ")
    chip_count = int(input("Enter the number \
of chips each player starts with: "))

# Use dictionaries to track players and their chip counts
    players = {
        player_name: chip_count,
        "Jason": chip_count,
        "Sam": chip_count,
    }

    round_number = 1

    while True:
        print(f"\n+{'-'*12}+")
        print(f"|  Round {round_number}  |")
        print(f"+{'-'*12}+")

        print("\nPlayer chip counts:")
        for player, chips in players.items():
            print(f"{player}: {chips} chips")

# Randomize turn order
        turn_order = list(players.keys())
        random.shuffle(turn_order)

        scores = {}
        
# Allow first player to roll up to 3 times
        previous_rolls = 3
        for i in range(len(turn_order)):
            player = turn_order[i]
            print(f"\n{player}'s turn:")
            score, rolls_taken\
                   = play_turn(player, player == player_name, previous_rolls)
            scores[player] = score
# Update maximum rolls for the next player
            previous_rolls = rolls_taken
# Print next turn message for everyone except last player
            if i != len(turn_order) - 1:  
                print("\nNext player's turn is coming...")
# Pause for 5 seconds
                time.sleep(5)

        highest_player, loser = resolve_round(players, scores)

# Display round winner and loser
        print(f"\nRound {round_number} Winner: {highest_player}")
        print(f"Round {round_number} Loser: {loser}")

# Check for a winner
        for player, chips in players.items():
            if chips <= 0:
                print("\nFinal Scores:")
                for p, c in players.items():
                    print(f"{p}: {c} chips")
                print(f"\n{player} wins the game!")
                return

        while True:
            continue_game = input("\nWould you like \
to continue to the next round? (y/n): ").lower()
            if continue_game in ["y", "n"]:
                break
            else:
                print("Invalid input. \
Please enter 'y' for yes or 'n' for no.")

        if continue_game != "y":
            print("Thanks for playing PoCo Loco!")
            break

        round_number += 1

# Start the game
start_game()

