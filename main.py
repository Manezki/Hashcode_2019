from hash_io import read_file, print_to_file
from os import path as op
from tqdm import tqdm
from bitsets import bitset
import random

def metric(left, right):
    inter = left & right
    l_out = left - right
    r_out = right - left
    return min(len(inter), len(l_out), len(r_out))


def jaccard(left, right):
    inter = left & right
    total = left | right
    return len(inter)/len(total)

def combine_verticals(verticals):
    """
    Returns: VxV table of sets. V[0,1] is the union of tags from photos 0,1
    """
    size = len(verticals)
    data = [[set() for i in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(i):
            data[i][j] |= verticals[i][1] | verticals[j][1]
    
    return data


def pair_verticals(verticals):

    photos = [k for k, _ in verticals.items()]

    size = len(photos) if len(photos)%2 == 0 else len(photos) - 1

    left = photos[:int(size/2)]
    right = photos[int(size/2):]

    random.shuffle(left)
    random.shuffle(right)

    paired = {}
    pairing = {}

    for i in range(len(left)):
        ls = verticals[left[i]][1]
        rs = verticals[right[i]][1]

        combined = ls | rs
        paired[left[i]] = ("V", combined)
        pairing[left[i]] = right[i]
    
    return paired, pairing



if __name__ == "__main__":
    #FN = "b_lovely_landscapes.txt"
    FN = "d_pet_pictures.txt"
    #FN = "c_memorable_moments.txt"
    #FN = "a_example.txt"
    #data = read_file(op.join(op.dirname(__file__), "data", "a_example.txt"))
    #data = read_file(op.join(op.dirname(__file__), "data", "c_memorable_moments.txt"))
    #data = read_file(op.join(op.dirname(__file__), "data", FN))
    data = read_file(op.join(op.dirname(__file__), "data", FN))
    

    reverse_lookup = {}
    universe = set()
    #print(data)

    for k, v in data.items():
        for tag in v[1]:
            photos = reverse_lookup.get(tag, set())
            photos.add(k)
            reverse_lookup[tag] = photos
        universe |= v[1]
    
    print("Reverse lookup done")
    #universe = bitset("universe", tuple(universe))

    horizontals = [k for k, v in data.items() if v[0] == "H"]
    verticals = [k for k, v in data.items() if v[0] == "V"]

    # VxV table lower-triangle, [row][col]
    #vertical_pairs = combine_verticals([(k, v[1]) for k, v in data.items() if v[0] == "V"])
    #print(vertical_pairs)

    ver_data = {}
    for k, v in data.items():
        if v[0] == "V":
            ver_data[k] = v

    if len(ver_data) != 0:
        ver_data, ver_pairing = pair_verticals(ver_data)
    ver_set = set([k for k, _ in ver_data.items()])
    
    reserve = set(horizontals)
    reserve |= ver_set
    used = set()

    if len(horizontals) == 0:
        slideshow = [random.choice(list(ver_set))]
    else:
        slideshow = [random.choice(horizontals)]
    reserve -= set([slideshow[-1]])
    used |= set([slideshow[-1]])
    used |= set([r for l, r in ver_pairing.items()])

    # TODO Stop if current value better than achievable
    for _ in tqdm(range(len(reserve))):
        current = slideshow[-1]
        argmax = (None, -1)

        cur_tags = data[current][1]
        candidates = set()

        for t in cur_tags:
            candidates |= reverse_lookup[t]
            if len(candidates) > 1000:
                break

        candidates -= used
    
        if len(candidates) == 0:
            argmax = (random.choice(list(reserve)), -1)
            
            slideshow.append(argmax[0])
            reserve -= set([argmax[0]])
            used |= set([slideshow[-1]])
            continue

        for photo in candidates:
            #value = (0.33 - jaccard(data[current][1], data[photo][1]))**2
            value = metric(data[current][1], data[photo][1])
            if value > argmax[1]:
                argmax = (photo, value)
        
        slideshow.append(argmax[0])
        reserve -= set([argmax[0]])
        used |= set([slideshow[-1]])
    
    print(slideshow)

    res = []

    for s in slideshow:
        if s in ver_set:
            res.append([s, ver_pairing[s]])
        else:
            res.append([s])

    print_to_file( res, FN[:-4] + "_result" )
