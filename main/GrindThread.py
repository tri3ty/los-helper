
from BotThread import *
from misc_functions import *
from CommandHandler import *
from Inventory import *
from Exceptions import *

class GrindThread(BotThread):
    def __init__(self, character, commandHandler, mudReaderHandler, mud_map, starting_path=None): 
        super().__init__(character, commandHandler, mudReaderHandler, mud_map)

        # Set TOTALPATHS.  Setting it lower than the actual number
        # of paths in decide_where_to_go is a way to truncate paths
        # you don't want to send low level characters on.

        if self.character.level <= 2:
            self.__TOTALPATHS = 8 # Kobolds are level 1 safe.
        elif self.character.level <= 7:
            self.__TOTALPATHS = 10 # include hookers for level 3   
        elif self.character.level <= 10:
            self.__TOTALPATHS = 20 # start the fort and bandits at lvl 8 
        elif self.character.level > 12:
            self.__TOTALPATHS = 24
        else:
            self.__TOTALPATHS = 22 # start the fort and bandits at lvl 8

        self.loot_threshold = 1  # the amount of loot to collect before selling

        if isinstance(starting_path, int) and starting_path < self.__TOTALPATHS:
            self.__nextpath = starting_path
        else:
            self.__nextpath = 0

    def do_run_startup(self):
        if not self.is_character_class("Mon"):
          self.set_up_automatic_ring_wearing()

        if self.direction_list is None:
          self.direction_list = [] #could append areaid45

        return

    def do_pre_go_actions(self):
        # Why are we resting before every 'go'... (?!)
        self.rest_and_check_aura()
        self.check_weapons()
        self.check_armour()
        # Answer: this applies to track grind and not smart grind
        return

    def decide_where_to_go(self):
        magentaprint("Inside decide_where_to_go", False)
        magentaprint("next path = " + str(self.__nextpath), False)
        
        LIMBO_TO_CHAPEL = ["ame", "out", "w", "n", "chapel"]

        SHOP_AND_TIP_PATH = ["out", "south", "west", 'west', 'west', 'south', 'south', "shop",
                          "sell_items", 
                          "out", "southeast", 'east', 'east', 'east', 'east', "northeast", "tip",
                          "drop_items",
                          "out", 'north', 'north', 'west', 'west', 'west', 'north', "chapel"]
                          
        THEATRE_PATH = ["out", "s", "w", "w", "w", "s", "theat", "stair",
                          "cubby", "out", "down", "swing", "seat", "out",
                          "down", "seat", "out", "door", "stage",
                          "side 2", "backstage", "door", "out", "curtain",
                          "stage", "side", "door",
                          "up", "out", "out", "n", "e",
                          "e", "e", "n", "chapel"]
        
        MARKET_PATH = ["out", 's', 'e', 'e', 'e', 'n', 'w', 'w', 'n', 'n',
                          's', 'w', 'e', 's', 'w', 's', 'n', 'w', 'e', 'n',
                          's', 'e', 'e', "out", 's', 'w', 'w', 'w', 'n',
                          "chapel"]
        
        MILITIA_SOLDIERS_PATH = ["out", "s", "e", "s", "s", "s", "w", "gate",
                          "s", "s", "sw", "sw", "sw", "sw", "s", "s", 's',"sw", "se",
                          "s", "s", "s", "s", 's', 's', 's', 's', 's', 'w',
                          'w', 'w', 'w', 'n', 'n', 's', 's', 'e', 'e', 'e', 'e', 'n',
                          'n', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e',
                          "ne", 'e', "ne", "ne", "ne", "ne", "ne", "ne", 'n',
                          'n', 'w', 's', "sw", "ne", 'n', 'e', 'n', 'n', 'n',
                          'n', 'n', 'n', 'n', 'n', 'n', 'n', "nw", "nw", "nw",
                          "pathway", "nw", 'n', 'n', 'n', "nw", "nw",
                          'n', 'n', "gate", 'w', 'n', "nw", "nw", 'n',
                          'e', 'e', 'e', 's', 's', 's', 's', "gate", 
                          's', 's', "se", "se",
                          's', 's', 's', "se", "s", 'w', 'w', 'w', "nw",
                          "nw", 'n', "gate", 'e', 'n', 'n', 'n', 'w', 'n',
                          "chapel"]
        
        KOBOLD_PATH = ['out', 'south', 'east', 'south', 'south', 'south',
                        'west', 'gate', 'south', 'southeast', 'southeast', 'east', 'east',
                        'east', 'southeast', 'southeast', 'southeast', 'south', 'south', 'south',
                        'south', 'south', 'east', 'east', 'southeast', 'east', 'south', 'south',
                        'south', 'south', 'glowing portal', "passage", "mines",
                          'down', 'n', 'n', 'n', 'n', "ne", 'n', 'w', 'n', 'n', 'e',
                          "door", 'w', "gully", 'up', "boulder", 'up',
                          "cave 3", 'ne', 'ne', 'n', 's', 'up', 'e', 'se', 
                          'cave', 'out', 
                          # Note: You can remove the following line of code 
                          # to remove the kobold guards and priests fights.
                          # Priests turn you very blue.  These fights may be 
                          # difficult.
                          # Also useful to test mobs who join in.
                          # They're commented because kobolds are allowed when you're 
                          # pale blue, which is one off of blue... and these guards 
                          # and priests are dangerous unless the bot decides on his 
                          # own to engage.  Todo: check aura here (if health is 
                          # high enough,) and go in if all's good.  Even fight the 
                          # priests - because the more 'good' we can get the 
                          # more chalices we can farm.
                          #"prepare", 'e', 'ne', "door", "door", "prepare", 'sw','w',
                          "ladder", 'cave', 'out', "sw", 'w', 
                          # Comment out insane kobold (TODO: check level here)
                          # 'cave', 'out', 
                          "sw", 'se', 'nw', 'w', "out", 'down',
                          "boulder", 'down', 'down', 'e', "door", 'w', 's', 's',
                          'e', 's', "sw", 's', 's', 's', 's', "gully",
                          'glowing portal', 'passage', 'coral', 'north', 'north',
                          'north', 'north', 'west', 'northwest', 'west', 'west',
                          'north', 'north', 'north', 'north', 'north', 'northwest',
                          'northwest', 'northwest', 'west', 'west', 'west', 'northwest',
                          'northwest', 'north', 'gate', 'east', 'north', 'north', 'north',
                          'west', 'north', 'chapel']

        CORAL_ALLEY_PATH = ["out", "s", 'e', 's', 's', 's', 'w', 'gate',
                              's', 'se', 'se', 'e', 'e', 'e',
                              'se', 'se', 'se', 's', 's', 's', 's', 'w',
                              'alley', 's', 's', 'door', 'stairs',
                              # angry hooker should be avoided unless lvl 5.
                              #'do 3', 'ou',
                              'stairs', 'out', 's',
                              #'w', 'e', #for zombies
                              # noticed drunken troublemakers arrive one east
                              # not sure what safest exit is... go north.
                              # red axer lvl 2 dropped studded leather collar
                              'n', 'n', 'n', 'n',
                              'e', 'n', 'n', 'n', 'n', 'nw', 'nw', 'nw',
                              'w', 'w', 'w', 'nw', 'nw', 'n',
                              'gate', 'e', 'n', 'n', 'n', 'w', 'n', 'chapel']
        
        FORT_PATH = ["out", 'n', 'n', 'w', "gate", 'n', 'n', 'n',
                          'n', 'n', "gate", 'n', 'n', 'w', 's', 's', 'e',
                          "gate", 's', 's', 's', 's', 's', 'gate', 'e',
                          's', 's', "chapel"]
        
        NORTHERN_BANDITS_PATH = ['out', 'n', 'n', 'w', 'gate', 'n', 'n', 'n',
                          'n', 'n', 'gate', 'n', 'n', 
                          "gate", 'n',
                          "nw", "nw", "sw", "sw", "sw", "sw", 's', "sw", "sw",
                          'w', 'w', "sw", "sw", "sw", "sw", "sw", "sw", 'w',
                          'w', 'w', 'w', "nw", 'w', 'w', "nw", "sw", "nw",
                          'w', 'w', 'w', "nw", 'w', 'w', 'w', 'w',
                          "south", 's', 's', 'n', 'n', 'n',
                          'e', 'e', 'e', 'e', "se", 'e', 'e', 'e',
                          "se", "ne", "se", 'e', 'e', "se", 'e', 'e', 'e',
                          'e', "ne", "ne", "ne", "ne", "ne", "ne", 'e', 'e',
                          "ne", "ne", 'n', "ne", "ne", "ne", "ne", "se", "se",
                          's', "gate", 's', 'w', 'e', 's',
                          "gate", 's', 's', 's', 's', 's', "gate", 'e', 's',
                          's', "chapel"]

        DWARVEN_FIELD_WORKERS_PATH = ['out', 'south', 'east', 'south', 'south',
                            'south', 'west', 'gate', 'south', 'southeast', 'southeast',
                            'east', 'east', 'east', 'pathway', 'northwest', 'north', 'north',
                            'north', 'southeast', 'east', 'east', 'gate', 'east', 'building',
                            'out', 'east', 'east', 'southeast', 'field', 'road', 'southeast',
                            'southeast', 'southeast', 'field', 'stile', 'stile', 'road',
                            'northwest', 'northwest', 'northwest', 'northwest', 'west', 'west',
                            'west', 'gate', 'west', 'west', 'northwest', 'south', 'south', 'south',
                            'southeast', 'south', 'west', 'west', 'west', 'northwest', 'northwest',
                            'north', 'gate', 'east', 'north', 'north', 'north', 'west', 'north', 'chapel']

        #both gates close at night unforunately...
        FIELD_WORKERS_PATH = ['out', 'south', 'east', 'south', 'south', 'south','west',
                            'gate', 'south', 'southeast', 'southeast', 'east', 'east',
                            'east', 'pathway', 'northwest', 'north', 'north', 'north',
                            'northwest', 'northwest', 'north', 'north', 'gate', 'west',
                            'north', 'northwest', 'northwest', 'north', 'gate', 'west',
                            'west', 'southwest', 'southwest', 'west', 'west', 'west',
                            'southwest', 'southwest', 'southeast', 'southeast', 'south',
                            'gate', 'stile', 'northwest', 'southeast', 'southwest',
                            'northeast', 'stile', 'gate', 'north', 'northwest', 'northwest',
                            'west', 'west', 'gate', 'south', 'west', 'west', 'west', 'north', 'chapel']

        #Contains lvl 2&3 mobs (stacker, furniture maker, sawmill operator, mill worker) and lvl 6 mobs (sawmill / mill supervisors)
        MILL_WORKERS = ['out', 'south', 'east', 'south', 'south', 'south', 'west', 'gate',
                        'south', 'south', 'south', 'south', 'south', 'southwest', 'south',
                        'southeast', 'southwest', 'south', 'south', 'southeast', 'south',
                        'south', 'southwest', 'bridge', 'south', 'southwest', 'west', 'canal',
                        'south', 'south', 'south', 'east', 'east', 'west', 'south', 'east',
                        'west', 'north', 'north', 'east', 'south', 'south', 'southwest', 'out',
                        'west', 'north', 'north', 'north', 'north', 'north', 'northwest',
                        'northeast', 'north', 'north', 'north', 'northeast', 'northeast',
                        'northeast', 'northeast', 'north', 'north', 'gate', 'east', 'north',
                        'north', 'north', 'west', 'north', 'chapel']

        RANCHER_SENTRY = ['out', 'south', 'east', 'south', 'south', 'south', 'west', 'gate',
                        'south', 'southeast', 'southeast', 'east', 'east', 'east', 'pathway',
                        'northwest', 'north','north', 'north', 'northwest', 'northwest', 'north',
                        'north', 'gate', 'northeast', 'north', 'northeast', 'north', 'gate',
                        'east', 'east', 'east', 'north', 'north', 'northeast', 'north',
                        'northeast', 'gate', 'arch', 'north', 'east', 'north', 'northwest',
                        'gate', 'north', 'east', 'east', 'south', 'east', 'north', 'south',
                        'west', 'west', 'west', 'gate', 'southwest', 'south', 'east', 'south',
                        'arch', 'gate', 'southwest', 'south', 'southwest', 'south', 'south', 'west',
                        'west', 'west', 'gate', 'south', 'southwest', 'south', 'southwest', 'gate',
                        'south', 'south', 'southeast', 'southeast', 'south', 'south', 'south',
                        'southeast', 'south', 'west', 'west', 'west', 'northwest', 'northwest',
                        'north', 'gate', 'east', 'north', 'north', 'north', 'west', 'north', 'chapel']

        #aid418, 1975, 1979, 1951, 415, 45
        SPIDER_FOREST = ['areaid418', 'areaid1975', 'areaid1979', 'areaid1951', 'areaid415', 'areaid45']

        #The following areas repeat a bit because the spawns are fast
        KNIGHTS = ['areaid1904', 'areaid1912', 'areaid1909', 'areaid1913',
                          'areaid1904', 'areaid1912', 'areaid1909', 'areaid1913',
                          'areaid1904', 'areaid1912', 'areaid1909', 'areaid45',] #end with chapel

        GNOLL_CAMP = ['areaid1574', 'areaid800', 'areaid1574', 'areaid800', 'areaid1574', 'areaid45', ]

        PATH_TO_SKIP_WITH = [ 'out', 'chapel' ]
        #return SHOP_AND_TIP_PATH
        
        if (self.character.DEAD):
            self.character.DEAD = False
            self.character.DEATHS += 1
            magentaprint("Died; Pulling up my bootstraps and starting again", False)
            return LIMBO_TO_CHAPEL

        self.__nextpath = (self.__nextpath + 1) % self.__TOTALPATHS

        if (self.__nextpath % 2 == 0):
            self.inventory.get_inventory()
            if len(self.inventory.sellable()) > self.loot_threshold:
                return SHOP_AND_TIP_PATH
            else:
                self.__nextpath = (self.__nextpath + 1) % self.__TOTALPATHS

        #return KOBOLD_PATH

        if(self.__nextpath == 1):
            return THEATRE_PATH

        elif(self.__nextpath == 3):
            return MARKET_PATH 

        elif(self.__nextpath == 5):
            return MILITIA_SOLDIERS_PATH 

        elif(self.__nextpath == 7):
            if self.character.AURA_SCALE < self.character.AURA_LIST.index('pale blue') and \
               self.character.AURA_SCALE <= self.character.AURA_PREFERRED_SCALE: 
                return KOBOLD_PATH
            else:
                magentaprint("Not going to do kobolds. Current aura, and preferred: %s,  %s" % 
                             (self.character.AURA_SCALE, self.character.AURA_PREFERRED_SCALE))
                self.__nextpath = self.__nextpath + 1  # So that we don't go selling
                return PATH_TO_SKIP_WITH

        elif(self.__nextpath == 9):
            # hookers ... I would avoid the drunken trouble makers, but I don't
            # quite remember where they are and don't want to go through Amber
            # Also I think it's safe enough in the dark... maybe just lvl 4 
            # there are thugs
            if(self.character.level <= 6):
                return CORAL_ALLEY_PATH
            else:            
                self.__nextpath = self.__nextpath + 1  # So that we don't go selling
                return PATH_TO_SKIP_WITH 

        elif(self.__nextpath == 11):
            return FORT_PATH

        elif(self.__nextpath == 13):
            if self.character.AURA_SCALE < self.character.AURA_LIST.index('pale blue') or \
               self.character.AURA_SCALE <= self.character.AURA_PREFERRED_SCALE:
                return NORTHERN_BANDITS_PATH
            else:
                magentaprint("Not going to do bandits. Current aura, and preferred: %s,  %s" % 
                             (self.character.AURA_SCALE, self.character.AURA_PREFERRED_SCALE))
                self.__nextpath = self.__nextpath + 1   # So that we don't go selling
                return PATH_TO_SKIP_WITH
        elif(self.__nextpath == 15):
            return DWARVEN_FIELD_WORKERS_PATH
        elif(self.__nextpath == 17):
            return MILL_WORKERS
        elif(self.__nextpath == 19):
            return RANCHER_SENTRY
        elif(self.__nextpath == 21):
            return SPIDER_FOREST
        elif(self.__nextpath == 23):
            return GNOLL_CAMP
        # elif(self.__nextpath == 25):
        #     return KNIGHTS
        else:
            magentaprint("Unexpected case in decide_where_to_go, nextpath==" +
                         str(self.__nextpath))
            return PATH_TO_SKIP_WITH
        return PATH_TO_SKIP_WITH

    def do_on_succesful_go(self):
        if len(self.direction_list) != 0:
          self.direction_list.pop(0)
  
        self.character.MOBS_JOINED_IN = [] 
        self.character.MOBS_ATTACKING = []

    def do_on_blocking_mob(self):
        self.engage_monster(self.character.GO_BLOCKING_MOB)
        self.get_items()
        self.character.GO_BLOCKING_MOB = ""
        self.engage_mobs_who_joined_in()
        self.engage_any_attacking_mobs()
        self.check_weapons()
        
        if (not self.character.BLACK_MAGIC):
            self.heal_up()
        return

    def do_post_go_actions(self):
        #here we would implement combat or whatever other other actions we want to do before we decide where to go again
        # Maybe this is more for do_on_successful_go()(?)
        if self.ready_for_combat():
            new_target = self.decide_which_mob_to_kill(self.character.MONSTER_LIST)
        else:
            new_target = ""
            magentaprint("GrindThread.do_post_go_actions() calling do_rest_hooks()")
            # Commented - I don't understand what do_rest_hooks is supposed to do at all...
            # self.do_rest_hooks()

        while new_target != "" and not self.is_stopping():
            # MudReader maintains MONSTER_LIST pretty well by
            # adding and removing.  
            # It will not remove from MOBS_JOINED_IN nor 
            # MOBS_ATTACKING because the three lists can contain 
            # common mobs.  So before engaging a mob in one of the 
            # latter two lists the bot should check that it is 
            # still in the MONSTER_LIST.  Also be mindful of timing:
            # MOBS_ATTACKING might not be populated as soon as the 
            # bot enters the room - that's why they are engaged last
            # (as a cleanup).

            # Now we can reference MONSTER_LIST again.  Note that
            # MudReader has already removed all of the mobs that we
            # killed.  (That's in fact how we knew combat was over)
            # The higher priority mobs were in the other lists 
            # and will also have been removed from MONSTER_LIST
            
            magentaprint("Targeting: " + new_target)

            self.engage_monster(new_target)
            self.get_items()
            self.engage_mobs_who_joined_in()
            self.engage_any_attacking_mobs()
            self.check_weapons()
            
            if (not self.character.BLACK_MAGIC):
                self.heal_up()
            
            if(self.ready_for_combat()):
                magentaprint("Picking a new target since " + new_target + " was defeated")
                new_target = self.decide_which_mob_to_kill(self.character.MONSTER_LIST)
            else:
                new_target = ""
        return

    def do_go_hooks(self, exit_str):
      #if you want to define custom hooks like sell_items / drop_items etc... you can do so here

      if (exit_str == "nw" or exit_str == "ne" or
           exit_str == "sw" or exit_str == "se" or
           exit_str == 'n' or exit_str == 'e' or
           exit_str == 's' or exit_str == 'w'):
            # self.commandHandler.process(exit_str)
            # return self.check_for_successful_go() 
            # return self.check_for_successful_go() 
            # return self.go(exit_str)   # Erhm self.go calls us, not the other way around
            self.commandHandler.go.persistent_execute(exit_str)
            return self.commandHandler.go.success
      elif exit_str == "prepare":
          self.commandHandler.process(exit_str)
          return True
      elif exit_str == "sell_items":
          self.sell_items()
          return True
      elif exit_str == "drop_items":
          self.drop_items()
          return True

      return super().do_go_hooks(exit_str)

