"""

TODO: catch exception


"""
def getconfig(configfile=None, debug=False, silent=False):
    """
    read config file

    Note the ConfigParser module has been renamed to configparser in Python 3

    look in cwd, home and home/.config

    home/.config not implemented yet




    """
    import os
    import configparser

    from configparser import SafeConfigParser
    # parser = SafeConfigParser()

    print('__file__', __file__)
    if configfile is None:
        if debug:
            print('__file__', __file__)
        configfile_default = os.path.splitext(__file__)[0] + '.cfg'
    if configfile is not None:
        configfile_default = configfile

    print('Open configfile:', configfile)
    if debug:
        print('Open configfile:', configfile)

    # read the configuration file
    config = configparser.RawConfigParser()

    try:
        if not silent:
           print('Reading config file', configfile)

        try:
            config.read(configfile)
        except IOError:
            print('config file', configfile, "does not exist")
            configfile = os.path.join(os.environ["HOME"], configfile)
            print('trying ', configfile)
            config.read(configfile)

    except Exception as e:
        print('Problem reading config file: ', configfile)
        print(e)


    if debug:
        print('configfile:', configfile)
        print('sections:', config.sections())
        for section_name in config.sections():
            print('Section:', section_name)
            print('Options:', config.options(section_name))
            for name, value in config.items(section_name):
                print('  %s = %s' % (name, value))
        print()


    return config
