#!/bin/bash
#SBATCH --job-name=launch_friends
#SBATCH --partition=short
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=logs/launch_%j.out
#SBATCH --error=logs/launch_%j.err

source ~/.bashrc
micromamba activate tcrdist311

python makejobs.py

for f in sbatches/*.sbatch; do
    sbatch "$f"
done

