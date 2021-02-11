
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

def getAllowedMoves(rushhour, carData):
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
                        tmpAllowedMoves.append(["L", i - 1])
                elif found and lastEntry == car and rushhour[loc][i] == empty_space:
                    # last position was car and right is empty, so right move allowed
                    tmpAllowedMoves.append(["R", i])
                    proceed_next_car = True
                lastEntry = rushhour[loc][i]
            else:
                if not found and rushhour[i][loc] == car:
                    found = True
                    if lastEntry == empty_space:
                        # last position was empty and current is car, so up move allowed
                        tmpAllowedMoves.append(["U", i - 1])
                elif found and lastEntry == car and rushhour[i][loc] == empty_space:
                    # last position was car and down is empty, so down move allowed
                    tmpAllowedMoves.append(["D", i])
                    proceed_next_car = True
                lastEntry = rushhour[i][loc]
            if proceed_next_car:
                break
        if found:
            allowedMoves[car] = {"moves": tmpAllowedMoves, "dir": dir, "loc": loc}
    return allowedMoves

def getCandidates(rushhour):
    return allowed

def findNextEmptyCell(rushhour, rowId, colId):
    row = rowId
    col = colId
    for i in range(row,9):
        for j in range(col,9):
            if rushhour[i,j] == 0:
                return i, j
        col = 0
    return None, None

def isSolved(rushhour):
    return rushhour.flatten().sum() == 405

def solve(rushhour, lastMoves = [], tabuSize = 1, carData=None, curSol = [], bestMove = []):
    retval = dict()
    # determine cars available
    if carData == None:
        carData = getCarData(rushhour)
    # now determine allowed moves
    allowedMoves = getAllowedMoves(rushhour, carData)
    print("maus")
    # loop through all allowed moves
    for car in allowedMoves.keys():
        moves = allowedMoves.get(car)["moves"]
        for move in moves:
            newRushhour = applyMove(rushhour, move, allowedMoves)
            curSol.append(car + move)
            # if solved
            if isSolved(newRushhour):
                # store solution
                retval['task'] = newRushhour
                retval['moves'] = curSol
                return retval
            elif len(bestMove) != 0 and len(curSol) > len(bestMove):
                solve(newRushhour)
        # perform move
        # apppend move to curSol

        # if solved
            # store solution
        # if curSol >= leength bestMove
            # return bestMove
        # else
            # solve()
        # end if







    # first determine next empty cell starting from rowId / colId, if current cell is not empty (!=0)



    if rushhour[rowId, colId] != 0:
        # field already set, find next empty cell
        rowId, colId = findNextEmptyCell(rushhour, rowId, colId)
        if rowId == None or colId == None:
            return rushhour
    # determine potential candidates for given cell
    cands = getCandidates(rushhour, rowId, colId)
    # loop through all candidates and
    for cand in cands:
        rushhour[rowId, colId] = cand
        rushhour = solve(rushhour, rowId, colId)
        if isSolved(rushhour):
            return rushhour
    rushhour[rowId, colId] = 0
    return rushhour

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