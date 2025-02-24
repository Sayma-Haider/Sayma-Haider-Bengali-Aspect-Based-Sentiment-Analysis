# -*- coding: utf-8 -*-
"""restaurent_final_trfbert.ipynb

Automatically generated by Colab.

"""

from google.colab import drive
drive.mount('/content/drive')

!pip install transformers

"""RoBERTa - Category"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from transformers import RobertaTokenizer, TFRobertaForSequenceClassification
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import LabelEncoder

# Load your Excel dataset
data = pd.read_excel("/content/drive/MyDrive/ML Projects/Restaurant.xlsx")

# Split data into categories, sentiments, and opinions
categories = data['Category'].astype(str)
polarities = data['Polarity'].astype(str)

# Tokenize and preprocess the aspect data
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Tokenize and preprocess the category data based on correct aspects
category_sequences = tokenizer(list(categories), truncation=True, padding=True, return_tensors='tf', max_length=64)

# Convert category labels to categorical format
num_category_classes = len(np.unique(categories))

# Split the data into training and testing sets for category classification
X_train_category, X_test_category, y_train_category, y_test_category = train_test_split(
    category_sequences['input_ids'].numpy(), categories, test_size=0.2, random_state=42)

# Create label encoder for category
label_encoder_category = LabelEncoder()
y_train_category_encoded = label_encoder_category.fit_transform(y_train_category)

# Load the pre-trained RoBERTa model for category classification
model_category = TFRobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=num_category_classes)

# Create a legacy optimizer (no need to build it) and compile the model
optimizer_legacy = tf.keras.optimizers.legacy.Adam(learning_rate=2e-5)
model_category.compile(optimizer=optimizer_legacy, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Define callbacks for early stopping and learning rate reduction
early_stopping_category = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
reduce_lr_category = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-7)

# Fine-tune the category classification model
for epoch in range(10):
    print(f"Category Classification - Epoch {epoch + 1}/10")
    history = model_category.fit(
        [X_train_category, X_train_category], y_train_category_encoded, epochs=1, batch_size=32,
        validation_split=0.2, callbacks=[early_stopping_category, reduce_lr_category])

# Use the trained category classification model to predict categories
predicted_categories = model_category.predict([X_test_category, X_test_category])
predicted_categories_classes = np.argmax(predicted_categories.logits, axis=1)

# Calculate accuracy for the category classification
accuracy_category = accuracy_score(y_test_category, label_encoder_category.classes_[predicted_categories_classes])

# Print accuracy for the category classification
print("Accuracy for Category Classification:", accuracy_category)

# Calculate classification report for the category classification
classification_report_category = classification_report(y_test_category, label_encoder_category.classes_[predicted_categories_classes], digits=4)

# Print classification report for the category classification
print("Classification Report for Category Classification:")
print(classification_report_category)

"""RoBERTa - Polarity"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from transformers import RobertaTokenizer, TFRobertaForSequenceClassification
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import LabelEncoder

# Load your Excel dataset
# Replace 'your_dataset.xlsx' with your actual dataset file
data = pd.read_excel("/content/drive/MyDrive/ML Projects/Restaurant.xlsx")

# Split data into categories, sentiments, and opinions
categories = data['Category'].astype(str)
polarities = data['Polarity'].astype(str)

# Tokenize and preprocess the polarity data
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Tokenize and preprocess the polarity data based on correct categories
polarity_sequences = tokenizer(list(polarities), truncation=True, padding=True, return_tensors='tf', max_length=64)

# Convert polarity labels to categorical format
num_polarity_classes = len(np.unique(polarities))

# Split the data into training and testing sets for polarity classification
X_train_polarity, X_test_polarity, y_train_polarity, y_test_polarity = train_test_split(
    polarity_sequences['input_ids'].numpy(), polarities, test_size=0.2, random_state=42)

# Create label encoder for polarity
label_encoder_polarity = LabelEncoder()
y_train_polarity_encoded = label_encoder_polarity.fit_transform(y_train_polarity)

# Load the pre-trained RoBERTa model for polarity classification
model_polarity = TFRobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=num_polarity_classes)

# Create an optimizer
optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)

# Compile the model
model_polarity.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Define callbacks for early stopping and learning rate reduction
early_stopping_polarity = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
reduce_lr_polarity = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-7)

# Fine-tune the polarity classification model with performance tuning
for epoch in range(10):  # Increase the number of epochs if necessary
    print(f"Polarity Classification - Epoch {epoch + 1}/10")
    history = model_polarity.fit(
        X_train_polarity, y_train_polarity_encoded, epochs=1, batch_size=32,
        validation_split=0.2, callbacks=[early_stopping_polarity, reduce_lr_polarity])

# Use the trained polarity classification model to predict polarity
predicted_polarities = model_polarity.predict(X_test_polarity)
predicted_polarities_classes = np.argmax(predicted_polarities.logits, axis=1)

# Calculate accuracy for the polarity classification
accuracy_polarity = accuracy_score(y_test_polarity, label_encoder_polarity.classes_[predicted_polarities_classes])

# Print accuracy for the polarity classification
print("Accuracy for Polarity Classification:", accuracy_polarity)

# Calculate classification report for the polarity classification
classification_report_polarity = classification_report(y_test_polarity, label_encoder_polarity.classes_[predicted_polarities_classes], digits=4)

