"""
Contains functionality for dealing with a linear programming model.
"""
from typing import Iterable
from collections import namedtuple

import pulp
from contexttimer import Timer

from pylp.constraint import Constraint
import warnings


if pulp.__version__ >= '2.1':
    import pulp.apis.cplex_api as cplex
    import pulp.apis.glpk_api as glpk
    import pulp.apis.choco_api as choco
    import pulp.apis.gurobi_api as gurobi
    import pulp.apis.coin_api as coin
else:
    import pulp.solvers as solvers
    warnings.warn('You are using pulp 2.0 or lower, pulp.apis.core has been changed to pulp.sovers automatically')

Status = namedtuple("Status", ["status", "time"])


def solve(
    *,
    objective=None,
    constraints: Iterable[Constraint] = None,
    minimize: bool = False,
    solver: str = "glpk",
    verbose: bool = False,
    options: list = None,
    solver_path: str = None,
    **kwargs,
) -> Status:
    """
    Solve the linear programming problem.

    Args:
        objective: The objective function
        constraints: The collection of constraints
        minimize: True for minimizing; False for maximizing
        solver: The solver to use. Current supports 'glpk', 'theo-cluster' and 'cplex'.
        verbose: If True, output the results of the solver
        options list: add options to the (glpk) solver
        **kwargs: is used to set the cluster path

    Returns:
        A tuple of the status (eg: Optimal, Unbounded, etc.) and the elapsed
        time

    solver: theo-cluster
        This is a specific version of the code to do cluster submission.
    """
    if minimize:
        sense = pulp.LpMinimize
    else:
        sense = pulp.LpMaximize

    problem = pulp.LpProblem(sense=sense)

    # Objective function is added first
    problem += objective.construct()

    if constraints:
        for constraint in constraints:
            problem += constraint.construct()

    if solver == "glpk":
        if solver_path!=None:
            solver = glpk.GLPK(msg=verbose, path=solver_path, options=options)
        else:
            print("solver_path is not set, going to default, without options")
            # This catches the error if glpk_path is not set
            solver = glpk.GLPK(msg=verbose)
    elif solver == "glpk-cluster":
        if solver_path!=None:
            solver = glpk.GLPK(msg=verbose, path=solver_path, options=options)
        else:
            print("solver_path is not set, going to default.")
            # This catches the error if glpk_path is not set
            solver = glpk.GLPK(msg=verbose, path="/home/theochri/ENV/bin/glpsol")
    elif solver == "cplex":
        solver = cplex.CPLEX(msg=verbose)
    elif solver == "gurobi":
        if solver_path!=None:
            solver = gurobi.GUROBI_CMD(msg=verbose,path=solver_path)
        else:
            solver = gurobi.GUROBI_CMD(msg=verbose)
    elif solver == "cbc":
        if solver_path!=None:
            solver = coin.PULP_CBC_CMD(msg=verbose,path=solver_path)
        else:
            solver = coin.PULP_CBC_CMD(msg=verbose)
    elif solver == "coin":
        if solver_path!=None:
            solver = coin.COIN_CMD(msg=verbose,path=solver_path)
        else:
            solver = coin.COIN_CMD(msg=verbose)
    elif solver == "choco":
        if solver_path!=None:
            solver = choco.PULP_CHOCO_CMD(msg=verbose,path=solver_path)
        else:
            solver = choco.PULP_CHOCO_CMD(msg=verbose)
    else:
        raise ValueError(f"Unsupported solver: {solver}")

    with Timer() as time:
        results = problem.solve(solver)

    status = pulp.LpStatus[results]

    return Status(status=status, time=time.elapsed)
