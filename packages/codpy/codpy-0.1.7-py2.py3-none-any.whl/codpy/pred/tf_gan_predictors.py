import numpy as np
from matplotlib import pyplot as plt
import os, sys
import time 
import numpy as np
from pathlib import Path
parent_path = os.path.dirname(__file__)
parent_path = os.path.dirname(parent_path)
if parent_path not in sys.path: sys.path.append(parent_path)
from include import *
from codpy_tools import *
from stat_tools import *
from data_generators import * 
from predictors import * 
from scikit_tools import * 
from mnist_codpy import * 
from time_series import*
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense, Dropout, LeakyReLU, Flatten
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model


def mean_squared_error(data):
  mse=0
  for X_batch, y_batch in data:
    mse += np.mean(np.square(X_batch[:, -1, 3:4]-y_batch[:, 3:4]))
  mse /= len(data)
  return mse

def mse(y_true, y_pred):
  return tf.reduce_mean(tf.square(y_true[:,3]-y_pred[:,3]))
def mae(y_true, y_pred):
    return tf.reduce_mean(tf.keras.backend.abs((y_true[:,3]-y_pred[:,3])))
def mape(y_true, y_pred):
    return tf.reduce_mean(tf.keras.backend.abs((y_true[:,3]-y_pred[:,3])/y_true[:,3]))
def rmse(y_true, y_pred):
    return tf.sqrt(tf.reduce_mean(tf.square(y_true[:,3]-y_pred[:,3])))
def ar(y_true, y_pred):
    mask = tf.cast(y_pred[1:,3] > y_true[:-1,3],tf.float32)
    return tf.reduce_mean((y_true[1:,3]-y_true[:-1,3])*mask)


class data_gan_generator(data_generator):
    def get_data(self,D=0,Nx=0,Ny=0,Nz=0,**kwargs):
      import yfinance as yf
      AC = kwargs.get("AC", False)
      data = yf.download('SPY', start='2021-05-01', end='2022-05-03')
      df=self.add_MA(data)
      xfx, zfz = train_test_split(df, **kwargs)
      return  xfx, zfz 
    def add_MA(self, dataframe):
      Ma_window=5
      for i in range(0,dataframe.shape[0]-Ma_window):
        dataframe.loc[dataframe.index[i+Ma_window],'Ma'] = np.round(((dataframe.iloc[i,4]+ dataframe.iloc[i+1,4] +dataframe.iloc[i+2,4] + dataframe.iloc[i+3,4]+ dataframe.iloc[i+4,4])/5),6)
      return dataframe[5:-5]
    def copy(self):
        return self.copy_data(data_gan_generator())

def train_test_split(dataframe, **kwargs):
  n_sequence = kwargs.get('n_sequence',5)
  n_features =  kwargs.get('n_features',7)
  n_batch =  kwargs.get('batch_size',32)

  data = dataframe.to_numpy() #.drop(columns='Date').to_numpy()
  targets = data
  n_samples = data.shape[0]
  train_test_split=int(n_samples*0.9)
  xfx = Standarized_TimeseriesGenerator(data, targets,
                                length=n_sequence, sampling_rate=1,
                                stride=1, batch_size=n_batch,
                                start_index = 0,
                                end_index = train_test_split,
                                shuffle = True)
  zfz = Standarized_TimeseriesGenerator(data, targets,
                                length=n_sequence, sampling_rate=1,
                                stride=1, batch_size=n_batch,
                                start_index = train_test_split,
                                end_index = n_samples-1)

  return xfx, zfz

class get_GAN_models():
    def __init__(self, **kwargs):
      self.n_sequence = kwargs.get('n_sequence',5)
      self.n_features =  kwargs.get('n_features',7)
    def make_generator_model(self):
      inputs = Input(shape=(self.n_sequence, self.n_features,))
      lstm_1 = LSTM(units=10, return_sequences = True, activation=None, kernel_initializer='random_normal')(inputs)
      batch_norm1=tf.keras.layers.BatchNormalization()(lstm_1)
      lstm_1_LRelu = LeakyReLU(alpha=0.3)(batch_norm1) 
      lstm_1_droput = Dropout(0.3)(lstm_1_LRelu)
      lstm_2 = LSTM(units=10, return_sequences = False, activation=None, kernel_initializer='random_normal')(lstm_1_droput)
      batch_norm2=tf.keras.layers.BatchNormalization()(lstm_2)
      lstm_2_LRelu = LeakyReLU(alpha=0.3)(batch_norm2) 
      lstm_2_droput = Dropout(0.3)(lstm_2_LRelu)
      output_dense = Dense(self.n_features, activation=None)(lstm_2_droput)
      output = LeakyReLU(alpha=0.3)(output_dense) 
      model = Model(inputs = inputs, outputs = output)
      model.compile(loss=None, metrics = [mse , mae, mape, rmse, ar])
      model.summary()
      return model
    def make_discriminator_model(self):
      model = Sequential()
      model.add(Flatten())
      model.add(Dense(units=72, input_shape=((self.n_sequence+1) * self.n_features,), activation=None, kernel_initializer='random_normal'))
      model.add(tf.keras.layers.LeakyReLU(alpha=0.3))
      model.add(tf.keras.layers.GaussianNoise(stddev=0.2))
      model.add(Dropout(0.3))
      model.add(Dense(units=100, activation=None, kernel_initializer='random_normal'))
      model.add(tf.keras.layers.LeakyReLU(alpha=0.3))
      model.add(Dropout(0.3))
      model.add(Dense(units=10, activation=None, kernel_initializer='random_normal'))
      model.add(tf.keras.layers.LeakyReLU(alpha=0.3))
      model.add(Dropout(0.3))
      model.add(Dense(1 ,activation='sigmoid'))
      model.compile(loss=self.discriminator_loss)
      return model
    def discriminator_loss(self, real_output, fake_output):
      real_loss = tf.keras.losses.binary_crossentropy(tf.ones_like(real_output), real_output)
      fake_loss = tf.keras.losses.binary_crossentropy(tf.zeros_like(fake_output), fake_output)
      total_loss = real_loss + fake_loss
      return total_loss
    def generator_loss(self, x, y, fake_output):
      a1=0.01
      g_loss = tf.keras.losses.binary_crossentropy(tf.ones_like(fake_output), fake_output)
      g_mse = tf.keras.losses.MSE(x, y)
      return a1*g_mse + (1-a1)*g_loss, g_mse


