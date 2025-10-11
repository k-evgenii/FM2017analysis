"""
Convenience runner to invoke the Attribute_correlation analysis from repo root.
Usage:
    python run_attribute_analysis.py --position 1
Or to run for all players:
    python run_attribute_analysis.py
"""
import sys
from pathlib import Path

# forward arguments to module script
script = Path(__file__).parent / 'fman_initial_Dat_Analysis_test' / 'Attribute_correlation.py'
if not script.exists():
    print(f"ERROR: Script not found: {script}")
    sys.exit(1)

# Build command
cmd = [sys.executable, str(script)] + sys.argv[1:]
print('Running:', ' '.join(cmd))

import subprocess
subprocess.check_call(cmd)
