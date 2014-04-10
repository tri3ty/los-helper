
import threading
from threading import Thread
import atexit 
import time
import re
import sys
import select

from misc_functions import *
from KillThread import *
from CastThread import *
from MyBuffer import *
from MyMudWaiterFlags import *

class MudReaderThread ( threading.Thread ):
    """This thread watches the the MUD output and appends it 
    to the buffer for the MudReaderThread to read it."""
    
    def __init__(self, MUDBuffer, Character, ConsoleHandler):
        Thread.__init__(self)       
        # Constants
        self.ASCII_EOT = 4
        self.ASCII_ESC = 27
        self.ASCII_m = 109
        
        self.MUDBuffer = MUDBuffer
        self.Character = Character
        self.ConsoleHandler = ConsoleHandler
        
        #TODO: change these all to mud waiter flags
        self.CHECK_GO_FLAG = False
        self.CHECK_AURA_FLAG = False
        self.CHECK_AURA_SUCCESS = False
        self.CHECK_SELL_FLAG = False
        self.CHECK_INVENTORY_FLAG = False
        #self.CHECK_KILL_MONSTER_GONE = False # This one isn't used yet, I think it's to react to when a monster flees
        
        self.BotReactionList = []
        
        # Internal Variables
        # variables used for the MUD_output_check function
        # These are used if I decide to implement MUD_output_check
        # which allows you to check for a non-hardcoded regex.
        # No need.
        #self.__check_regex_true = ""
        #self.__check_regex_false = ""
        #self.__check_M_obj = None
        #self.__check_flag = False 
        
        # Two parallel arrays.
        # I believe this to be appropriate for what they are used for.
        # These were used when I wanted to act when a flag was raised.
        # I decided that was too complicated.
        #self.flag_names = ["aura", "go", "inventory", "monster", "sell"]
        #self.request_flags = [False, False, False, False, False]
                            #{"aura":False,
                            #"go":False, 
                            #"inventory":False,
                            #"monster":False,
                            #"sell":False}
            # These flags are set by the MudHandler and notify the 
            # MudReader to look for certain text patterns.  For 
            # example the inventory flag notifies the MudReader to 
            # look for the inventory coming along into the buffer. 
            # Typically a flag is set when something calls one of the 
            # MudHandler functions.
            # order: alphabetical
            # ... the better pattern is for the MudReader (observer) to 
            # always match the pattern and let things subscribe to notifications.
        
        self.__stopping = False
        atexit.register(self.stop)
                
    def stop(self):
        self.__stopping = True
    
    def run(self):
        self.__left_off_index = 0  # This is a save point index of the buffer 
                            # so that we know where in the buffer to begin 
                            # printing again.
        currently_escaping = False  # Used to filter escape sequences
        text_buffer = ""
        while(not self.__stopping):
            time_loop_start = time.time()
            
            # Do a wait loop.  This means that the main loop will 
            # iterate every time new text comes in.
            # Put in a sleep so the loop doesn't hog too many resources
            timeout = 3
            start_time = time.time()
            run_time = 0

            while(self.__left_off_index == len(self.MUDBuffer.buffer) and 
                run_time < timeout):
                 time.sleep(0.005) 
                 run_time = time.time() - start_time
                
            # Note that that check on the length of the MUD buffer means 
            # that now there's probably new text data.  It doesn't matter 
            # if it timed out, the loop will just iterate with no new data.                 
            
            time_loop_after_waiting = time.time()
                 
            # There seems to be ANSI escape sequence codes which I
            # am going to filter out.  
            # If you are trying to read it, also remember that
            # currently_escaping may remain false over top of a loop
            # iteration.  They're ANSI escape codes (read wikipedia)
                       
            MUDBuffer_copy = self.copy_MUDBuffer()
            new_left_off_index = len(self.MUDBuffer.buffer)            
            
            # First print the new characters.
            unparsed_unprinted_characters_from_server = list(MUDBuffer_copy[self.__left_off_index:len(MUDBuffer_copy)])
            self.__left_off_index = new_left_off_index

            text_out = ""
            num_escape_characters=0
            for c in unparsed_unprinted_characters_from_server:
                if (ord(c) == self.ASCII_EOT):
                    magentaprint("MudReaderThread: Saw the EOT, quitting.")
                    self.stop()
                elif(ord(c) == self.ASCII_ESC):
                    num_escape_characters = num_escape_characters + 1
                    escape_sequence = "" + c
                    currently_escaping = True  
                elif (currently_escaping and ord(c) == self.ASCII_m):
                    num_escape_characters = num_escape_characters + 1
                    escape_sequence = escape_sequence + c
                    currently_escaping = False
                    # Finished an escape sequence... change color.
                    # Print all the stuff in buffer from before the esc
                    # Must be printed here so that the color change occurse 
                    # at the right point.
                    #sys.stdout.write(text_out)
                    manage_telnet_output(text_out)
                    text_buffer = text_buffer + text_out
                    text_out = ""
                    self.set_colour(escape_sequence);  # Call subroutine to do this.
                elif (currently_escaping):
                    escape_sequence = escape_sequence + c
                    num_escape_characters = num_escape_characters + 1
                else:  #not currently escaping:             
                    text_out = text_out + c
            # Check for some colors.
                    
            # Print to console.
            #sys.stdout.write(text_out)
            manage_telnet_output(text_out)

            # Not using print because it inserts extra spaces.
            
            #sys.stdout.write("/"+out_str)  # puts slashes between text fragments for debugging
            sys.stdout.flush()
                                        
            # Debug:  Print ascii out!  (doesn't do every character)
            #for i in range(0, len(out_str)):
            #    sys.stdout.write(str(ord(out_str[i])) + ' ')

            # Store that in a text buffer.  
            text_buffer = text_buffer + text_out
            
            # Unfortunately there are two buffers now, one with and one without 
            # the escape sequences.
            
            # Trim buffers if they are too long.
            L = len(text_buffer)
            if(L >= self.MUDBuffer.size):
                text_buffer = text_buffer[L-self.MUDBuffer.size:L]
            #print "<REPRINT>"+MUD_buffer+"<\REPRINT>"
            
            while(self.MUDBuffer.access_flag == True):
                time.sleep(0.05)

            self.MUDBuffer.access_flag = True
            L = len(self.MUDBuffer.buffer)

            if(L > self.MUDBuffer.size):
                trim_amount = L - self.MUDBuffer.size
                self.__left_off_index = self.__left_off_index - trim_amount
                self.MUDBuffer.buffer = self.MUDBuffer.buffer[trim_amount:L]
                #magentaprint("Trimmed MUDBuffer: "+str(trim_amount))
                #magentaprint("L is "+str(L))
                #magentaprint("MUDBuffer.size is "+str(self.MUDBuffer.size))
            
            self.MUDBuffer.access_flag = False

            ###### Now match the buffer with some REs  #######
            text_buffer_trunc = 0
            
            #### Bot Reactions ####

            # TODO: create a flag that stops other threads from writing the list
            # while I'm in here.  (could cause a missed reaction)
            reactions_to_delete = []
            for reaction in self.BotReactionList:
                for regex in reaction.regexes:
                    M_obj = re.search(regex, text_buffer)

                    if(M_obj != None):
                        # magentaprint("MudReaderThread: calling notify on " + str(reaction))
                        reaction.notify(regex, M_obj)  
                        text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                    
                    if reaction.unregistered:
                        reactions_to_delete.append(reaction)
         
            reaction_counter = 0  # TODO: delete reaction_counter and all reaction printing
            for reaction in reactions_to_delete:
                self.BotReactionList.remove(reaction)
                reaction_counter = reaction_counter + 1
            
            if (reaction_counter > 0):
                magentaprint("MudReaderThread removed " + str(reaction_counter) + 
                             " reactions," + str(len(self.BotReactionList)) + 
                             " reactions left.")
                             # Seeing "2 reactions left" here is perfect (means combat threads are getting removed.)
                             # The two reactions are the ring and wield reactions.

            #### Prompt ####
            M_obj = re.search("\[(.*?) H (.*?) M\]", text_buffer)
            if (M_obj):
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])                
                try:
                    #magentaprint("MudReader: Got health %s mana %s." % (health, mana))
                    self.Character.HEALTH = int(M_obj.group(1))
                    self.Character.MANA = int(M_obj.group(2))
                except ValueError:
                    # The exception is if there's a glitch in the ANSI code or
                    # character order... happens sometimes.  (Think its the
                    # MUD's fault)  Its not critical...
                    magentaprint("MudReader: Got exception when reading prompt.")
                    pass

            #### INFO screen stuff ####
            # Note: First instinct was to parse whole screen at once but that 
            # doesn't seem necessary now. 
            # Nor does it seem necessary to even have a flag with the Bot... but the bot may need that.
            s_numbered = "( 1st| 2nd| 3rd| 4th| 5th| 6th| 7th| 8th| 9th| 10th| 11th| 12th| 13th| 14th| 15th| 16th| 17th| 18th| 19th)?"

            M_obj = re.search("     (.+?) the (.+?), a (.+?) of the" + s_numbered + " level    ",text_buffer)
            if(M_obj != None):
                self.Character.NAME = M_obj.group(1)
                self.Character.RACE = M_obj.group(2)
                self.Character.TITLE = M_obj.group(3)
                self.Character.LEVEL = int(re.search("\d+",M_obj.group(4)).group(0))
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                #magentaprint("MudReader got name, race, class, level: %s %s %s %s" % 
                #            (self.Character.NAME, self.Character.RACE, 
                #             self.Character.TITLE, self.Character.LEVEL))  
                # Print checks out.
                
            M_obj = re.search("Your preferred alignment is (.+?)     ",text_buffer)
            if(M_obj != None):
                self.Character.AURA_PREFERRED = M_obj.group(1)
                self.Character.AURA_PREFERRED_SCALE = my_list_search(self.Character.AURA_LIST, 
                                                                          self.Character.AURA_PREFERRED)
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                #magentaprint("MudReader got AURA_PREFERRED and scale: %s %s " % 
                #             (self.Character.AURA_PREFERRED, self.Character.AURA_PREFERRED_SCALE)) 
                # Print checks out.

            #M_obj = re.search("     Sharp   : (\d+) +%  |  |     Earth : (\d+) +%     |",text_buffer)
            #if(M_obj != None):
            #    self.Character.SKILLS['sharp'] = M_obj.group(1)
            #    self.Character.SKILLS['earth'] = M_obj.group(2)
            #    text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            #    magentaprint("MudReader got sharp and earth: %s %s " % 
            #                 (self.Character.SKILLS['sharp'], self.Character.SKILLS['earth']))
            
            #M_obj = re.search("     Thrust  : (\d+) +%  |  |     Water : (\d+) +%     |",text_buffer)
            #if(M_obj != None):
            #    self.Character.SKILLS['thrust'] = M_obj.group(1)
            #    self.Character.SKILLS['water'] = M_obj.group(2)
            #    text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            #    magentaprint("MudReader got thrust and water: %s %s " % 
            #                 (self.Character.WEAPON_SKILLS['thrust'], self.Character.MAGIC_SKILLS['water']))

            #M_obj = re.search("     Blunt   : (\d+) +%  |  |     Fire  : (\d+) +%     |",text_buffer)
            #if(M_obj != None):
            #    self.Character.SKILLS['blunt'] = M_obj.group(1)
            #    self.Character.SKILLS['fire'] = M_obj.group(2)
            #    text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            #    magentaprint("MudReader got blunt and fire: %s %s " % 
            #                 (self.Character.WEAPON_SKILLS['blunt'], self.Character.MAGIC_SKILLS['fire']))

            #M_obj = re.search("     Pole    : (\d+) +%  |  |     Wind  : (\d+) +%     |",text_buffer)
            #if(M_obj != None):
            #    self.Character.SKILLS['pole'] = M_obj.group(1)
            #    self.Character.SKILLS['wind'] = M_obj.group(2)
            #    text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            #    magentaprint("MudReader got pole and wind: %s %s " % 
            #                 (self.Character.WEAPON_SKILLS['pole'], self.Character.MAGIC_SKILLS['wind']))

            #M_obj = re.search("     Missile : (\d+) +%  |  |     Astral: (\d+) +%     |",text_buffer)
            #if(M_obj != None):
            #    self.Character.SKILLS['missile'] = M_obj.group(1)
            #    self.Character.SKILLS['astral'] = M_obj.group(2)
            #    text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            #    magentaprint("MudReader got missile and astral: %s %s " % 
            #                 (self.Character.WEAPON_SKILLS['missile'], self.Character.MAGIC_SKILLS['astral']))
            
            #TODO: continue with MAXHP, MAXMP, GOLD, EXP, LEVELGOLD, LEVELEXP, etc.
            M_obj = re.search("Exp : (\d+)",text_buffer)
            if (M_obj != None):
                self.Character.TOTAL_EXPERIENCE = M_obj.group(1)

            M_obj = re.search("Gold : (\d+)",text_buffer)
            if (M_obj != None):
                self.Character.TOTAL_GOLD = M_obj.group(1)

            #### Casting regexes ####
            
            # Now we are setting flags to tell the Handler that the cast command 
            # went through (instead of stopping the cast/kill threads ourselves.)
            # Actually, we're scrapping the flags
            M_obj = re.search("That spell does not exist\.", text_buffer)
            if(M_obj):
                # refresh cast clock (cooldown wasn't used)
                self.Character.CAST_CLK = time.time() - self.Character.CAST_WAIT 
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("You don't know that spell\.", text_buffer)
            if(M_obj):
                self.Character.CAST_CLK = time.time() - self.Character.CAST_WAIT
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("You cannot meet the casting cost!", text_buffer)
            if(M_obj):
                self.Character.CAST_CLK = time.time() - self.Character.CAST_WAIT 
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("Spell name is not unique\.", text_buffer)
            if(M_obj):
                self.Character.CAST_CLK = time.time() - self.Character.CAST_WAIT 
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("Cast what\?", text_buffer)
            if(M_obj):
                self.Character.CAST_CLK = time.time() - self.Character.CAST_WAIT 
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("Your spell fails\.", text_buffer)
            if(M_obj):
                self.Character.CAST_CLK = time.time() - self.Character.CAST_WAIT
                # TODO: BUG
                #  - some spells can be cast again immediately if they fail and some cannot
                #  - equivalently you can move or not move immediately after failing a spell
                #    based on what spell it was.
                #  - Spells that should reset here are vigor, light, show-aura
                #  - spells that should not reset are black magic.  
                    # reset cast clock
                # Do not kill the cast thread if the spell failed  
                if(self.CHECK_AURA_FLAG):
                    self.CHECK_AURA_FLAG=0;
                    self.CHECK_AURA_SUCCESS=0;
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                
            #### Haste ####
            M_obj = re.search("You feel yourself moving faster\.",text_buffer)
            if(M_obj != None):
                self.Character.HASTING = True
                self.Character.ATTACK_WAIT = self.Character.ATTACK_PERIOD_HASTE
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("You're already hastened\.",text_buffer)
            #TODO: Its still possible that haste state is invalid.  Here user types
            #haste and I trigger on "You're already hastened"... can by improved by
            #doing everything under covers! (maybe send a command to telnet and use
            #the response to update variables but don't print anything!  This could
            #be a thread.  Or I could cover all the cases that invalidate haste,
            #which is mainly logging in.  TODO: Login_Update() (do with main thread
            #before raw_input call.)
            if(M_obj != None):
                self.Character.HASTING = True
                self.Character.ATTACK_WAIT = self.Character.ATTACK_PERIOD_HASTE
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("You feel slower\.",text_buffer)
            if(M_obj != None):
                self.Character.HASTING = False
                self.Character.ATTACK_WAIT = self.Character.ATTACK_PERIOD
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                            
            #### Set weapon strings ####
            M_obj = re.search("You wield (.*?)\.", text_buffer)
            if (M_obj != None and not re.search(" in your off hand", M_obj.group(1))):
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                weap1 = M_obj.group(1)
                # Clip the "a " or the "some "
                if(re.match("a ", weap1)):
                    weap1 = weap1[2:]
                elif(re.match("some ", weap1)):
                    weap1 = weap1[5:]
                self.Character.WEAPON1 = weap1
            M_obj = re.search("You wield (.*?) in your off hand\.", text_buffer)
            if (M_obj != None):
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                weap2 = M_obj.group(1)
                if(re.match("a ",weap2)):
                    weap2 = weap2[2:]
                elif(re.match("some ",weap2)):
                    weap2 = weap2[5:]
                self.Character.WEAPON2 = weap2
                      
            #### Shopping stuff ####
            # On gold pickup:
            M_obj = re.search("You now have (.+?) gold coins", text_buffer)
            if(M_obj):
                self.Character.GOLD = int(M_obj.group(1))
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            # On tip drop:                    
            M_obj = re.search("You have (.+?) gold\.", text_buffer)
            if(M_obj):
                self.Character.GOLD = int(M_obj.group(1))
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])

            # On vendor ... also manage the sell check flag (signal to bot)
            M_obj = re.search("The shopkeep gives you (.+?) gold for (an?|some) (.+?)\.", text_buffer)
            if(M_obj):
                self.Character.GOLD = self.Character.GOLD + int(M_obj.group(1))
                self.Character.MUD_RETURN_ITEM_SOLD = True
                self.CHECK_SELL_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("The shopkeep won't buy that from you\.", text_buffer)
            if(M_obj):
                self.Character.MUD_RETURN_ITEM_SOLD = False
                self.CHECK_SELL_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("It isn't empty!", text_buffer)
            if(M_obj):
                self.Character.MUD_RETURN_ITEM_SOLD = False
                self.CHECK_SELL_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("The shopkeep says, \"I won't buy that rubbish from you\.\"", text_buffer)
            if(M_obj):
                self.Character.MUD_RETURN_ITEM_SOLD = False
                self.CHECK_SELL_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            M_obj = re.search("Sell what\?", text_buffer)
            if(M_obj):
                self.Character.MUD_RETURN_ITEM_SOLD = False
                self.CHECK_SELL_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                
            #### Check if we're dead ####
            M_obj = re.search("Obvious exits: amethyst", text_buffer)
            if(M_obj):
                print ("Shucks anyhow")
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                self.Character.DEAD = True
                #self.stop()  # breaks program but allows me to see what happened

            ########    Monster Gets Killed    ######
            
            #M_obj = re.search("Your enemy, the" + s_numbered + " (.+?) has been defeated\.", MUDBuffer)            
            M_obj = re.search("Your attack overwhelms the" + s_numbered + " (.+?) and (s?he|it) collapses!", text_buffer)
            if(M_obj != None):
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                if(my_list_search(self.Character.MONSTER_LIST, M_obj.group(2)) != -1):
                    magentaprint( "Removing " + M_obj.group(2) + " from MONSTER_LIST")
                    self.Character.MONSTER_LIST.remove(M_obj.group(2))
                else:
                    magentaprint("MudReaderThread: Could not remove " + M_obj.group(2) + " from MONSTER_LIST")
            # Experience
            M_obj = re.search("You gain (.+?) experience\.", text_buffer)       
            if(M_obj):
                self.Character.MOBS_KILLED += 1
                self.Character.EXPERIENCE = self.Character.EXPERIENCE + int(M_obj.group(1))
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            # Monster flees.
            #TODO chasing function.
            M_obj = re.search("The" + s_numbered + " (.+?) flees to the (.+?)\.", text_buffer)
            if(M_obj):
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                if(my_list_search(self.Character.MONSTER_LIST, M_obj.group(2)) != -1):
                    magentaprint("Removing " + M_obj.group(2) + " from MONSTER_LIST")
                    self.Character.MONSTER_LIST.remove(M_obj.group(2))
                else:
                    magentaprint("MudReaderThread: Could not remove " + M_obj.group(2) + " from MONSTER_LIST")
                # TODO: make sure we're matching damage text for all kinds of attacks.
                
            # Stop combat threads on "You don't see that here"
            M_obj = re.search("You don't see that here\.",text_buffer)
            # I don't like PREV_COMMAND.
            # "You don't see that here" needs to terminate kk because
            # MONSTER_LIST can be wrong if a mob arrives at the same time
            # as I leave an area.  So I'm removing prev command and
            # combat will always be stopped on "You don't see that here
            #prev_cmd_kill = re.match("k ",PREV_COMMAND)
            #if(M_obj != None and prev_cmd_kill != None):
            if(M_obj):
                self.Character.ATTACK_CLK = time.time()-self.Character.ATTACK_WAIT
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])

            M_obj = re.search("They are not here\.", text_buffer)
            if(M_obj):
                self.Character.MONSTER_LIST = []
                self.Character.CAST_CLK = time.time() - self.Character.CAST_WAIT
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                               
            # Monster wanders to specific exit
            M_obj = re.search("The" + s_numbered + " (.+?) just wandered to the .+?\.", text_buffer)
            if(M_obj):
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                if(my_list_search(self.Character.MONSTER_LIST, M_obj.group(2)) != -1):
                    self.Character.MONSTER_LIST.remove(M_obj.group(2))
                else:
                    magentaprint("MudReaderThread: Could not remove " + M_obj.group(2) + " from MONSTER_LIST")
            # Monster wanders away
            M_obj = re.search("The" + s_numbered + " (.+?) just wandered away\.", text_buffer)
            if(M_obj):
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                if(my_list_search(self.Character.MONSTER_LIST, M_obj.group(2)) != -1):
                    self.Character.MONSTER_LIST.remove(M_obj.group(2))
                else:
                    magentaprint("MudReaderThread: Could not remove " + M_obj.group(2) + " from MONSTER_LIST")
            # Monster arrival
            M_obj = re.search("An? (.+?) just arrived\.", text_buffer)
            if(M_obj):
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                self.Character.MONSTER_LIST.append(M_obj.group(1))
            # TODO: handle "Two lay followers just arrived."
            # Monsters joining in
            # Two strings which can occur
            # This one is for when a mob that is present starts fighting
            # Note that the following is safe if two strings occur 
            # simultaneously!
            #  Aside:  Maybe more of the matches should work this way.
            #  However I'm hoping to move away from read_very_eager so 
            #  that task is pending.
            join_in_regex = "the" + s_numbered + " (.+?) joins in the fight!"
            M_obj = re.search(join_in_regex, text_buffer)
            new_trunc = 0
            temp_buf = text_buffer[:] # copy
            # Need to check for multiple matches here.
            while(M_obj):
                new_trunc = new_trunc + M_obj.end()
                text_buffer_trunc = max([text_buffer_trunc, new_trunc])
                self.Character.MOBS_JOINED_IN.append(M_obj.group(2))
                    # Note... this thread just appends... let the bot
                    # remove stuff.  I can't differentiate between 
                    # any mob and one that joined in!
                    # I will only remove from MONSTER_LIST
                temp_buf = temp_buf[new_trunc:]
                M_obj = re.search(join_in_regex, temp_buf)
                
            # This other string occurs when a mob wanders in and joins the fight    
            second_join_in_regex = "the" + s_numbered + " (.+?) decides to join in on the fight!"
            M_obj = re.search(second_join_in_regex, text_buffer)
            new_trunc = 0
            temp_buf = text_buffer[:] # copy
            while(M_obj):
                new_trunc = new_trunc + M_obj.end()
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                self.Character.MOBS_JOINED_IN.append(M_obj.group(2))
                temp_buf = temp_buf[new_trunc:]
                M_obj = re.search(second_join_in_regex, temp_buf)
                
            # Mobs Attacking you (not from joining in)
            
            mobs_attacking_regexes = [
                "The" + s_numbered + " (.+?) punches you for (.+?) damage\.",
                "The" + s_numbered + " (.+?) throws a wild punch at you, but it misses\.",
                "The" + s_numbered + " (.+?) kicks you for (.+?) damage\.",
                "The" + s_numbered + " (.+?) kicks at you, but fails to hurt you\.",
                "The" + s_numbered + " (.+?) grabs you and gouges you for (.+?) damage\.",
                "The" + s_numbered + " (.+?) tries to grab you, but you break free of (his|her|its) grasp\.",
                "The" + s_numbered + " (.+?) tries to gouge you, but you shake (him|her|it) off\.",
                "The" + s_numbered + " (.+?) lashes out and thumps you for (.+?) damage\.",
                "The" + s_numbered + " (.+?) lashes out at you, but misses\.",               
                "The" + s_numbered + " (.+?) painfully head-butts you for (.+?) damage\.",
                "The" + s_numbered + " (.+?) casts a (.+?) on you for (.+?) damage\.",
                "The" + s_numbered + " (.+?) casts a (.+?) at you for (.+?) damage\."] #not sure if its 'on' or 'at'
                # Thought:  We know a mob is attacking also on strings where I attack it, 
                # but it's doubtfully necessary to add that mob to MOBS_ATTACKING.
            for attacking_regex in mobs_attacking_regexes:
                # I think it would be difficult to determine here how many of a certain mob are 
                # attacking so just make sure that there's one instance of the attacking mob 
                # in ATTACKING_MOBS
                M_obj = re.search(attacking_regex, text_buffer)
                if(M_obj):
                    text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                    if(my_list_search(self.Character.MOBS_ATTACKING, M_obj.group(2)) == -1):
                        self.Character.MOBS_ATTACKING.append(M_obj.group(2))    
            

            '''"\n\r(.?+)\n\r\n\rObvious exits: (.+?)\.\n\r"  group(1) is the area name, group(2) is an exit list which will have to be parsed for commas
            "(?s)\n\r(.+?)\n\r\n\r(.+?)\n\rObvious exits: (.+?)\.\n\r(You see .+?\.)?" and group(2) is now the description.

            AreaMatched = False
            M_obj = re.search("(?s)\n\r(.+?)\n\r\n\r(.+?)\n\rObvious exits: (.+?)\n\r(You see .+?\.)", text_buffer)
            if(M_obj):
                self.Character.AREA_TITLE = str(M_obj.group(1)) #title
                #magentaprint("Exits " + str(M_obj.group(3)),False)
                self.Character.EXIT_LIST = self.parse_exit_list(M_obj.group(3)) #exits
                #magentaprint("Mobs " + str(M_obj.group(4)),False)
                self.Character.MONSTER_LIST = self.parse_monster_list(M_obj.group(4)) #mob list

                self.Character.SUCCESSFUL_GO = True
                self.CHECK_GO_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
                AreaMatched = True

            #Case where there are no monsters - there will always be exits and area titles unless it's dark
            M_obj = re.search("(?s)\n\r(.+?)\n\r\n\r(.+?)\n\rObvious exits: (.+?)\n\r", text_buffer)
            if(M_obj != None and not AreaMatched):
                self.Character.AREA_TITLE = str(M_obj.group(1)) #title
                self.Character.EXIT_LIST = self.parse_exit_list(M_obj.group(3)) #exits
                self.Character.MONSTER_LIST = []

                self.Character.SUCCESSFUL_GO = True
                self.CHECK_GO_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])'''

            #This should be moved to the cartographer
            M_obj = re.search("It's too dark to see\.", text_buffer)
            if(M_obj):
                self.Character.AREA_TITLE = ""
                self.Character.AREA_ID = ""
                self.Character.LAST_DIRECTION = ""
                self.Character.EXIT_LIST = []
                self.Character.MONSTER_LIST = []
                self.Character.SUCCESSFUL_GO = True
                self.CHECK_GO_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])

            M_obj = re.search("The" + s_numbered + " (.+?) blocks your exit\.", text_buffer)
            if(M_obj):
                #magentaprint("MudReader: unsuccessful go %f" % (time.time()-self.Character.START_TIME))
                self.Character.GO_BLOCKING_MOB = M_obj.group(2)  
                self.Character.SUCCESSFUL_GO = False
                self.CHECK_GO_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])

            M_obj = re.search("Please wait 1 more second\.", text_buffer)
            if(M_obj):
                magentaprint("MudReader: unsuccessful go (please wait)")
                self.Character.GO_PLEASE_WAIT = True
                self.Character.SUCCESSFUL_GO = False
                self.CHECK_GO_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])

            M_obj = re.search("You can't go that way\.", text_buffer)
            if(M_obj):
                # This one is pretty problematic... as it should never happen.
                # Means we're off course.
                #magentaprint("MudReader: unsuccessful go (you can't go that way)")
                self.Character.GO_NO_EXIT = True
                self.Character.SUCCESSFUL_GO = False
                self.CHECK_GO_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])

            M_obj = re.search("I don't see that exit\.", text_buffer)
            if(M_obj):
                #magentaprint("MudReader: unsuccessful go (you can't go that way)")
                self.Character.GO_NO_EXIT = True
                self.Character.SUCCESSFUL_GO = False
                self.CHECK_GO_FLAG = 0
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])

            M_obj = re.search("You glow with an? (.+?) aura\.", text_buffer)
            if(M_obj):
                self.Character.AURA = M_obj.group(1)
                self.Character.AURA_SCALE = my_list_search(self.Character.AURA_LIST, self.Character.AURA)
                if(self.Character.AURA_SCALE == -1):
                    magentaprint('Error in reading aura (not in list), came out as ' + self.Character.AURA + '.')
                self.CHECK_AURA_FLAG = 0
                self.CHECK_AURA_SUCCESS = 1
                text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
        
            # TODO: Having a red aura in the chapel will kill the bot.  
            #M_obj = re.search("The goodness here sickens and repels you!", text_buffer)
            #if(M_obj):
            #    text_buffer_trunc = max([text_buffer_trunc, M_obj.end()])
            ##    self.CommandHandler_inst.process("ou")
            
            # Internal check function MUD_output_check
            #if(self.__check_flag):
            #    M_obj = re.search(self.__check_regex_true, text_buffer)
            #    if(M_obj):
            #        self.__check_M_obj = M_obj
            #        self.__check_flag = False
            #    M_obj = re.search(self.__check_regex_false, text_buffer)
            #    if(M_obj):
            #        self.__check_M_obj = None
            #        self.__check_flag = False
            ##### DONE MATCHING RE's  WOOOOOOOO ######
        
            #sys.stdout.write('"' + MUDBuffer[MUD_buffer_trunc] + '"') #debug.  Shows where last match took place. Gives MUD_buffer not defined error.
            #magentaprint("Clearing text buffer.  len: %d.  trunc: %d.  last matched char: %c." % (
            #           len(text_buffer), text_buffer_trunc, text_buffer[text_buffer_trunc]))
            text_buffer = text_buffer[text_buffer_trunc:]
        
            #magentaprint("MudReader loop times: incl wait: %f; iteration time: %f" % 
            #             (time.time()-time_loop_start, time.time()-time_loop_after_waiting))
        # end loop          

    # end run  (congrats!)

    def copy_MUDBuffer(self):
        
        # Routine to copy the buffer shared with MudListenerThread.
        # Wait for access flag to go down for the read.
        while(self.MUDBuffer.access_flag == True):
            time.sleep(0.05)
            
        self.MUDBuffer.access_flag = True
        MUDBuffer_copy = self.MUDBuffer.buffer[:]
        self.MUDBuffer.access_flag = False
        return MUDBuffer_copy

    def set_colour(self,ANSI_escape_sequence):
        """ This routine takes an ANSI escape sequence as an argument and
        calls the ConsoleHandler class routines to have the windows console react."""
        bright_char = ANSI_escape_sequence[2]
        colour_char = ANSI_escape_sequence[3]
        if(bright_char == '3'):
            self.ConsoleHandler.set_dark()
        elif(bright_char == '4'):
            self.ConsoleHandler.set_bright()
        else:
            pass # do nothing
        # Maybe check if character 2 is a '3' or '4' which designate colour
        # commands but I'm too lazy.
        if(colour_char == '0'):
            self.ConsoleHandler.black()
        elif(colour_char == '1'):
            self.ConsoleHandler.red()
        elif(colour_char == '2'):
            self.ConsoleHandler.green()
        elif(colour_char == '3'):
            self.ConsoleHandler.yellow()
        elif(colour_char == '4'):
            self.ConsoleHandler.blue()
        elif(colour_char == '5'):
            self.ConsoleHandler.magenta()
        elif(colour_char == '6'):
            self.ConsoleHandler.cyan()
        elif(colour_char == '7' or colour_char == '9'):
            self.ConsoleHandler.white()
        else:
            # Do nothing (don't know this ANSI code)
            pass
    
    
