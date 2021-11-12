import numpy as np
from nuscenes import NuScenes
from nuscenes.utils.data_classes import LidarPointCloud, RadarPointCloud

from pyquaternion import Quaternion
from typing import List


def load_bounding_boxes_annotations():
    pass

def load_sample_tokens_in_scene(nusc: NuScenes, scene: str) -> List[str]:
    """Function that loads all the sample tokens that are in a determined
    scene.

    Args:
        - nusc: NuScenes handler
        - scene [str]: metadata scene name.
    Return:
        - all_samples [List[str]]: list containing all sample tokens in 
            a scene.
    See also:
        - nusc.list_scene() for available scenes.
    """

    # Load the required scene, its first and last token name.
    scene = nusc.scene[0]
    first_sample_token = scene["first_sample_token"]
    last_sample_token = scene["last_sample_token"]

    # Iterate over the scene to obtain all sample tokens in the scene.
    all_samples = []
    cur_sample = nusc.get('sample', first_sample_token)
    for i in range(1, int(scene["nbr_samples"]+1)):
        all_samples.append(cur_sample["token"])
        if i != int(scene["nbr_samples"]):
            nxt_sample = nusc.get('sample', cur_sample["next"])
            cur_sample = nxt_sample
    return all_samples


def load_radar_pc(nusc: NuScenes, sample_token: str, filepath: str) -> np.ndarray:
    """Function that loads a point cloud corresponding to the sensor
    fusion of all the radars mounted in NuScenes vehicle. The point 
    cloud is referenced to the ego frame.

    Args:
        - nusc: NuScenes handler
        - sample_token [str]:
        - filepath [os.path]: indicates where the dataset is stored.
    Return:
        - radar_pc [np.ndarray(n x 5)]:
    """

    # Define the available radar channels.
    channels = ["RADAR_FRONT", "RADAR_FRONT_LEFT", "RADAR_FRONT_RIGHT", "RADAR_BACK_LEFT", "RADAR_BACK_RIGHT"]

    # Get the sample data using NuScenes handler.
    sample = nusc.get("sample", sample_token)

    # Create a dict in which tokens for each radar token in the sample are loaded.
    channel_tokens = dict()
    for k, v in sample["data"].items():
        if k in channels:
           channel_tokens[k] = v

    # Merging radar point clouds in the sample.
    for (i, channel) in enumerate(channels):

        # Get the point cloud of a sensor.
        data = nusc.get("sample_data", sample["data"][channel])
        pc = RadarPointCloud.from_file(filepath + data["filename"])

        # Transform into the ego motion frame (frame normalization policy).
        transformation = nusc.get("calibrated_sensor", data["calibrated_sensor_token"])
        pc.rotate(Quaternion(transformation["rotation"]).rotation_matrix)
        pc.translate(np.array(transformation["translation"]))

        # Choose the columns of interest.
        coi = np.array([0,1,2,8,9]) # 0: X, 1: Y, 2: Z, 8: vx_comp, 9: vy_comp

        # Interested in returning a N x len(coi) array.
        pc_npy = pc.points[coi, :].transpose()

        # Stack with the rest of clouds.
        radar_pc = pc_npy if i == 0 else np.vstack((radar_pc, pc_npy))

    return radar_pc


def load_lidar_pc(nusc: NuScenes, sample_token: str, filepath: str) -> np.ndarray:
    """Function that loads a point cloud corresponding to the Lidar
    sensor mounted in top of the NuScenes vehicle. The point cloud
    is referenced to the ego frame.

    Args:
        - nusc: NuScenes handler
        - sample_token [str]:
        - filepath [os.path]: indicates where the dataset is stored.
    Return:
        - radar_pc [np.ndarray(n x 3)]:
    """

    # Get the sample data using NuScenes handler.
    sample = nusc.get("sample", sample_token)

    # Process lidar point cloud.
    data = nusc.get("sample_data", sample["data"]["LIDAR_TOP"])
    pc = LidarPointCloud.from_file(filepath + data["filename"])

    # Transform into the ego motion frame (frame normalization policy).
    transformation = nusc.get("calibrated_sensor", data["calibrated_sensor_token"])
    pc.rotate(Quaternion(transformation["rotation"]).rotation_matrix)
    pc.translate(np.array(transformation["translation"]))

    # Choose the columns of interest.
    coi = np.array([0,1,2]) # 0: X, 1: Y, 2: Z

    # Interested in returning a N x len(coi) array.
    pc_npy = pc.points[coi, :].transpose()

    return pc_npy