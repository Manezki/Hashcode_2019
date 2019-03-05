import numpy as np
import torch
import itertools
from tqdm import tqdm
from hash_io import read_file, print_to_file
from os import path as op
from main import create_slideshow, pair_verticals


class NN():
    def __init__(self):
        #torch.device("cpu")

        #self.w_l1 = np.random.rand(7, 3) - 0.5
        #self.b_l1 = np.random.rand(7, 1) - 0.5

        #self.w_l2 = np.random.rand(5, 7) - 0.5
        #self.b_l2 = np.random.rand(5, 1) - 0.5

        #self.w_l3 = np.random.rand(1, 5) - 0.5
        #self.b_l3 = np.random.rand(1, 1) - 0.5

        self.model = torch.nn.Sequential(
            torch.nn.Linear(3, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 8),
            torch.nn.ReLU(),
            torch.nn.Linear(8, 1),
            torch.nn.Sigmoid()
        )

        self.loss_fn = torch.nn.MSELoss()
        self.ln = 1e-5
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.ln)


    def set_metric(self, left, right):
        inter = len(left & right)
        l_out = len(left - right)
        r_out = len(right - left)
        union = inter + l_out + r_out

        X = torch.tensor([[l_out/union, r_out/union, inter/union]])

        return X


    def slideshow_metric(self, slideshow_ids, sets):
        metric = 0
        for i in range(1, len(slideshow_ids)):
            left = slideshow_ids[i - 1]
            right = slideshow_ids[i]
            
            left_set = sets[left][1]
            right_set = sets[right][1]
            
            inter = left_set & right_set
            l_out = left_set - right_set
            r_out = right_set - left_set

            metric += min(len(inter), len(l_out), len(r_out))

        return metric

    def permutations(self, sample):
        
        permutations = list(itertools.permutations(sample))
        ret = set()

        for p in permutations:
            if p[::-1] not in ret:
                ret.add(p)

        return list(ret)

    def train(self, album):

        photo_ids = [k for k, _ in album.items()]

        average = 0

        for i in range(1001):

            sample = np.random.choice(photo_ids, 7, replace=False)

            slideshows = self.permutations(sample)
            
            maximum = -1
            best_ss = None
            for ss in slideshows:
                m = self.slideshow_metric(ss, album)
                if m > maximum:
                    maximum = m
                    best_ss = ss
            
            # Skip training, when maximum is 0
            if maximum == 0:
                continue

            paired = [self.set_metric(album[best_ss[i-1]][1], album[best_ss[i]][1]) for i in range(1, len(ss))]
            X = torch.stack(paired, dim=0)

            pred = self.model(X).sum()

            #print(maximum)
            #print(pred)
            loss = self.loss_fn(pred, torch.tensor([maximum], dtype=torch.float))
            #print(loss)

            self.model.zero_grad()
            loss.backward()

            #print(f"Loss after iter {i} was {loss.item()}")

            average += loss.item()
            if i % 100 == 0:
                print(f"Average over last 100 iterations: {average/100}")
                average = 0

            self.optimizer.step()


    def pred(self, left, right):
        X = self.set_metric(left, right)
        pred = self.model(X)
        return pred.item()


    def fitness(self, left, right):
        inter = len(left & right)
        l_out = len(left - right)
        r_out = len(right - left)
        union = inter + l_out + r_out

        X = np.array([[l_out/union], [r_out/union], [inter/union]])

        return X




def adapt_for_album(album):
    assert hasattr(album, iter), "Need to be iterable"

    
if __name__ == "__main__":
    nn = NN()

    FN = "d_pet_pictures.txt"
    FN = "c_memorable_moments.txt"
    data = read_file(op.join(op.dirname(__file__), "data", FN))
    nn.train(data)

    horizontals = [k for k, v in data.items() if v[0] == "H"]
    verticals = [k for k, v in data.items() if v[0] == "V"]

    ver_data = {}
    for k, v in data.items():
        if v[0] == "V":
            ver_data[k] = v

    if len(ver_data) != 0:
        ver_data, ver_pairing = pair_verticals(ver_data)
        
        # Update data dict
        for k, v in ver_data.items():
            data[k] = v

    ss = create_slideshow(horizontals, [k for k, _ in ver_data.items()], data, ver_pairing, nn.pred)

    res = []

    ver_set = set([k for k, v in ver_data.items()])

    for s in ss:
        if s in ver_set:
            res.append([s, ver_pairing[s]])
        else:
            res.append([s])

    print_to_file( res, FN[:-4] + "_result_nn" )
