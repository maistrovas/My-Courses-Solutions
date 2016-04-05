import math

def f(x):
    return 400*math.e**(math.log(0.5)/3.66 * x)

#My implementation
def radiationExposure(start, stop, step):
    '''
    Computes and returns the amount of radiation exposed
    to between the start and stop times. Calls the 
    function f (defined for you in the grading script)
    to obtain the value of the function at any point.
 
    start: integer, the time at which exposure begins
    stop: integer, the time at which exposure ends
    step: float, the width of each rectangle. You can assume that
      the step size will always partition the space evenly.

    returns: float, the amount of radiation exposed to 
      between start and stop times.
    '''
    area_X = stop - start
    exposure = 0
    beans = float(area_X)/step
    begin = start
    for i in range(int(beans)):
        rect = f(begin)*step
        exposure += rect
        begin += step
    return exposure

#Approximation algorithm   
def radiationExposure2(start,stop,step):
    a=0
    area=0
    while start+a < stop:
        area+=f(start+a)*step
        a+=step
    return area


print radiationExposure2(0, 4, 0.25)

