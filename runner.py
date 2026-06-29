import Server
import Client
import sys

HELP_MESSAGE = ('''
This is a simple runner script that helps running the server or the client
    python runner.py [APPLICATION]

    [APPLICATION]:
        -c --client: run the client
        -s --server: run the server
''')


def count_lines(dir):
    total_lines = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    total_lines += len(f.readlines())
    return total_lines


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Insufficient arguments provided. Use -h or --help for help")
        sys.exit(1)
    arg = sys.argv[1]
    if arg == '-c' or arg == '--client':
        Client.run()
    elif arg == '-s' or arg == '--server':
        Server.run()
    elif arg == '-h' or arg == '--help':
        print(HELP_MESSAGE)
    elif arg == '-f' or arg == '--flake8':
        # Check if the project is correct regarding PEP specification
        import subprocess
        subprocess.run([
            sys.executable, '-m', 'flake8', '.', '--exclude', 'PPEnv',
            '--ignore', 'F401,W503,E125'
        ])
    elif arg == '--count':
        # Count the number of lines in the project
        import os
        total_lines = (
            count_lines('./Utils')
            + count_lines('./Server')
            + count_lines('./Client')
        )
        print(f'Total lines of code: {total_lines}')
    else:
        print("Invalid argument provided. Use -h or --help for help")
        sys.exit(1)
