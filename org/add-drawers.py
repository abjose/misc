import sys

# Add a properties drawer to every project.

# change these
properties_drawer = """:PROPERTIES:
:business-y:  0
:complexity:  0
:cost:        0
:interesting: 0
:priority:    0
:started:     C-c-!
:time:        0
:END:
"""

file_name = sys.argv[1]
output_name = file_name.split(".")[0] + "-out." + file_name.split(".")[1]
with open(file_name) as f:
    output_lines = []
    was_header = False
    for line in f:
        # If previous line was a header and this isn't a properties drawer, add.
        if was_header and ":PROPERTIES:" not in line:
            output_lines.append(properties_drawer)
        # Remember if we find a header.
        was_header = len(line.strip()) > 0 and line.strip()[0] == "*"
        output_lines.append(line)

    # just in case...
    if was_header: output_lines.append(properties_drawer)
        
    # save the modified file
    with open(output_name, 'w') as out:
        out.write("".join(output_lines))
