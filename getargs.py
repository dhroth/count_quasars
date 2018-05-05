"""

Template getargs function

Usage

python getargs.py --help


def getargs():

....

if __name__=='__main__':

    args = getargs()
    debug = args.debug()

"""

def getargs(verbose=False):
    """

    parse command line arguements

    not all args are active

    """
    import sys
    import pprint
    import argparse

    # there is probably a version function out there
    __version__ = '0.1'

    description = 'This is a template using getargs'
    epilog = """WARNING: Not all options may be supported
             """
    parser =  argparse.ArgumentParser(
        description=description, epilog=epilog,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)


    # the destination defaults to the option parameter
    # defaul=False might not be needed

    parser.add_argument("-s", "--saveOutput", help="Save output to disk",
                        action="store_true")

    parser.add_argument("-f", "--forceOverwrite",
                        help="Overwrite output files " +
                        "if they already exist", action="store_true")

    parser.add_argument("-x", "--minLimitingDepth",
                         help="x-axis minimum value", type=float)

    parser.add_argument("-X", "--maxLimitingDepth",
                        help="x-axis maximum value", type=float)

    parser.add_argument("-y", "--yMin", help="y-axis minimum value", type=float)

    parser.add_argument("-Y", "--yMax", help="y-axis maximum value", type=float)


    parser.add_argument("--configfile",
                        default=None,
                        help="configuration file")

    parser.add_argument("--debug",
                        action='store_true',
                        help="debug option")

    parser.add_argument("--verbose", default=verbose,
                        action='store_true',
                        help="verbose option")

    parser.add_argument("--version", action='store_true',
                        help="verbose option")


    args = parser.parse_args()


    if args.debug or args.verbose:
        print('Number of arguments:', len(sys.argv),
              'arguments: ', sys.argv[0])

    if args.debug or args.verbose:
        pprint.pprint(args)

    if args.version:
        print('version:', __version__)
        sys.exit(0)

    return args


if __name__=='__main__':

    args = getargs(verbose=True)
