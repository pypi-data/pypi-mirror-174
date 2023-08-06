# example of loading the generator model and generating images
import numpy as np
from numpy import asarray
from numpy.random import randn
from numpy.random import randint
from keras.models import load_model
from matplotlib import pyplot
import tensorflow as tf
# from tensorflow.keras.preprocessing import image
from numpy import asarray
import glob
import imageio
import ganskit.cgan.fid as fid
import os
import cv2
from imageio import imread
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# generate points in latent space as input for the generator
def generate_latent_points(latent_dim, n_samples, n_classes=10):
    # generate points in the latent space
    x_input = randn(latent_dim * n_samples)
    # reshape into a batch of inputs for the network
    z_input = x_input.reshape(n_samples, latent_dim)
    # generate labels
    labels = randint(0, n_classes, n_samples)
    return z_input, labels

# create and save a plot of generated images
def save_plot(examples, n_class,n_sample_num):
    # plot images
    for i in range(n_class * n_sample_num):
        # define subplot
        pyplot.subplot(n_class, n_sample_num, 1 + i)
        # turn off axis
        pyplot.axis('off')
        # plot raw pixel data
        pyplot.imshow(examples[i, :, :, 0],cmap='gray_r')
    pyplot.show()

def to_gray_image(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    shrink_img = cv2.resize(img_gray, (28, 28), interpolation=cv2.INTER_AREA)
    return shrink_img

def get_FID(label_id,stats_folder=None):
    # Paths
    image_path = 'generated/'+str(label_id)  # set path to some generated images
    if stats_folder==None:
        stats_path = 'gray_dataset/fid_stats_'+str(label_id)+'.npz'  # training set statistics
    else:
        stats_path=f"{stats_folder}/fid_stats_{label_id}.npz"
    inception_path = fid.check_or_download_inception(None)  # download inception network

    # loads all images into memory (this might require a lot of RAM!)
    image_list = glob.glob(os.path.join(image_path, '*.jpg'))
    images = np.array([imread(str(fn),as_gray=False,pilmode="RGB").astype(np.float32) for fn in image_list])

    # load precalculated training set statistics
    f = np.load(stats_path)
    mu_real, sigma_real = f['mu'][:], f['sigma'][:]
    f.close()

    fid.create_inception_graph(inception_path)  # load the graph into the current TF graph
    with tf.compat.v1.Session() as sess:
        sess.run(tf.compat.v1.global_variables_initializer())
        mu_gen, sigma_gen = fid.calculate_activation_statistics(images, sess, batch_size=100)

    fid_value = fid.calculate_frechet_distance(mu_gen, sigma_gen, mu_real, sigma_real)
    print("FID: %s" % fid_value)
    return fid_value

def evaluate(model_path='cgan_generator-1.h5',save_folder="generated",stats_folder="gray_dataset"):
    # load model
    model = load_model(model_path)
    # config parameters
    N_DIM = 100
    N_CLASS = 4
    N_SAMPLE_PER_CLASS = 10

    LABEL_ID = 3
    labels = []
    for i in range(100):
        # generate images
        latent_points, labels = generate_latent_points(N_DIM, N_CLASS * N_SAMPLE_PER_CLASS, n_classes=N_CLASS)
        # specify labels
        labels = asarray([x for _ in range(N_SAMPLE_PER_CLASS) for x in range(N_CLASS)])

        X = model.predict([np.array([latent_points[LABEL_ID]]), np.array([labels[LABEL_ID]])])
        # scale from [-1,1] to [0,1]
        X = (X + 1) / 2.0
        # plot the result
        pyplot.title('label = ' + str(labels[LABEL_ID]))
        pyplot.imshow(X[0, :, :, 0], cmap='gray_r')
        img = asarray(X[0] * 255.)
        folder=save_folder+'/' + str(LABEL_ID) + '/'
        if not os.path.exists(folder):
            os.mkdir(folder)
        cv2.imwrite(folder+ str(i + 1) + '.jpg',img)

    # evaluate

    fid_value = get_FID(LABEL_ID,stats_folder)
    print("obtained FID value for " + str(LABEL_ID) + " :", fid_value)
    return fid_value

    # pyplot.show()

