import networkx as nx


class Label:
    def __init__(self, last_node, cost, demand, earliest_time, last_label):
        self.last_node = last_node
        self.cost = cost
        self.demand = demand
        self.earliest_time = earliest_time
        self.last_label = last_label


class Pricer:
    """
    Solver for the Resource Constrained Shortest Path Problem, implements a basic Labeling Algorithm.
    """

    def __init__(self, graph, demands, time_windows, start_depot, end_depot, capacity, distance_fn=None,
                 first_found=False):
        self.graph = graph
        self.start_depot = start_depot
        self.end_depot = end_depot
        self.time_windows = time_windows
        self.demands = demands
        self.capacity = capacity
        self.ncustomers = len(demands) - 1
        if distance_fn:
            self.distance_fn = distance_fn
        else:
            self.distance_fn = lambda i, j: self.graph[i][j]['cost']
        self.time_fn = lambda i, j: self.graph[i][j]['time']
        self.first_found = first_found

    def path_from_label(self, label: Label):
        curr = label
        path = []
        cost = 0
        while curr is not None:
            path.insert(0, curr.last_node)
            if curr.last_label:
                cost += self.distance_fn(curr.last_label.last_node, curr.last_node)
            curr = curr.last_label
        return tuple(path), cost

    def add_path_to_rmp(self, path, cost, solver):
        customer_counts = {}
        for i in path:
            if i in customer_counts:
                customer_counts[i] += 1
            else:
                customer_counts[i] = 1

        row_ids = []
        row_coeffs = []
        for customer in solver.customers:
            if customer in path:
                row_ids.append(customer - 1)
                row_coeffs.append(customer_counts[customer])

        solver.rmp.addcols(objcoef=[cost],
                           start=[0, len(solver.customers)],
                           rowind=row_ids,
                           rowcoef=row_coeffs,
                           lb=[0],
                           ub=[xp.infinity],
                           names=["-".join(map(str, path))],
                           types=['C'])

    def find_path(self, duals, added_paths):
        unprocessed = {}
        processed = {}

        for i in range(self.ncustomers + 1):  # customers + end depot
            unprocessed[i] = set()
            processed[i] = set()

        unprocessed[self.start_depot] = {Label(self.start_depot, 0, 0, 0, None)}
        unprocessed_count = 1

        while unprocessed_count > 0:
            label_to_expand = self.choose_label_to_expand(unprocessed)
            unprocessed_count -= 1
            # print('***', unprocessed_count)
            next_node_to_expand = label_to_expand.last_node
            for neighbor in nx.neighbors(self.graph, next_node_to_expand):

                demand, last_visited, redcost, earliest_time = self.expand_label(duals, label_to_expand, neighbor,
                                                                                 next_node_to_expand)

                new_label = Label(last_visited, redcost, demand, earliest_time, label_to_expand)

                if self.is_feasible(demand, earliest_time, neighbor):
                    dominated = self.dominance_check({new_label}, processed[neighbor] | unprocessed[neighbor])
                    if len(dominated) == 0:
                        if self.first_found and neighbor == self.end_depot and new_label.cost < -200:
                            best_path, best_path_travel_cost = self.path_from_label(new_label)
                            if best_path not in added_paths:
                                return best_path, best_path_travel_cost, new_label.cost
                        dominated = self.dominance_check(unprocessed[neighbor], {new_label})
                        unprocessed[neighbor] = (unprocessed[neighbor] - dominated) | {new_label}
                        unprocessed_count += 1 - len(dominated)
            processed[next_node_to_expand].add(label_to_expand)

        best_path_label = None
        best_path_redcost = float("inf")
        if processed[self.end_depot]:
            for label in processed[self.end_depot]:
                if label.cost <= best_path_redcost:
                    best_path_label = label
                    best_path_redcost = label.cost
        best_path, best_path_travel_cost = self.path_from_label(best_path_label)
        return best_path, best_path_travel_cost, best_path_redcost

    def is_feasible(self, demand, earliest_time, neighbor):
        return demand <= self.capacity and earliest_time <= self.time_windows[neighbor][1]

    def expand_label(self, duals, label_to_expand, neighbor, next_node_to_expand):
        distance = self.distance_fn(next_node_to_expand, neighbor)
        redcost = label_to_expand.cost + (distance - duals[next_node_to_expand])
        last_visited = neighbor
        demand = label_to_expand.demand + self.demands[neighbor]
        earliest_time = max(label_to_expand.earliest_time + self.time_fn(next_node_to_expand, neighbor),
                            self.time_windows[neighbor][0])
        return demand, last_visited, redcost, earliest_time

    def dominance_check(self, A, B):
        """
        Dominance check between two sets of labels

        :param A: set of labels
        :param B: set os labels
        :return: set of labels in A that are dominated by at least one label from B
        """
        dominated = set()
        for label_a in A:
            for label_b in B:
                if self.dominates(label_b, label_a):
                    dominated.add(label_a)
                    break
        return dominated

    @staticmethod
    def choose_label_to_expand(unprocessed):
        # todo: choose one with min time
        # returns first label it sees
        for customer, labels in unprocessed.items():
            if len(labels):
                return labels.pop()
        return None

    def dominates(self, label_a, label_b):
        is_less_or_eq = label_a.cost <= label_b.cost and label_a.demand <= label_b.demand and \
                        label_a.earliest_time <= label_b.earliest_time
        one_is_strictly_less = label_a.cost < label_b.cost or label_a.demand < label_b.demand or \
                               label_a.earliest_time < label_b.earliest_time
        return is_less_or_eq and one_is_strictly_less
