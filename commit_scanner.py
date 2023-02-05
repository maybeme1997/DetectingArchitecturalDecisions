"""
This python program runs Archi and uses git to switch commits of the hadoop repository
"""

from os import path, getcwd
import subprocess
from threading import Thread
from subprocess import check_output
from collections import deque

# The list of commits to scan
commits_file = open(path.join(getcwd(), 'commits.txt'), "r").readlines()

# The path the results should be stored
results_directory = path.join(getcwd(), 'results')

# The paths to the project directories. Each additional clone is an extra thread.
project_directories = [
    path.join(getcwd(), 'hadoop1'),
    path.join(getcwd(), 'hadoop2'),
    path.join(getcwd(), 'hadoop3')
]

# The path the Archi jar file
archi_path = path.join(getcwd(), 'Archi.jar')

# The Archi command and path
archi_command = r"java -jar " + archi_path + " %s " + path.join(getcwd(), 'IndicatorTerms.csv') + " 0.4 %s"

queue = deque(commits_file)
number_of_commits = len(commits_file)
iteration = 5  # Current iteration, may be changed to skip commits that have been done.


def scan_commit(_project_directory, _iteration, _commit_hash, _archi_command):
    try:
        # Try to check out the commit
        print(check_output("git checkout " + _commit_hash, cwd=_project_directory, shell=True).decode())
    except subprocess.CalledProcessError:

        # Sometimes line endings suddenly change, so we need to force a checkout to recover.
        print(check_output("git checkout -f master", cwd=_project_directory, shell=True).decode())
        print(check_output("git checkout " + _commit_hash, cwd=_project_directory, shell=True).decode())

    print(_archi_command % (_project_directory, path.join(results_directory, str(_iteration) + '_' + _commit_hash)))

    # Run the archi jar file
    archi_output = check_output(
        _archi_command % (
            _project_directory,
            path.join(results_directory, str(_iteration) + '_' + _commit_hash)),
        cwd=_project_directory,
        shell=True).decode()

    print(archi_output)


# Skip the commits that we may have already done
for i in range(iteration):
    queue.popleft()


# Repeat until each commit has been scanned by Archi
while len(queue) > 0:

    active_threads = []

    # For each project directory make a new thread for Archi
    for project_directory in project_directories:
        commit_hash = queue.popleft().split(sep=' ')[0]
        active_threads.append(
            Thread(target=scan_commit, args=(project_directory, iteration, commit_hash, archi_command)))
        active_threads[-1].start()
        iteration = iteration + 1

    # Wait for each thread to finish
    for threads in active_threads:
        threads.join()

    print('Progress:', iteration / number_of_commits, 'Remaining:', len(queue), 'Iteration', iteration)
