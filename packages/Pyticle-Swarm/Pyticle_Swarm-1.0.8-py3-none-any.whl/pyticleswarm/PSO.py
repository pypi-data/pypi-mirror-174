# -*- coding: utf-8 -*-
import random
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib
import warnings


#Algorithm Functions
def generate_int_pop_rand(n_particles,n_vars,low_bounds,up_bounds):
    """
    Generate initial population function.
    Here, random values between the lower and the higer bounds are defined for the initial population:
    
    x1^j = rand[xlb^j, xub^j]

    Parameters:
        n_particles: int
            Number of particles
        n_vars: int
            Number of variables
        low_bounds: matrix
            Matrix containing the lowest boundaries the solution array might have for each particle
        up_bounds: matrix
            Matrix containing the highest boundaries the solution array might have for each particle
    
    Returns: matrix
        Matrix containing the initial population values for each particle
    """

    particle_position_vector=np.array([[np.random.uniform(low_bounds[j,i],up_bounds[j,i]) for i in range(n_vars)] for j in range(n_particles)], dtype=float)
    return particle_position_vector


def generate_int_pop_mean(n_particles,n_vars,low_bounds,up_bounds):
    """
    Generate initial population function.
    Here, the mean value between the low and the up bounds are defined for the initial solution:
    
    x1^j = (xlb^j+xub^j)/2

    Parameters:
        n_particles: int
            Number of particles
        n_vars: int
            Number of variables
        low_bounds: matrix
            Matrix containing the lowest boundaries the solution array might have for each particle
        up_bounds: matrix
            Matrix containing the highest boundaries the solution array might have for each particle
    
    Returns: matrix
        Matrix containing the initial population values for each particle
    """
    particle_position_vector=np.array([[(low_bounds[j,i]+up_bounds[j,i])/2 for i in range(n_vars)] for j in range(n_particles)], dtype=float)
    return particle_position_vector


def inertia_update(iteration,n_iterations,wmin,wmax):
    """
    Time varying acceleration inertia:
    
    w^k = wmax - (wmax - wmin)/kmax * k

    Parameters:
        iteration: int
            The number of the iteration
        n_iterations: int
            The number of total iterations
        wmin: float
            The minimum value of the itertia weight
        wmax: float
            The maximum value of the inertia weight

    Returns: float
        The new intertia weight value
    """

    W=wmax-((wmax-wmin)/n_iterations)*iteration
    return W


def coef_updation(c1min,c1max,c2min,c2max,iteration,n_iterations):
    """
    Coeficients update function

    Parameters:
        c1min: float
            Minimum value of the acceleration coefficient c1
        c1max: float
            Maximum value of the acceleration coefficient c1
        c2min: float
            Minimum value of the acceleration coefficient c2
        c2max: float
            Maximum value of the acceleration coefficient c1
        iteration: int
            The number of the iteration
        n_iterations: int
            The number of total iterations    

    Returns: float, float
        The new acceleration coefficients c1 and c2
    """
    
    c1=c1max-((c1max-c1min)/n_iterations)*iteration # decreasing
    c2=c2min+((c2max-c2min)/n_iterations)*iteration # increasing
    return c1, c2


def velocity_limits_update(low_bounds,up_bounds,n_vars,n_particles,iteration,n_iterations):
    """
    Velocity limits update function

    Parameters:
        low_bounds: matrix
            Matrix containing the lowest boundaries the solution array might have for each particle
        up_bounds: matrix
            Matrix containing the highest boundaries the solution array might have for each particle
        n_particles: int
            The total number of particles
        iteration: int
            The number of the iteration
        n_iterations: int
            The total number of iterations

    Returns: float, float
        The maximum and minimum velocity
    """

    f=0.5-((0.5-0.01)/n_iterations)*iteration
    VelMax=np.array([[f*(up_bounds[j,i]-low_bounds[j,i]) for i in range(n_vars)] for j in range(n_particles)])
    VelMin=-VelMax
    return VelMax,VelMin


