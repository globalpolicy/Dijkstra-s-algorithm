from Dijkstra import Dijkstra

dijkstra=Dijkstra("nodes.csv",1)
dijkstra.solve()
print(dijkstra.getOptimalPath(14))
print(dijkstra.getOptimalDistance(14))
