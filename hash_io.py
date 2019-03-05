from bitsets import bitset

AMOUNT_TAGS = {"a": 6,
               "b": 840000,
               "c": 2166,
               "d": 220,
               "e": 500}

def read_file(fp):
    """
    Returns Dict (photo_id : ( (H,V), set (tags) )
    """
    data = {}
    lookup = {}

    with open(fp, "r") as f:
        amount = int(f.readline())
        for i in range(amount):
            line = f.readline()[:-1].split(" ")
            ori = line[0]
            tags = set()
            for tag in line[2:]:
                int_tag = lookup.get(tag, len(lookup))
                lookup[tag] = int_tag
                tags.add(int_tag)
            data[i] = (ori, tags)

    print("Data from " + fp + " contains " + str(len(lookup)) + " tags")
            
    return data
    
def print_to_file(output_list, name):
    """
    Prints the output format to file given slides like [[1],[2,4],[3],[5],[10,12]]
    """
    fopen = open(name + ".txt",'w')
    N = len(output_list)
    fopen.write(str(N)+"\n")
    for item in output_list:    
        fopen.write(" ".join(str(x) for x in item)+"\n")
    fopen.close()


if __name__ == "__main__":
    import os

    data_dir = os.path.join(os.path.dirname(__file__), "data")

    for f in os.listdir(data_dir):
        read_file(os.path.join(data_dir, f))