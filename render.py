import matplotlib.pyplot as plt
import numpy as np

def render_lidar_and_radar_pc(lpc: np.ndarray, rpc: np.ndarray, title: str="Point Cloud",) -> plt.Axes:
    """
    """

    (lx, ly, lz) = lpc[:,0], lpc[:,1], lpc[:,2]
    (rx, ry, rz) = rpc[:,0], rpc[:,1], rpc[:,2]

    fig = plt.figure(figsize=plt.figaspect(0.5))

    # axes for the first plot
    ax1 = fig.add_subplot(1,2,1, projection='3d')
    ax1.set_title("Lidar")
    ax1.scatter(lx, ly, lz, s=1, alpha=1)
    # ax.set_xlim3d(0, 1000)
    # ax.set_ylim3d(0, 1000)
    ax1.set_zlim3d(0, 25)

    # axes for the second plot
    ax2 = fig.add_subplot(1,2,2, projection='3d')
    ax2.set_title("Radar")
    ax2.scatter(rx, ry, rz, s=1, alpha=1)
    ax2.set_zlim3d(0, 25)

    plt.show()