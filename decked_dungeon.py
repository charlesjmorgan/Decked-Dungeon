# OOP Test

import os
import time
import random
import pygame
import sys
from pygame import *
from socket import *

SCREEN_H = 480
SCREEN_W = 640

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

card_dict = {}


def main():

    pygame.init()
    pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Decked Dungeon")

    main_menu = MainMenu()

    main_menu.draw_start_screen()

    game_over = False

    while not game_over:

        for event in pygame.event.get():
            mpos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if main_menu.active:
                if event.type == MOUSEBUTTONUP:
                    if main_menu.start_rect.collidepoint(mpos):
                        level_select = LevelSelect()
                        level_select.draw_level_select()
                        level_select.active = True
                        main_menu.active = False
                    if main_menu.quit_rect.collidepoint(mpos):
                        pygame.quit()
                        sys.exit()

            elif level_select.active:
                if event.type == MOUSEBUTTONUP:
                    if level_select.lvl1_rect.collidepoint(mpos):
                        level = "levels\\lvl1.txt"
                        arena = Arena(level, ["Player", "Enemy"])
                        arena.draw_arena()
                        arena.draw_player_hand()
                        arena.active = True
                        level_select.active = False
                    if level_select.lvl2_rect.collidepoint(mpos):
                        level = "levels\\lvl2.txt"
                        arena = Arena(level, ["Player", "Enemy"])
                        arena.draw_arena()
                        arena.draw_player_hand()
                        arena.active = True
                        level_select.active = False
                    if level_select.lvl3_rect.collidepoint(mpos):
                        level = "levels\\lvl3.txt"
                        arena = Arena(level, ["Player", "Enemy"])
                        arena.draw_arena()
                        arena.draw_player_hand()
                        arena.active = True
                        level_select.active = False

            elif arena.active:
                if arena.player_turn:
                    if event.type == MOUSEBUTTONUP:
                        if arena.end_turn_rect.collidepoint(mpos):
                            arena.player_turn = False
                            arena.enemy_take_turn()
                            arena.refresh_stats()
                        if arena.hand_rect.collidepoint(mpos):
                            if get_card_rect(0).collidepoint(mpos) and len(arena.user.hand.cards) >= 1:
                                arena.player_take_turn(0)
                            if get_card_rect(1).collidepoint(mpos) and len(arena.user.hand.cards) >= 2:
                                arena.player_take_turn(1)
                            if get_card_rect(2).collidepoint(mpos) and len(arena.user.hand.cards) >= 3:
                                arena.player_take_turn(2)
                            if get_card_rect(3).collidepoint(mpos) and len(arena.user.hand.cards) >= 4:
                                arena.player_take_turn(3)
                            if get_card_rect(4).collidepoint(mpos) and len(arena.user.hand.cards) >= 5:
                                arena.player_take_turn(4)
                            if get_card_rect(5).collidepoint(mpos) and len(arena.user.hand.cards) >= 6:
                                arena.player_take_turn(5)
                elif event.type == MOUSEBUTTONUP:
                    arena.draw_message("It is not your turn")
            else:
                main_menu.draw_start_screen()
                main_menu.active = True
                level_select.active = False
                arena.active = False

    # if player.health == 0:
    #     self.completed = True
    #     if player.name == "Enemy":
    #         os.system("cls")
    #         print("Congratulations! You Won!")
    #         player.print_stats()
    #         player.opponent.print_stats()
    #         print('\n', self.rounds, " Rounds completed", sep='')
    #         input("\nPress enter to go back to main menu...")
    #         return True, True
    #     elif player.name == "Player":
    #         os.system("cls")
    #         print("You lost :(")
    #         player.print_stats()
    #         player.opponent.print_stats()
    #         print('\n', self.rounds, " Rounds completed", sep='')
    #         input("\nPress enter to go back to main menu...")

    pygame.quit()
    sys.exit()


def get_card_rect(slot):

    card_rect = pygame.Rect((20, 296), (96, 128))
    card_rect.centerx = (60 + 120 * slot)
    return card_rect


