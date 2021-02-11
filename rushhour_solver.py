
def applyMove(rushhour, car, move):
    dim = len(rushhour)
    empty_space = '-'
    mv = move[0]
    loc = move[1]
    idx = move[2]
    if mv == 'U':
        for i in range(dim-1, -1, -1):
            if rushhour[i][loc] == car:
                rushhour[i][loc] = empty_space
                rushhour[idx][loc] = car
                break
    elif mv == 'D':
        for i in range(0, dim, 1):
            if rushhour[i][loc] == car:
                rushhour[i][loc] = empty_space
                rushhour[idx][loc] = car
                break
    elif mv == 'L':
        for i in range(dim-1, -1, -1):
            if rushhour[loc][i] == car:
                rushhour[loc][i] = empty_space
                rushhour[loc][idx] = car
                break
    elif mv == 'R':
        for i in range(0, dim, 1):
            if rushhour[loc][i] == car:
                rushhour[loc][i] = empty_space
                rushhour[loc][idx] = car
                break
    return rushhour

def getCarData(rushhour):
    carData = {}
    mv_horizontal, mv_vertical = 1, 2
    empty_space = "-"
    cars = set()
    dim = len(rushhour)
    assert dim > 0
    # determine sorted set of cars w/o empty space
    for row in rushhour:
        cars.update(set(row))
    cars.remove(empty_space)
    cars = sorted(cars)
    # build dict with allowed moves
    for car in cars:
        found = False
        found_x = None
        found_y = None
        proceed_next_car = False
        for i in range(0, dim):
            for j in range(0, dim):
                if not found and rushhour[i][j] == car:
                    # found car-character for first time
                    found = True
                    found_x, found_y = i,j
                elif found and rushhour[i][j] == car:
                    # found character 2nd time (>1-block sized car)
                    # determine orientation of car (horiz/vert)
                    if found_x == i:
                        carData[car] = {"dir": mv_horizontal, "loc": i}
                    elif found_y == j:
                         carData[car] = {"dir": mv_vertical, "loc": j}
                    proceed_next_car = True
                if proceed_next_car:
                    break
            if proceed_next_car:
                break
    return carData

def getAllowedMoves(rushhour, carData, curSol):
    allowedMoves = {}
    mv_horizontal, mv_vertical = 1, 2
    empty_space = "-"
    dim = len(rushhour)
    for car in carData.keys():
        dir = carData[car]["dir"]
        loc = carData[car]["loc"]
        found = False
        proceed_next_car = False
        lastEntry = ""
        tmpAllowedMoves = []
        for i in range(0, dim):
            if dir == mv_horizontal:
                if not found and rushhour[loc][i] == car:
                    found = True
                    if lastEntry == empty_space:
                        # last position was empty and current is car, so left move allowed
                        # prune counter moves
                        if len(curSol) == 0 or len(curSol)>0 and (curSol[-1][0] != car or curSol[-1][1] != 'R'):
                           tmpAllowedMoves.append(["L", loc, i - 1])
                elif found and lastEntry == car and rushhour[loc][i] == empty_space:
                    # last position was car and right is empty, so right move allowed
                    # prune counter moves
                    if len(curSol) == 0 or len(curSol)>0 and (curSol[-1][0] != car or curSol[-1][1] != 'L'):
                        tmpAllowedMoves.append(["R", loc, i])
                    proceed_next_car = True
                lastEntry = rushhour[loc][i]
            else:
                if not found and rushhour[i][loc] == car:
                    found = True
                    if lastEntry == empty_space:
                        # last position was empty and current is car, so up move allowed
                        # prune counter moves
                        if len(curSol) == 0 or len(curSol)>0 and (curSol[-1][0] != car or curSol[-1][1] != 'D'):
                            tmpAllowedMoves.append(["U", loc, loc, i - 1])
                elif found and lastEntry == car and rushhour[i][loc] == empty_space:
                    # last position was car and down is empty, so down move allowed
                    # prune counter moves
                    if len(curSol) == 0 or len(curSol) > 0 and (curSol[-1][0] != car or curSol[-1][1] != 'U'):
                        tmpAllowedMoves.append(["D", loc, i])
                    proceed_next_car = True
                lastEntry = rushhour[i][loc]
            if proceed_next_car:
                break
        if found:
            allowedMoves[car] = {"moves": tmpAllowedMoves, "dir": dir, "loc": loc}
    return allowedMoves

def isSolved(rushhour):
    dim = len(rushhour)
    redcar = 'X'
    empty_space = '-'
    found = False
    blocked = False
    for i in range(0, dim):
        if rushhour[2][i] == redcar:
            found = True
        elif found and rushhour[2][i] != empty_space:
                blocked = True
                break
    return not blocked

def solve(rushhour, lastMoves = [], tabuSize = 1, carData=None, curSol = [], bestMove = []):
    retval = dict()
    max_size = 20
    # determine cars available
    if carData == None:
        carData = getCarData(rushhour)
    print(curSol)
    # now determine allowed moves
    allowedMoves = getAllowedMoves(rushhour, carData, curSol)
    # loop through all allowed moves
    for car in allowedMoves.keys():
        moves = allowedMoves.get(car)["moves"]
        for move in moves:
            # perform move
            newRushhour = applyMove(rushhour, car, move)
            curSol.append(car + move[0])
            # apppend move to curSol
            # if solved
            if isSolved(newRushhour):
                # store solution
                retval['task'] = newRushhour
                retval['moves'] = curSol
                if len(curSol) < max_size and (len(bestMove) == 0 or len(bestMove) < len(curSol)):
                    bestMove = curSol
                return retval
            elif len(curSol) < max_size and (len(bestMove) == 0 or len(curSol) < len(bestMove)):
                # if not solved and current move-list not longer than best solution found
                # try solve
                retval = solve(newRushhour, carData = carData, curSol = curSol, bestMove = bestMove)
                newRushhour = retval['task']
                if isSolved(newRushhour):
                    if len(bestMove) == 0 or len(bestMove) < len(curSol):
                        bestMove = curSol
                    return retval
                else:
                    curSol.pop()
    return retval

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # task #4
    rushhour = [["O","-","-","P","-","-"],
                ["O","-","-","P","-","-"],
                ["O","X","X","P","-","-"],
                ["-","-","A","Q","Q","Q"],
                ["-","-","A","-","-","B"],
                ["-","-","R","R","R","B"]]
    result = solve(rushhour)
    print(result)
