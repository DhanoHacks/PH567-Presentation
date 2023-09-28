# Plot the bifurcation diagram for a given map
from utils import *

def plot_bifurcation_diagram(A, points, name, save=False):
    for i in range(len(A)):
        unique_points = np.unique(points[i,:])
        n = len(unique_points)
        if i==0:
            plot_points = np.vstack((np.repeat(A[i],n),unique_points))
        else:
            plot_points = np.hstack((plot_points, np.vstack((np.repeat(A[i],n),unique_points))))
    fig,ax = plt.subplots(figsize = (8,6))
    ax.plot(plot_points[0,:],plot_points[1,:],"b.",markersize=1)
    plt.xlabel("A")
    plt.ylabel("Attractor")
    plt.title(f"{name} Bifurcation Diagram")
    if save:
        plt.savefig(f"plots/{name.split(' ')[0].lower()}_bifurcation_diagram.png")
    # plt.show()
    plt.close()

def main(mode):
    x0 = 0.1
    arr_size = 256
    t = 10000
    full = False
    hd = False
    (chosen_map,left,right,name) = [(logistic_map,0 if full else 2.9,4,"Logistic Map"),(sine_map,0 if full else 2,np.pi,"Sine Map"),(quadratic_map,0,2,"Quadratic Map")][mode]
    A = np.arange(left,right,0.001 if hd else 0.004)
    asymptotic_trajectory = evolution(x0, A, t, arr_size, chosen_map)
    plot_bifurcation_diagram(A, asymptotic_trajectory, name, save=True)

if __name__ == "__main__":
    plot_all = True
    if plot_all:
        for i in range(3):
            main(i)
    else:
        mode = 2 # 0: logistic map, 1: sine map, 2: quadratic map
        main(mode)