import random
import numpy as np
import matplotlib.pyplot as plt


class EloPlayer:
    def __init__(self, initial_rating=1500):
        self.rating = initial_rating
        self.rating_history = [initial_rating]
        self.matches_played = 0

    def expected_score(self, opponent_rating):
        """Calculate expected score against an opponent."""
        return 1 / (1 + 10 ** ((opponent_rating - self.rating) / 400))

    def update_rating(self, opponent_rating, actual_score, k_factor=32):
        """Update player's rating based on match result."""
        expected_score = self.expected_score(opponent_rating)
        rating_change = k_factor * (actual_score - expected_score)

        # Dynamically adjust K-factor based on number of matches
        # if self.matches_played < 10:
        #     rating_change *= 2  # More volatile ratings for new players

        self.rating += rating_change
        self.rating_history.append(self.rating)
        self.matches_played += 1
        return rating_change


class MatchmakingSystem:
    def __init__(self, players, rating_range_percentage=0.2):
        """
        Initialize matchmaking system
        :param players: List of players
        :param rating_range_percentage: Percentage of rating to use as matchmaking range
        """
        self.players = players
        self.rating_range_percentage = rating_range_percentage

    def find_match(self, player):
        """
        Find a suitable opponent for a given player
        Prioritizes players within a certain rating range
        """
        # Calculate rating range
        min_rating = player.rating * (1 - self.rating_range_percentage)
        max_rating = player.rating * (1 + self.rating_range_percentage)

        # Filter potential opponents
        potential_opponents = [
            p
            for p in self.players
            if p != player and min_rating <= p.rating <= max_rating
        ]

        # If no opponents in range, expand search
        if not potential_opponents:
            potential_opponents = [p for p in self.players if p != player]

        # Choose opponent
        return random.choice(potential_opponents)


def simulate_match(player1, player2):
    """Simulate a match between two players."""
    # Use expected score as probability of winning
    expected_score1 = player1.expected_score(player2.rating)

    # Simulate match outcome with some randomness
    random_value = random.random()

    if random_value < expected_score1:
        player1.update_rating(player2.rating, 1)
        player2.update_rating(player1.rating, 0)
        return 1  # Player 1 wins
    else:
        player1.update_rating(player2.rating, 0)
        player2.update_rating(player1.rating, 1)
        return 2  # Player 2 wins


def monte_carlo_elo_simulation(num_players=50, num_matches=10000, initial_rating=1500):
    """Run a Monte Carlo simulation of an Elo rating system with matchmaking."""
    # Create players
    players = [
        EloPlayer(initial_rating)
        for _ in range(num_players)
    ]

    # Create matchmaking system
    matchmaker = MatchmakingSystem(players)

    # Simulation results tracking
    match_results = []

    # Run matches
    for _ in range(num_matches):
        # Find suitable opponents using matchmaking
        p1 = random.choice(players)
        p2 = matchmaker.find_match(p1)

        # Simulate match
        winner = simulate_match(p1, p2)
        match_results.append(winner)

    return players, match_results


def plot_rating_analysis(players):
    """Comprehensive visualization of rating dynamics."""
    plt.figure(figsize=(15, 10))

    # Rating Histories
    plt.subplot(2, 2, 1)
    for player in players:
        plt.plot(player.rating_history, alpha=0.3)
    plt.title("Player Rating Histories")
    plt.xlabel("Matches")
    plt.ylabel("Elo Rating")

    # Final Rating Distribution
    plt.subplot(2, 2, 2)
    final_ratings = [player.rating for player in players]
    plt.hist(final_ratings, bins=20, edgecolor="black")
    plt.title("Final Rating Distribution")
    plt.xlabel("Elo Rating")
    plt.ylabel("Number of Players")

    # Rating Volatility
    plt.subplot(2, 2, 3)
    volatilities = [np.std(player.rating_history) for player in players]
    plt.hist(volatilities, bins=20, edgecolor="black")
    plt.title("Player Rating Volatility")
    plt.xlabel("Rating Standard Deviation")
    plt.ylabel("Number of Players")

    # Matches Played Distribution
    plt.subplot(2, 2, 4)
    matches_played = [player.matches_played for player in players]
    plt.hist(matches_played, bins=20, edgecolor="black")
    plt.title("Matches Played Distribution")
    plt.xlabel("Number of Matches")
    plt.ylabel("Number of Players")

    plt.tight_layout()
    plt.show()


# Run the simulation
random.seed(42)
players, match_results = monte_carlo_elo_simulation(
    num_players=1000, num_matches=100000
)

# Analyze and plot results
plot_rating_analysis(players)

# Print summary statistics
final_ratings = [player.rating for player in players]
print("Elo Rating Statistics:")
print(f"Mean Rating: {np.mean(final_ratings):.2f}")
print(f"Median Rating: {np.median(final_ratings):.2f}")
print(f"Standard Deviation: {np.std(final_ratings):.2f}")
print(f"Minimum Rating: {min(final_ratings):.2f}")
print(f"Maximum Rating: {max(final_ratings):.2f}")

# Print top and bottom rated players
sorted_players = sorted(players, key=lambda x: x.rating, reverse=True)
print("\nTop 5 Players:")
for i, player in enumerate(sorted_players[:5], 1):
    print(f"{i}. Rating: {player.rating:.2f}, Matches: {player.matches_played}")

print("\nBottom 5 Players:")
for i, player in enumerate(sorted_players[-5:], 1):
    print(f"{i}. Rating: {player.rating:.2f}, Matches: {player.matches_played}")
