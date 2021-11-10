#!/usr/bin/env python3

# LiRa-nuScenes.
# Code written by Santiago Montiel-Marín, 2021.

""" 
"""

import argparse
import os
import numpy as np

from nuscenes import NuScenes

from loader import load_sample_tokens_in_scene, load_radar_pc, load_lidar_pc
from render import render_lidar_and_radar_pc

import matplotlib.pyplot as plt

def main() -> None:
    """Main function for LiRa-NuScenes.
    """

    # Read input parameters.
    NUSCENES_PATH = '/media/robesafe/Santi/data/sets/nuscenes/'

    # Initialize NuScenes database.
    nusc = NuScenes(version="v1.0-mini", dataroot=NUSCENES_PATH, verbose=False,)

    # List available scenes.
    nusc.list_scenes()

    # Load all samples for desired scene.
    all_samples = load_sample_tokens_in_scene(nusc, nusc.scene[1])

    # Scene execution loop.
    for sample in all_samples:
        radar_pc = load_radar_pc(nusc, sample, NUSCENES_PATH)
        lidar_pc = load_lidar_pc(nusc, sample, NUSCENES_PATH)


if __name__ == "__main__":
    main()