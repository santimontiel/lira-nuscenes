#!/usr/bin/env python3

# LiRa-nuScenes.
# Code written by Santiago Montiel-Marín, 2021.

""" 
"""

import argparse
import os
import numpy as np
from nuscenes import NuScenes
import matplotlib.pyplot as plt
import open3d as o3d

# LiRa-MOT modules
from detection_helper import classify_clusters_o3d
# from data_classes import Box3D

# NuScenes specific modules
from loader import load_sample_tokens_in_scene, load_radar_pc, load_lidar_pc
from render import render_lidar_and_radar_pc


def main() -> None:
    """Main function for LiRa-NuScenes.
    """

    # Read input parameters.
    NUSCENES_PATH = '/media/robesafe/Santi/data/sets/nuscenes/'

    # Initialize NuScenes database.
    nusc = NuScenes(version="v1.0-mini", dataroot=NUSCENES_PATH, verbose=False,)

    # List available scenes and load a scene.
    nusc.list_scenes()
    scene = nusc.scene[2]["token"]

    # Load all samples for desired scene.
    all_sample_tokens = load_sample_tokens_in_scene(nusc, nusc.scene[2])

    # Scene execution loop.
    for sample_token in all_sample_tokens:

        # Get groundtruth-annotations
        sample = nusc.get("sample", sample_token)
        ann_tokens = sample["anns"]

        boxes_anns_gt = [nusc.get_box(ann_token) for ann_token in ann_tokens]
        suma = 0
        for box in boxes_anns_gt:
            print(box.name[0:7])
            if box.name[0:7] == "vehicle":
                suma += 1
        print(f"Suma is {suma}")


        # fig = plt.figure(figsize=plt.figaspect(1))
        # ax1 = fig.add_subplot(1,1,1, projection='3d')
        # for box in boxes_anns_gt:
        #     transformation = nusc.get("calibrated_sensor", data["calibrated_sensor_token"])
        #     box.rotate(Quaternion(transformation["rotation"]).rotation_matrix)
        #     box.translate(np.array(transformation["translation"]))
        #     box.render(axis=ax1)
        # plt.show()
        # boxes_obj_gt = [Box3D(center, size, orientation, velocity)]

        # print(len(boxes_gt))
        # print(boxes_gt)

        # for (i, box) in enumerate(boxes_anns_gt):
        #     print(f"Box {i} is {box}")
        #     Box3D(center, size, orientation, velocity)

        # Load radar and lidar point clouds for this sample.
        radar_pc = load_radar_pc(nusc, sample_token, NUSCENES_PATH)
        lidar_pc = load_lidar_pc(nusc, sample_token, NUSCENES_PATH)

        # # TODO: Get ground-truth annotations for lidar and radar.
        # print(sample)
        # sd_rec = nusc.get("sample_data", nusc.scene[1])
        # s_rec = nusc.get("sample", sd_rec["sample_token"])
        # print(sample)
        # print(sd_rec)
        # print(s_rec)


        # ann_recs = [nusc.get("sample_annotation", token) for token in s_rec


        # Radar object detection processing.
        xyz_vect = np.array([0,1,2])
        radar_o3d_pc = o3d.geometry.PointCloud()
        print(np.shape(radar_pc[:,xyz_vect]))
        radar_o3d_pc.points = o3d.utility.Vector3dVector(radar_pc[:,xyz_vect])
        print(radar_o3d_pc)

        radar_labels = np.array(radar_o3d_pc.cluster_dbscan(eps=1, min_points=2))
        (radar_clusters, radar_indices) = classify_clusters_o3d(radar_o3d_pc, radar_labels)
        # print(radar_clusters)
        # print(len(radar_clusters))
        # print(type(radar_clusters))

        for (i, cluster) in enumerate(radar_clusters):
            print(f"Cluster {i}")
            for (j, point) in enumerate(cluster):
                print(f"Point {j} is {point}")

        render_lidar_and_radar_pc(lidar_pc, radar_pc)

        raise SystemExit


if __name__ == "__main__":
    main()