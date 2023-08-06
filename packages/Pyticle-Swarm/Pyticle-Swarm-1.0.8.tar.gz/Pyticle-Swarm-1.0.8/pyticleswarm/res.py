class Res:
    """
    Class to represent the result of the PSO algorithm

    Attributes:
        fitness_value: float
            The best fitness value after running the PSO algorithm
        it_fitness_value: matrix
            All the fitness values of each execution after running the PSO algorithm
        solution: array of floats
            The solution of the best execution corresponding to the best fitness value
        tot_exec_time: float
            Total execution time of the PSO algorithm
        avg_exec_time: float
            Average execution time of the PSO algorithm
    """

    def __init__(self,fitness_value,it_fitness_value,solution,tot_exec_time,avg_exec_time):
        """
        Parameters:
            fitness_value: float
                The best fitness value after running the PSO algorithm
            it_fitness_value: matrix
                All the fitness values of each execution after running the PSO algorithm
            solution: array of floats
                The solution of the best execution corresponding to the best fitness value
            tot_exec_time: float
                Total execution time of the PSO algorithm
            avg_exec_time: float
                Average execution time of the PSO algorithm
        """

        self.fitness_value = fitness_value
        self.it_fitness_value = it_fitness_value
        self.solution = solution
        self.tot_exec_time = tot_exec_time
        self.avg_exec_time = avg_exec_time
