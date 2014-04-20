
import time

from Exceptions import *
from BotReactions import *
from misc_functions import *


class Inventory(BotReactionWithFlag):

    def __init__(self, mudReaderHandler, commandHandler):
        self.you_have = "(?s)You have: (.+?)\."
        self.wont_buy = "The shopkeep says, \"I won't buy that rubbish from you\.\""
        self.sold = "The shopkeep gives you (.+?) gold for (.+?)\."
        self.dropped = "(?s)You drop (.+?)\.\n\rThanks for recycling\.\n\rYou have (.+?) gold\."
        self.not_a_pawn_shop = "This is not a pawn shoppe\."
        self.you_now_have = "You now have (.+?) gold pieces\."
        self.not_empty = "It isn't empty!"
        super(Inventory, self).__init__([self.you_have, self.wont_buy, self.sold, self.dropped, 
                                         self.not_a_pawn_shop, self.not_empty])

        self.mudReaderHandler = mudReaderHandler
        self.commandHandler = commandHandler
        self.inventory = []
        self.gold = 0
        self.__stopping = False
        self.mudReaderHandler.register_reaction(self)

    def notify(self, regex, M_obj):
        if regex is self.you_have:
            self.parse_inventory_list(M_obj.group(1))
        elif regex is self.sold:
            self.gold = self.gold + int(M_obj.group(1))
            self.inventory.remove(self.remove_a_an_some(M_obj.group(2)))
        elif regex is self.dropped:
            magentaprint("removing " + M_obj.group(1) + " from inventory.")
            magentaprint("inventory:" + str(self.inventory))
            try:
                self.inventory.remove(self.remove_a_an_some(M_obj.group(1)))
            except Exception:
                magentaprint("Inventory removal exception - did you drop all or something?", False)          
            self.gold = int(M_obj.group(2))
        elif regex is self.you_now_have:
            self.gold = int(M_obj.group(1))

        super(Inventory, self).notify(regex, M_obj)

    def get_inventory(self):
        self.commandHandler.process("i")
        self.wait_for_flag()
        return self.inventory

    def get_number_of_items(self, item):
        return self.inventory.count(item)

    def sell_stuff(self):
        self.get_inventory()  # Unnecessary if inventory is well tracked

        for item in self.sellable():
            if not self.__stopping:
                self.sell(item)
            else:
                return

    def sell(self, item):
        magentaprint("selling " + str(item))
        self.commandHandler.process("sell " + item)
        self.wait_for_flag()

    # def sell_fast(self):

    def drop_stuff(self):
        self.get_inventory()  # Unnecessary if sell manages to match everything.

        for item in self.sellable():
            if not self.__stopping:
                self.drop(item)
            else:
                return

    def drop(self, item):
        self.commandHandler.process("drop " + item)
        magentaprint("dropped: " + str(item))
        self.wait_for_flag()

    def drop_fast(self):
        pass

    def give(self, item, target):
        pass

    def put_in_sack(self, item, sack):
        pass

    def stop(self):
        self.__stopping = True

    def remove_a_an_some(self, aString):
        if aString[0:2] == "a ":
            aString = aString[2:]
        elif aString[0:3] == "an ":
            aString = aString[3:]
        elif aString[0:5] == "some ":
            aString = aString[5:]

        return aString

    def parse_inventory_list(self, inventory_string):
        self.inventory = []
        inventory_string = replace_newlines_with_spaces(inventory_string)
        inv_list = inventory_string.split(',')
        inv_list = [item.lstrip() for item in inv_list]
        inv_list = [item.rstrip() for item in inv_list]
        numbers = ["a ", "an ", "some ", "two ", "three ", "four ", "five ", "six ", "seven ", 
                   "eight ", "nine ", "ten ", "eleven ", "twelve ", "thirteen ", "fourteen ", 
                   "fifteen" , "sixteen ", "seventeen ", "eighteen ", "nineteen ", "twenty "]
        numbers.extend([str(i) for i in range(21, 100)])

        for item in inv_list:
            for n in range(0, len(numbers)):
                number = numbers[n]
                if item[0:len(number)] == number:
                    if n < 3:
                        item = item[len(number):]
                        self.inventory.append(item)
                    else:
                        sets_of = "sets of "
                        if item[len(number):len(number)+len(sets_of)] == sets_of:
                        # if item[len(number) + (0:9)] == " sets of ":
                            item = item[len(number)+len(sets_of):]
                        else:
                            item = item[len(number):]
                            if item[len(item)-1] == 's':
                                if item[len(item)-3:] == "ses" or item[len(item)-3:] == "xes":
                                    item = item[:len(item)-2]
                                else:
                                    item = item[:len(item)-1]

                        for _ in range(0, n-1):
                            self.inventory.append(item)

                    continue



    def sellable(self):
        # Go backwards through the list because we want to sell in reverse order
        # That way the numbers don't change.
        # Here we are counting the items so we can come up with "silver 5" and stuff like that.

        # The word "reference" is used as a more generic term for the word "item" in case you 
        # have a large axe and a large knife, their references are both "large" 

        references = []
        numbered_references = []


        for i in range(0, len(self.inventory)):
            reference = self._item_string_to_reference(self.inventory[i])

            #magentaprint(str(self.inventory[i]) + " " + str(reference), False)

            if self.inventory[i].strip() not in self.keep_list:
                references.append(reference)
                prev_items_with_same_reference = references.count(reference) - 1
                if(prev_items_with_same_reference == 0):
                    numbered_references.append(reference)
                else:
                    numbered_references.append(reference + " " + str(prev_items_with_same_reference + 1))

        numbered_references.reverse()
        return numbered_references
      

    def _item_string_to_reference(self, item_string):
        # 'grey cloak' will change to 'grey'
        # It just takes the first word.
        #magentaprint("item_string: " + item_string.strip(), False)
        return item_string.strip().split(" ")[0].split(".")[0]


    # should probably depend on level.
    keep_list = ["small restorative", "small chalice", "steel bottle"] 
   
    MUD_RETURN_ITEM_SOLD = False

