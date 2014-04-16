
from misc_functions import magentaprint 
import time

class BotReaction(object):
    """ This type of object has a list of regexes and defines notify.  
    It gets registered with the MudReader and the notify 
    gets executed when the Mud sends text matching any regex. """

    unregistered = False # MudReaderHandler uses this variable as part of the unregister procedure

    def __init__(self, regexes):

        if isinstance(regexes, str):
            regexes = [regexes]

        self.regexes = regexes

    def notify(self, regex, M_obj):
        """ This function is called by MudReaderThread when regex was 
        matched.  MudReaderThread gives the regex back so that the Reaction 
        can know which was matched, and M_obj is given so that the matching 
        text can be used.  
        """
        raise NotImplementedError()


class BotReactionWithFlag(BotReaction):
    """ wait_for_flag() is useful when you send a telnet command and 
    want to wait for the server's response to that command. """

    __waiter_flag = True
    good_MUD_timeout = 1.2 

    def notify(self, regex, M_obj):
        """ Subclasses should implement notify and also ensure that __waiter_flag
        gets set."""
        self.__waiter_flag = True

    def wait_for_flag(self):
        self.__waiter_flag = False
        start_time = time.time()
        run_time = 0

        while not self.__waiter_flag and run_time < self.good_MUD_timeout:
            time.sleep(0.05)
            run_time = time.time() - start_time

        if not self.__waiter_flag:
            return False  # Timed out
        else:
            self.__waiter_flag = False
            return True


class GenericBotReaction(BotReaction):
    """ BotReaction which takes telnet_commands as an additional argument, 
    and uses it to define notify.  This type of BotReaction can't make 
    use of M_obj."""
    
    def __init__(self, regexes, commandHandler, telnet_commands):
        super(GenericBotReaction, self).__init__(regexes)

        if isinstance(telnet_commands, str):
            self.telnet_commands = [telnet_commands]
        else:
            self.telnet_commands = telnet_commands

        self.commandHandler = commandHandler
        
    def notify(self, regex, M_obj):
        for cmd in self.telnet_commands:
            self.commandHandler.process(cmd) 
            
# add init with character and commandHandler
# make a reaction type for kill thread

class WieldReaction(BotReaction):
    """ notify will execute wield commands."""
    
    def __init__(self, character, commandHandler):
        # Note: regex should specify the weapon string in a group.
        super(WieldReaction, self).__init__([
            "Your (.*?) breaks and you have to remove it\.",
            "Your (.*?) shatters\."]
            )
        self.character = character
        self.commandHandler = commandHandler

    def notify(self, regex, M_obj):
        magentaprint("Reequiping weapon..." + M_obj.group(1))
        self.reequip_weapon(M_obj.group(1))
        
    def reequip_weapon(self, weapon):        
        if(self.character.WEAPON1 == self.character.WEAPON2):
            self.commandHandler.process("wie " + weapon)
            self.commandHandler.process("seco " + weapon)
        else:
            if(weapon == self.character.WEAPON1):
                self.commandHandler.process("wie " + weapon)
            else:
                self.commandHandler.process("seco " + weapon)