def BRM_control_bounce_back(new_position,low_bounds,up_bounds,_):
    """
    Bondary control function (Bounce back)
    Relocates the parameter in between the bound it exceeded and the corresponding parameter from the base vector [1].
    
    [1] K. Price, R. Storn, and J. Lampinen, Differential Evolution—A Practical Approach to Global Optimization. Berlin, Germany: Springer, 2005.
    
    Parameters:
        new_position: array
            The solution array
        low_bounds: array
            Array containing the lowest boundaries the solution array might have for one particle
        up_bounds: array
            Array containing the highest boundaries the solution array might have for one particle

    Returns: array
        The new solution array after checking if solution values are within the boundaries
    """

    # Bounce Back update
    position=np.minimum(new_position, up_bounds)
    position=np.maximum(position, low_bounds)    
    return position, 0


def BRM_control_random_reinitialization(new_position,low_bounds,up_bounds,_):
    """
    Bondary control function (Random Reinicialization).
    Replaces a parameter that exceeds its bounds by a randomly chosen value from within the allowed range following [2], [1].
    
    [1] K. Price, R. Storn, and J. Lampinen, Differential Evolution—A Practical Approach to Global Optimization. Berlin, Germany: Springer, 2005.
    
    [2] J. Lampinen and I. Zelinka, “Mixed integer-discrete-continuous optimization with differential evolution,” in Proc. 5th Int. Mendel Conf. Soft Comput., Jun. 1999, pp. 71–76.

    Parameters:
        new_position: array
            The solution array
        low_bounds: array
            Array containing the lowest boundaries the solution array might have for one particle
        up_bounds: array
            Array containing the highest boundaries the solution array might have for one particle

    Returns: array
        The new solution array after checking if solution values are within the boundaries
    """

    # Random reinicialization
    position = new_position.copy()
    for i in range(len(new_position)):
        if new_position[i]>up_bounds[i] or new_position[i]<low_bounds[i]:
            position[i] = np.random.uniform(low_bounds[i],up_bounds[i])
    return position, 0


def BRM_control_brick_wall_penalty(new_position,low_bounds,up_bounds,custom_penalty):
    """
    Bondary control function (Brick wall penalty).
    If any parameter of a vector falls beyond the pre-defined lower or upper bounds, objective function value of the vector is made high enough (by afixed big number) to guarantee that it never gets selected [1].
    
    [1] K. Price, R. Storn, and J. Lampinen, Differential Evolution—A Practical Approach to Global Optimization. Berlin, Germany: Springer, 2005.

    Parameters:
        new_position: array
            The solution array
        low_bounds: array
            Array containing the lowest boundaries the solution array might have for one particle
        up_bounds: array
            Array containing the highest boundaries the solution array might have for one particle
        custom_penalty: float
            Penalty value to be applied

    Returns: array
        The new solution array after checking if solution values are within the boundaries
    """

    # Brick wall penalty
    for i in range(len(new_position)):
        if new_position[i]>up_bounds[i] or new_position[i]<low_bounds[i]:
            return new_position, custom_penalty
    return new_position, 0


def BRM_control_adaptive_penalty(new_position,low_bounds,up_bounds, custom_penalty):
    """
    Bondary control function (Brick wall penalty)
    Similar to brick wall penalty, but here the increase in the objective function value of the offender vector may depend on the number of parameters violating bound constraints and their magnitudes of violation [3], [4].
    
    [3] R. Storn, “Differential evolution design of an IIR-filter with requirements for magnitude and group delay,” in Proc. IEEE Int. Conf. Evol. Comput., 1996, pp. 268–273.
    
    [4] R. Storn, “On the usage of differential evolution for function optimization,” in Proc. North Am. Fuzzy Inform. Process. Soc., 1996, pp.
    
    Parameters:
        new_position: array
            The solution array
        low_bounds: array
            Array containing the lowest boundaries the solution array might have for one particle
        up_bounds: array
            Array containing the highest boundaries the solution array might have for one particle
        custom_penalty:
            Penalty offset to be used within the adaptive penalty formula

    Returns: array
        The new solution array after checking if solution values are within the boundaries
    """

    # Adaptive penalty
    penalty = 0
    quantity = 0
    for i in range(len(new_position)):
        if new_position[i]>up_bounds[i]:
            penalty+= (new_position[i]-up_bounds[i])
            quantity+=1
        elif new_position[i]<low_bounds[i]:
            penalty+= (low_bounds[i] - new_position[i])
            quantity+=1
    return new_position, (penalty*quantity*custom_penalty)


