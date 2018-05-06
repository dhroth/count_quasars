"""

TODO: catch exception


"""
def getconfig(configfile=None, debug=False, silent=False):
    """
    read config file

    Note the Python 2.7 ConfigParser module has been renamed
    to configparser in Python 3

    could look in cwd, home and home/.config

    home/.config not implemented yet


    """
    import os
    import configparser

    from configparser import SafeConfigParser

    import numpy as np

    # parser = SafeConfigParser()


    # read the configuration file
    # config = configparser.RawConfigParser()
    conf = configparser.SafeConfigParser()
    if configfile is None:
        conf.read("countQuasars.conf")

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

   # get general config params

    survey = conf.get("general", "survey")
    f = conf.get("general", "filter")
    reddening = conf.getfloat("general", "reddening")
    skyArea = conf.getfloat("general", "area")
    qlfParamsFilename = conf.get("general", "qlfParamsFilename")
    qlfName = conf.get("general", "qlfName")
    k = conf.getfloat("general", "k")

    # get output config params
    outputDir = conf.get("output", "outputDir")
    outFilenameTbl = conf.get("output", "outFilenameTbl")
    outFilenamePlt = conf.get("output", "outFilenamePlt")

    # get SED config params
    sedDir = conf.get("sed", "sedDir")
    sedFilenameFormat = conf.get("sed", "sedFilenameFormat")

    # get integral config params
    zMin = conf.getfloat("integral", "zMin")
    zMax = conf.getfloat("integral", "zMax")
    zStep = conf.getfloat("integral", "zStep")

    M1450Min = conf.getfloat("integral", "M1450Min")
    M1450Max = conf.getfloat("integral", "M1450Max")
    M1450Step = conf.getfloat("integral", "M1450Step")

    # get cosmology config params
    km_s_Mpc2Hz = 3.24077828 * 10**-20
    m2pc = 3.24078e-17
    c = 3. * 10**8
    H0 = conf.getfloat("cosmology", "H0") * km_s_Mpc2Hz
    DH = c / H0
    omegaM = conf.getfloat("cosmology", "omegaM")
    omegaLambda = 1 - omegaM

    # get plot config params
    plotTitle = conf.get("plot", "plotTitle")
    yMin = conf.getfloat("plot", "yMin")
    yMax = conf.getfloat("plot", "yMax")
    plotGrid = conf.getboolean("plot", "plotGrid")

    minLimitingDepth = conf.getfloat("plot", "minLimitingDepth")
    maxLimitingDepth = conf.getfloat("plot", "maxLimitingDepth")
    limitingDepthStep = 0.1

    zCutoffs = map(float, conf.get("plot", "zCutoffs").split(","))
    zCutoffs = np.array(list(zCutoffs))
    zColors = list(map(str.strip, conf.get("plot", "zColors").split(",")))
    if len(zCutoffs) != len(zColors):
        raise ValueError("zCutoffs and zColors must have the same length in " +
                         "the configuration file")

    errorEnvelopeAlpha = conf.getfloat("plot", "errorEnvelopeAlpha")
    errorNSigma = conf.getfloat("plot", "errorNSigma")

    # get achievedMedianDepths config params
    sec = "achievedMedianDepths"
    if conf.has_option(sec, "{}-{}Depths".format(survey, f)):
        depths = conf.get(sec, "{}-{}Depths".format(survey, f))
        depths = list(map(float, depths.split(",")))
        labels = conf.get(sec, "{}-{}Labels".format(survey, f))
        labels = list(map(str.strip, labels.split(",")))

        depthNSigma = conf.getint(sec, "{}-{}NSigma".format(survey, f))
        depthLabelXs = conf.get(sec, "{}-{}LabelXs".format(survey, f))
        depthLabelXs = list(map(float, depthLabelXs.split(",")))
        depthLabelYs = conf.get(sec, "{}-{}LabelYs".format(survey, f))
        depthLabelYs = list(map(float, depthLabelYs.split(",")))
    else:
        depths = []
        labels = []
        depthNSigma = 0
        depthLabelXs = []
        depthLabelYs = []

    if not (len(depthLabelXs) == len(depthLabelYs) == len(depths) == len(labels)):
        raise ValueError("The depths, labels, and labelX and labelY arrays " +
                         "must all be the same length in the .conf")

    if debug:
        print('configfile:', configfile)
        print('sections:', config.sections())
        for section_name in config.sections():
            print('Section:', section_name)
            print('Options:', config.options(section_name))
            for name, value in config.items(section_name):
                print('  %s = %s' % (name, value))
        print()


    return
