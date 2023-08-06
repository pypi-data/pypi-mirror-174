import json
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from .problem import Problem, Time
from .routing_model import RoutingModel


Node = int
Index = int
Trip = list[Node]
IndexTrip = list[Index]


class Solution:
    def __init__(self, problem: Problem, routingModel: RoutingModel):
        self.problem = problem
        self.routingModel = routingModel

    def solve(self, searchParameters = pywrapcp.DefaultRoutingSearchParameters()):
        self.solution = self.routingModel.orToolsModel.SolveWithParameters(searchParameters)
        return self


    def getObjective(self):
        return {
            'min': self.solution.ObjectiveMin(),
            'value': self.solution.ObjectiveMin(),
            'max': self.solution.ObjectiveMax(),
        }
    

    def getIndexTripForVehicle(self, vehicleId: int = 0, allIndexes: bool = False):
        orToolsModel = self.routingModel.orToolsModel
        index = orToolsModel.Start(vehicleId)
        indexTrip = []

        while not orToolsModel.IsEnd(index):
            indexTrip.append(index)
            index = self.solution.Value(orToolsModel.NextVar(index))
        
        indexTrip.append(index)

        if allIndexes:
            return indexTrip

        if not self.problem.endsAtDepot:
            del indexTrip[-1]

        if not self.problem.startsAtDepot:
            del indexTrip[0]

        return indexTrip


    def getIndexTrips(self, allIndexes: bool = False):
        def isEmptyTrip(indexes: list[int]):
            trip = [
                self.routingModel.indexManager.IndexToNode(index)
                for index in indexes
            ]

            if allIndexes:
                emptyTrip = [0, 0]
                return trip == emptyTrip

            emptyTrip = (
                [self.problem.depot] if self.problem.startsAtDepot else []
                + [self.problem.depot] if self.problem.endsAtDepot else []
            )

            return trip == emptyTrip
            
        indexTrips = [
            self.getIndexTripForVehicle(vehicleId, allIndexes)
            for vehicleId in range(self.problem.numVehicles)
        ]

        return {
            vehicleId: trip
            for vehicleId, trip in enumerate(indexTrips)
            if not isEmptyTrip(trip)
        }


    def getIndexTime(self, index: Index):
        return self.solution.Min(self.routingModel.timeDimension.CumulVar(index))


    def getTimes(self, indexTrips = None):
        if indexTrips is None:
            indexTrips = self.getIndexTrips()

        return {
            vehicleIndex: [
                self.getIndexTime(index)
                for index in trip
            ]
            for vehicleIndex, trip in indexTrips.items()
        }
    

    def getVehicleTotalTime(self, vehicleId = 0):
        allTimes = self.getTimes()

        if vehicleId not in allTimes:
            return 0

        times = allTimes[vehicleId]
        return times[-1] - times[0]


    def getTotalTime(self):
        return sum(self.getVehicleTotalTime(i) for i in range(self.problem.numVehicles))
    

    def getTrips(self) -> dict[int, Trip]:
        return {
            vehicleIndex: [
                self.routingModel.indexManager.IndexToNode(index)
                for index in trip
            ]
            for vehicleIndex, trip in self.getIndexTrips().items()
        }


    def getSortedTrips(self) -> list[Trip]:
        return sorted(list(self.getTrips().values()))


    def getObjectiveValue(self):
        return self.solution.ObjectiveValue()


    def getTotalLateness(self):
        def getLateness(index):
            time = self.getIndexTime(index)
            upperBound = self.routingModel.timeDimension.GetCumulVarSoftUpperBound(index)
            return max(0, time - upperBound)

        indexTrips = self.getIndexTrips(allIndexes=True)

        return sum(
            getLateness(i)
            for k, trip in indexTrips.items()
            for i in trip
        )