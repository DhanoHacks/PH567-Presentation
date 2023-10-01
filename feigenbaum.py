# Calculate the feigenbaum constant for a given map
from utils import *

def get_bifurcation_points(x0,t,arr_size,A_min,A_max,thresh,num_points_required,chosen_map):
    bifurcation_points = []
    asymptotic_trajectories = []
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
        asymptotic_trajectories.append(asymptotic_trajectory)
        # print(f"Found bifurcation point {A[0]}")
    return bifurcation_points,asymptotic_trajectories

if __name__ == "__main__":
    t = 100000
    arr_size = 1024
    mode = 0 # 0: logistic map, 1: sine map, 2: quadratic map
    (x0,chosen_map,left,right,name) = [(0.1,logistic_map,2.99,3.57,"Logistic Map"),(0.1,sine_map,2.26,2.72,"Sine Map"),(0,quadratic_map,0.74,1.4015, "Quadratic Map")][mode]
    thresh = 1e-8
    num_points_required = 6

    bifurcation_points,asymptotic_trajectories = get_bifurcation_points(x0,t,arr_size,left,right,thresh,num_points_required,chosen_map)

    # calculate feigenbaum constant
    differences = np.diff(bifurcation_points)
    print(f"Bifurcation points: {bifurcation_points}")
    print(f"Feigenbaum deltas: {differences[:-1]/differences[1:]}")

    tine_widths = []
    for i in range(1,num_points_required):
        asymptotic_trajectories[i] = asymptotic_trajectories[i][0][:2**i]
        asymptotic_trajectories[i].sort()
        curr_tine_widths = []
        for j in range(int(2**(i-1))):
            curr_tine_widths.append(asymptotic_trajectories[i][2*j+1]-asymptotic_trajectories[i][2*j])
        tine_widths.append(curr_tine_widths)
    
    alphas = []
    for i in range(num_points_required-2):
        curr_alphas = np.repeat(tine_widths[i],2)/tine_widths[i+1]
        for j in range(2**i):
            if curr_alphas[2*j]<curr_alphas[2*j+1]:
                curr_alphas[2*j+1] = np.sqrt(curr_alphas[2*j+1])
            else:
                curr_alphas[2*j] = np.sqrt(curr_alphas[2*j])
        alphas.append(curr_alphas)
    print(f"Feigenbaum Alphas: {alphas}")

    # plot boxplot of feigenbaum alphas
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.boxplot(alphas)
    ax.set_xlabel("Bifurcation #")
    ax.set_ylabel("Calculated Alpha")
    ax.set_title(f"Feigenbaum Alphas for {name}")
    ax.axhline(y=2.5029,color="k",linestyle="--",label="True Feigenbaum Constant")
    ax.legend()
    plt.savefig(f"slides/plots/{name.split(' ')[0].lower()}_feigenbaum_alphas.png")
