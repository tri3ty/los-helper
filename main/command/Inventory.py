
import time, re, collections

from Exceptions import *
from reactions.BotReactions import *
from misc_functions import *
from db.MudItem import *
from db.GenericMudList import *
from MudObjectDict import *

class Inventory(BotReactionWithFlag):
    equipped_items = {}

    # keep_list = ["large bag", "large sack", "black bag",
    #     "silver chalice", "steel bottle", 'glowing potion',
    #     "chicken soup", 'scarlet potion', 'white potion', "tree root",
    #     "Elixir of Morinva", "granite potion", "philtre of perception",
    #     "burnt ochre potion", "milky potion"]

    keep_list = ["large bag", "large sack", "black bag",
        "silver chalice", "steel bottle", "glowing potion",
        "chicken soup", "small restorative", "small flask", 
        "large restorative", "scarlet potion", "white potion", "tree root",
        "Elixir of Morinva", "granite potion", "philtre of perception",
        "burnt ochre potion", "milky potion",
        # weapons
        'war hammer', "adamantine sword", 'adamantine axe', "claymore", 
        "spider leg", 'heavy crossbow', 
        "spear", "bolos", 'javelin', "long bow", 
        "heathen amulet",
        "broad sword", "rapier",
        #"crossbow", "horn bow",  # < 70% missile
        # armour
        "hard cap", "hard gloves", "hard boots", "padded hat",
        "mountain gloves", "mountain boots", "mountain boots with crampons",
        "travellers cross", "leather mask", "leather collar",
        "studded leather collar", "studded leather sleeves",
        "studded leather boots", "studded leather pants",
        "studded leather gloves",
        # "chain mail armour", 
        'chain mail sleeves', 'chain mail leggings', 
        'chain mail gloves', # mill worker
        'chain mail hood', 'chain mail boots', 
        "ring mail armour", "ring mail sleeves", "ring mail leggings", 
        "ring mail hood", "ring mail gauntlets", "leather collar", 
        "enchanted indigo cloak", "fine elven cloak", "light elven cloak",
        'lion charm', "poison ring",
        "iron shield", 'platinum ring', 'gold ring', 'steel ring', 'silver ring',
        'granite rod', "miner's lamp",
        #'steel mask' # the bot slowly collects these 
        'large orcish sword',
        "small mace", "studded leather leggings", 'plate mail leggings', 'plate mail armor'
    ]

    def __init__(self, mudReaderHandler, telnetHandler, character):
        self.you_have = "(?s)You have: (.+?)\."
        self.wont_buy = "The shopkeep says, \"I won't buy that rubbish from you\.\""
        self.wont_buy2 = "The shopkeep won't buy that from you\."
        self.sold = "The shopkeep gives you (.+?) gold for (.+?)\."
        self.you_drop = "(?s)You drop (.+?)\."
        self.disintegrates = "A (.+?) disintegrates\."
        self.gold_from_tip = "You have (.+?) gold\."
        self.not_a_pawn_shop = "This is not a pawn shoppe\."
        self.you_now_have = "You now have (.+?) gold pieces\."
        self.not_empty = "It isn't empty!"
        self.you_wear = "You wear (.+?)\."
        self.nothing_to_wear = "You have nothing you can wear\."
        self.you_get = "(?s)[^ ]You get (.+?)\.(?:\nYou now have (.+?) gold pieces\.)?"
        self.you_remove = "(?s)You removed? (.+?)\."
        self.nothing_to_remove = "You aren't wearing anything that can be removed\."
        self.you_wield = "You wield (.+?)( in your off hand)?\."
        self.you_give = "(?s)You give (.+?) to (.+?)\."
        self.bought = "Bought\."
        self.you_put_in_bag = "(?s)You put (.+?) in(to)? (.+?)\."
        self.gave_you = ".+? gave (.+?) to you\."
        self.you_hold = "(?s)You hold (.+?)\."
        self.weapon_breaks = "Your (.+?) breaks and you have to remove it\."
        self.armor_breaks = "Your (.+?) fell apart\."
        self.current_equipment = "You see (.+?) (?:the .+?)\.\n?\r?(?:(?:.+?\.\n?\r?)+)?((?:.+?:.+\n?\r?)+)"
        self.no_inventory = "You currently have no carried inventory\."
        self.wearing = "\n?\r?(?:On )?(.+?):[\s]*(?:a |an |some )(.+)"

        self.regexes = [self.you_have, self.you_get, self.wont_buy, self.wont_buy2, self.sold, 
            self.you_drop, self.disintegrates, self.not_a_pawn_shop, self.you_now_have, self.gold_from_tip,
            self.not_empty, self.you_wear, self.nothing_to_wear, self.you_remove,  
            self.nothing_to_remove, self.you_wield, self.you_give, self.bought,
            self.you_put_in_bag, self.gave_you, self.you_hold, self.weapon_breaks,
            self.armor_breaks, self.current_equipment, self.no_inventory]

        self.mudReaderHandler = mudReaderHandler
        self.telnetHandler = telnetHandler
        self.character = character
        self.inventory = MudObjectDict()
        self.gold = 0
        self.__stopping = False
        self.mudReaderHandler.register_reaction(self)
        self.is_bulk_vendoring = False

        for index, item in enumerate(self.keep_list):
            self.keep_list[index] = MudItem(item)

    def notify(self, regex, M_obj):
        if regex is self.you_have:
            self.set_inventory(M_obj.group(1))
            #magentaprint(str(self.inventory), False)
        elif regex is self.sold:
            self.gold = self.gold + int(M_obj.group(1))
            self.remove(M_obj.group(2))
        elif regex is self.you_now_have or regex is self.gold_from_tip:
            self.gold = int(M_obj.group(1))
        elif regex is self.you_wield:
            weapon = M_obj.group(1)
            
            if M_obj.group(2) is not None:
                self.equipped_items["Second"] = [weapon]
            else:
                self.equipped_items["Wielded"] = [weapon]

            # magentaprint(weapon, False)
            self.remove(weapon)
            self.get_equipment()
        elif regex is self.you_get:
            item = self.clip_from_a_container(M_obj.group(1))
            self.add(item)
        elif regex in (self.you_drop, self.you_give, self.you_put_in_bag, self.disintegrates):
            # magentaprint(str(M_obj.group(1)), False)
            self.remove(M_obj.group(1))
        elif regex in (self.you_wear, self.you_hold):
            self.remove(M_obj.group(1))
            self.get_equipment()
            #we know this is armor of some kind so we need to find a way to assign it to the right spot
        elif regex is self.you_remove or regex is self.gave_you:
            self.add(M_obj.group(1))
        elif regex is self.bought:
            pass
            # if not self.is_bulk_vendoring:
            #     self.get_inventory()  # There are some notes about this at the bottom
            #     # I don't like this very much! I can't use ! to buy a lot of a thing.
        elif regex in (self.weapon_breaks, self.armor_breaks):
            item = M_obj.group(1)
            self.add_broken(M_obj.group(1)) 
            self.get_equipment()
        elif regex is self.current_equipment:
            character_name = M_obj.group(1)
            equipment_list = re.findall(self.wearing, M_obj.group(2))

            if character_name == self.character.name:
                for slot in equipment_list:
                    if slot[0] not in self.equipped_items:
                        self.equipped_items[slot[0]] = []

                    self.equipped_items[slot[0]].append(MudItem(slot[1]))
            # magentaprint(self.equipped_items,False)

        # magentaprint(self.inventory, False)

        super().notify(regex, M_obj)

    def get_inventory(self):
        self.telnetHandler.write("i")
        self.wait_for_flag()
        return self.inventory

    def get_equipment(self):
        return
        # self.telnetHandler.write("l " + self.character.name)
        # self.wait_for_flag()

    # def has_restorative(self):
    #     return self.has(self.restoratives)

    # def use_restorative(self):
    #     self.use(self.restoratives)

    def has(self, mud_item_string):
        mud_item = MudItem(mud_item_string)
        mud_item.map()

        if self.inventory.count(mud_item) > 0:
            return True

        return False

    def has_slot_equipped(self, slot_to_check, quantity=1):
        has_slot_equipped = False

        for slot in self.equipped_items:
            if slot == slot_to_check:
                if len(self.equipped_items[slot]) >= quantity:
                    has_slot_equipped = True
                    break

        return has_slot_equipped

    def get_item_of_type(self, itemModel, itemData, level=1):
        return self.inventory.get_object_of_type(itemModel, itemData, level)

    def use(self, item_or_list):
        item = ""
        if type(item) is list:
            for i in item_or_list:
                if i in self.inventory:
                    item = i
                    break
        else:
            item = item_or_list

        self.telnetHandler.write("use " + item)
        Inventory.remove_from_qty_dict(self.inventory, (item, 1))
    # the following version has 'usable' error checking
    # def use(self, item, target=None):
    #     if item in self.usable:
    #         if target:
    #             self.telnetHandler.write("use " + item + " " + target)
    #         else:
    #             self.telnetHandler.write("use " + item)
    #     else:
    #         magentaprint("Inventory: Error: " + item + " not usable.")
    #             self.telnetHandler.write("use " + item)
    def sell_stuff(self):
        self.__stopping = False
        self.get_inventory()  # Unnecessary if inventory is well tracked

        for item_ref in self.sellable():
            if not self.__stopping:
                self.sell(item_ref)
            else:
                return

    def sell(self, item_ref):
        self.telnetHandler.write("sell " + item_ref)
        self.wait_for_flag()

    def bulk_sell(self, item_string, quantity):
        i = 0
        magentaprint("Bulk selling: " + item_string + " #" + quantity)
        self.is_bulk_vendoring = True

        while i < (quantity ):
            self.sell(item_string)
            i += 1

        self.sleep(3) #breathe!

        self.is_bulk_vendoring = False

    def buy_stuff(self, item_string):
        #this should be implemented to match sell stuff
        #programmatic purchasing via a shopping list or something
        return

    def buy(self, item_string):
        self.telnetHandler.write("buy " + item_string)
        self.wait_for_flag
        self.add(item_string)

    def bulk_buy(self, item_string, quantity):
        i = 0
        self.is_bulk_vendoring = True

        while i < (quantity ):
            self.telnetHandler.write("buy " + item_string)
            i += 1

        self.sleep(3) #breathe!

        self.is_bulk_vendoring = False


    # def sell_fast(self):

    def drop_stuff(self):
        self.__stopping = False
        self.get_inventory()  # Maybe unnecessary, except I see "You don't have that" if removed

        for item_ref in self.sellable():
            if not self.__stopping:
                self.drop(item_ref)
            else:
                return

    def drop(self, item_ref):
        self.telnetHandler.write("drop " + item_ref)
        self.wait_for_flag()

    def drop_item_at_position(self, item_string, position):
        self.telnetHandler.write("drop " + item_string  + " " + str(position))
        self.wait_for_flag()

    def drop_last(self, item_string):
        item_ref = self._item_string_to_reference(item_string)
        self.drop_item_at_position(item_ref, self.inventory[item_string])

    def stop(self):
        self.__stopping = True

    def set_inventory(self, item_string):
        self.inventory = MudObjectDict()
        self.inventory.add(self.parse_item_list(item_string))

    def add(self, item_string):
        items = self.parse_item_list(item_string)
        self.inventory.add(items)

    def add_broken(self, item_string):
        items = self.parse_item_list(item_string)

        for item in items:
            item.is_unusable = True

        self.inventory.add(items)

    def remove(self, item_string):
        item_list = self.parse_item_list(item_string)
        self.inventory.remove(item_list)

    def equip_item(self, equip_string):
        self.telnetHandler.write(equip_string)
        self.wait_for_flag()


    def clip_in_your_off_hand(self, wield_string):
        # Example wield_string: a spear in your off hand
        wield_string = wield_string.replace('\n\r', ' ')
        length = len(wield_string)

        if wield_string[length-17:length] == " in your off hand":
            return wield_string[:length-17]
        else:

            return wield_string

    def clip_from_a_container(self, get_string):
        # Example get_string: some chicken soup from a sack
        get_string = get_string.replace('\n\r', ' ')
        M_obj = re.search("(.+?) from (.+?)", get_string)

        if M_obj != None:
            return M_obj.group(1)
        else:
            return get_string

    def parse_item_list(self, inventory_string):
        ''' Returns a dict {item: quantity} ie. {"chicken soup": 5, steel bottle: 1} '''
        return_dict = {}
        inventory_string = inventory_string.replace("\n\r", ' ')
        # inventory_string = inventory_string.replace("  ", ' ') #replace double space with a single one
        inv_list = inventory_string.split(',')
        inv_list = [item.strip(' \t\n\r') for item in inv_list]
        singles = ['a ', 'an ', 'some ']
        numbers = ['two ', 'three ', 'four ', 'five ', 'six ', 'seven ', 
                   'eight ', 'nine ', 'ten ', 'eleven ', 'twelve ', 'thirteen ', 'fourteen ', 
                   'fifteen ' , 'sixteen ', 'seventeen ', 'eighteen ', 'nineteen ', 'twenty ']
        numbers.extend([str(i) + " " for i in range(21, 200)])

        for item in inv_list:
            number_found = False
            gold_coin_match = re.match("(\d+) gold coins?", item)
            if gold_coin_match:
                # self.add_to_dict(return_dict, 'gold coin', int(gold_coin_match.group(1)))
                continue
            for s in singles:
                if item[0:len(s)] == s:
                    number_found = True
                    self.add_to_dict(return_dict, item[len(s):], 1)
                    break
            if number_found:
                continue
            for n in range(0, len(numbers)):
            # for number in numbers:
                number = numbers[n]
                if item[0:len(number)] == number:
                    number_found = True
                    if "sets of" in item:
                        item = item.replace("sets of ", "")
                    item = item[len(number):]
                    # if item[len(item)-1] == 's':
                    if item.endswith('ses') or item.endswith('xes'):
                        item = item[:len(item)-2]
                    elif item.endswith('s'):
                        item = item[:len(item)-1]

                        # mud_item = MudItem(item)
                        # mud_item.map()
                        # # mud_items = []
                        # # for _ in range(n - 1):
                        # #     mud_items.append(mud_item)
                        # # item_list = GenericMudList(mud_items)
                        # item_list = GenericMudList([mud_item] * (n - 1))
                        # return_dict[mud_item] = item_list
                    self.add_to_dict(return_dict, item, n+2)
                    break
            if number_found is False:
                magentaprint("Inventory parsed " + item)
                #if the item wasn't received with a/an/some etc...
                #we assume it's just one item
                # mud_item = MudItem(item)
                # mud_item.map()
                # item_list = GenericMudList([mud_item])
                # return_dict[mud_item] = item_list
                self.add_to_dict(return_dict, item, 1)

        return return_dict

    def add_to_dict(self, d, item_str, qty):
        mud_item = MudItem(item_str)
        mud_item.map()
        d[mud_item] = GenericMudList([mud_item] * qty)

    def sellable(self):
        return self.inventory.get_unique_references(self.keep_list)

    def output_inventory(self):
        magentaprint(str(self.inventory),False)

    restoratives = ["chicken soup", "small restorative", "small flask", 
                    "large restorative", "scarlet potion", "white potion", "tree root"]
    # usable = ["small retorative", "large restorative", "chicken soup", "scarlet potion", 
    #           "steel bottle", "silver chalice", "milky potion",
    #           "glowing potion",
    #           "adamantine rod", "granite rod", "zinc wand"]

    # should probably depend on level.
    #keep_list = ["small restorative", "silver chalice", "steel bottle", "milky potion"] 

    #thick liquid silences you !!!

    MUD_RETURN_ITEM_SOLD = False


