# calculate the lyapunov exponent for a given trajectory
from utils import *
import re

def lyapunov_exponent(trajectory,A,chosen_map_derivative=logistic_map_derivative):
    return np.mean(np.log(np.abs(chosen_map_derivative(trajectory,A))),axis=1)

def plot_lyapunov_exponents(A,exponents,map_name,save=False):
    plt.axhline(0,color='black')
    plt.plot(A,exponents)
    plt.xlabel("A")
    plt.ylabel("Lyapunov exponent")
    plt.title(f"Lyapunov exponent for {map_name} map")
    if save:
        plt.savefig(f"slides/plots/{map_name}_lyapunov_exp.png",dpi=600)
    plt.show()
    plt.close()

def main(mode):
    x0 = 0.1
    t = 10000
    results_file = f'{["logistic","sine","quadratic","biquadratic"][mode]}_map_results.txt'
    bifurcation_points = eval(re.findall("\[.*\]",open(results_file,"r").read().split("\n")[0])[0])
    A = np.array([])
    A = np.hstack((A,np.linspace(0.001,bifurcation_points[0],1000,endpoint=False)))
    for i in range(len(bifurcation_points)-1):
        A = np.hstack((A,np.linspace(bifurcation_points[i],bifurcation_points[i+1],100,endpoint=False)))
    right_limit = [4,4,2,2][mode]
    A = np.hstack((A,np.linspace(bifurcation_points[-1],right_limit,1000)))
    chosen_map = [logistic_map,sine_map,quadratic_map,biquadratic_map][mode]
    chosen_map_derivative = [logistic_map_derivative,sine_map_derivative,quadratic_map_derivative,biquadratic_map_derivative][mode]
    map_name = ["logistic","sine","quadratic","biquadratic"][mode]

    # calculate lyapunov exponent
    trajectory = evolution(x0, A, t, None,chosen_map)
    exponents = lyapunov_exponent(trajectory,A,chosen_map_derivative)
    plot_lyapunov_exponents(A,exponents,map_name,save=False)

if __name__ == "__main__":
    plot_all = False
    if plot_all:
        for i in range(4):
            main(i)
            
    else:
        main(1) # mode = 0: logistic map, 1: sine map, 2: quadratic map