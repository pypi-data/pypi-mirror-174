from time import time

from scip_routing.pricing import Pricer


class VRPTWSolver:
    def __init__(self, graph, customers, start_depot, end_depot, demands, time_windows, capacity, pricer='dp',
                 verbose=False, first_found_pricing=False, price_and_branch=False):
        self.demands = demands
        self.start_depot = start_depot
        self.end_depot = end_depot
        self.customers = customers
        self.pricer = Pricer(graph, demands, time_windows, start_depot, end_depot, capacity,
                             first_found=first_found_pricing)
        self.verbose = verbose
        self.rmp = self.init_rmp()
        self.added_paths = set()
        self.obj = float("inf")
        self.price_and_branch = price_and_branch

    def init_rmp(self):
        rmp = xp.problem()
        obj = 0
        for customer in self.customers:
            var_name = f"{self.start_depot}-{customer}-{self.end_depot}"
            cost = self.pricer.graph[self.start_depot][customer]["cost"] + self.pricer.graph[customer][self.end_depot][
                "cost"]
            var = xp.var(lb=0, ub=xp.infinity, name=var_name, vartype=xp.continuous)
            rmp.addVariable(var)
            obj += cost * var
            rmp.addConstraint(var == 1)
        rmp.setObjective(obj, sense=xp.minimize)
        return rmp

    def solve(self):
        start_time = time()
        done = False
        i = 1
        while not done:
            self.rmp.solve()
            assert (self.rmp.getProbStatusString() == "lp_optimal")
            sol = self.rmp.getSolution()
            self.obj = self.rmp.getObjVal()
            duals = self.rmp.getDual()
            if self.pricer.__class__.__name__ == "MIPPricer":
                path, cost, redcost = self.pricer.find_path([0] + duals)
            else:
                path, cost, redcost = self.pricer.find_path([0] + duals, self.added_paths)
            if self.verbose:
                print(f"at iteration#{i}")
                print(f"obj={self.obj}")
                print(f"sol={sol}")
                # reducedcosts = self.rmp.getRCost()
                # print(f"redcosts={reducedcosts}")
                # print(f"duals={duals}")
                print(f"generated path {path} with cost {cost} and redcost {redcost}")
            i += 1
            if redcost <= 0 - 10e-13:
                self.added_paths.add(path)
                self.pricer.add_path_to_rmp(path, cost, self)
                self.rmp.write("prob", "lp")
                self.rmp.writebasis("basis", "lp")
                self.rmp = xp.problem()
                self.rmp.read("prob")
                self.rmp.readbasis("basis")
            else:
                done = True
                if self.verbose:
                    print("*** lp relaxation sol:")
                    for var in self.rmp.getVariable():
                        solution = self.rmp.getSolution(var)
                        if solution > 0:
                            print("*", var, solution)
        if self.price_and_branch:
            lp_obj = self.obj
            nvars = len(self.rmp.getVariable())
            self.rmp.chgcoltype(self.rmp.getVariable(), ["I"] * nvars)
            self.rmp.solve()
            if self.verbose:
                print("price-and-branch result:")
                self.obj = self.rmp.getObjVal()
                print("obj=", self.obj)
                print("gap=", (self.obj - lp_obj) / (self.obj) * 100)
                for var in self.rmp.getVariable():
                    solution = self.rmp.getSolution(var)
                    if 1 + 1e-15 >= solution >= 1e-15:
                        print(var, solution)
                print("Finished in", time() - start_time, "seconds")
