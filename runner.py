import Server
import Client
import sys


from colortag import c

HELP_MESSAGE = c(
'''
<About: blue;bold>
This is a simple runner script that helps running the server or the client
<Usage: blue;bold>
    python runner.py [APPLICATION]

    [APPLICATION]:
        -c --client: run the client
        -s --server: run the server
'''
)

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
        subprocess.run([sys.executable, '-m', 'flake8', '.'])
    else:
        print("Invalid argument provided. Use -h or --help for help")
        sys.exit(1)
