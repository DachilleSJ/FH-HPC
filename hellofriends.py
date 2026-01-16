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
