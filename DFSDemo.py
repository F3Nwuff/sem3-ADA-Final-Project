from pyamaze import maze,agent,textLabel,COLOR
import sys
import memory_profiler

printed1 = False
def DFS(m,start=None):
    if start is None:
        start=(m.rows,m.cols)
    explored=[start]
    frontier=[start]
    dfsPath={}
    dSeacrh=[]
    while len(frontier)>0:
        currCell=frontier.pop()
        dSeacrh.append(currCell)
        if currCell==m._goal:
            break
        poss=0
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d =='E':
                    child=(currCell[0],currCell[1]+1)
                if d =='W':
                    child=(currCell[0],currCell[1]-1)
                if d =='N':
                    child=(currCell[0]-1,currCell[1])
                if d =='S':
                    child=(currCell[0]+1,currCell[1])
                if child in explored:
                    continue
                poss+=1
                explored.append(child)
                frontier.append(child)
                dfsPath[child]=currCell
        if poss>1:
            m.markCells.append(currCell)
    fwdPath={}
    cell=m._goal

    total_space2 = 0
    total_space2 += sys.getsizeof(m)
    total_space2 += sys.getsizeof(start)
    total_space2 += sys.getsizeof(frontier)
    total_space2 += sys.getsizeof(dfsPath)
    total_space2 += sys.getsizeof(explored)
    total_space2 += sys.getsizeof(dSeacrh)
    total_space2 += sys.getsizeof(fwdPath)
    total_space2 += sys.getsizeof(cell)

    global printed1
    if not printed1:
        print(f"The total space usage of the program DFS is {total_space2} bytes.")
        printed1 = True

    while cell!=start:
        fwdPath[dfsPath[cell]]=cell
        cell=dfsPath[cell]
    return dSeacrh,dfsPath,fwdPath

if __name__=='__main__':
    m=maze(10,10)
    m.CreateMaze(2,4)
    # m.CreateMaze(loadMaze='maze--17--20-31.csv')

    dSeacrh,dfsPath,fwdPath=DFS(m,(5,1))

    a=agent(m,5,1,goal=(2,4),footprints=True,shape='square',color=COLOR.green)
    b=agent(m,2,4,goal=(5,1),footprints=True,filled=True)
    c=agent(m,5,1,footprints=True,color=COLOR.yellow)
    total_space3 = 0
    total_space3 += sys.getsizeof(a)
    total_space3 += sys.getsizeof(b)
    total_space3 += sys.getsizeof(c)
    print(f"The total space usage of the DFS pathings is {total_space3} bytes.")
    m.tracePath({a:dSeacrh},showMarked=True)
    m.tracePath({b:dfsPath})
    m.tracePath({c:fwdPath})
    m.run()

