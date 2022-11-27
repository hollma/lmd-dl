from configparser import ConfigParser

def read_config():
    config = ConfigParser()
    config.read("config.ini")
    return config

def main():
    config = read_config()
    for sec in config.sections():
        print("[", sec, "]", sep="")
        for key in config[sec]:
            print(key, "=", config[sec][key])
        print()

if __name__ == "__main__":
    main()
