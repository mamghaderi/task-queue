"""Simple travelling salesman problem between cities."""
import json
import math

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def calculate_distance_matrix(data):
    """:param data: list of paired [lat, lon]s: [[lat1, lon1], [lat2, lon2], ...]"""
    """:returns: distance_matrix: [[], [], ]"""

    distance_matrix = [[] for _ in range(len(data))]
    for i in range(len(data)):
        selected_point = data[i]
        for j in range(i, len(data)):
            dist = math.dist(selected_point, data[j])
            distance_matrix[i].append(dist)
            if i != j:
                distance_matrix[j].append(dist)

    return distance_matrix


def create_data_model(raw_data):
    """Stores the data for the problem."""
    """:param row_data: list of paired [lat, lon]s: [[lat1, lon1], [lat2, lon2], ...]"""

    data = {}
    data['distance_matrix'] = calculate_distance_matrix(json.loads(raw_data))
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)
    return plan_output


def process_sales_man(raw_data):
    # Instantiate the data problem.
    data = create_data_model(raw_data)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(manager, routing, solution)