# Print classification report for the polarity classification
print("Classification Report for Polarity Classification:")
print(classification_report_polarity)

"""BERT - Category"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from transformers import BertTokenizer, TFBertForSequenceClassification
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import LabelEncoder

# Load your Excel dataset
# Replace 'your_dataset.xlsx' with your actual dataset file
data = pd.read_excel("/content/drive/MyDrive/ML Projects/Restaurant.xlsx")

# Split data into categories, sentiments, and opinions
categories = data['Category'].astype(str)
polarities = data['Polarity'].astype(str)

# Tokenize and preprocess the category data based on correct aspects
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

category_sequences = tokenizer(list(categories), truncation=True, padding=True, return_tensors='tf', max_length=64)

# Convert category labels to categorical format
label_encoder_category = LabelEncoder()
y_category_encoded = label_encoder_category.fit_transform(categories)

# Use the last 20% of data for testing and the first 80% for training
split_index = int(0.8 * len(category_sequences['input_ids']))
X_train_category, X_test_category = category_sequences['input_ids'][:split_index], category_sequences['input_ids'][split_index:]
y_train_category_encoded, y_test_category = y_category_encoded[:split_index], y_category_encoded[split_index:]

# Load the pre-trained BERT model for category classification
num_category_classes = len(label_encoder_category.classes_)
model_category = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_category_classes)

# Create a legacy optimizer (no need to build it) and compile the model
optimizer_legacy = tf.keras.optimizers.legacy.Adam(learning_rate=2e-5)
model_category.compile(optimizer=optimizer_legacy, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Define callbacks for early stopping and learning rate reduction
early_stopping_category = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
reduce_lr_category = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-7)

# Fine-tune the category classification model
for epoch in range(10):
    print(f"Category Classification - Epoch {epoch + 1}/10")
    history = model_category.fit(
        [X_train_category, X_train_category], y_train_category_encoded, epochs=1, batch_size=32,
        validation_split=0.2, callbacks=[early_stopping_category, reduce_lr_category])

# Use the trained category classification model to predict categories
predicted_categories = model_category.predict([X_test_category, X_test_category])
predicted_categories_classes = np.argmax(predicted_categories.logits, axis=1)

# Calculate accuracy for category classification
accuracy_category = accuracy_score(y_test_category, predicted_categories_classes)

# Print accuracy for category classification
print("Accuracy for Category Classification:", accuracy_category)

# Calculate classification report for category classification
classification_report_category = classification_report(y_test_category, predicted_categories_classes, digits=4)

# Print classification report for category classification
print("Classification Report for Category Classification:")
print(classification_report_category)

"""BERT - Polarity"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from transformers import BertTokenizer, TFBertForSequenceClassification
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import LabelEncoder

# Load your Excel dataset
# Replace 'your_dataset.xlsx' with your actual dataset file
data = pd.read_excel("/content/drive/MyDrive/ML Projects/Restaurant.xlsx")

# Split data into categories, sentiments, and opinions
categories = data['Category'].astype(str)
polarities = data['Polarity'].astype(str)

# Tokenize and preprocess the aspect data
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize and preprocess the polarity data based on correct categories
polarity_sequences = tokenizer(list(polarities), truncation=True, padding=True, return_tensors='tf', max_length=64)

# Convert polarity labels to categorical format
label_encoder_polarity = LabelEncoder()
y_polarity_encoded = label_encoder_polarity.fit_transform(polarities)

# Use the last 20% of data for testing and the first 80% for training
split_index = int(0.8 * len(polarity_sequences['input_ids']))
X_train_polarity, X_test_polarity = polarity_sequences['input_ids'][:split_index], polarity_sequences['input_ids'][split_index:]
y_train_polarity_encoded, y_test_polarity = y_polarity_encoded[:split_index], y_polarity_encoded[split_index:]

# Load the pre-trained BERT model for polarity classification
num_polarity_classes = len(label_encoder_polarity.classes_)
model_polarity = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_polarity_classes)

# Create a legacy optimizer (no need to build it) and compile the model
optimizer_legacy = tf.keras.optimizers.legacy.Adam(learning_rate=2e-5)
model_polarity.compile(optimizer=optimizer_legacy, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Define callbacks for early stopping and learning rate reduction
early_stopping_polarity = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
reduce_lr_polarity = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-7)

# Fine-tune the polarity classification model
for epoch in range(10):
    print(f"Polarity Classification - Epoch {epoch + 1}/10")
    history = model_polarity.fit(
        [X_train_polarity, X_train_polarity], y_train_polarity_encoded, epochs=1, batch_size=32,
        validation_split=0.2, callbacks=[early_stopping_polarity, reduce_lr_polarity])

# Use the trained polarity classification model to predict polarity
predicted_polarities = model_polarity.predict([X_test_polarity, X_test_polarity])
predicted_polarities_classes = np.argmax(predicted_polarities.logits, axis=1)

# Calculate accuracy for polarity classification
accuracy_polarity = accuracy_score(y_test_polarity, predicted_polarities_classes)

# Print accuracy for polarity classification
print("Accuracy for Polarity Classification:", accuracy_polarity)

# Calculate classification report for polarity classification
classification_report_polarity = classification_report(y_test_polarity, predicted_polarities_classes, digits=4)

# Print classification report for polarity classification
print("Classification Report for Polarity Classification:")
print(classification_report_polarity)
