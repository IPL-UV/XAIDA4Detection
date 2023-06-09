#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse, yaml
from datetime import datetime

def setup(filename):
    """
    Open configuration file .yaml as a dictionary

    Parameters
    ----------
    filename : path to .yaml configuration file.

    Returns
    -------
    config : python dictionary.
    """
    
    # Load YAML config file into a dict variable
    with open(filename) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python dictionary format
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config
    
def setup_config():
    """
    Gets the configuration for the current experiment and creates the needed folder structure.
    If provided, some hyperparameters can be added

    Returns
    -------
    config : python dictionary with the experiment configuration.
    """
    
    # Parent path
    parent_path = '.'
    
    # Define the experiment
    general_parser = argparse.ArgumentParser(description = "ArgParse")
   
    # General arguments
    general_parser.add_argument('--config', default = '/configs/config.yaml', type = str)
    general_parser.add_argument('--exp_id', default= datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), type = str)
    
    # Add the variables   
    args = general_parser.parse_args()

    # Load configuration files
    filename = parent_path + args.config
    config = setup(filename)
    
    # Update config
    config['experiment_id'] = args.exp_id
    
    # Create experimental folder structure
    if not os.path.isdir(config['save_path']):
        os.mkdir(config['save_path'])
        
    config['save_path'] = config['save_path'] + config['experiment_id']
    if not os.path.isdir(config['save_path']):
        os.mkdir(config['save_path'])
    
    # Save experiment config into the experiment folder
    with open(config['save_path'] + '/config.yaml', 'w') as file:
        yaml.dump(config, file)
    
    return config