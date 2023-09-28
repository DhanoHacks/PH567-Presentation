# calculate the lyapunov exponent for a given trajectory
from utils import *

def initialize(mode):
    x0 = 0.1
    t = 10000
    if mode==0: # logistic map
        bifurcation_points = [2.999919451326132, 3.4494625471532343, 3.544081568568945, 3.564405039995909, 3.568759296685456, 3.569693561047315]
    elif mode==1: # sine map
        bifurcation_points = [2.2617597829736775, 2.617756718602032, 2.6973907856456947, 2.714597988333553, 2.718290666397661, 2.7190821440331634]
    elif mode==2: # quadratic map
        bifurcation_points = [0.7499077196456492, 1.2499600123651324, 1.3680846406109632, 1.3940418727807702, 1.39963031661883, 1.400828912612051]
    A = np.array([])
    A = np.hstack((A,np.linspace(0.001,bifurcation_points[0],1000,endpoint=False)))
    for i in range(len(bifurcation_points)-1):
        A = np.hstack((A,np.linspace(bifurcation_points[i],bifurcation_points[i+1],100,endpoint=False)))
    right_limit = [4,4,2][mode]
    A = np.hstack((A,np.linspace(bifurcation_points[-1],right_limit,1000)))
    chosen_map = [logistic_map,sine_map,quadratic_map][mode]
    chosen_map_derivative = [logistic_map_derivative,sine_map_derivative,quadratic_map_derivative][mode]
    map_name = ["logistic","sine","quadratic"][mode]
    return x0, A, t, chosen_map, chosen_map_derivative, map_name

def lyapunov_exponent(trajectory,A,chosen_map_derivative=logistic_map_derivative):
    return np.mean(np.log(np.abs(chosen_map_derivative(trajectory,A))),axis=1)

def plot_lyapunov_exponents(A,exponents,map_name,save=False):
    plt.axhline(0,color='black')
    plt.plot(A,exponents)
    plt.xlabel("A")
    plt.ylabel("Lyapunov exponent")
    plt.title(f"Lyapunov exponent for {map_name} map")
    if save:
        plt.savefig(f"plots/{map_name}_lyapunov_exp.png",dpi=600)
    # plt.show()
    plt.close()

def main(mode):
    x0, A, t, chosen_map, chosen_map_derivative, map_name = initialize(mode)
    trajectory = evolution(x0, A, t, None,chosen_map)
    exponents = lyapunov_exponent(trajectory,A,chosen_map_derivative)
    plot_lyapunov_exponents(A,exponents,map_name,save=True)

if __name__ == "__main__":
    plot_all = True
    if plot_all:
        for i in range(3):
            main(i)
            
    else:
        main(0) # mode = 0: logistic map, 1: sine map, 2: quadratic map