class tf_GAN():
  def __init__(self, xfx, zfz, **kwargs):
    self.n_sequence = kwargs.get('n_sequence',5)
    self.n_features =  kwargs.get('n_features',7)
    self.n_batch =  kwargs.get('batch_size',32)
    learning_rate=1e-4
    self.generator_optimizer = tf.keras.optimizers.Adam(learning_rate, beta_1=0.5)
    self.discriminator_optimizer = tf.keras.optimizers.Adam(learning_rate, beta_1=0.5)
    gan_models = get_GAN_models()
    self.generator = gan_models.make_generator_model()
    self.discriminator = gan_models.make_discriminator_model()
    self.generator_loss = gan_models.generator_loss
    self.discriminator_loss = gan_models.discriminator_loss
    # self.tf_check_point()
    self.epochs = kwargs.get('epochs',200)
    self.xfx = xfx
    self.zfz = zfz
    self.z, self.fz = self.zfz[0]
    pass
  def train_step_def(self, sequences, sequences_end):
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
      generated_prediction = self.generator(sequences, training=True)

      sequences_true = tf.concat((sequences, sequences_end[:, None, :]), axis=1)
      sequences_fake = tf.concat((sequences, generated_prediction[:, None, :]), axis=1)

      real_output = self.discriminator(sequences_true, training=True)
      fake_output = self.discriminator(sequences_fake, training=True)

      gen_loss, gen_mse_loss = self.generator_loss(generated_prediction, 
                                              sequences_end, 
                                              fake_output)
      disc_loss = self.discriminator_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, self.generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, self.discriminator.trainable_variables)

    self.generator_optimizer.apply_gradients(zip(gradients_of_generator, self.generator.trainable_variables))
    self.discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, self.discriminator.trainable_variables))

    return tf.reduce_mean(gen_loss), tf.reduce_mean(disc_loss), tf.reduce_mean(gen_mse_loss)

  def test_step_def(self, sequences, sequences_end):
    generated_prediction = self.generator(sequences, training=False)
    sequences_true = tf.concat((sequences, sequences_end[:,None,:]), axis=1)
    sequences_fake = tf.concat((sequences, generated_prediction[:,None,:]), axis=1)

    real_output = self.discriminator(sequences_true, training=False)
    fake_output = self.discriminator(sequences_fake, training=False)

    gen_loss, gen_mse_loss = self.generator_loss(generated_prediction, sequences_end, fake_output)
    disc_loss = self.discriminator_loss(real_output, fake_output)
    return tf.reduce_mean(gen_loss), tf.reduce_mean(disc_loss), tf.reduce_mean(gen_mse_loss)

  def train(self):
    self.history = np.empty(shape = (self.n_features + 1, self.epochs))
    self.history_val = np.empty(shape = (self.n_features + 1, self.epochs))
    len_dataset = len(self.xfx)
    len_dataset_val = len(self.zfz)
    for epoch in range(self.epochs):
      start = time.time()
      cur_dis_loss, cur_gen_loss, cur_gen_mse_loss = 0, 0, 0
      for sequence_batch, sequence_end_batch in self.xfx:
        aux_cur_losses = self.train_step(tf.cast(sequence_batch, tf.float32), 
                                    tf.cast(sequence_end_batch, tf.float32))
        cur_gen_loss += aux_cur_losses[0]/len_dataset
        cur_dis_loss += aux_cur_losses[1]/len_dataset
        cur_gen_mse_loss += aux_cur_losses[2]/len_dataset
      cur_gen_metrics = self.generator.evaluate(self.xfx,verbose=False)[1:]
      self.history[:, epoch] = cur_gen_loss, cur_dis_loss, cur_gen_mse_loss, *cur_gen_metrics
      cur_gen_metrics_val = self.generator.evaluate(self.zfz,verbose=False)[1: ]

      cur_gen_loss_val, cur_dis_loss_val, cur_gen_mse_loss_val = 0, 0, 0

      for sequence_batch, sequence_end_batch in self.zfz:
        aux_cur_losses_val = self.test_step(tf.cast(sequence_batch, tf.float32), 
                                      tf.cast(sequence_end_batch, tf.float32))
        cur_gen_loss_val += aux_cur_losses_val[0]/len_dataset_val
        cur_dis_loss_val += aux_cur_losses_val[1]/len_dataset_val
        cur_gen_mse_loss_val += aux_cur_losses_val[2]/len_dataset_val
      
      self.history_val[:, epoch] = cur_gen_loss_val, cur_dis_loss_val, cur_gen_mse_loss_val, *cur_gen_metrics_val
      print ('Time for epoch {} is {} sec Generator Loss: {},  Discriminator_loss: {}'
            .format(epoch + 1, time.time()-start, cur_gen_loss, cur_dis_loss))
      # if (epoch + 1) % 15 == 0:
      #   self.checkpoint.save(file_prefix = self.checkpoint_prefix)
  def predictor(self, **kwargs):
    self.train()
    self.f_z = self.generator.predict(self.z)[...,3]
  @tf.function
  def train_step(self,sequences, sequences_end):
    return self.train_step_def(sequences, sequences_end)
  @tf.function
  def test_step(self,sequences, sequences_end):
    return self.test_step_def(sequences, sequences_end)
    # def tf_check_point(self):
  #   checkpoint_dir = './training_checkpoints'
  #   self.checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
  #   self.checkpoint = tf.train.Checkpoint(generator_optimizer=self.generator_optimizer,
  #                                   discriminator_optimizer=self.discriminator_optimizer,
  #                                   generator=self.generator,
  #                                   discriminator=self.discriminator)


