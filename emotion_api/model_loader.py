from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout
from tensorflow.keras.layers import Activation, Flatten, BatchNormalization, Input

def build_emotion_model():
    model = Sequential()
    model.add(Input(shape=(48,48,1)))

    for filters in [32, 64, 128, 256]:
        model.add(Conv2D(filters, (3,3), padding='same', kernel_initializer='he_normal'))
        model.add(Activation('elu'))
        model.add(BatchNormalization())
        model.add(Conv2D(filters, (3,3), padding='same', kernel_initializer='he_normal'))
        model.add(Activation('elu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D((2,2)))
        model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(64, activation='elu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='elu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(5, activation='softmax'))

    return model
