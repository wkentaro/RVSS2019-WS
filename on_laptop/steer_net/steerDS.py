import os.path as osp
import numpy as np
from glob import glob
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import cv2
from glob import glob
from os import path

class SteerDataSet(Dataset):
    
    def __init__(self,root_folder,img_ext = ".jpg" , transform=None):
        self.root_folder = root_folder
        self.transform = transform        
        self.img_ext = img_ext        
        self.filenames = sorted(glob(path.join(self.root_folder,"*" + self.img_ext)))
        self.totensor = transforms.ToTensor()
        
    def __len__(self):        
        return len(self.filenames)
    
    def __getitem__(self,idx):
        img_file = self.filenames[idx]        
        img = cv2.imread(img_file)
        img = img[110:, :, :]
        img = cv2.resize(img, (84, 84))

        if self.transform == None:
            img = self.totensor(img)
        else:
            img = self.transform(img)

        base = osp.splitext(img_file)[0]
        txt_file = base + '.txt'
        with open(txt_file) as f:
            steering = np.float32(f.read())

        # steering = filename.split("/")[-1].split(self.img_ext)[0][6:]
        steering = np.float32(steering)        

        # 11 class classification
        # -0.5, -0.4, -0.3, ... 0, ..., 0.5
        assert -0.5 <= steering <= 0.5
        steering_class = ((steering + 0.5) * 10).round().astype(np.int64)

        sample = {
            "image": img ,
            "steering": steering,
            "steering_class": steering_class,
        }

        return sample


def test():
    transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    ds = SteerDataSet("../dev_data/training_data",".jpg",transform)

    print("The dataset contains %d images " % len(ds))

    ds_dataloader = DataLoader(ds,batch_size=1,shuffle=True)
    for S in ds_dataloader:
        im = S["image"]    
        y  = S["steering"]
        
        print(im.shape)
        print(y)
        break



if __name__ == "__main__":
    test()