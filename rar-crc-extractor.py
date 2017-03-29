import os
import subprocess
import sys
import re
import glob


def clean_line(line):
    return str(line).strip("\r\n *")


crcs = {} # empty dictionary
cleaned_rar_filenames = set() # set cannot have duplicate items

password = ""

if sys.argv[1] == "-p":
    use_password = True
    password = sys.argv[2]
    command_line_filenames = sys.argv[3:]
else:
    use_password = False
    command_line_filenames = sys.argv[1:]

for rar_filename in command_line_filenames:
    for real_rar_filename in glob.glob(rar_filename):
        real_rar_filename = os.path.abspath(real_rar_filename)
        multi_part_match = re.search(r"^(.*)part(\d+)\.rar$", real_rar_filename)
        if multi_part_match:
            filename_without_part = multi_part_match.group(1)
            part_number = multi_part_match.group(2)

            # skip this rar if any other part of it has already been added to cleaned_rar_filenames
            skip = False
            for cleaned_rar_filename in cleaned_rar_filenames:
                if str.startswith(cleaned_rar_filename, filename_without_part):
                    skip = True
                    break
            if skip:
                continue

        cleaned_rar_filenames.add(real_rar_filename)

for rar_filename in cleaned_rar_filenames:
    if use_password:
        p = subprocess.Popen(["unrar", "v", "-v", "-p" + password, rar_filename], stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(["unrar", "v", "-v", rar_filename], stdout=subprocess.PIPE)

    lines = p.stdout.readlines()

    # -v operator lists all parts even if just one part was given (like in this case)
    # each part output is enclosed in 79 hyphens (-----)
    # find text between those hyphens and put is into a rar_infos list
    rar_infos = [] # empty list

    one_rar_info = [] # empty list
    line_started = False
    for line in lines:
        line = clean_line(line)
        if re.match(r"-{79}", line):
            if not line_started:
                line_started = True
            else:
                rar_infos.append(one_rar_info)
                one_rar_info = [] # empty list
                line_started = False

        elif line_started:
            one_rar_info.append(line)

    for rar_info in rar_infos:
        for line_no in range(0, len(rar_info), 2):
            info_filename = rar_info[line_no]
            info_items = rar_info[line_no + 1].split()

            info_crc = info_items[len(info_items) - 3] # third last item is crc
            info_attr = info_items[len(info_items) - 4] # forth last item is attr
            info_ratio = info_items[len(info_items) - 7] # seventh last item is attr

            # ignore directories in rar
            # on windows they have attr of ".D....."
            if info_attr == ".D.....":
                continue

            # only take crc from entries, that have a ratio of
            #   "<number>%" (means: this file is only part of this archive -> this archive has the correct crc)
            # or
            #   "<--" (means: this file ends in this archive part -> this archive has the correct crc)
            if info_ratio == "<--" or re.match(r"\d+%", info_ratio):
                crcs[info_filename] = info_crc

max_filename_length = -1
for filename in crcs:
    max_filename_length = max(len(filename), max_filename_length)

for filename in sorted(crcs):
    print(filename.ljust(max_filename_length) + " " + crcs[filename])
