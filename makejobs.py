import os
from pathlib import Path

FRIENDS_FILE = "friends.txt"
SBATCH_DIR = Path("sbatches")
LOG_DIR = Path("logs")
PYTHON_SCRIPT = Path("hellofriends.py")

SBATCH_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

with open(FRIENDS_FILE) as f:
    names = [line.strip() for line in f if line.strip()]

for name in names:
    sbatch_path = SBATCH_DIR / f"{name}.sbatch"
    with open(sbatch_path, "w") as f:
        f.write(f"""#!/bin/bash
#SBATCH --job-name={name}
#SBATCH --partition=short
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:01:00
#SBATCH --output={LOG_DIR}/{name}.out
#SBATCH --error={LOG_DIR}/{name}.err

source ~/.bashrc
micromamba activate tcrdist311

python {PYTHON_SCRIPT} {name}
""")
    print(f"Generated {sbatch_path}")

