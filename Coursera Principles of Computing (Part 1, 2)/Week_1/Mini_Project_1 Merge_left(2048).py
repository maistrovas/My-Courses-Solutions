"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    zeros = []
    for _ in line:
        zeros.append(0)
    result_index = 0
    #in this step restlt = [0,0,0,0]
    result = zeros[:]
    for _ in range(len(line)):
        if line[_] != 0:
            result[result_index] = line[_]
            result_index +=1
    #in this step result = [2,2,2,0]
    for _ in range(1, len(result)):
        if result[_-1] ==result[_]:
            result[_-1] += result[_]
            result[_] = 0
    #in this step result = [4,0,2,0]
    final_result = zeros
    final_result_index = 0
    for _ in range(len(result[:])):
        if result[_] != 0:
            final_result[final_result_index] = result[_]
            final_result_index +=1
    return final_result


line = [8,16,16,8]
print merge(line)



