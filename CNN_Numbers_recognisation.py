import tkinter as tk
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from PIL import Image, ImageDraw, ImageOps

# Create a CNN Model for shape and number recognition
def create_model():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')  # For 10 classes (digits 0-9)
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Load or train the model with a dataset (e.g., MNIST for digits)
def load_or_train_model():
    try:
        model = tf.keras.models.load_model("shape_number_model.h5")
        print("Model loaded successfully.")
    except:
        # Load MNIST dataset for training (for number recognition)
        (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
        train_images = train_images / 255.0  # Normalize
        test_images = test_images / 255.0
        train_images = np.expand_dims(train_images, -1)  # Add channel dimension
        test_images = np.expand_dims(test_images, -1)

        model = create_model()
        model.fit(train_images, train_labels, epochs=5, validation_data=(test_images, test_labels))

        model.save("shape_number_model.h5")
        print("Model trained and saved successfully.")
    return model

# Function to predict the shape or number
def predict_drawn_shape(canvas_image):
    # Convert the canvas image to grayscale and resize it to 28x28
    img_array = canvas_image.convert('L')  # Convert to grayscale
    img_array = img_array.resize((28, 28))  # Resize to 28x28
    img_array = ImageOps.invert(img_array)  # Invert colors (white to black)
    
    img_array = np.array(img_array)  # Convert to numpy array
    img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension
    img_array = img_array / 255.0  # Normalize
    
    # Predict the shape/number
    prediction = model.predict(np.expand_dims(img_array, axis=0))  # Predict
    predicted_label = np.argmax(prediction)
    return predicted_label

# Create the canvas for drawing
def setup_canvas():
    root = tk.Tk()
    root.title("Draw a Shape or Number")

    canvas = tk.Canvas(root, width=280, height=280, bg="white")
    canvas.grid(row=0, column=0, padx=10, pady=10)

    # Create a PIL Image object for canvas
    canvas_image = Image.new("RGB", (280, 280), color="white")
    draw = ImageDraw.Draw(canvas_image)

    # Draw line with the mouse
    def draw_line(event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        canvas.create_line(x1, y1, x2, y2, width=5, fill="black")
        draw.line([x1, y1, x2, y2], fill="black", width=5)

    canvas.bind("<B1-Motion>", draw_line)

    # Button to predict the shape/number
    def predict_shape():
        prediction = predict_drawn_shape(canvas_image)
        result_label.config(text=f"Predicted: {prediction}")

    predict_button = tk.Button(root, text="Predict Shape/Number", command=predict_shape)
    predict_button.grid(row=1, column=0, pady=10)

    # Button to clear the canvas
    def clear_canvas():
        canvas.delete("all")  # Clear all drawn lines from the canvas
        canvas_image.paste((255, 255, 255), [0, 0, canvas_image.size[0], canvas_image.size[1]])  # Clear the image

    clear_button = tk.Button(root, text="Clear Canvas", command=clear_canvas)
    clear_button.grid(row=1, column=1, padx=10)

    # Label to display the prediction result
    result_label = tk.Label(root, text="Predicted: ")
    result_label.grid(row=2, column=0, columnspan=2)

    return root, canvas, canvas_image

# Initialize the model
model = load_or_train_model()

# Set up the canvas and UI
root, canvas, canvas_image = setup_canvas()

# Run the Tkinter main loop
root.mainloop()
