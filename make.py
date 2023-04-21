import subprocess

# Compiling the solver code
subprocess.call(["g++", "-o", "solver", "solver-naive.cpp"])

# Running all 16x16 boards
subprocess.call(["./solver", "16", "easy-16.txt"])
subprocess.call(["python3", "checker.py", "solved-easy-16.txt"])
subprocess.call(["./solver", "16", "random1-16.txt"])
subprocess.call(["python3", "checker.py", "solved-random1-16.txt"])
subprocess.call(["./solver", "16", "random2-16.txt"])
subprocess.call(["python3", "checker.py", "solved-random2-16.txt"])
subprocess.call(["./solver", "16", "edge-16.txt"])
subprocess.call(["python3", "checker.py", "solved-edge-16.txt"])

# Running all 25x25 boards
subprocess.call(["./solver", "25", "easy-25.txt"])
subprocess.call(["python3", "checker.py", "solved-easy-25.txt"])
subprocess.call(["./solver", "25", "random1-25.txt"])
subprocess.call(["python3", "checker.py", "solved-random1-25.txt"])
subprocess.call(["./solver", "25", "random2-25.txt"])
subprocess.call(["python3", "checker.py", "solved-random2-25.txt"])
subprocess.call(["./solver", "25", "edge-25.txt"])
subprocess.call(["python3", "checker.py", "solved-edge-25.txt"])