# Just thinking about changing top level...
 
# I don't like this version because mobs will leave and arrive while in
# combat.  It makes more sense to recheck list every time I enter combat...
# right?  That means doing a look between every mob.  I want to avoid the
# complication of multiple threads, I want the two threads to interact only
# via flag handshakes... so I don't want MUD_read to edit monster_list.
# How about MUD_read sets a flag when a mob arrives or leaves and I update
# monster list only when I have to?  Still doing the unnecessary look although
# not very often.  Maybe its okay to edit monster_list in the case of
# arriving mobs... and leaving mobs?  Seems like a bad idea.  However, when
# do I react to a guard arriving?  I think that I need a list that MUD_read
# will edit and I need to keep a local copy.  Hey I'm already doing it.

# Okay.  So monster_list is the local copy, and MUD_read will edit
# MONSTER_LIST relatively freely:
#   - Full update when MONSTER_CHECK_FLAG is set high by bot.
#   - one-by-one additions if monsters arrive (no flag)
# Then I can check for arrived monsters in the bot by checking if the
# lists are different.
# However, that is for later.  I wanted to make it possible to implement later
# fleeing when a guard arrives, but I won't be doing that yet.

# New approach is to keep a mob list up to date (with mob arrivals and
# departures, ideally,) and then changing logic to say, decide on WHICH
# mob to kill.  That also doubles as deciding whether to engage.  Its a
# sensible way to check for guards.
 
# You can't.  Its broken.  (Means the bot ran out of weapons.)