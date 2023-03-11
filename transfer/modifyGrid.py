import ManifestReader

def modifyGrid(list, filename):
    reader = ManifestReader.manifest_reader()

    reader.set_manifest("transfer\\" + filename + ".txt")
    containers = reader.read_manifest()

    for c in containers:
        multiplier = ManifestReader.container.getRow(c) + 1
        index = containers.index(c) + (27 * multiplier)
        list[index] = [index, ManifestReader.container.getName(c)]
    
    return list

    # for c in containers:
        # ManifestReader.container.display_info(c)