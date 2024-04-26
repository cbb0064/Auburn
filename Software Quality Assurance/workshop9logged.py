from myLogger import giveMeLoggingObject
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets, linear_model
import pandas as pd
import numpy as np
import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist

# Obtain the custom logger
logger = giveMeLoggingObject()

def readData():
    try:
        iris = datasets.load_iris()
        logger.info("IRIS dataset loaded successfully")  # Log successful dataset load
        X = iris.data
        Y = iris.target
        df = pd.DataFrame(X, columns=iris.feature_names)
        # Check for nulls to detect data anomalies that may indicate poisoning
        if df.isnull().values.any():
            logger.warning("Data contains null values - potential data poisoning")  # Warning for potential data poisoning
    except Exception as e:
        logger.error("Failed to load or process IRIS dataset: {}".format(e))  # Log exceptions that occur during data load
        raise
    return df

def makePrediction():
    try:
        iris = datasets.load_iris()
        knn = KNeighborsClassifier(n_neighbors=6)
        knn.fit(iris['data'], iris['target'])
        logger.info("KNN model trained successfully")  # Log successful training
        X = [
            [5.9, 1.0, 5.1, 1.8],
            [3.4, 2.0, 1.1, 4.8],
        ]
        prediction = knn.predict(X)
        logger.info("Predictions made successfully: {}".format(prediction))  # Log successful predictions
        # Check predictions against expected values to detect model tricking
        expected_predictions = [2, 1]  # Hypothetical expected results for the inputs
        if not all(pred == exp for pred, exp in zip(prediction, expected_predictions)):
            logger.warning("Prediction output differs from expected - possible model tricking detected")  # Warning for potential model tricking
    except Exception as e:
        logger.error("Prediction process failed: {}".format(e))  # Log exceptions that occur during prediction
        raise

def doRegression():
    try:
        diabetes = datasets.load_diabetes()
        logger.info("Diabetes dataset loaded successfully")  # Log successful dataset load
        diabetes_X = diabetes.data[:, np.newaxis, 2]
        diabetes_X_train = diabetes_X[:-20]
        diabetes_X_test = diabetes_X[-20:]
        diabetes_y_train = diabetes.target[:-20]
        diabetes_y_test = diabetes.target[-20:]
        regr = linear_model.LinearRegression()
        regr.fit(diabetes_X_train, diabetes_y_train)
        logger.info("Regression model trained successfully")  # Log successful model training
        diabetes_y_pred = regr.predict(diabetes_X_test)
        logger.info("Regression predictions made successfully")  # Log successful predictions
        # Evaluate regression error for signs of adversarial interference
        if np.mean((diabetes_y_test - diabetes_y_pred) ** 2) > 1000:  # Hypothetical threshold
            logger.warning("High mean squared error in regression predictions - check for potential adversarial interference")  # Warning for possible adversarial attack
    except Exception as e:
        logger.error("Regression model training or prediction failed: {}".format(e))  # Log exceptions that occur during model training or prediction
        raise

def doDeepLearning():
    try:
        # Load data using keras.datasets
        (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

        # Normalize and reshape data
        train_images = (train_images / 255) - 0.5
        test_images = (test_images / 255) - 0.5
        train_images = train_images.reshape((-1, 28, 28, 1))
        test_images = test_images.reshape((-1, 28, 28, 1))

        num_filters = 8
        filter_size = 3
        pool_size = 2

        model = Sequential([
            Conv2D(num_filters, filter_size, input_shape=(28, 28, 1)),
            MaxPooling2D(pool_size=pool_size),
            Flatten(),
            Dense(10, activation='softmax'),
        ])

        # Compile the model
        model.compile(
            'adam',
            loss='categorical_crossentropy',
            metrics=['accuracy'],
        )

        # Train the model
        model.fit(
            train_images,
            to_categorical(train_labels),
            epochs=3,
            validation_data=(test_images, to_categorical(test_labels)),
        )

        model.save_weights('cnn.weights.h5')
        predictions = model.predict(test_images[:5])
        logger.info("Deep learning predictions made: {}".format(np.argmax(predictions, axis=1)))

        # Evaluate model accuracy
        _, accuracy = model.evaluate(test_images, to_categorical(test_labels), verbose=0)
        if accuracy < 0.8:
            logger.warning("Deep learning model accuracy unexpectedly low - possible adversarial attack")
    except Exception as e:
        logger.error("Deep learning model training or prediction failed: {}".format(e))
        raise

if __name__=='__main__':
    data_frame = readData()
    makePrediction()
    doRegression()
    doDeepLearning()
