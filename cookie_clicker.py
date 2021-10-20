"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history_list = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        state = ""
        state += '\nTime = ' + str(self._current_time)
        state += '\nCurrent_Cookies = ' + str(self._current_cookies)
        state += '\nCPS = ' + str(self._current_cps)
        state += '\nTotal_Cookies = ' + str(self._total_cookies)
        return state
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history_list)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies < cookies:
            return math.ceil((cookies - self._current_cookies) / self._current_cps)
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            temp = self._current_cps * time
            self._current_cookies += temp
            self._total_cookies += temp
            self._current_time += time
        else:
            return 
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_cookies:
            self._current_cookies += -cost
            self._current_cps += additional_cps
            self._history_list.append((self._current_time, item_name, cost, self._total_cookies))
        else:
            return

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    info = build_info.clone()
    clicker = ClickerState()
    
    while clicker.get_time() <= duration:
        time_left = duration - clicker.get_time()
        item = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), time_left, info)
        if item == None:
            break
        time_until = clicker.time_until(info.get_cost(item))
        if time_until > time_left:
            break
        clicker.wait(time_until)
        clicker.buy_item(item, info.get_cost(item), info.get_cps(item))
        info.update_item(item)
    
    clicker.wait(time_left)
    
    return clicker

def history_test(history, item):
    """
    This helper function checks if an item has been previously in the history
    """
    for record in history:
        if record[1] == item:
            return True
    return False

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    info = build_info # info of upgrades
    items = info.build_items()
    potential = cookies + cps * time_left # available resources to buy upgrades
    temp = []
    flag = False
    for item in items: # filter those upgrades that are feasible
        if info.get_cost(item) <= potential:
            temp.append(item)
    if len(temp) > 0:
        flag = True
        cheap_item = temp[0] # initialze item arbitrarily
        for item in temp:
            if info.get_cost(item) < info.get_cost(cheap_item): # criteria of selection
                cheap_item = item
    if flag:
        return cheap_item
    else:
        return None
    
def strategy_cheap_once(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford, from the "once cheapest" list
    """
    info = build_info # info of upgrades
    items = info.build_items()
    potential = cookies + cps * time_left # available resources to buy upgrades
    temp = []
    flag = False
    for item in items: # filter those upgrades that are feasible
        if info.get_cost(item) <= potential and not history_test(history, item):
            temp.append(item)
    if len(temp) > 0:
        flag = True
        cheap_item = temp[0] # initialze item arbitrarily
        for item in temp:
            if info.get_cost(item) < info.get_cost(cheap_item): # criteria of selection
                cheap_item = item
    if flag:
        return cheap_item
    else:
        return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    info = build_info # info of upgrades
    items = info.build_items()
    potential = cookies + cps * time_left # available resources to buy upgrades
    temp = []
    flag = False
    for item in items: # filter those upgrades that are feasible
        if info.get_cost(item) <= potential:
            temp.append(item)
    if len(temp) > 0: # if feasible
        flag = True
        expensive_item = temp[0] # initialize item arbitrarily
        for item in temp:
            if info.get_cost(item) > info.get_cost(expensive_item): # criteria of selection
                expensive_item = item
    if flag:
        return expensive_item
    else:
        return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    info = build_info # info of upgrades
    items = info.build_items()
    potential = cookies + cps * time_left # available resources to buy upgrades
    temp = []
    flag = False
    for item in items: # filter those upgrades that are feasible
        if info.get_cost(item) <= potential:
            temp.append(item)
    if len(temp) > 0: # if feasible
            flag = True
            best_item = temp[0] # initialize item arbitrarily
            ratio_best = float(info.get_cps(best_item)) / info.get_cost(best_item)
            for item in temp:
                ratio_item = float(info.get_cps(item)) / info.get_cost(item)
                if ratio_best < ratio_item:
                    best_item = item
    if flag:
        return best_item
    else:
        return None
    
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    run_strategy("None", SIM_TIME, strategy_none)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
#run()

   

