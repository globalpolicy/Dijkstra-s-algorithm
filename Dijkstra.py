import csv


class Dijkstra:
    startingNode = 0
    __adjacencyMatrix = []
    __visitedNodes = []
    solvedListOfNodeTuples = []  # [[optimal parent node, optimal total distance to node],...] NOTE: these 'tuples' are just 2-member lists

    def __init__(self, adjacencyMatrixCSVFilePath, originNode):
        self.startingNode = originNode
        with open(adjacencyMatrixCSVFilePath, "r") as file:
            csv_reader = csv.reader(file)
            for row_index, row in enumerate(csv_reader):
                correctedRow = []
                for column_index, column_element in enumerate(row):
                    if column_element != '':
                        correctedRow.append(float(column_element))
                self.__adjacencyMatrix.append(correctedRow)
                self.solvedListOfNodeTuples.append([0, 1000])

    # returns list of tuples : (index of neighboring node,distance to that node)
    # assumes path of travel as row to column
    def __getConnectedNodes(self, parentNode):
        connectedNodes = []
        parentNodeRow = self.__adjacencyMatrix[parentNode]
        for index, distance in enumerate(parentNodeRow):
            if index not in self.__visitedNodes and distance != 0 and distance != 1000:
                connectedNodes.append((index, distance))
        return connectedNodes

    # updates the solvedListOfNodeTuples list
    def __updateSolvedList(self, startFromNodes):  # startFromNodes is a list of nodes to start processing from
        if len(startFromNodes) == 0: return
        neighborsOfInputNodes = []  # input for next iteration of this function
        for node in startFromNodes:
            nodeNeighbors = self.__getConnectedNodes(node)
            for neighborNode, edgeDistance in nodeNeighbors:
                neighborsOfInputNodes.append(
                    neighborNode)  # append to the list of new nodes to be processed after this iteration
                if self.solvedListOfNodeTuples[neighborNode][1] > self.solvedListOfNodeTuples[node][1] + edgeDistance:
                    self.solvedListOfNodeTuples[neighborNode][1] = self.solvedListOfNodeTuples[node][1] + edgeDistance
                    self.solvedListOfNodeTuples[neighborNode][0] = node
        self.__visitedNodes.extend(startFromNodes)  # add the parent nodes to the visited nodes list
        neighborsOfInputNodes = list(dict.fromkeys(neighborsOfInputNodes))  # pruning duplicate nodes
        self.__updateSolvedList(neighborsOfInputNodes)

    def solve(self):
        startNodeNeighbors = self.__getConnectedNodes(self.startingNode)  # get neighboring nodes to the start point node
        for neighborNode, edgeDistance in startNodeNeighbors:
            self.solvedListOfNodeTuples[neighborNode][0] = self.startingNode
            self.solvedListOfNodeTuples[neighborNode][1] = edgeDistance
        self.__visitedNodes.append(self.startingNode)  # add the starting node to the visited nodes list
        self.__updateSolvedList([node[0] for node in startNodeNeighbors])

    # gets optimal route as a list to the target node from solvedListOfNodeTuples, which is a self-referential list of optimal paths
    # Huge thanks to https://stackoverflow.com/questions/13437063/python-recursive-function-result-depends-on-previous-calls-when-parameter-has-de for saving my sanity
    def getOptimalPath(self, targetNode, backTracedPath=None):
        if (targetNode == self.startingNode):
            return [targetNode]
        if backTracedPath is None:
            backTracedPath = []
            backTracedPath.append(targetNode)
        lastOptimalOriginNode = self.solvedListOfNodeTuples[targetNode][0]
        backTracedPath.append(lastOptimalOriginNode)
        if lastOptimalOriginNode != self.startingNode:
            self.getOptimalPath(lastOptimalOriginNode, backTracedPath)
            return backTracedPath
        else:
            backTracedPath.reverse()
            return backTracedPath

    # gets optimal distance to the target node
    def getOptimalDistance(self,targetNode):
        if(targetNode==self.startingNode):
            return 0
        return self.solvedListOfNodeTuples[targetNode][1]