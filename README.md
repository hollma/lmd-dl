# lmd-dl
A free and open source download manager for subscribers of the German edition of Le Monde Diplomatique.

## Get lmd-dl

You can clone the repository from Github:
```
git clone https://github.com/hollma/lmd-dl.git
```

## Usage

Firstly, edit `src/config.ini`.
Initially, the config looks like this:

```
[CREDENTIALS]
username = change_me
password = change_me

[FORMATS]
pdf    = yes
pdfz   = yes
epub   = yes
epubt  = yes
ascii  = yes
asciiz = yes
html   = yes
mp3    = yes

[PATHS]
cache_dir  = /path/to/the/cache/directory
output_dir = /path/to/the/output/directory

[DOWNLOAD_OPTIONS]
issue_count = 1
```

Replace `username` and `password` with your credentials.
Moreover, enter valid directory paths in the `PATHS` section.
Modify the remaining options according to your own preferences.

Run `python3 src/lmd-dl.py -h` in order to show the help option.

If everything is set up, run `python3 src/lmd-dl.py` in order to download the most recent issues of 
Le Monde Diplomatique to the cache directory (see `src/config.ini`). 

### TODO
- further processing of the cached files (extract zip files, ...)

## Technical background