class Screens:
    def __init__(self):

        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.text = pygame.font.SysFont('Calibri Bold', 48)


class MainMenu(Screens):
    def __init__(self):

        super().__init__()

        self.active = True

        self.start_text = self.text.render("Click to start", True, BLACK)
        self.start_rect = self.start_text.get_rect()
        self.start_rect.center = (200, 300)

        self.quit_text = self.text.render("Quit", True, BLACK)
        self.quit_rect = self.quit_text.get_rect()
        self.quit_rect.center = (200, 350)

    def draw_start_screen(self):

        self.screen.fill(WHITE)

        self.screen.blit(self.start_text, self.start_rect)
        self.screen.blit(self.quit_text, self.quit_rect)
        pygame.display.update()


class LevelSelect(Screens):

    def __init__(self):
        super().__init__()

        self.active = False

        self.levels = []
        for file in os.listdir('levels\\'):
            lvl_num = file[3]
            self.levels.append(lvl_num)

        self.level_menu = True

        self.header = self.text.render("Levels", True, WHITE)
        self.header_rect = self.header.get_rect()
        self.header_rect.center = (200, 200)

        self.lvl1_text = self.text.render("Level 1", True, WHITE)
        self.lvl1_rect = self.lvl1_text.get_rect()
        self.lvl1_rect.center = (200, 250)

        self.lvl2_text = self.text.render("Level 2", True, WHITE)
        self.lvl2_rect = self.lvl2_text.get_rect()
        self.lvl2_rect.center = (200, 300)

        self.lvl3_text = self.text.render("Level 3", True, WHITE)
        self.lvl3_rect = self.lvl3_text.get_rect()
        self.lvl3_rect.center = (200, 350)

    def draw_level_select(self):

        self.screen.fill(BLACK)

        self.screen.blit(self.header, self.header_rect)
        self.screen.blit(self.lvl1_text, self.lvl1_rect)
        self.screen.blit(self.lvl2_text, self.lvl2_rect)
        self.screen.blit(self.lvl3_text, self.lvl3_rect)

        pygame.display.update()


