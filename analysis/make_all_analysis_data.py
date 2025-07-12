#!/usr/bin/env python3
"""
Orchestration script to run all three analysis scripts in sequence:
1. 1_make_longform_orders_data.py 
2. 2_make_convo_data.py
3. 3_make_phase_data.py

This script passes the same CLI arguments to each script.

eg

# Basic usage with all parameters
python analysis/make_all_analysis_data.py --selected_game game1 game2 --game_data_folder "/path/to/Game Data" --output_folder "/path/to/Game Data - Analysis" --analysis_folder "/path/to/analysis"

# Using output_folder as analysis_folder
python analysis/make_all_analysis_data.py --selected_game game1 --game_data_folder "/path/to/Game Data" --output_folder "/path/to/Game Data - Analysis"

# or leave out to process all games in the data folder
python analysis/make_all_analysis_data.py --game_data_folder "/path/to/Game Data" --output_folder "/path/to/Game Data - Analysis"
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

def run_script(script_name, args_dict):
    """Run a script with the provided arguments."""
    print(f"\n=== Running {script_name} ===")
    
    cmd = [sys.executable, script_name]
    
    # Add all arguments that apply to this script
    for arg_name, arg_value in args_dict.items():
        if arg_value:  # Only add if value exists
            if isinstance(arg_value, list):
                cmd.append(f"--{arg_name}")
                cmd.extend(arg_value)
            else:
                cmd.append(f"--{arg_name}")
                cmd.append(str(arg_value))
    
    print(f"Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, text=True)
    
    # Print output
    if result.stdout:
        print("\nOutput:")
        print(result.stdout)
    
    # Check for errors
    if result.returncode != 0:
        print("\nERROR:")
        print(result.stderr)
        return False
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run all three analysis scripts in sequence with the same arguments.")
    
    parser.add_argument(
        "--selected_game", 
        type=str, 
        nargs='*', 
        help="One or more specific games to process. If not provided, all games in the data folder will be processed."
    )
    parser.add_argument(
        "--game_data_folder", 
        type=str, 
        required=True,
        help="The folder where game data is stored."
    )
    parser.add_argument(
        "--analysis_folder", 
        type=str, 
        required=True,
        help="The folder to save the new analysis folders and files"
    )

    args = parser.parse_args()
    
    # Convert namespace to dictionary
    args_dict = vars(args)
    args_dict["analysis_folder"] = Path(args_dict["analysis_folder"])
    args_dict["game_data_folder"] = Path(args_dict["game_data_folder"])
    
    # Prepare arguments for each script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    script1_path = os.path.join(script_dir, "1_make_longform_orders_data.py")
    script2_path = os.path.join(script_dir, "2_make_convo_data.py")
    script3_path = os.path.join(script_dir, "3_make_phase_data.py")
    
    # Run scripts in order
    if not run_script(script1_path, {k: v for k, v in args_dict.items()}):
        print("ERROR: Failed to run 1_make_longform_orders_data.py. Stopping.")
        sys.exit(1)
        
    if not run_script(script2_path, {k: v for k, v in args_dict.items()}):
        print("ERROR: Failed to run 2_make_convo_data.py. Stopping.")
        sys.exit(1)
        
    if not run_script(script3_path, {k: v for k, v in args_dict.items()}):
        print("ERROR: Failed to run 3_make_phase_data.py. Stopping.")
        sys.exit(1)
        
    print("\n=== All analysis scripts completed successfully! ===")
