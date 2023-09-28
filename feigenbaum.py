# Calculate the feigenbaum constant for a given map
from utils import *

def get_bifurcation_points(x0,t,arr_size,A_min,A_max,thresh,num_points_required,chosen_map):
    bifurcation_points = []
    for i in range(num_points_required):
        left = A_min
        right = A_max
        target_periods = (2**i,2**(i+1))
        # A = np.array([left, (left+right)/2, right])
        A = np.array([(left+right)/2])
        while right-left>thresh:
            asymptotic_trajectory = evolution(x0, A, t, arr_size,chosen_map)
            points,periods = calculate_periods(asymptotic_trajectory,A)
            # assert periods[0] <= target_periods[0] and periods[2] >= target_periods[1]
            # print(periods[0],target_periods)
            assert periods[0] <= target_periods[0] or periods[0] >= target_periods[1]
            if periods[0] <= target_periods[0]:
                left = (left+right)/2
            elif periods[0] >= target_periods[1]:
                right = (left+right)/2
            # A = np.array([left, (left+right)/2, right])
            A = np.array([(left+right)/2])
        bifurcation_points.append(A[0])
        # print(f"Found bifurcation point {A[0]}")
    return bifurcation_points

if __name__ == "__main__":
    t = 100000
    arr_size = 1024
    mode = 1 # 0: logistic map, 1: sine map, 2: quadratic map
    (x0,chosen_map,left,right) = [(0.1,logistic_map,2.99,3.57),(0.1,sine_map,2.26,2.72),(0,quadratic_map,0.74,1.4015)][mode]
    thresh = 1e-8
    num_points_required = 6

    bifurcation_points = get_bifurcation_points(x0,t,arr_size,left,right,thresh,num_points_required,chosen_map)

    # calculate feigenbaum constant
    differences = np.diff(bifurcation_points)
    print(f"Bifurcation points: {bifurcation_points}")
    print(f"Feigenbaum constants: {differences[:-1]/differences[1:]}")