class Arena(Screens):

    def __init__(self, level_name, players):
        super().__init__()

        self.player_turn = True

        self.active = False

        os.system("cls")

        self.chars = []

        with open(level_name, 'r') as lvl:

            for line in lvl:
                line = line.split(",")
                self.chars.append(line)

        self.players = []

        for name in players:
            if name == "Player":
                self.user = (User(name, self.chars[0]))
                self.players.append(self.user)
            elif name == "Enemy":
                self.enemy = (Enemy(name, self.chars[1]))
                self.players.append(self.enemy)

        self.user.opponent = self.enemy
        self.enemy.opponent = self.user

        self.rounds = 0
        self.completed = False

        self.header = self.text.render("Arena", True, WHITE)
        self.header_rect = self.header.get_rect()
        self.header_rect.center = ((SCREEN_W / 2), 30)

        self.text = pygame.font.SysFont('Calibri', 20)

        self.background = pygame.image.load(os.path.join("data", "images", "arenabg1.png"))
        self.background = self.background.convert_alpha()
        self.background_rect = self.background.get_rect()

        self.end_turn = pygame.image.load(os.path.join("data", "images", "end_turn.png"))
        self.end_turn = self.end_turn.convert_alpha()
        self.end_turn_rect = self.end_turn.get_rect()
        self.end_turn_rect.center = (320, 450)

        self.player_stats_bg = pygame.image.load(os.path.join("data", "images", "player_stats.png"))
        self.player_stats_bg = self.player_stats_bg.convert_alpha()
        self.player_stats_bg = pygame.transform.scale(self.player_stats_bg, (128, 256))
        self.player_stats_bg_rect = self.player_stats_bg.get_rect()

        self.enemy_stats_bg = pygame.image.load(os.path.join("data", "images", "enemy_stats.png"))
        self.enemy_stats_bg = self.enemy_stats_bg.convert_alpha()
        self.enemy_stats_bg = pygame.transform.scale(self.enemy_stats_bg, (128, 256))
        self.enemy_stats_bg_rect = self.enemy_stats_bg.get_rect()
        self.enemy_stats_bg_rect = self.enemy_stats_bg_rect.move((SCREEN_W - 128), 0)

        self.hand_rect = pygame.rect.Rect((0, 260), (640, 170))

        self.card_back_surf = pygame.image.load(os.path.join("data", "images", "card.png"))
        self.card_back_surf = self.card_back_surf.convert_alpha()
        self.card_back_rect = self.card_back_surf.get_rect()

    def draw_arena(self):

        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.header, self.header_rect)
        self.screen.blit(self.player_stats_bg, self.player_stats_bg_rect)
        self.screen.blit(self.enemy_stats_bg, self.enemy_stats_bg_rect)
        self.screen.blit(self.end_turn, self.end_turn_rect)
        pygame.display.update()
        self.draw_stats()

    def draw_stats(self):

        self.screen.blit(self.player_stats_bg, self.player_stats_bg_rect)
        self.screen.blit(self.enemy_stats_bg, self.enemy_stats_bg_rect)
        pygame.display.update()

        for player in self.players:

            self.draw_health(player)
            self.draw_armor(player)
            self.draw_actions(player)
            self.draw_damage(player)

    def draw_health(self, player):

        player_health = str(format(player.health, '.0f'))
        player_health = self.text.render(str(player_health), True, BLACK)
        player_health_rect = player_health.get_rect()
        player_health_rect.centerx = player.x_offset
        player_health_rect.centery = 93
        self.screen.blit(player_health, player_health_rect)
        pygame.display.update(player_health_rect)

    def draw_armor(self, player):

        player_armor = str(format(player.armor, '.0f'))
        player_armor = self.text.render(str(player_armor), True, BLACK)
        player_armor_rect = player_armor.get_rect()
        player_armor_rect.centerx = player.x_offset
        player_armor_rect.centery = 139
        self.screen.blit(player_armor, player_armor_rect)
        pygame.display.update(player_armor_rect)

    def draw_actions(self, player):

        player_actions = str(player.actions.actions_pt)
        player_actions = self.text.render(str(player_actions), True, BLACK)
        player_actions_rect = player_actions.get_rect()
        player_actions_rect.centerx = player.x_offset
        player_actions_rect.centery = 185
        self.screen.blit(player_actions, player_actions_rect)
        pygame.display.update(player_actions_rect)

    def draw_damage(self, player):

        player_damage = str(format(player.damage, '.0f'))
        player_damage = self.text.render(str(player_damage), True, BLACK)
        player_damage_rect = player_damage.get_rect()
        player_damage_rect.centerx = player.x_offset
        player_damage_rect.centery = 231
        self.screen.blit(player_damage, player_damage_rect)
        pygame.display.update(player_damage_rect)

    def draw_player_hand(self):

        self.screen.blit(self.background, self.hand_rect, self.hand_rect)

        pygame.time.wait(400)

        pygame.display.update()

        for counter, value in enumerate(self.user.hand.cards):
            x_offset = counter * 110 + 60
            card_name = self.text.render(value.name, True, BLACK)
            card_name_rect = card_name.get_rect()
            card_name_rect.center = (x_offset, 360)
            card_desc = self.text.render(value.desc, True, BLACK)
            card_desc_rect = card_desc.get_rect()
            card_desc_rect.center = (x_offset, 340)

            temp_card_surf = self.card_back_surf
            temp_card_rect = self.card_back_rect
            temp_card_rect.center = (x_offset, 360)

            self.screen.blit(temp_card_surf, temp_card_rect)
            self.screen.blit(card_name, card_name_rect)

            pygame.display.update()

    def draw_message(self, message):

        message = self.text.render(message, True, WHITE)
        message_rect = message.get_rect()
        message_rect.center = (320, 120)
        self.screen.blit(message, message_rect)
        pygame.display.update(message_rect)
        pygame.time.wait(10000)
        self.screen.blit(self.background, message_rect, message_rect)
        pygame.display.update(message_rect)

    def enemy_take_turn(self):

        self.enemy.actions.actions_pt += self.enemy.actions.base_actions
        self.enemy.draw_cards(1)

        while self.enemy.actions.actions_pt > 0 and self.enemy.health > 0 and self.enemy.opponent.health > 0:

            try:
                chosen_card = self.enemy.choose_card()
                self.enemy.hand.remove_card(chosen_card)

                message = "Enemy played " + chosen_card.name
                self.draw_message(message)

                for effect in chosen_card.effects:

                    if effect.target == "self":
                        self.enemy.apply_effects(effect)
                    else:
                        self.user.apply_effects(effect)

                self.enemy.actions.actions_pt -= 1
            except ValueError:
                pass

        if self.enemy.health == 0:
            self.draw_message("You win!")
            self.active = False
        elif self.user.health == 0:
            self.draw_message("You lose :(")
            self.active = False

        self.user.draw_cards(1)

        self.draw_player_hand()

        self.player_turn = True

    def player_take_turn(self, index):

        if self.user.actions.actions_pt > 0 and self.user.health > 0 and self.user.opponent.health > 0:

            card = self.user.hand.cards[index]

            self.user.play_card(card)
            message = "User played " + card.name
            self.draw_message(message)
            self.draw_stats()
            self.draw_player_hand()

        if self.user.health == 0:

            self.draw_message("You are dead!")
            self.active = False

        elif self.enemy.health == 0:
            self.draw_message("You win!")
            self.active = False

        elif self.user.actions.actions_pt == 0:
            self.draw_message("You are out of actions")

    def refresh_stats(self):
        self.user.actions.actions_pt += self.user.actions.base_actions
        self.draw_stats()


