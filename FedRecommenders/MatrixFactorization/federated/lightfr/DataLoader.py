import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader as TDataLoader



class DataLoaderCenter():
    def __init__(self, configs, val_data):
        self.configs = configs
        self.val_data= val_data


    def get_val_dataloader(self):

        users, books, labels = torch.LongTensor(np.array(self.val_data.iloc[:, [0]], dtype='int32')), torch.LongTensor(np.array(self.val_data.iloc[:, [1]], dtype='int32')),torch.FloatTensor(np.array(self.val_data.iloc[:, [2]], dtype='float32'))

        dataset = UserItemRatingDataset(user_tensor=users, book_tensor=books, target_tensor=labels)

        data_len = self.configs['num_negative_test'] + 1

        return TDataLoader(dataset, batch_size=data_len, shuffle=False)

 

class UserItemRatingDataset(Dataset):
    """Wrapper, convert <user, item, rating> Tensor into Pytorch Dataset"""

    def __init__(self, user_tensor, book_tensor, target_tensor):
        self.user_tensor = user_tensor
        self.book_tensor = book_tensor
        self.target_tensor = target_tensor

    def __getitem__(self, index):
        return self.user_tensor[index], self.book_tensor[index], self.target_tensor[index]

    def __len__(self):
        return self.user_tensor.size(0)
