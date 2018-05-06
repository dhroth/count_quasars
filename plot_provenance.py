
import subprocess

import  matplotlib.pyplot as plt

import config



def plot_provenance():

    # put provenance on the side of the plot
    try:
        gitHash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
    except subprocess.CalledProcessError as e:
        print("You need to be in a git repository in order to put provenance " +
              "information on the plots. Please clone the repository instead " +
              "of downloading the source files directly, and ensure that your " +
              "local git repo hasn't been corrupted")
        exit()
    gitHash = gitHash.decode("utf-8")
    try:
        producer = subprocess.check_output(["git", "config", "user.name"]).strip()
    except subprocess.CalledProcessError as e:
        print("You have not set the git user.name property, which is needed " +
              "to add provenance information on the plots. You can set this " +
              "property globally using the command git config --global " +
              "user.name '<my name>'")
        exit()
    provenance = producer.decode("utf-8") + ", " + gitHash
    provenance += "\n Using {} QLF with k={:2.4f}".format(config.qlfName, config.k)
    plt.figtext(0.93, 0.5, provenance, rotation="vertical",
                verticalalignment="center", alpha=0.7)

    return