class tfGANpredictor(tfRegressor, tf_GAN):

    def get_params(**kwargs): return kwargs.get('tfRegressor',{})

    # def predictor(self,**kwargs):
    #     model = get_tensorflow_model(input_shape = [self.D],**tfRegressor.get_params(**kwargs))
    #     epochs = kwargs.get('epochs',128)
    #     batch_size = kwargs.get('batch_size',16)
    #     validation_split = kwargs.get('validation_split',0.1)
    #     model.fit(self.x, self.fx, epochs=epochs,validation_split = validation_split,batch_size = batch_size, verbose=0)
    #     self.f_z = model.predict(self.z, verbose= 0)
    
    def id(self,name = "Tensorflow"):
        return "Tensorflow"

def plot_history(history, history_val):
  metrics = ["gen_loss","dis_loss","gen_mse_loss", 'mse','mae','mape','rmse','ar']
  for i, metric_name in enumerate(metrics):  
    plt.figure()
    plt.title(metric_name)
    plt.plot(history[i], label='train')
    plt.plot(history_val[i], label='test')
    plt.legend()
    plt.title(metric_name)
  plt.show()

def plot_frame(fz, f_z, **kwargs):
  plt.figure()
  plt.title("closing price")
  plt.plot(fz[...,3], label="true")
  plt.plot(f_z, label="prediction")
  plt.legend()
  plt.show()

def get_best_results(history):
  min_index = np.argmin(history[3, :])
  return history[:, min_index]

class Standarized_TimeseriesGenerator(tf.keras.preprocessing.sequence.TimeseriesGenerator):
  def __getitem__(self, index):
    samples, targets  = super(Standarized_TimeseriesGenerator, self).__getitem__(index)
    #shape : (n_batch, n_sequence, n_features)
    mean = samples.mean(axis=1)
    std = samples.std(axis=1)
    samples = (samples - mean[:,None,:])/std[:,None,:] #standarize along each feature
    targets = (targets - mean)/std # The close value is our target
    return samples, targets


if __name__ == "__main__":
  kwargs = {
  'batch_size':32,
  'n_features':7,
  'n_sequence': 5,
  'epochs': 2000,
  'learning_rate':1e-4,
  }


  # scenarios_list = [ (-1, -1, -1, -1) ]
  # pd_scenarios_list = pd.DataFrame(scenarios_list)
  # set_kernel = kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 0,1e-8 ,map_setters.set_mean_distance_map)
  # scenarios = scenario_generator()
  # scenarios.run_scenarios(scenarios_list,data_gan_generator(),tfGANpredictor(set_kernel = set_kernel),data_accumulator(),**kwargs)

  xfx, zfz = data_gan_generator().get_data(**kwargs)
  tfGAN = tf_GAN(xfx, zfz,**kwargs)
  tfGAN.predictor()
  f_z, fz = tfGAN.f_z, tfGAN.fz
  history, history_values = tfGAN.history, tfGAN.history_val


  plot_history(history, history_values)
  plot_frame(fz,f_z)
  print("[MSE] train:",mean_squared_error(xfx)," test:", mean_squared_error(zfz))

  get_best_results(history_values)



