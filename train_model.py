# train_model.py

import os
import numpy as np
from models import inceptionv3
from random import shuffle

def make_training_data_subsets(data, width, height, test_size):
    """Return four subsets of training and validation data."""
    np.random.shuffle(data)

    train = data[:-test_size]
    test = data[-test_size:]

    train_x = np.array([i[0] for i in train]).reshape(-1, width, height, 3)
    train_y = [i[1] for i in train]
    test_x = np.array([i[0] for i in test]).reshape(-1, width, height, 3)
    test_y = [i[1] for i in test]

    return train_x, train_y, test_x, test_y

def main():
    WIDTH = 240
    HEIGHT = 180
    LR = 1e-3
    EPOCHS = 25
    DATALEN = 100
    MODEL_TYPE = 'inceptionv3'

    MODEL_NAME = f'tmnf-car-{LR}-{MODEL_TYPE}-{EPOCHS}-epochs-{DATALEN}K-data.model'
    PREV_MODEL = f'tmnf-car-{LR}-{MODEL_TYPE}-{EPOCHS}-epochs-{DATALEN}K-data.model'
    LOAD_MODEL = False

    model = inceptionv3(WIDTH, HEIGHT, 3, LR, output=8, model_name=MODEL_NAME)

    if LOAD_MODEL:
        model.load(PREV_MODEL)
        print('Previous model loaded.')

    for e in range(EPOCHS):

        data_order = [i for i in range(1, len(os.listdir('data')) + 1)]
        shuffle(data_order)

        for i in data_order:
            try:
                file_name = f'data/TRAINING_DATA-{i}.npy'
                train_data = np.load(file_name)
                train_x, train_y, test_x, test_y = make_training_data_subsets(train_data,
                                                                              WIDTH,
                                                                              HEIGHT,
                                                                              100)

                model.fit({'input': train_x},
                          {'targets': train_y},
                          n_epoch = 1,
                          validation_set = ({'input': test_x},
                                            {'targets': test_y}),
                                            snapshot_step = 2500,
                                            show_metric = True,
                                            run_id = MODEL_NAME)

            except Exception as err:
                print(err)

        print('Saving model...')
        model.save(os.path.join('models', MODEL_NAME))

if __name__ == '__main__':
    main()