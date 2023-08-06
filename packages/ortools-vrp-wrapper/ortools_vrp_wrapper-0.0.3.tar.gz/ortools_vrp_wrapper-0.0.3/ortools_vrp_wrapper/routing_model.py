from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from .problem import Cost, Problem, Time, TimeTable, TimeWindow, TimeWindows, Weight
from sys import maxsize


class RoutingModel:
    def __init__(
        self,
        problem: Problem
    ):
        tripTimeTable = problem.properTripTimeTable()

        self.indexManager = pywrapcp.RoutingIndexManager(
            len(tripTimeTable),
            problem.numVehicles,
            problem.depot,
        )

        self.orToolsModel = pywrapcp.RoutingModel(self.indexManager)

        self.timeCallback = self.__registerTimeCallback(tripTimeTable)
        self.timeDimension = self.__createTimeDimension(problem.vehicleMaxTime)

        self.__setArcCosts()
        self.__setTimeObjective(problem.numVehicles)

        latenessPenalty = self.__getLatenessPenalty(problem)

        self.__setTimeWindows(problem.timeWindows, latenessPenalty, problem.depot, problem.numVehicles)
        self.__setStartTime(problem.startTime, problem.depot, problem.timeWindows, problem.numVehicles)

        if problem.softVehicleMaxTime is not None:
            self.__setSoftMaxTime(problem.softVehicleMaxTime, latenessPenalty, problem.numVehicles)

        self.__setVehicleFixedCost(problem.vehicleFixedCost)

        if problem.demands is not None and problem.vehicleCapacities is not None:
            self.demandCallback = self.__registerDemandCallback(problem.demands)
            self.__addCapacityDimension(problem.vehicleCapacities)


    def __setVehicleFixedCost(self, cost):
        self.orToolsModel.SetFixedCostOfAllVehicles(cost)


    def __registerTimeCallback(self, tripTimeTable: TimeTable):
        def time_callback(from_index, to_index):
            from_node = self.indexManager.IndexToNode(from_index)
            to_node = self.indexManager.IndexToNode(to_index)
            return tripTimeTable[from_node][to_node]
        

        return self.orToolsModel.RegisterTransitCallback(time_callback)


    def __setArcCosts(self):
        self.orToolsModel.SetArcCostEvaluatorOfAllVehicles(self.timeCallback)


    def __createTimeDimension(self, vehicleMaxTime: Time):
        time = 'Time'
        self.orToolsModel.AddDimension(
            self.timeCallback,
            0,
            vehicleMaxTime,
            False,
            time)

        return self.orToolsModel.GetDimensionOrDie(time)


    def __setTimeWindows(self, timeWindows: TimeWindows, latenessPenalty: Cost, depot: int, numVehicles: int):
        for node, timeWindow in timeWindows.items():
            indexes = (
                self.__startIndexes(numVehicles)
                if node == depot
                else [self.indexManager.NodeToIndex(node)]
            )

            self.__setCumulLowerBound(self.timeDimension, indexes, timeWindow.start)
            self.__setCumulSoftUpperBound(self.timeDimension, indexes, timeWindow.end, latenessPenalty)


    # This number will be used as a penalty for not arriving on time.
    # It needs to be high enough to never be worthy,
    # but if we use max int size the router wont be able to
    # choose the better one all possible unfeasible routes.
    def __getLatenessPenalty(self, problem: Problem):
        return problem.averageTripTimeEstimate(numEffectiveVehicles=1)


    def __setStartTime(self, startTime: Time, depot: int, timeWindows: TimeWindows, numVehicles: int):
        indexes = self.__startIndexes(numVehicles)
        self.__setCumulLowerBound(self.timeDimension, indexes, startTime)


    def __setSoftMaxTime(self, maxTime: Time, latenessPenalty: Cost, numVehicles: int):
        indexes = self.__endIndexes(numVehicles)
        self.__setCumulSoftUpperBound(self.timeDimension, indexes, maxTime, latenessPenalty)


    def __setCumulLowerBound(self, dimension, indexes, value):
        for index in indexes:
            var = dimension.CumulVar(index)

            if var.OldMin() >= value:
                return

            var.SetMin(value)


    def __setCumulSoftUpperBound(self, dimension, indexes, value, latenessPenalty):
        for index in indexes:
            if (
                dimension.HasCumulVarSoftUpperBound(index)
                and dimension.GetCumulVarSoftUpperBound(index) <= value
            ):
                return

            dimension.SetCumulVarSoftUpperBound(index, value, latenessPenalty)


    def __setTimeObjective(self, numVehicles: int):
        for i in range(numVehicles):
            self.orToolsModel.AddVariableMinimizedByFinalizer(
                self.timeDimension.CumulVar(self.orToolsModel.End(i))
            )

            self.orToolsModel.AddVariableMaximizedByFinalizer(
                self.timeDimension.CumulVar(self.orToolsModel.Start(i))
            )


    def __registerDemandCallback(self, demands: list[Weight]):
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = self.indexManager.IndexToNode(from_index)
            return demands[from_node]


        return self.orToolsModel.RegisterUnaryTransitCallback(demand_callback)


    def __addCapacityDimension(self, vehicleCapacities: list[Weight]):
        self.orToolsModel.AddDimensionWithVehicleCapacity(
            self.demandCallback,
            0,  # null capacity slack
            vehicleCapacities,
            True,  # start cumul to zero
            'Capacity',
        )


    def __startIndexes(self, numVehicles: int):
        return [self.orToolsModel.Start(i) for i in range(numVehicles)]


    def __endIndexes(self, numVehicles: int):
        return [self.orToolsModel.End(i) for i in range(numVehicles)]