class Players(object):

    def __init__(self, name, stats_list):

        self.name = name
        self.opponent = None
        self.hand = Hand()
        self.health = float(stats_list.pop(0))
        self.armor = float(stats_list.pop(0))
        self.damage = float(stats_list.pop(0))
        self.actions = Actions(stats_list.pop(0))

        if self.name == "Player":
            self.x_offset = 30
        else:
            self.x_offset = 542

        self.deck = Deck(stats_list)
        self.draw_cards(3)

    def draw_cards(self, amt):

        for card in self.deck.draw_cards(amt):
            self.hand.add_card(card)

    def apply_effects(self, effect):

        method_call = "self." + effect.name + "(" + str(effect.amt) + ")"
        eval(method_call)

    def change_actions(self, amt):
        amt = int(amt)

        if self.actions.actions_pt + amt >= 0:
            self.actions.actions_pt += amt

            print(self.name, "Actions", amt)

    # function change_attack_damage takes a char dict and a number as an input
    # it returns the char dict after changing the attack damage by the amt
    def change_attack_damage(self, amt):
        amt = int(amt)

        if self.damage + amt >= 0:
            self.damage += amt
            print(self.name + "Damage changed by", amt)

    def get_attacked(self, amt):
        amt = int(amt) * self.opponent.damage

        ARMOR_MULTIPLIER = 2

        if self.armor > 0:
            if self.armor + amt * ARMOR_MULTIPLIER >= 0:
                self.armor += amt * ARMOR_MULTIPLIER
                print(self.name + "Armor", amt * ARMOR_MULTIPLIER)
            else:
                left_over_dmg = self.armor / ARMOR_MULTIPLIER + amt
                self.armor = 0
                if self.health + left_over_dmg >= 0:
                    self.health += left_over_dmg
                    print("Health", left_over_dmg)
                else:
                    self.health = 0
                    print(self.name + "Health -", self.health, sep='')
        else:
            if self.health + amt >= 0:
                self.health += amt
                print(self.name + "Health", amt)
            else:
                self.health = 0
                print(self.name + "Health -", self.health, sep='')

    # function change_health takes a char dict and a number as an input
    # it returns the char dict after changing the health by the amt
    def change_health(self, amt):
        amt = int(amt)

        if self.health + amt >= 0:
            self.health += amt
            print(self.name + "Health", amt)
        else:
            self.health = 0
            print(self.name + "Health -", self.health, sep='')

    # function change_armor takes a char dict and number as an input
    # it returns the char dict after changing the armor by the amt
    def change_armor(self, amt):
        amt = int(amt)

        if self.armor + amt >= 0:  # currently no cap on armor
            self.armor += amt
            print(self.name, "armor ", amt)

    # function discard takes a char dict and number as an input
    # it then randomly discards a card from the chars hand
    def discard(self, amt):
        amt = int(amt)

        cards_discarded = []

        for i in range(amt):
            card_index = random.randrange(len(self.deck.deck))
            cards_discarded.append(self.deck.deck[card_index])

        for item in cards_discarded:
            self.hand.remove_card(item)


