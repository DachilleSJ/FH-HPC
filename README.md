# Using the FH HPC
The FH has its own HPC which we can run jobs on, just like at St. Jude.

It has its own set of commands. At St. Jude we would use bsub, but here we use SBATCH for jobs as it is **Slurm** based.

## Using Slurm

### Connect to the HPC
Connect to the HPC by opening a terminal instance (on Mac) and typing
```
ssh rhino02
```
You will then be prompted to type in your password to enter the HPC.

Note: rhino above has a number after it, to keep your same tmux session (below) use the same number when using "sshing" into rhino.

### Use tmux to create sessions
To manage different tasks, you can use a command called ``tmux ``. This command allows you to swap between different sessions which can run different tasks. If you are running some code and have to go off and do something, your tmux session can be running in the background without you losing it if you are logged out.

You can swap between sessions using ``ctrl + B, then W`` in sequence. Type ``logout`` to end a tmux session. 

There is a tmux cheatsheet [here](https://tmuxcheatsheet.com/#google_vignette). 

### Setup your conda/mamba environments
See my previous tutorial. you dont really need a special env for this, but you should make one.


### Grab a node
On St. Jude, you used to have to run
```hpcf_interactive```
or a bsub job specifying memory. Here it is arguably easier. Just type:
```
grabnode
``` 
and you will be prompted with questions to answer, like how much memory, how many cores, and how much time would you like the session to run for?

Note: You **can** exceed the memory allotted to you, as you are sharing the resources. Be a good data steward and don't load things into memory that are larger than the memory you allocated. 

You can view the queue with 

```
hitparade
```

or the top using

```
hitparade | head -n 5
```

or even our usage with 

```
hitparade | grep thomas_p
```

You can also check usage with 
```
htop
```
and exit the view with "q"

### Running srun jobs
This is similar to how we run bsub jobs, but on an individual basis. this is one sigular job that you are kicking off right there.

- more notes needed for proper notation now. check Koshlan repo.


### Running SBATCH jobs
Sbatch jobs are what we will use for most big job submissions and is very similar to how the HPC at st jude worked with bjobs. 

Here is a vignette:

You can find all the files at ``/fh/fast/thomas_p/grp/dachille/slurm_fun``

I made a list of "friends" in a text file called ``friends.txt``, some code to say hi to a friend in ``hellofriends.py``. I also made a script to make lots of jobs, just to test the sbatch system in ``makejobs.py``, this is a template to set up a job kickoff, may need some edits if you want to use it for other things. lastly there is ``runjobs.sh`` which is the actual file that is run. 

To run the job, which basically says "Hello <friend>" in the <friend_name>.out log file and in a separate <friend_name> to all of my "friends", type:

```
sbatch runjobs.sh
```

while in this directory ``/fh/fast/thomas_p/grp/dachille/slurm_fun``

### Try for yourself

If you want to copy this and test out some slurm job submission stuff, here is the code for all the files mentioned here:

They can also be found in this repo!

friends.txt
```
Randy
Stan
Kyle
Kenny
Cartman
Wendy
Bebe
Butters
Craig
Tweek
Jimmy
Timmy
Heidi
Clyde
Sharon
Gerald
Sheila
Ike
Towelie
```

hellofriends.py
```
import sys
import os

if len(sys.argv) < 2:
    print("Name not long enough")
    sys.exit(1)

name = sys.argv[1]

print(f"Runtime Hello {name}")

outdir = "/fh/fast/thomas_p/grp/dachille/slurm_fun"
os.makedirs(outdir, exist_ok=True)

filepath = os.path.join(outdir, name)

try:
	with open(filepath, 'w') as f:
		f.write(f"File Hello {name}")
except IOError as e:
	print(f"An error occured: {e}:")
```

makejobs.py
```
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
```

runjobs.sh
```
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
```




