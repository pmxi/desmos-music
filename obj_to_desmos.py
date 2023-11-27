import argparse
import json

parser = argparse.ArgumentParser(description='Converts a .obj file to a Desmos graph.')
parser.add_argument('obj_file', metavar='obj_file', type=str, help='Path to the .obj file to convert')


args = parser.parse_args()

# get file
obj_file = open(args.obj_file, 'r')
# write as with statement
v = []
f = []
with open(args.obj_file + '.desmos', 'w') as desmos_file:
    # make list of vertexes with format [x, y, z] and faces
    # only use vertex coordinate ignore texture and normal
    for line in obj_file:
        if line[0] == 'v':
            v.append([float(x) for x in line.split()[1:]])
        elif line[0] == 'f':
            f.append([float(x.split('/', 1)[0]) for x in line.split()[1:]])

# print json of vertexes and faces for desmos table
a = ([
    {
        "columns": [
            {"latex": "v_{x}", "values": [x[0] for x in v]},
            {"latex": "v_{y}", "values": [x[1] for x in v]},
            {"latex": "v_{z}", "values": [x[2] for x in v]}
        ],
        "type": "table"
    },
    {
        'columns': [
            {'latex': 'f_{1}', 'values': [x[0] for x in f]},
            {'latex': 'f_{2}', 'values': [x[1] for x in f]},
            {'latex': 'f_{3}', 'values': [x[2] for x in f]}
        ],
        'type': 'table'
    }
])
print(json.dumps(a))

# create new file and write to ti

desmos_file = open(args.obj_file + '.desmos.txt', 'w')
desmos_file.write(json.dumps(a))
desmos_file.close()


