def read_file(fp):
    """
    Returns Dict (photo_id : ( (H,V), set (tags) )
    """
    data = {}

    with open(fp, "r") as f:
        amount = int(f.readline())
        for i in range(amount):
            line = f.readline()[:-1].split(" ")
            print(line)
            ori = line[0]
            tags = set()
            for tag in line[2:]:
                tags.add(tag)
            data[i] = (ori, tags)
            
    return data
    
def print_to_file(output_list):
    fopen = open("result.txt",'w')
    N = len(output_list)
    fopen.write(str(N)+"\n")
    for item in output_list:    
        fopen.write(" ".join(str(x) for x in item)+"\n")
