"""
Cookie Clicker Simulator
"""

#import simpleplot
# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)
import poc_clicker_provided as provided
import math
# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 500
class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_coocies = 0.0
        self._current_coocies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Total coocies = %s \n Current coocies = %s \n Time  = %s \n CPS = %s" %(self._total_coocies, self._current_coocies, self._current_time, self._current_cps)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_coocies
    
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
        
        return self._history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies > 0 and cookies >= self._current_coocies:
            return math.ceil((cookies-self._current_coocies)/self._current_cps)
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._current_coocies += time * self._current_cps
            self._total_coocies += time * self._current_cps
            self._current_time += time
        else:
            pass
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_coocies:
            self._current_coocies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time,
                item_name, cost, self._total_coocies))
        else:
            pass
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_clone = build_info.clone()
    clicker = ClickerState()
    while clicker.get_time() <= duration :
        time_left = duration - clicker.get_time()
        next_byilding = strategy(clicker.get_cookies(), clicker.get_cps(),
            clicker.get_history(), time_left, build_clone)
        if next_byilding == None:
            break
        building_cps = build_clone.get_cps(next_byilding)
        building_cost = build_clone.get_cost(next_byilding)
        time_needed = clicker.time_until(building_cost)
        if time_needed > time_left:
            break
        else:
            next_byilding = strategy(clicker.get_cookies(), clicker.get_cps(),
            clicker.get_history(), time_left, build_clone)
            clicker.wait(time_needed)
            clicker.buy_item(next_byilding, building_cost, building_cps)
            build_clone.update_item(next_byilding)
    clicker.wait(time_left)
    return clicker

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
    variants = []
    for item in build_info.build_items():
        if cookies + cps * time_left >= build_info.get_cost(item):
            variants.append([item, build_info.get_cost(item)])
    if len(variants) == 0:
        return None
    minn = variants[0][1]
    for elem in variants:
        if elem[1] < minn:
            result = elem[0] 
        else:
            result = variants[0][0]
    return result

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    variants = []
    for item in build_info.build_items():
        if cookies + cps * time_left >= build_info.get_cost(item):
            variants.append([item, build_info.get_cost(item)])
    if len(variants) == 0:
        return None
    maxx = variants[0][1]
    for elem in variants:
        if elem[1] > maxx:
            result = elem[0] 
        else:
            result = variants[0][0]
    return result

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    item_lst = build_info.build_items()
    cost_lst = map(build_info.get_cost, item_lst)
    cps_lst = map(build_info.get_cps, item_lst)
    eff_lst = []
    for dummy_i in range(len(item_lst)):
        efficiency = cps_lst[dummy_i] / cost_lst[dummy_i]
        eff_lst.append(efficiency)
    most_eff_idx = eff_lst.index(max(eff_lst))
    most_eff_item = item_lst[most_eff_idx] 
    return most_eff_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    #Ready 
    #state = simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 5000.0, strategy_none)
    #state = simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 500.0, strategy_cursor_broken)
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    # Plot total cookies over time
    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it
    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

run()