def PSO_alg(wmax,wmin,c1min,c1max,c2min,c2max,initial_solution,initial_population_gen,brm_function,custom_penalty,perc_repair,
                       n_iterations,n_particles,n_vars,
                       up_bounds,low_bounds,fitness_function,direct_repair, show_graphics):
    """
    The PSO algorithm

    Parameters:
        wmin: float
            The minimum value of the itertia weight
        wmax: float
            The maximum value of the inertia weight
        c1min: float
            Minimum value of the acceleration coefficient c1
        c1max: float
            Maximum value of the acceleration coefficient c1
        c2min: float
            Minimum value of the acceleration coefficient c2
        c2max: float
            Maximum value of the acceleration coefficient c1
        initial_solution: matrix or array
            Matrix or array containing the initial solutions or solution
        initial_population_gen: int
            Defines the type of the initial population. One of: generate_int_pop_rand (1), generate_int_pop_mean (2)
        brm_function: function
            Function to handle boundary constraint violation. One of: BRM_control_brick_wall_penalty (1), BRM_control_adaptive_penalty (2), BRM_control_random_reinitialization (3), BRM_control_bounce_back (4), or a custom one created by the user. 
        perc_repair: float
            Value between 0 and 1 that determines the percentage of iterations starting from the end where a repair function is applied
        n_iterations: int
            The total number of iterations
        n_particles: int
            The total number of particles
        n_vars: int
            The number of variables present in the solution
        low_bounds: matrix
            Matrix containing the lowest boundaries the solution array might have for each particle
        up_bounds: matrix
            Matrix containing the highest boundaries the solution array might have for each particle
        fitness_function: function
            The fitness function
        direct_repair: function
            The direct repair function
        show_graphics: bol
            Boolean that indicates if the particles graphics are to be shown or not (Only works with solutions of 2 dimensions)
    
    Returns: float, matrix, array
        The best fitness value, all fitness values and the solution array
    """
    np.random.seed(10)
    # Create Variables
    particle_position_vector=np.array([[float('inf') for _ in range(n_vars)] for _ in range(n_particles)])
    pbest_position=np.array([[float('inf') for _ in range(n_vars)] for _ in range(n_particles)])
    fitness_cadidate=np.array([float('inf') for _ in range(n_particles)])
    pbest_fitness_value=np.array([float('inf') for _ in range(n_particles)])
    gbest_fitness_value=float('inf')
    gbest_position=np.array([[float('inf') for _ in range(1)] for _ in range(n_vars)])
    gbest_it_fitness_value=np.array([float('inf') for _ in range(n_iterations+1)])
    vat_it=np.array([float('inf') for _ in range(n_iterations+1)])
    velocity_vector =np.zeros([n_particles,n_vars])
    brm_function = BRM_control_bounce_back if brm_function==4 else BRM_control_random_reinitialization if brm_function==3 else BRM_control_brick_wall_penalty if brm_function==1 else BRM_control_adaptive_penalty if brm_function==2 else brm_function

    #Initialize Variables
    if len(initial_solution) == n_particles:
        particle_position_vector = initial_solution
    elif len(initial_solution) == 1:
        generate_int_pop = generate_int_pop_rand if initial_population_gen==1 else generate_int_pop_mean
        particle_position_vector = np.concatenate((generate_int_pop(n_particles-1,n_vars,low_bounds,up_bounds),initial_solution))
    else:
        generate_int_pop = generate_int_pop_rand if initial_population_gen==1 else generate_int_pop_mean
        particle_position_vector = generate_int_pop(n_particles,n_vars,low_bounds,up_bounds)
    for i in range(n_particles):
        #Apply Position Limits Boundary Control
        particle_position_vector[i], penalty=brm_function(particle_position_vector[i],low_bounds[i],up_bounds[i],custom_penalty)
        if direct_repair != None:
            if perc_repair==1:
                # Direct Repair 
                new_position=direct_repair(particle_position_vector[i])
                particle_position_vector[i]=new_position
                if brm_function==1 or brm_function ==2:
                        particle_position_vector[i],penalty = brm_function(particle_position_vector[i],low_bounds[i],up_bounds[i],custom_penalty)
        fitness_cadidate[i] = fitness_function(particle_position_vector[i]) + penalty

    pbest_position = particle_position_vector.copy()
    pbest_fitness_value = fitness_cadidate.copy()
    gbest_fitness_value = min(fitness_cadidate)
    gbest_it_fitness_value[0]=gbest_fitness_value
    id_best=np.argmin(fitness_cadidate)
    gbest_position = particle_position_vector[id_best]
    vat_it[0]=np.var(particle_position_vector)

    iteration = 1

    while iteration <= n_iterations:
        #Inertia update
        W = inertia_update(iteration,n_iterations,wmin,wmax)
        #Update coeficients
        c1,c2 = coef_updation(c1min,c1max,c2min,c2max,iteration,n_iterations)
        #Velocity Limits
        VelMax,VelMin = velocity_limits_update(low_bounds,up_bounds,n_vars,n_particles,iteration,n_iterations)
        #Update position
        for i in range(n_particles):
            # new volocity calculation
            new_velocity = (W*velocity_vector[i]) + (c1*np.random.uniform()) * (pbest_position[i] - particle_position_vector[i]) + (c2*np.random.uniform()) * (gbest_position-particle_position_vector[i])
            # Apply velocity limits
            new_velocity=np.minimum(new_velocity, VelMax[i])
            new_velocity=np.maximum(new_velocity, VelMin[i])
            # new position
            new_position = new_velocity + particle_position_vector[i]
            velocity_vector[i] = new_velocity
            # Velocity Mirror Effect
            #IsOutside_low=(new_position<low_bounds[i])
            #IsOutside_up=(new_position>up_bounds[i])
            #IsOutside=np.array(IsOutside_low|IsOutside_up)
            #velocity=np.array([new_velocity[j]*-1*IsOutside[j]+new_velocity[j]*(1-IsOutside[j]) for j in range(n_vars)])
            #new_velocity=velocity
            #Apply Position Limits Boundary Control
            position,penalty = brm_function(new_position,low_bounds[i],up_bounds[i],custom_penalty)
            # update position
            particle_position_vector[i] = position
            if direct_repair != None:
                if iteration>perc_repair*n_iterations:
                    # Direct Repair 
                    new_position=direct_repair(particle_position_vector[i])
                    particle_position_vector[i]=new_position
                    if brm_function == 1 or brm_function ==2:
                        particle_position_vector[i],penalty = brm_function(particle_position_vector[i],low_bounds[i],up_bounds[i],custom_penalty)
            # calculate new fitness
            fitness_cadidate[i] = fitness_function(particle_position_vector[i]) + penalty
            if(pbest_fitness_value[i] > fitness_cadidate[i]):
                pbest_fitness_value[i] = fitness_cadidate[i]
                pbest_position[i] = particle_position_vector[i]
        gbest_fitness_value = min(pbest_fitness_value)
        gbest_it_fitness_value[iteration]=gbest_fitness_value
        vat_it[iteration]=np.var(particle_position_vector)
        id_best=np.argmin(pbest_fitness_value)
        gbest_position = pbest_position[id_best]
        iteration += 1
        if show_graphics:
            if len(gbest_position) == 2:
                plt.clf()
                plt.xlim([low_bounds[0][0],up_bounds[0][0]])
                plt.ylim([low_bounds[0][1],up_bounds[0][1]])
                x = np.linspace(low_bounds[0][0],up_bounds[0][0])
                y = np.linspace(low_bounds[0][1],up_bounds[0][1])
                X,Y = np.meshgrid(x, y)
                Z = []
                for e in np.array((X,Y)).T:
                    Z2 = []
                    for e2 in e:
                        Z2.append(fitness_function(e2))
                    Z.append(Z2)
                c=plt.contour(X,Y,Z)
                norm= matplotlib.colors.Normalize(vmin=c.cvalues.min(), vmax=c.cvalues.max())
                sm = plt.cm.ScalarMappable(norm=norm, cmap = c.cmap)
                sm.set_array([])
                plt.colorbar(sm, ticks=c.levels)
                plt.scatter([e[0] for e in pbest_position],[e[1] for e in pbest_position],c="black", marker=(5,2))
                plt.pause(0.01)
            else:
                warnings.warn("Not possible to show the graphics when solution array does not have 2 dimensions.")
    gbest_it_fitness_value=np.delete(gbest_it_fitness_value, -2)
    return gbest_fitness_value, gbest_it_fitness_value, gbest_position