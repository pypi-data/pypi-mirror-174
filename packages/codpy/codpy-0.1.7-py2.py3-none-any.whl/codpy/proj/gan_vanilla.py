import os
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms
from torchvision.utils import save_image

import numpy as np
from matplotlib.pyplot import imshow, imsave
#%matplotlib inline
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from preamble import *

def get_gan_params():

    kwargs = {
    'rescale_kernel':{'max': 2000, 'seed':42},
    'discrepancy:xmax':500,
    'discrepancy:ymax':500,
    'discrepancy:zmax':500,
    'discrepancy:nmax':1000,
    # 'set_codpy_kernel': kernel_setters.kernel_helper(kernel_setters.set_linear_regressor_kernel, 2,1e-8,map_setters.set_unitcube_map),
    # 'set_codpy_kernel': kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 0,0 ,map_setters.set_standard_mean_map),
    # 'set_codpy_kernel': kernel_setters.kernel_helper(kernel_setters.set_sumnorm_kernel, 0,0,map_setters.set_unitcube_map),
    # 'set_codpy_kernel': kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 0,0,map_setters.set_unitcube_map),
    'set_codpy_kernel': kernel_setters.kernel_helper(kernel_setters.set_matern_norm_kernel, 0,1e-8 ,map_setters.set_standard_mean_map),
    # 'set_codpy_kernel': kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0,0 ,map_setters.set_standard_min_map),
    # 'set_codpy_kernel': kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0,0 ,map_setters.set_standard_min_map),
    # 'random_sample':lambda size: np.random.normal(size=size),
    'rescale':True,
    'grid_projection':True,
    'D':784,
    'Nx':-1,
    'Ny':500,
    'Nz':100,
    'get_proba':True,
    'reordering':True,
    'seed':42,
    'distance':'norm1',
    'nablainv':False
    }
    return kwargs


def get_MNIST_data_loader(batch_size, **kwargs):
    data_short = kwargs.get('data_short', True)
    transform = transforms.Compose([transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])])
    if data_short:
        mnist = datasets.MNIST(root='../data/', train=False, transform=transform, download=True)
    else:
        mnist = datasets.MNIST(root='../data/', train=True, transform=transform, download=True)
    data_loader = DataLoader(dataset=mnist, batch_size=batch_size, shuffle=True, drop_last=True)
    return data_loader

class MNIST_GAN_data_generator(data_generator):
    tfx, tffx, tfz, tffz = [],[],[],[]
    def pre(img):
        import numpy.linalg as la
        # return img / la.norm(img)
        return img
    def get_data(self,D=0,Nx=0,Ny=0,Nz=0,**kwargs):
        if (len(self.tfx)*len(self.tfz) == 0):
            import tensorflow as tf
            (self.tfx, self.tffx), (self.tfz, self.tffz) = tf.keras.datasets.mnist.load_data()
            self.tfx, self.tfz = self.tfx.reshape(len(self.tfx),-1), self.tfz.reshape(len(self.tfz),-1)
            x,fx,y,fy,z,fz = self.tfx.copy(), np.ones(self.tfx.shape[0]), self.tfx.copy(), self.tffx.copy(),self.tfz.copy(), np.ones(self.tfz.shape[0])
            x,y,z = MNIST_GAN_data_generator.pre(x),MNIST_GAN_data_generator.pre(x),MNIST_GAN_data_generator.pre(z)
        return (self.tfx.copy(), np.ones(self.tfx.shape[0]), self.tfx.copy(), np.ones(self.tfx.shape[0]),self.tfz.copy(), np.ones(self.tfz.shape[0]))

    def update(self,z,fz):
        self.z = z
        # self.x = np.concatenate([self.x,z],axis=0)
        # self.fx = np.concatenate([self.fx,fz],axis=0)
        self.Ny = self.y.shape[0]
        self.Nz = self.z.shape[0]
        self.Nx = self.x.shape[0]
        self.D = self.x.shape[1]
        self.Df = get_matrix(self.fx).shape[1]

    def copy(self):
        return self.copy_data(MNIST_GAN_data_generator())


def kernel_image_generator(kwargs = get_gan_params()):
    MNIST_data_generator_ = MNIST_GAN_data_generator(**kwargs)
    # MNIST_data_generator_.z,x,z = alg.sampler(fx= MNIST_data_generator_.x, M = MNIST_data_generator_.Nz, distance = 'norm22', **kwargs)
    MNIST_data_generator_.z,x,y,z = alg.sampler(fx= MNIST_data_generator_.x, M = MNIST_data_generator_.Nz, **kwargs)
    MNIST_data_generator_.update(z = MNIST_data_generator_.z,fz = np.zeros(MNIST_data_generator_.z.shape[0]))
    MODEL_NAME = kwargs.get('MODEL_NAME', 'CoDpy')
    # MNIST_data_predictor_ = codpyprClassifier(**kwargs).set_data(generator = MNIST_data_generator_,**kwargs)
    N,D = int(np.sqrt(MNIST_data_generator_.Nz)),int(np.sqrt(MNIST_data_generator_.D))
    f_z = np.reshape(MNIST_data_generator_.z, (MNIST_data_generator_.Nz,D,D))
    def filter(img):
            import numpy.linalg as la
            # img = ( img-np.min(img) ) / (np.max(img)-np.min(img))
            # f1 = lambda x:  np.tanh(x)
            # f1 = lambda x:  np.power(x,2)
            # img = f1(img)
            # from skimage import img_as_uint
            # img = img_as_uint( img > 0.5 )
            # img /= la.norm(img)
            return img
    def tiles(x,filter = None):
        N,D = int(np.sqrt(x.shape[0])),int(np.sqrt(x.shape[1]))
        if filter is not None: 
            for n in range(N*N): x[n] = filter(x[n]) 
        img = np.zeros([N*N, D,D])
        for j in range(N*N): img[j] = x[j].reshape((D,D))
        out = np.zeros([N*D, N*D])
        for j in range(N): 
            for k in range(N): out[j*D:(j+1)*D,k*D:(k+1)*D] = img[j*N+k]
        return out
    imx = tiles(MNIST_data_generator_.x[:100],filter=filter)
    imfz = tiles(MNIST_data_generator_.z,filter=filter)
    # imshow(imx, cmap='gray')
    # imshow(imfz, cmap='gray')
    # imsave('samples/{}_Ny{}.jpg'.format(MODEL_NAME, str(MNIST_data_generator_.Ny).zfill(5)), imfz, cmap='gray')
    return {'imx':imx,'imfz':imfz}
    pass


