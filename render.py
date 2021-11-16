import matplotlib.pyplot as plt
import numpy as np

def render_lidar_and_radar_pc(lpc: np.ndarray, rpc: np.ndarray, title: str="Point Cloud",) -> plt.Axes:
    """
    """

    (lx, ly, lz) = lpc[:,0], lpc[:,1], lpc[:,2]
    (rx, ry, rz) = rpc[:,0], rpc[:,1], rpc[:,2]

    fig = plt.figure(figsize=plt.figaspect(1))

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


    # Line 1
    ax2.plot([-18.02, -18.02], [-10.09, -8.82], [0,0]) # L12
    ax2.plot([-18.02, -17.18], [-10.09, -10.09], [0,0]) # L13
    ax2.plot([-17.18, -17.18], [-10.09, -8.82], [0,0]) # L12
    ax2.plot([-18.02, -17.18], [-8.82, -8.82], [0,0]) # L12


    plt.show()

def render_bounding_box():
    pass




"""

Point 0 is [-17.96525019  -8.82170258   0.53      ]
Point 1 is [-18.02369565  -9.41884866   0.53      ]
Point 2 is [-17.25427026  -8.66897144   0.53      ]
Point 3 is [-17.1864291   -9.66666758   0.53      ]
Point 4 is [-17.5583707  -10.09288256   0.53      ]

xmin = -18.02369565  xmax = -17.1864291
ymin = -10.09288256  ymax = -8.82170258


"""