# Ok I want to set up reactions to keep myself up to date.
# I am thinking of steel bottles and restoratives, so I want 
# a function to return how many I have.
# How about losHelper sets me up.  I think that's doable.

# Ok what about selling, dropping, giving, wielding, wearing.  
# I think I can see why I never wrote this thing.  
# Well how about we just make it stupid a ignore those things.
# (Alternative is to ask commandHandler to do all of these things
# through the inventory object... inventory.sell() inventory.wear()
# which isn't terrible.  Hmmmm)

# The obvious case is picking up, so we should have a reaction for that.
# (I think BotReactions needs to have a regex list...!)  Makes it a bit 
# harder to use, since you need to put in a list.  Well can we make the 
# list optional?  That isn't much better.

# Ok I am ready for a regex list in BotReactions.

# Your brass ring fell apart.
# You are not yet adept enough to use this!


# BUYING STUFF

# Hmmm, how to keep inventory up to date when buying stuff?
# How about printing the inventory on this regex? 
# Oooh, maybe we could convince MudReaderThread to repress the output.
# Well, we could have commandHandler call 'buy' and then confirm ... 
# oooff that doesn't even work because we don't have the full name of what we bought
# Maybe printing the inventory won't be too annoying... 

# NEWLINES

# I wonder if there's a bug whenever a newline occurs outside of the (.+?).  
# That would probably be MudReader's job to fix on a global level.
# No, the mud doesn't put newlines there.  The console will wrap it but 
# that doesn't constitute a newline.  The mud always puts them between words.
# so s = s.replace('\r\n', ' ') is always a good move.

# Would be nice to keep track of white amulet usages
# It'd be good to consider the weight when deciding whether to sell.