# Calculate the feigenbaum constant for a given map
from utils import *
import re
plt.rcParams.update({'font.size': 16})

def get_bifurcation_points(x0,t,arr_size,A_min,A_max,thresh,num_points_required,chosen_map):
    bifurcation_points = []
    asymptotic_trajectories = []
    for i in range(num_points_required):
        left = A_min
        right = A_max
        target_periods = (2**i,2**(i+1))
        A = np.array([(left+right)/2])
        while right-left>thresh:
            asymptotic_trajectory = evolution(x0, A, t, arr_size,chosen_map)
            points,periods = calculate_periods(asymptotic_trajectory,A)
            # print(periods[0],target_periods)
            assert periods[0] <= target_periods[0] or periods[0] >= target_periods[1]
            if periods[0] <= target_periods[0]:
                left = (left+right)/2
            elif periods[0] >= target_periods[1]:
                right = (left+right)/2
            A = np.array([(left+right)/2])
        bifurcation_points.append(A[0])
        asymptotic_trajectories.append(asymptotic_trajectory)
        # print(f"Found bifurcation point {A[0]}")
    return bifurcation_points,asymptotic_trajectories

def plot_feigenbaum_constants(map_names, all_deltas, delta_true_values, all_alphas, alpha_true_values):
    fig,ax = plt.subplots(figsize = (9,6))
    for i in range(len(map_names)):
        ax.plot(np.arange(1,len(all_deltas[i])+1),all_deltas[i],"-",markersize=10,label=f"{map_names[i]}")
        ax.set_xticks(np.arange(1,len(all_deltas[i])+1))
    ax.axhline(y=delta_true_values[0],color="k",linestyle="-",label="True $\delta$ for Logistic, Sine, Quadratic")
    ax.axhline(y=delta_true_values[3],color="k",linestyle="--",label="True $\delta$ for Biquadratic")
    ax.set_xlabel("n")
    ax.set_ylabel("$\delta_n$")
    ax.set_title(f"Feigenbaum $\delta$ for all maps")
    ax.legend()
    plt.savefig(f"slides/plots/feigenbaum_deltas.png")
    plt.close()

    fig,ax = plt.subplots(figsize = (9,6))
    for i in range(len(map_names)):
        ax.plot(np.arange(1,len(all_alphas[i])+1),all_alphas[i],"-",markersize=10,label=f"{map_names[i]}")
        ax.set_xticks(np.arange(1,len(all_alphas[i])+1))
    ax.axhline(y=alpha_true_values[0],color="k",linestyle="-",label="True $\\alpha$ for Logistic, Sine, Quadratic")
    ax.axhline(y=alpha_true_values[3],color="k",linestyle="--",label="True $\\alpha$ for Biquadratic")
    ax.set_xlabel("n")
    ax.set_ylabel("$\\alpha_n$")
    ax.set_title(f"Feigenbaum $\\alpha$ for all maps")
    ax.legend()
    plt.savefig(f"slides/plots/feigenbaum_alphas.png")
    plt.close()

if __name__ == "__main__":
    # t = 200000
    # arr_size = 1024
    # mode = 3 # 0: logistic map, 1: sine map, 2: quadratic map, 3: biquadratic map
    # (x0,chosen_map,left,right,name) = [(0.1,logistic_map,2.99,3.58,"Logistic Map"),(0.1,sine_map,2.26,2.72,"Sine Map"),(0,quadratic_map,0.74,1.4015, "Quadratic Map"),(0,biquadratic_map,0.4,1.596, "Biquadratic Map")][mode]
    # thresh = 1e-10
    # num_points_required = 6

    # bifurcation_points,asymptotic_trajectories = get_bifurcation_points(x0,t,arr_size,left,right,thresh,num_points_required,chosen_map)
    # print(f"Bifurcation points: {bifurcation_points}")

    # # calculate feigenbaum delta
    # differences = np.diff(bifurcation_points)
    # feigenbaum_deltas = differences[:-1]/differences[1:]
    # print(f"Feigenbaum deltas: {feigenbaum_deltas}")

    # # calculate feigenbaum alpha
    # highest_cycle_elements = []
    # for i in range(1,num_points_required):
    #     asymptotic_trajectories[i] = asymptotic_trajectories[i][0][:2**i]
    #     asymptotic_trajectories[i].sort()
    #     highest_cycle_elements.append(asymptotic_trajectories[i][-1]-asymptotic_trajectories[i][-2])
    # highest_cycle_elements = np.array(highest_cycle_elements)
    # feigenbaum_alphas = (highest_cycle_elements[:-1]/highest_cycle_elements[1:])**(0.25 if mode==3 else 0.5)
    # print(f"Feigenbaum Alphas: {feigenbaum_alphas}")

    modes = [0,1,2,3]
    map_names = ["Logistic Map","Sine Map","Quadratic Map","Biquadratic Map"]
    all_deltas = []
    all_alphas = []
    for mode in modes:
        (x0,chosen_map,left,right,name) = [(0.1,logistic_map,2.99,3.58,"Logistic Map"),(0.1,sine_map,2.26,2.72,"Sine Map"),(0,quadratic_map,0.74,1.4015, "Quadratic Map"),(0,biquadratic_map,0.4,1.596, "Biquadratic Map")][mode]

        results_file = f'{["logistic","sine","quadratic","biquadratic"][mode]}_map_results.txt'
        feigenbaum_deltas = eval(re.findall("\[.*\]",open(results_file,"r").read().split("\n")[1])[0].replace(" ",","))
        feigenbaum_alphas = eval(re.findall("\[.*\]",open(results_file,"r").read().split("\n")[2])[0].replace(" ",","))
        all_deltas.append(feigenbaum_deltas)
        all_alphas.append(feigenbaum_alphas)

    # plot feigenbaum constants
    plot_feigenbaum_constants(map_names, all_deltas, [4.6692,4.6692,4.6692,7.29], all_alphas, [2.5029,2.5029,2.5029,1.69])

    # tine_widths = []
    # for i in range(1,num_points_required):
    #     asymptotic_trajectories[i] = asymptotic_trajectories[i][0][:2**i]
    #     asymptotic_trajectories[i].sort()
    #     curr_tine_widths = []
    #     for j in range(int(2**(i-1))):
    #         curr_tine_widths.append(asymptotic_trajectories[i][2*j+1]-asymptotic_trajectories[i][2*j])
    #     tine_widths.append(curr_tine_widths)
    
    # alphas = []
    # for i in range(num_points_required-2):
    #     curr_alphas = np.repeat(tine_widths[i],2)/tine_widths[i+1]
    #     for j in range(2**i):
    #         if curr_alphas[2*j]<curr_alphas[2*j+1]:
    #             curr_alphas[2*j+1] = np.sqrt(curr_alphas[2*j+1])
    #         else:
    #             curr_alphas[2*j] = np.sqrt(curr_alphas[2*j])
    #     alphas.append(curr_alphas)
    # print(f"Feigenbaum Alphas: {alphas}")

    # # plot boxplot of feigenbaum alphas
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.boxplot(alphas)
    # ax.set_xlabel("Bifurcation #")
    # ax.set_ylabel("Calculated Alpha")
    # ax.set_title(f"Feigenbaum Alphas for {name}")
    # ax.axhline(y=2.5029,color="k",linestyle="--",label="True Feigenbaum Constant")
    # ax.legend()
    # plt.savefig(f"slides/plots/{name.split(' ')[0].lower()}_feigenbaum_alphas.png")
