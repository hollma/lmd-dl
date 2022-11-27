from configparser import ConfigParser
from argparse import ArgumentParser
import requests


FILETYPES = {"pdf"    : "Download LMD as pdf",
             "pdfz"   : "Download LMD as pdf (zipped)",
             "epub"   : "Download LMD as epub",
             "epubt"  : "Download LMD as epub (text-only)",
             "ascii"  : "Download LMD as txt",
             "asciiz" : "Download LMD as txt (zipped)",
             "html"   : "Download LMD as html (zipped)",
             "mp3"    : "Download LMD as mp3 (zipped)"
             }
DEBUG = True
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

    return config

def get_url(filetype):
    return "https://dl.monde-diplomatique.de/{}".format(filetype)

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

    # TODO: build the correct URLs for all requested filetypes and dates
    # this is just a dummy implementation
    filetype = "pdf"
    filename = "lmd_2022_11_10.113503.pdf"
    username = config["CREDENTIALS"]["username"]
    password = config["CREDENTIALS"]["password"]

    myfile = download_file(filetype, filename, username, password)
    with open(config["PATHS"]["cache_dir"] + "/" + filename , 'wb') as f:
        f.write(myfile)


if __name__ == "__main__":
    main()
