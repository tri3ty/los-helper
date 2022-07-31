
from threading import Thread
from itertools import chain

from command.Command import Command
from misc_functions import magentaprint

class ThreadingMixin2:
    # This needs Command or CommandThatRemovesFromInventory also mixed in
    # (Needs .execute)

    # "prayc" or "hastec" or "berserkc"
    # Since abilities can fail, it's nice to have an object that knows the cooldown
    # You can use this to queue up the command to go when it's ready
    # And this is done with a thread.
    # ThreadingMixin2 actually doesn't bother inheriting Thread though,
    # the Thread is made inline with the constructor.

    # This one doesn't use class variables like the first ThreadingMixin.
    # For this one, I don't like that.
    # I also don't like copying code but - I can only do thing at a time.
    # Children need to set self.end_thread_regex_cart

    # kk, use, haste... could maybe all use the same code with different cooldowns
    # Use needs CommandThatRemovesFromInventory but also has a cooldown

    def notify(self, regex, M_obj):
        super().notify(regex, M_obj)
        # if regex in self.success_regexes or regex in self.error_regexes:
        if regex in chain.from_iterable(self.end_thread_regexes):
            self.stop()

    # def __init__(self, telnetHandler):
    def __init__(self):
        # super().__init__(telnetHandler)
        self.thread = None

    def start_thread(self, target=None):
        self.spam(target)

    def spam(self, target=None):
        self.stopping = False

        if self.thread is None or not self.thread.is_alive():
            # not is_alive() means it won't look at stopping anymore so we're good.
            self.thread = Thread(target=self.run, args=(target,))
            self.thread.daemon = True
            self.thread.start()
        else:
            # Well the other thread CAN stil be sleeping from a kill error.  (ie misspelled target)
            # That puts it into a 3 second sleep, then the timer gets corrected 0.3s after.
            # So.... maybe it must poll fast... or we need signals... do we use that thread or a new thread??
            # Maybe we write its code smarter to handle this case... don't sleep till after the cooldown's verified
            magentaprint("Command will be sent in " + str(round(self.wait_time())) + " seconds.")

    # run
        # kk, cc, SmartCombat need a version that stops when combat over.
        # Abilities need a version that stops on command success or error.
    def run(self, target=None):
        while not self.stopping:
            magentaprint("Sending '" + str(self.command) + "' in " + str(round(self.wait_time())) + " seconds.")
            self.wait_until_ready()
            if self.stopping:
                magentaprint(str(self) + " ability ready.")
            else:
                self.execute(target) # This part needs command
                self.wait_for_flag()

    def stop(self):
        self.stopping = True

    def keep_going(self):
        magentaprint(str(self) + ": keep_going() (stopped:  " + str(self.stopping) + ")")
        self.stopping = False
