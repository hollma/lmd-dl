from configparser import ConfigParser
from argparse import ArgumentParser
import requests
from bs4 import BeautifulSoup
import pprint
import os
from zipfile import ZipFile


FILETYPES = {"pdf"    : "Download LMD as pdf",
             "pdfz"   : "Download LMD as pdf (zipped)",
             "epub"   : "Download LMD as epub",
             "epubt"  : "Download LMD as epub (text-only)",
             "ascii"  : "Download LMD as txt",
             "asciiz" : "Download LMD as txt (zipped)",
             "html"   : "Download LMD as html (zipped)",
             "mp3"    : "Download LMD as mp3 (zipped)"
             }

ZIPPED = ["html", "mp3"]

DEBUG = False


def read_config():
    config = ConfigParser()
    config.read("config.ini")
    return config


def initialize_config_variables():
    config = read_config()

    parser = ArgumentParser(
        prog = "lmd-dl",
        description = "A free and open source download manager for subscribers of the German edition of Le Monde Diplomatique.",
        epilog="Get the most recent version at https://github.com/hollma/lmd-dl."
    )

    group = parser.add_argument_group("Authentication information")
    group.add_argument("--username", default=config["CREDENTIALS"]["username"], help="Your username")
    group.add_argument("--password", default=config["CREDENTIALS"]["password"], help="Your password")

    group = parser.add_argument_group("Supported filetypes")
    for filetype, helpmsg in FILETYPES.items():
        group.add_argument("--{}".format(filetype), action="store_true", help=helpmsg)

    group = parser.add_argument_group("Download options")
    group.add_argument("-c", "--count", type=int, default=config["DOWNLOAD_OPTIONS"]["issue_count"], help="Download the <count> most recent issues of Le Monde Diplomatique.")

    args = parser.parse_args()
    arguments_dict = vars(args)

    # if any filetype CLI argument is passed, they overwrite the config.ini entries (missing filetypes default to False)
    filetype_arg_values = [v for k, v in arguments_dict.items() if k in FILETYPES.keys()]
    if any(filetype_arg_values):
        for k, v in arguments_dict.items():
            if k in FILETYPES.keys():
                if v:
                    config["FORMATS"][k] = "yes"
                else:
                    config["FORMATS"][k] = "no"

    # if credentials are passed as CLI arguments, they overwrite the config.ini entries
    config["CREDENTIALS"]["username"] = arguments_dict["username"]
    config["CREDENTIALS"]["password"] = arguments_dict["password"]

    config["DOWNLOAD_OPTIONS"]["issue_count"] = str(arguments_dict["count"])
    return config


def get_url(filetype):
    return "https://dl.monde-diplomatique.de/{}".format(filetype)


def get_filenames(filetype):
    url = get_url(filetype) + "/" + "list"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")

    filenames = [li.find("a").get("href").split("/")[-1] for li in soup.find_all("li")]

    return filenames


def download_file(filetype, filename, username, password):
    download_url = get_url(filetype)
    data = {"name" : username,
            "password" : password,
            "id" : filename,
            "Laden" : "+Laden+",
            "year" : ""}

    response = requests.post(download_url, data = data)
    # Keep in mind that there is no check whether the right file was actually downloaded.
    # We assume that response.content contains the requested file.
    return response.content


def main():
    config = initialize_config_variables()

    if DEBUG:
        for sec in config.sections():
            print("[", sec, "]", sep="")
            for key in config[sec]:
                print(key, "=", config[sec][key])
            print()

    filenames = {}
    for filetype in FILETYPES.keys():
        filenames[filetype] = get_filenames(filetype)

    if DEBUG:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(filenames)

    username = config["CREDENTIALS"]["username"]
    password = config["CREDENTIALS"]["password"]
    issue_count = int(config["DOWNLOAD_OPTIONS"]["issue_count"])

    for filetype in FILETYPES.keys():
        if config["FORMATS"].getboolean(filetype):
            from_old_to_new_filenames = filenames[filetype][0:issue_count]
            from_old_to_new_filenames.reverse()

            for current_filename in from_old_to_new_filenames:
                print("Downloading", current_filename, "...")
                myfile = download_file(filetype, current_filename, username, password)
                subdir = os.path.join(config["PATHS"]["cache_dir"], filetype)
                os.makedirs(subdir, exist_ok=True)
                with open(os.path.join(subdir, current_filename), 'wb') as f:
                    f.write(myfile)

                if filetype in ZIPPED:
                    with ZipFile(os.path.join(subdir, current_filename), 'r') as zObject:
                        zObject.extractall(subdir)


if __name__ == "__main__":
    main()