class User(Players):

    def __init__(self, name, stats_list):

        super().__init__(name, stats_list)

    def play_card(self, chosen_card):

        self.hand.remove_card(chosen_card)

        for effect in chosen_card.effects:

            if effect.target == "self":
                self.apply_effects(effect)
            else:
                self.opponent.apply_effects(effect)

        self.actions.actions_pt -= 1


class Enemy(Players):

    def __init__(self, name, stats_list):

        super().__init__(name, stats_list)

    def choose_card(self):

        return self.hand.cards[random.randrange(len(self.hand.cards))]


# actions are the number of moves a player gets per turn
class Actions:

    def __init__(self, base_actions):

        self.base_actions = int(base_actions)
        self.actions_pt = self.base_actions

    def add_actions_pt(self, amt):
        self.actions_pt += amt

    def remove_actions_pt(self, amt):
        self.actions_pt -= amt


# a hand is a list of the cards that they player has
# its' methods include print add and remove
class Hand:

    def __init__(self):

        self.cards = []
        self.length = 0

    def add_card(self, card):

        self.cards.append(card)

    def remove_card(self, card):

        self.cards.remove(card)


# a deck can be used to draw cards
# each player has their own deck that is used to draw their cards
class Deck:

    def __init__(self, cards_list):

        self.deck = []

        with open('cards.txt', 'r') as infile:

            for line in infile:

                line = line.rstrip().lower()

                card = line.split(",")

                card_name = card.pop(0)
                card_name = card_name.lower()
                card_desc = card.pop(0)

                action_dict = {}

                for item in range(0, len(card), 3):
                    action_dict[card[item]] = [card[item + 1], card[item + 2]]

                # {'card name': [{'action': ['amt', 'target'], 'action': ['amt', 'target']}, 'Card Description']}
                card = Card(card_name, card_desc, action_dict)

                if card.name in cards_list:

                    index = cards_list.index(card.name)

                    for i in cards_list[index + 1]:
                        self.deck.append(card)

    def draw_cards(self, amt):

        cards_drawn = []

        for i in range(amt):

            possible_deck = []

            for card in self.deck:
                possible_deck.append(card)

            if len(possible_deck) != 0:

                card_index = random.randrange(len(possible_deck))

                card_drawn = possible_deck[card_index]

                cards_drawn.append(card_drawn)

                self.deck.remove(card_drawn)

        return cards_drawn


# a card is useless
class Card(object):

    def __init__(self, card_name, card_desc, actions_dict):
        self.name = card_name
        self.desc = card_desc
        self.effects = []
        for name, info in actions_dict.items():
            if info[0] == "self":
                self.effects.append(AffectSelf(name, info))
            else:
                self.effects.append(AffectOpponent(name, info))

    def play_card(self):

            return self.name, self.effects


class Effects:

    def __init__(self, name, info):
        self.name = name
        self.amt = int(info[0])


class AffectSelf(Effects):

    def __init__(self, name, info):

        self.target = info[1]

        super().__init__(name, info)


class AffectOpponent(Effects):

    def __init__(self, name, info):

        self.target = info[1]

        super().__init__(name, info)


main()
