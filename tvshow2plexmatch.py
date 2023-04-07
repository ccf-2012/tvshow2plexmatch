import os
import argparse
import xml.etree.ElementTree as ET


def uselessFile(entryName):
    return entryName in ['@eaDir', '.DS_Store', '.@__thumb']

def tryint(instr):
    try:
        string_int = int(instr)
    except ValueError:    
        string_int = 0
    return string_int


def mkPlexMatch(targetDir, tmdbid, title, year):
    pmfilepath = os.path.join(targetDir, '.plexmatch')
    with open(pmfilepath, "w") as pmfile:
        pmfile.write("Title: %s\ntmdbid: %s\n" %
                    (title, tmdbid))
        intyear = tryint(year)
        if intyear > 1990:
            pmfile.write("Year: %s\n" % (year))


def make_plexmatch_from_tvshow_nfo(root_dir):
    for index, dirname in enumerate(os.listdir(root_dir)):
        if uselessFile(dirname):
            continue

        dirpath = os.path.join(root_dir, dirname)
        if os.path.isdir(dirpath):
            nfo_found = False
            for subfile in os.listdir(dirpath):
                if os.path.isdir(os.path.join(dirpath, subfile)):
                    # print(f"{subfile} skip")
                    continue

                if subfile.endswith('.nfo'):
                    nfo_path = os.path.join(dirpath, subfile)

                    tree = ET.parse(nfo_path)
                    root = tree.getroot()

                    tmdb_elem = root.find('tmdbid')
                    year_elem = root.find('year')
                    title_elem = root.find('title')
                    if tmdb_elem.text is not None:
                        nfo_found = True
                        print(f"{index} : {tmdb_elem.text}, {title_elem.text} ({year_elem.text})")
                        mkPlexMatch(dirpath, tmdb_elem.text, title_elem.text, year_elem.text)
                        break
            if not nfo_found:
                print(f"{index} : {dirname} tmdbid not found")


def loadArgs():
    global ARGS
    parser = argparse.ArgumentParser(description='read tvshow.nfo and generate .plexmatch file.')
    parser.add_argument('dir', help='folder path.')
    ARGS = parser.parse_args()
    ARGS.dir = os.path.expanduser(ARGS.dir)


def main():
    loadArgs()
    make_plexmatch_from_tvshow_nfo(ARGS.dir)


if __name__ == '__main__':
    main()
