#!/bin/bash

# Activate the conda environment
source ~/.bashrc
conda activate pyDjango

# If there are any arguments, run them as a command
if [ $# -gt 0 ]; then
  # Run the provided command
  "$@"
  # After the command finishes, start an interactive shell
  exec bash
else
  # If no arguments are provided, start an interactive shell
  exec bash
fi