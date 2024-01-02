import tkinter as tk
from tkinter import messagebox
import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def play_card(self):
        return self.hand.pop(0)

class WarGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("War Card Game")
        self.deck = Deck()
        self.player = Player("Human")
        self.computer = Player("Computer")
        self.round = 1

        self.label = tk.Label(master, text="War Card Game")
        self.label.pack()


        for _ in range(len(self.deck.cards)//2):
            self.player.add_card(self.deck.draw_card())
            self.computer.add_card(self.deck.draw_card())

        self.label = tk.Label(master, text="Round " + f"{self.round}")
        self.label.pack()
        
        self.play_button = tk.Button(master, text="Play Round", command=self.play_round)
        self.play_button.pack()

        self.label_player = tk.Label(master, text="Player Cards: " + f"{len(self.player.hand)}")
        self.label_player.pack()

        self.label_computer = tk.Label(master, text="Computer Cards: " + f"{len(self.computer.hand)}")
        self.label_computer.pack()

        self.label_result = tk.Label(master, text="")
        self.label_result.pack()

    def play_round(self):
        # print("here", len(self.player.hand), len(self.computer.hand), len(self.deck.cards))
        self.round += 1
        self.label["text"] = "Round " + f"{self.round}"
        if self.player.hand and self.computer.hand:
            # print("here")
            card1 = self.player.play_card()
            card2 = self.computer.play_card()

            result = self.compare_cards(card1, card2)

            self.label_result["text"] = "Round result: \n" + result
            # messagebox.showinfo("Round Result", result)

            if not self.player.hand:
                messagebox.showinfo("Game Over", "Computer wins the game!")
            elif not self.computer.hand:
                messagebox.showinfo("Game Over", "Human wins the game!")
        self.label_player["text"] = "Player Cards: " + f"{len(self.player.hand)}"
        self.label_computer["text"] = "Computer Cards: " + f"{len(self.computer.hand)}"

    def compare_cards(self, card1, card2):
        result = f"Human plays: {card1}\nComputer plays: {card2}\n"

        if card1.rank > card2.rank:
            result += "Human wins the round!"
            self.player.add_card(card1)
            self.player.add_card(card2)
        elif card1.rank < card2.rank:
            result += "Computer wins the round!"
            self.computer.add_card(card1)
            self.computer.add_card(card2)
        else:
            result += "It's a tie! Time for war..."
            self.war()

        return result

    def war(self):
        if len(self.player.hand) < 4 or len(self.computer.hand) < 4:
            messagebox.showinfo("Game Over", "Not enough cards for a war. It's a tie!")
        else:
            war_cards = [self.player.play_card(), self.computer.play_card()]
            war_cards.extend([self.player.play_card() for _ in range(3)])
            war_cards.extend([self.computer.play_card() for _ in range(3)])

            result = f"{self.player.name} and {self.computer.name} go to war with {war_cards[-2]} and {war_cards[-1]}\n"

            result += self.compare_cards(war_cards[-2], war_cards[-1])

            messagebox.showinfo("War Result", result)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    game_gui = WarGameGUI(root)
    root.mainloop()
