import os

# Script to execute 'compute_dynamic_genetics.py' with varying parameters
for i in range(20, 51, 5):
    print(f"Executing: python compute_dynamic_genetics.py {i}")
    # Simulating execution - In actual use, the following line should run the command
    os.system(f"python compute_dynamic_genetics.py {i}")