import time
import re
# import threading
from misc_functions import *
from Exceptions import *
from mini_bots.travel_bot   import TravelBot
from mini_bots.shopping_bot import ShoppingBot
from mini_bots.mini_bot     import MiniBot
from db.Database            import AreaStoreItem

class PotionBot(MiniBot):
    def __init__(self, character, command_handler, mud_map):
        super().__init__()
        self.character = character
        self.inventory = character.inventory
        self.command_handler = command_handler
        self.shopping_bot = ShoppingBot(self.character, self.command_handler, mud_map)
        # magentaprint(str(AreaStoreItem.get_by_name('milky potion')[0].item.id) + " test", False)
        self.potion_store = AreaStoreItem.get_by_name('misty potion')[0]
        self.aura_pots_count = 0
    
    def run(self):
        self.stopping = False
        magentaprint("running potion bot", False)
        for _ in range(self.aura_pots_count, 10):
            magentaprint("buying misty", False)
            self.shopping_bot.buy_with_ref(self.potion_store, 'misty')

        self.stop()
    
    def check_potions(self):
        return self.needs_to_shop()

    def needs_to_shop(self):
        self.aura_pots_count = self.inventory.count_aura_pots()
        # magentaprint("Aura potions on hand: " + str(self.aura_pots_count), False)
        needs_to_shop = False
        if self.aura_pots_count <= 5:
            needs_to_shop = True

        # magentaprint("Needs to shop for pots: " + str(needs_to_shop), False)        
        return needs_to_shop
    
    def stop(self):
        self.stopping = True
        self.shopping_bot.stop()