import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop

class TrainModel:
    
    def __init__(self,trainPath,testPath,batch_size,epochs,targetWidth,targetHeight,filename):
        self.train = ImageDataGenerator(rescale=1/255)
        self.validation = ImageDataGenerator(rescale=1/255)

        self.train_dataset = self.train.flow_from_directory(trainPath,
                                                    target_size=(targetWidth, targetHeight),
                                                    batch_size = batch_size,
                                                    class_mode = "binary")

        self.test_dataset = self.validation.flow_from_directory(testPath,
                                                            target_size=(224, 224),
                                                            batch_size = batch_size,
                                                            class_mode = "binary")
        self.epochs = epochs
        self.filename = filename

    def GenerateModel(self):

        model = tf.keras.models.Sequential([
                tf.keras.layers.Conv2D(16,(3,3),activation='relu',input_shape=(224,224,3)),
                tf.keras.layers.MaxPool2D(2,2),
                tf.keras.layers.Conv2D(32,(3,3),activation='relu'),
                tf.keras.layers.MaxPool2D(2,2),
                tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
                tf.keras.layers.MaxPool2D(2,2),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(512,activation="relu"),
                tf.keras.layers.Dense(1,activation="sigmoid")
            ])

        model.compile(loss="binary_crossentropy",
                    optimizer = RMSprop(learning_rate=0.001),
                    metrics = ['accuracy'])

        model_fit = model.fit(self.train_dataset,
                        epochs = self.epochs,
                        validation_data = self.test_dataset)

        loss, accuracy = model.evaluate(self.test_dataset)

        print(f"Accuracy: {accuracy:.2f}")

        model.save(self.filename)