# putting stuff in bags etc.


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




#def extract_sellable_and_droppable(inv_list, keep_list):
    # Now... do fix for selling the wrong thing...
    # Go through and rename things so that the bot
    # can refer to them uniquely.  Use the second word
    # more often.

    # Note: items in keep_list should not yet be removed from the 
    # inventory list.
#    return_list = []
#    unusable_words = []
    #inv_list = inv_list_in[:] # make a copy because I want to change around.
#    for i in range(0, len(inv_list)):
#        item_split = inv_list[i].split(" ")
        # There is an exception from item "two by four" which can't be
        # referred to as 'by'
#        if(my_list_search(item_split, "by") != -1):
#            item_split.remove("by")
        # exception "bolt of cloth"
#        if(my_list_search(item_split, "of") != -1):
#            item_split.remove("of")
                              
        # First check if its a keeper.
        # Then check if its the same as the prev item.
        #   If so then insert the same as the prev item (could be '' if
        #   there was not a matching string)       
#        if(my_list_search(keep_list, inv_list[i]) != -1):
            # If its in the keep list, add it to unusable words and that's it.
            # Do nothing.  However every case does that so do nothing.
#            pass
#        elif(i > 0 and inv_list[i] == inv_list[i-1]):# and
            #my_list_search(item_split, return_list[len(return_list)-1]) != -1):
#            print "Appending " + return_list[len(return_list)-1] + " because i am on " + inv_list[i] + " which is the same as " + inv_list[i-1]
#            return_list.append(return_list[len(return_list)-1])
#        elif(len(item_split) == 1):
            # It's a one-word item.
#            unique_item_string = item_split[0]
#            if(my_list_search(unusable_words, item_split[0]) == -1):
#                return_list.append(unique_item_string)
#            else:
#                print "extract_sellable_and_droppable: could not fit \"" + unique_item_string+"\""
#                return_list.append("")
#        else:
            # Its got more than one word.
#            for n in [1] + [0] + range(2, len(item_split)):
#                unique_item_string = item_split[n]
#                if(my_list_search(unusable_words, unique_item_string) == -1):
#                    return_list.append(unique_item_string)
#                    break
#                elif(n == len(item_split) - 1):
#                    return_list.append("") # add an empty string so that this
                        # remains a parallel list with SELL_LIST
#                    print "extract_sellable_and_droppable: could not fit \""+inv_list[i]+"\""
#        for s in item_split:
#            unusable_words.append(s)
#    return return_list               

