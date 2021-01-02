import sys, argparse

def _echo(message: str):
    print ("ECHO: " + message)

    return


if __name__ == "__main__":

    # Accept and organize arguments.
    parser = argparse.ArgumentParser(description='ECS input output 1 app')
    parser.add_argument('echostring', type=str, metavar='<String to echo>', help='A string to echo')
    parser.add_argument('-d', '--datetime', metavar='<Target datetime in ISO 8601>', dest='datetime', help='A datetime to process.')
    parser.add_argument('-s', '--succeed', action="store_true", dest='succeed', help='Specify whether the process succeeds or fails.')
    parser.add_argument('-r', '--running-mode', type=str, choices=["alpha", "beta"], dest='running_mode', help='Specify which mode you want to run.')

    # Check the arguments.
    args = parser.parse_args()
    print(args)

    if (args.running_mode == 'alpha'):
        print('You are going in alpha mode.')
    
    if (args.running_mode == 'beta'):
        print('You are going in beta mode.')
    else:
        print("You didn't specify running mode.")


    # Perform main steps
    _echo(args.echostring)

    # Decide whether this process will fail or succeed.
    if (args.succeed == True):
        print('This program will end with an exit code 0.')
        sys.exit(0)
    else:
        print('This program will end with an exit code 9.')
        sys.exit(9)


