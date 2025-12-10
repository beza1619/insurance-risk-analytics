# git_branches.py - Create task branches
import subprocess

# List of branches to create
branches = [
    'task-1-eda',
    'task-2-dvc', 
    'task-3-hypothesis',
    'task-4-modeling'
]

print("Creating Git branches for tasks...")

for branch in branches:
    # Create branch
    cmd = f'git checkout -b {branch}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Created: {branch}")
    else:
        print(f"Could not create {branch}: {result.stderr}")
    
    # Switch back to main
    subprocess.run('git checkout main', shell=True)

print("All branches created!")
print("Use: git checkout task-2-dvc")
