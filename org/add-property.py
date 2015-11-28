import sys

# For each properties drawer, add the spec'd property if it isn't there.

def add_property(drawer_lines, new_property):
    # Given list of property drawer lines, sort and add in new property
    # first check to see this is necessary...
    for line in drawer_lines:
        if ":" + new_property + ":" in line:
            return drawer_lines
    
    # strip first and last lines (":PROPERTIES:" and ":END:")
    drawer_lines = drawer_lines[1:-1]
    # add on new property and sort
    drawer_lines.append(":" + new_property + ": 0\n")
    return [":PROPERTIES:\n"] + sorted(drawer_lines) + [":END:\n"]

file_name = sys.argv[1]
property_name = sys.argv[2]
output_name = file_name.split(".")[0] + "-out." + file_name.split(".")[1]
with open(file_name) as f:
    output_lines = []
    drawer = []
    for line in f:
        if drawer != [] or ":PROPERTIES:" in line:
            drawer.append(line)            
        else:
            output_lines.append(line)

        # if reached end of drawer, add new property and save
        if ":END:" in line:
            output_lines.extend(add_property(drawer, property_name))
            drawer = []

    # save the modified file
    with open(output_name, 'w') as out:
        out.write("".join(output_lines))
