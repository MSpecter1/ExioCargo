import ManifestReader
import os

def modifyGrid(list, filename):
    reader = ManifestReader.manifest_reader()

    path = '../ExioCargo/tests/' + filename + '.txt'
    fileName = os.path.abspath(path)
    # relative paths taken from Nicholas Jones on https://stackoverflow.com/questions/918154/relative-paths-in-python

    reader.set_manifest(fileName)
    containers = reader.read_manifest()

    for c in containers:
        multiplier = ManifestReader.container.getRow(c) + 1
        index = containers.index(c) + (27 * multiplier)
        list[index] = [index, ManifestReader.container.getName(c)]
    
    return list