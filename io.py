def read_file(fp):
    """
    Returns Dict (photo_id : ( (H,V), set (tags) )
    """
    data = {}

    with open(fp, "r") as f:
        amount = int(f.readline())
        for i in range(amount):
            line = f.readline().split(" ")
            ori = line[0]
            tags = set()
            for tag in line[1:]:
                tags.add(tag)
            data[i] = (ori, tags)
            