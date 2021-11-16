import numpy as np
from typing import Optional, List

class Box3D:
    """Data class that represents a 3D Bounding Box.
    """

    def __init__(
        self,
        center: np.ndarray,
        size: np.ndarray,
        orientation: float,
        velocity: nd.array,
        name: Optional[str] = None,
    ):
        """Initialize.

        Params:
            - center [np.ndarray(1x3)]: center of the box as x, y, z.
            - size [np.ndarray(1x3)]: size of the box as width (x), length (y),
                height (z).
            - orientation [float]: angle with respect of Z-axis (yaw).
            - velocity [np.ndarray(1x3)]: velocity of the box in x, y, z.
            - name [Optional(str)]: descriptive name. Can be used to categorize.
        """
        self.center = center
        self.size = size
        self.orientation = orientation
        self.velocity = velocity
        self.name = name
    
    @classmethod
    def from_nuscenes_box(
        self,
        center: List[float],
        size: List[float],
        orientation: float,
        velocity: List[float],
        name: Optional[str] = None
    ):
        """ 
        """
        pass

    @classmethod
    def from_lidar_cluster(cls, points: np.ndarray) -> Box3D:
        """
        """
        center = np.array([
            [(max(points[:,0]) - min(points[:,0])) / 2,
            (max(points[:,1]) - min(points[:,1])) / 2,
            (max(points[:,2]) - min(points[:,2])) / 2]
        ])
        size = np.array([
            [abs((max(points[:,0]) - min(points[:,0])) * np.cos(orientation)),
            abs((max(points[:,1]) - min(points[:,1])) * np.sin(orientation)),
            abs((max(points[:,2]) - min(points[:,2])))]
        ])
        orientation = 0
        velocity = np.zeros((1,3))
        name = "lidar"

        return cls(center, size, orientation, velocity, name)

    @classmethod
    def from_radar_cluster(cls, points: np.ndarray):
        pass

