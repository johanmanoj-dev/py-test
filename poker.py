import random
import itertools
from collections import Counter

class Card:
    """Represents a standard playing card."""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.rank_value = self._get_rank_value()

    def _get_rank_value(self):
        """Assigns a numerical value to a card's rank."""
        if self.rank in 'TJQKA':
            return {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[self.rank]
        return int(self.rank)

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    """Represents a deck of 52 playing cards."""
    def __init__(self):
        suits = '♠♥♦♣'
        ranks = '23456789TJQKA'
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def deal(self, num_cards):
        """Deals a specified number of cards from the deck."""
        if len(self.cards) < num_cards:
            raise ValueError("Not enough cards in the deck to deal.")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

class Player:
    """Represents a player in the poker game."""
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False

    def bet(self, amount):
        """Places a bet."""
        if amount > self.chips:
            amount = self.chips # All-in
        self.chips -= amount
        self.current_bet += amount
        if self.chips == 0:
            self.is_all_in = True
        return amount

    def reset_for_new_round(self):
        """Resets player status for a new round."""
        self.hand = []
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False

    def __repr__(self):
        return f"{self.name} ({self.chips} chips)"

class PokerGame:
    """Manages the logic of a Texas Hold'em poker game."""
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.dealer_button = random.randint(0, len(self.players) - 1)

    def _evaluate_hand(self, hand):
        """
        Evaluates a 7-card hand and returns its rank and the best 5-card combination.
        Returns a tuple: (rank_value, best_5_cards).
        Rank values: 9 (Royal Flush) down to 1 (High Card).
        """
        all_cards = sorted(hand, key=lambda card: card.rank_value, reverse=True)
        
        # Generate all possible 5-card combinations
        best_hand_rank = (-1, [])
        for combo in itertools.combinations(all_cards, 5):
            combo = sorted(list(combo), key=lambda c: c.rank_value, reverse=True)
            ranks = [c.rank_value for c in combo]
            suits = [c.suit for c in combo]
            rank_counts = Counter(ranks)
            
            is_flush = len(set(suits)) == 1
            # Check for straight: five consecutive ranks
            is_straight = len(set(ranks)) == 5 and (max(ranks) - min(ranks) == 4)
            # Ace-low straight (A-2-3-4-5)
            if not is_straight and set(ranks) == {14, 2, 3, 4, 5}:
                is_straight = True
                # Reorder ranks for correct sorting: A, 5, 4, 3, 2
                ranks = [5, 4, 3, 2, 14] 
                combo = sorted(combo, key=lambda c: ranks.index(c.rank_value))

            # Determine hand rank
            hand_rank = 0
            sorted_by_count = sorted(rank_counts.items(), key=lambda item: (item[1], item[0]), reverse=True)
            counts = [c[1] for c in sorted_by_count]
            hand_values = [c[0] for c in sorted_by_count]

            if is_straight and is_flush:
                hand_rank = 9 if ranks[0] == 14 else 8 # Royal Flush or Straight Flush
            elif counts[0] == 4: # Four of a Kind
                hand_rank = 7
            elif counts[:2] == [3, 2]: # Full House
                hand_rank = 6
            elif is_flush:
                hand_rank = 5
            elif is_straight:
                hand_rank = 4
            elif counts[0] == 3: # Three of a Kind
                hand_rank = 3
            elif counts[:2] == [2, 2]: # Two Pair
                hand_rank = 2
            elif counts[0] == 2: # One Pair
                hand_rank = 1
            else: # High Card
                hand_rank = 0
            
            # Compare with the best hand found so far
            current_hand_score = (hand_rank, hand_values)
            best_rank_score = (best_hand_rank[0], [c.rank_value for c in best_hand_rank[1]])
            if current_hand_score > best_rank_score:
                best_hand_rank = (hand_rank, combo)
                
        return best_hand_rank

    def _get_player_action(self, player, current_bet):
        """Gets an action from the player."""
        while True:
            action_prompt = f"{player.name} ({player.chips} chips), your turn. Current bet is {current_bet}. "
            action_prompt += f"You have already bet {player.current_bet}. "
            
            valid_actions = ["fold", "check"]
            if player.chips > 0:
                valid_actions.extend(["call", "bet"])
            
            if current_bet == 0 or player.current_bet == current_bet:
                action_prompt += "You can 'check', 'bet', or 'fold': "
            else:
                call_amount = min(current_bet - player.current_bet, player.chips)
                action_prompt += f"You can 'call' ({call_amount}), 'raise', or 'fold': "
            
            action = input(action_prompt).lower().strip()
            
            if action == 'fold':
                player.is_folded = True
                return None, 0
            
            if action == 'check':
                if player.current_bet < current_bet:
                    print("You can't check, there is a bet to you. Please 'call', 'raise', or 'fold'.")
                    continue
                return 'check', 0
            
            if action == 'call':
                call_amount = min(current_bet - player.current_bet, player.chips)
                return 'call', call_amount
                
            if action in ['bet', 'raise']:
                if player.chips <= (current_bet - player.current_bet):
                    print("You don't have enough chips to raise. You can only call or fold.")
                    continue
                while True:
                    try:
                        amount_str = input(f"Enter amount to {'bet' if action == 'bet' else 'raise'}: ")
                        amount = int(amount_str)
                        if action == 'bet' and amount < 20: # Minimum bet
                            print("Minimum bet is 20.")
                        elif action == 'raise' and amount < current_bet:
                            print(f"You must raise by at least the current bet of {current_bet}.")
                        elif amount > player.chips:
                             print("You don't have enough chips.")
                        else:
                            return 'raise', amount
                    except ValueError:
                        print("Invalid amount. Please enter a number.")

    def _run_betting_round(self, start_index):
        """Manages a single round of betting."""
        current_bet = 0
        last_raiser = None
        players_in_round = [p for p in self.players if not p.is_folded and not p.is_all_in]
        
        # Reset current bets for the round
        for p in self.players:
            p.current_bet = 0

        active_players = len(players_in_round)
        current_player_index = start_index % len(self.players)
        
        while active_players > 1:
            player = self.players[current_player_index]
            
            if not player.is_folded and not player.is_all_in:
                # Check if betting round should end
                if last_raiser is not None and last_raiser == player:
                    break
                
                print("-" * 20)
                print(f"Pot: {self.pot}")
                for p in self.players:
                    status = ""
                    if p.is_folded: status = " (Folded)"
                    if p.is_all_in: status = " (All-in)"
                    print(f"{p.name}: {p.chips} chips {status}")
                print(f"Community Cards: {self.community_cards}")
                print(f"Your hand {player.name}: {player.hand}")
                
                action, amount = self._get_player_action(player, current_bet)
                
                if action == 'fold':
                    print(f"{player.name} folds.")
                    active_players -=1
                elif action in ['call', 'check']:
                    if amount > 0:
                        print(f"{player.name} calls {amount}.")
                        bet_made = player.bet(amount)
                        self.pot += bet_made
                    else:
                        print(f"{player.name} checks.")
                elif action in ['bet', 'raise']:
                    total_player_bet = player.current_bet + amount
                    if total_player_bet > current_bet: # It's a raise
                        print(f"{player.name} raises to {total_player_bet}.")
                        current_bet = total_player_bet
                        last_raiser = player
                    else: # It's just a bet
                         print(f"{player.name} bets {amount}.")
                         current_bet = amount
                         last_raiser = player
                    
                    bet_made = player.bet(amount)
                    self.pot += bet_made

            # Move to next player
            current_player_index = (current_player_index + 1) % len(self.players)
            
            # End if we've gone around once and no one raised
            if last_raiser is None and current_player_index == start_index:
                 break
                 
            if len([p for p in self.players if not p.is_folded]) <= 1:
                break

    def play_round(self):
        """Plays one full round of poker."""
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        for p in self.players:
            p.reset_for_new_round()

        # Deal hands
        for p in self.players:
            p.hand = self.deck.deal(2)
        
        print("\n--- New Round ---")
        self.dealer_button = (self.dealer_button + 1) % len(self.players)

        # --- Betting Rounds ---
        print("\n--- Pre-flop Betting ---")
        self._run_betting_round((self.dealer_button + 1) % len(self.players))

        if len([p for p in self.players if not p.is_folded]) > 1:
            self.community_cards.extend(self.deck.deal(3))
            print(f"\n--- Flop: {self.community_cards} ---")
            self._run_betting_round((self.dealer_button + 1) % len(self.players))

        if len([p for p in self.players if not p.is_folded]) > 1:
            self.community_cards.extend(self.deck.deal(1))
            print(f"\n--- Turn: {self.community_cards} ---")
            self._run_betting_round((self.dealer_button + 1) % len(self.players))

        if len([p for p in self.players if not p.is_folded]) > 1:
            self.community_cards.extend(self.deck.deal(1))
            print(f"\n--- River: {self.community_cards} ---")
            self._run_betting_round((self.dealer_button + 1) % len(self.players))

        # --- Showdown ---
        active_players = [p for p in self.players if not p.is_folded]
        if not active_players:
            return

        if len(active_players) == 1:
            winner = active_players[0]
            print(f"\n{winner.name} wins the pot of {self.pot}!")
            winner.chips += self.pot
        else:
            print("\n--- Showdown ---")
            player_hands = {}
            for p in active_players:
                player_hands[p] = self._evaluate_hand(p.hand + self.community_cards)
                print(f"{p.name} has {p.hand} -> Best hand: {player_hands[p][1]}")

            # Find the winner(s)
            best_rank = max(player_hands.values(), key=lambda x: (x[0], [c.rank_value for c in x[1]]))[0]
            winners = [p for p, hand in player_hands.items() if hand[0] == best_rank]

            if len(winners) == 1:
                winner = winners[0]
                print(f"\n{winner.name} wins the pot of {self.pot}!")
                winner.chips += self.pot
            else:
                # Handle split pot
                print(f"\nSplit pot between: {', '.join(w.name for w in winners)}")
                split_amount = self.pot // len(winners)
                for winner in winners:
                    winner.chips += split_amount

if __name__ == '__main__':
    # Start the game
    player_names = ["Alice", "Bob", "Charlie"] # You can add more players
    game = PokerGame(player_names)
    
    round_num = 1
    while True:
        print(f"\n{'='*10} Round {round_num} {'='*10}")
        game.play_round()
        
        # Check for game over
        surviving_players = [p for p in game.players if p.chips > 0]
        if len(surviving_players) <= 1:
            winner = surviving_players[0] if surviving_players else "No one"
            print(f"\nGame over! {winner.name} is the winner!")
            break
        
        # Remove players with no chips
        game.players = surviving_players
        
        play_again = input("Play another round? (y/n): ").lower()
        if play_again != 'y':
            break
        round_num += 1