class Discriminator(nn.Module):
    def __init__(self, input_size=784, num_classes=1):
        super(Discriminator, self).__init__()
        self.layer = nn.Sequential(
            nn.Linear(input_size, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, num_classes),
            nn.Sigmoid(),
        )
    
    def forward(self, x):
        y_ = x.view(x.size(0), -1)
        y_ = self.layer(y_)
        return y_

class Generator(nn.Module):
    def __init__(self, input_size=100, num_classes=784):
        super(Generator, self).__init__()
        self.layer = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 512),
            nn.BatchNorm1d(512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 1024),
            nn.BatchNorm1d(1024),
            nn.LeakyReLU(0.2),
            nn.Linear(1024, num_classes),
            nn.Tanh()
        )
        
    def forward(self, x):
        y_ = self.layer(x)
        y_ = y_.view(x.size(0), 1, 28, 28)
        return y_

class vanilla_gan():
    def __init__(self, n_noise, DEVISE = None) -> None:
        if DEVICE is None:
            self.DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.DEVICE = DEVICE
        self.D = Discriminator().to(self.DEVICE)
        self.G = Generator(n_noise).to(self.DEVICE)
        self.n_noise = n_noise
        
    def fit(self, data_loader, batch_size, **kwargs):
        step = kwargs.get('step',0)
        seed = kwargs.get('seed',None)
        if seed is not None:
            torch.manual_seed(seed)
        # n_critic = kwargs.get('n_critic', 1)
        max_epoch = kwargs.get('max_epoch',50)
        MODEL_NAME = kwargs.get('MODEL_NAME', 'VanillaGAN')
        D_labels = torch.ones(batch_size, 1).to(self.DEVICE) # Discriminator label to real
        D_fakes = torch.zeros(batch_size, 1).to(self.DEVICE) # Discriminator label to fake
        D_opt = torch.optim.Adam(self.D.parameters(), lr=0.0002, betas=(0.5, 0.999))
        G_opt = torch.optim.Adam(self.G.parameters(), lr=0.0002, betas=(0.5, 0.999))
        criterion = nn.BCELoss()

        for epoch in range(max_epoch):
            for _, (images, _) in enumerate(data_loader):
                ## Training Discriminator
                x = images.to(self.DEVICE)
                x_outputs = self.D(x)
                D_x_loss = criterion(x_outputs, D_labels)

                z = torch.randn(batch_size, self.n_noise).to(self.DEVICE)
                z_outputs = self.D(self.G(z))
                D_z_loss = criterion(z_outputs, D_fakes)
                D_loss = D_x_loss + D_z_loss
                self.D.zero_grad()
                D_loss.backward()
                D_opt.step()

                #if step % n_critic == 0:
                ## Training Generator
                z = torch.randn(batch_size, self.n_noise).to(self.DEVICE)
                z_outputs = self.D(self.G(z))
                G_loss = criterion(z_outputs, D_labels)
                self.G.zero_grad()
                G_loss.backward()
                G_opt.step()


                if step % 1000 == 0:
                    print('Epoch: {}/{}, Step: {}, D Loss: {}, G Loss: {}'.format(epoch, max_epoch, step, D_loss.item(), G_loss.item()))
                    self.G.eval()
                    img = get_sample_images(self.G, self.n_noise, **kwargs)
                    imsave('samples/{}_steps{}.jpg'.format(MODEL_NAME, str(step).zfill(3)), img, cmap='gray')
                    self.G.train()
                step += 1
        return self.G


def get_sample_images(G, n_noise, **kwargs):
    """
        The function outputs n_noise images
    """
    seed = kwargs.get('seed',None)
    if seed is not None:
        torch.manual_seed(seed)
    z = torch.randn(n_noise, n_noise).to(DEVICE)
    y_hat = G(z).view(n_noise, 28, 28)
    result = y_hat.cpu().data.numpy()
    img = np.zeros([280, 280])
    for j in range(10):
        img[j*28:(j+1)*28] = np.concatenate([x for x in result[j*10:(j+1)*10]], axis=-1)
    return img


if __name__ == "__main__":
    if not os.path.exists('samples'):
        os.makedirs('samples')
    kwargs = get_gan_params()
    kernel_image_generator(kwargs)
    for n in range(1,10):
        kwargs['Ny'] = n*100
        # kwargs['Nx'] = n*100
        kernel_image_generator(kwargs)
    n_noise = 100
    batch_size = 64
    data_loader = get_MNIST_data_loader(batch_size)
    gan = vanilla_gan(n_noise)
    G = gan.fit(data_loader, batch_size,**get_gan_params()).eval()
    imshow(get_sample_images(G, n_noise), cmap='gray')
    pass


