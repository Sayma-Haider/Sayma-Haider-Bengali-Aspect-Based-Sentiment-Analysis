# -*- coding: utf-8 -*-
"""final_cricket_trfbert.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CxmYMuMeRP0-fGuaL0NwW6ZH7KYbRZMv
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install transformers

"""roberta-polarity final"""

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
data = pd.read_excel("/content/drive/MyDrive/SA/Cricket.xlsx")

# Split data into categories, sentiments, and opinions
categories = data['Category'].astype(str)
polarities = data['Polarity'].astype(str)

# Tokenize and preprocess the polarity data based on correct categories
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

polarity_sequences = tokenizer(list(polarities), truncation=True, padding=True, return_tensors='tf', max_length=64)

# Convert polarity labels to categorical format
label_encoder_polarity = LabelEncoder()
y_polarity_encoded = label_encoder_polarity.fit_transform(polarities)

# Use the last 20% of data for testing and the first 80% for training
split_index = int(0.8 * len(polarity_sequences['input_ids']))
X_train_polarity, X_test_polarity = polarity_sequences['input_ids'][:split_index], polarity_sequences['input_ids'][split_index:]
y_train_polarity_encoded, y_test_polarity = y_polarity_encoded[:split_index], y_polarity_encoded[split_index:]

# Load the pre-trained RoBERTa model for polarity classification
num_polarity_classes = len(label_encoder_polarity.classes_)
model_polarity = TFRobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=num_polarity_classes)

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

"""polarity bert final"""

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
data = pd.read_excel("/content/drive/MyDrive/SA/Cricket.xlsx")

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

"""*category* **bert** final"""

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
data = pd.read_excel("/content/drive/MyDrive/SA/Cricket.xlsx")

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

!pip install sentencepiece

"""roberta category final"""

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
data = pd.read_excel("/content/drive/MyDrive/SA/Cricket.xlsx")

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

"""Hybrid-category-final"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Input, Dense, Concatenate, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Load your Excel dataset
# Replace 'your_dataset.xlsx' with your actual dataset file
data = pd.read_excel("/content/drive/MyDrive/SA/Cricket.xlsx")

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

# Fine-tune the category classification model without dropout layers
for epoch in range(10):
    print(f"Category Classification - Epoch {epoch + 1}/10")
    history = model_category.fit(
        X_train_category, y_train_category_encoded, epochs=1, batch_size=32,
        validation_split=0.2, callbacks=[early_stopping_category, reduce_lr_category])

# Use the trained category classification model to predict categories
predicted_categories = model_category.predict(X_test_category)
predicted_categories_classes = np.argmax(predicted_categories[0], axis=1)  # Fix dimension issue here

# Calculate accuracy for category classification
accuracy_category = accuracy_score(y_test_category, predicted_categories_classes)

# Print accuracy for category classification
print("Accuracy for Category Classification:", accuracy_category)

# Vectorize the text data for Random Forest
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_train_rf = vectorizer.fit_transform(categories[:split_index])
X_test_rf = vectorizer.transform(categories[split_index:])

# Encode the test category labels for Random Forest evaluation
y_test_category_encoded = label_encoder_category.transform(categories[split_index:])

# Create the Random Forest classifier with dropout
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Add dropout layer to the RF model
rf_model = Pipeline([
    ('classifier', rf_model)
])

# Train the Random Forest classifier
rf_model.fit(X_train_rf, y_train_category_encoded)

# Use the trained Random Forest model to predict
X_test_rf_predictions = rf_model.predict(X_test_rf)

# Ensure the data types match for concatenation
X_test_rf_predictions = X_test_rf_predictions.astype(np.float32)  # Convert Random Forest predictions to float32

# Combine BERT features with machine learning predictions
combined_features = np.concatenate([predicted_categories[0], X_test_rf_predictions.reshape(-1, 1)], axis=1)

# Build the final hybrid model for category classification without dropout in BERT
input_layer = Input(shape=(num_category_classes + 1,))  # +1 for the Random Forest prediction
dense_layer = Dense(128, activation='relu')(input_layer)
output_layer = Dense(num_category_classes, activation='softmax')(dense_layer)
model_hybrid = Model(inputs=input_layer, outputs=output_layer)

# Compile the hybrid model
model_hybrid.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the hybrid model without dropout in BERT
model_hybrid.fit(combined_features, y_test_category_encoded, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the hybrid model on the test set
test_loss, test_accuracy = model_hybrid.evaluate(combined_features, y_test_category_encoded)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

# Predict categories using the hybrid model

# Use the trained hybrid model to predict categories
predicted_hybrid_categories = model_hybrid.predict(combined_features)
predicted_hybrid_categories_classes = np.argmax(predicted_hybrid_categories, axis=1)
target_names = ['other', 'team', 'batting', 'team_management', 'bowling']
# Calculate and print the classification report
classification_rep_category = classification_report(y_test_category_encoded, predicted_hybrid_categories_classes, target_names=target_names)

print("Classification Report for Category (Hybrid Model):\n", classification_rep_category)

"""hybrid-polarity

Polarity hybrid final
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Input, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

# Load your Excel dataset
data = pd.read_excel("/content/drive/MyDrive/SA/Cricket.xlsx")

# Split data into categories, sentiments, and opinions
categories = data['Category'].astype(str)
polarities = data['Polarity'].astype(str)

# Tokenize and preprocess the polarity data based on correct aspects
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

polarity_sequences = tokenizer(list(polarities), truncation=True, padding=True, return_tensors='tf', max_length=64)

# Convert polarity labels to categorical format
label_encoder_polarity = LabelEncoder()
y_polarity_encoded = label_encoder_polarity.fit_transform(polarities)

# Split the data into training and testing sets
split_index = int(0.8 * len(polarity_sequences['input_ids']))
X_train_polarity, X_test_polarity = polarity_sequences['input_ids'][:split_index], polarity_sequences['input_ids'][split_index:]
y_train_polarity_encoded, y_test_polarity = y_polarity_encoded[:split_index], y_polarity_encoded[split_index:]

# Load the pre-trained BERT model for polarity classification
num_polarity_classes = len(label_encoder_polarity.classes_)
model_polarity = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_polarity_classes)

# Compile the model with reduced regularization
model_polarity.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Fine-tune the polarity classification model with increased complexity
for epoch in range(10):
    print(f"Polarity Classification - Epoch {epoch + 1}/10")
    model_polarity.fit(
        X_train_polarity, y_train_polarity_encoded, epochs=1, batch_size=64,  # Increase batch size
        validation_split=0.2)

# Use the trained polarity classification model to predict polarities
predicted_polarities = model_polarity.predict(X_test_polarity)
predicted_polarities_classes = np.argmax(predicted_polarities[0], axis=1)

# Calculate accuracy for polarity classification
accuracy_polarity = accuracy_score(y_test_polarity, predicted_polarities_classes)

# Print accuracy for polarity classification
print("Accuracy for Polarity Classification:", accuracy_polarity)

# Vectorize the text data for Random Forest
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_train_rf = vectorizer.fit_transform(polarities[:split_index])
X_test_rf = vectorizer.transform(polarities[split_index:])

# Encode the test polarity labels for Random Forest evaluation
y_test_polarity_encoded = label_encoder_polarity.transform(polarities[split_index:])

# Create the Random Forest classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the Random Forest classifier
rf_model.fit(X_train_rf, y_train_polarity_encoded)

# Use the trained Random Forest model to predict
X_test_rf_predictions = rf_model.predict(X_test_rf)

# Ensure the data types match for concatenation
X_test_rf_predictions = X_test_rf_predictions.astype(np.float32)  # Convert Random Forest predictions to float32

# Combine BERT features with machine learning predictions
combined_features = np.concatenate([predicted_polarities[0], X_test_rf_predictions.reshape(-1, 1)], axis=1)

# Build the final hybrid model for polarity classification with reduced regularization
input_layer = Input(shape=(num_polarity_classes + 1,))  # +1 for the Random Forest prediction
dense_layer = Dense(128, activation='relu', kernel_regularizer=l2(0.001))(input_layer)  # Increase complexity
dropout_layer = Dropout(0.3)(dense_layer)  # Reduce dropout rate
output_layer = Dense(num_polarity_classes, activation='softmax')(dropout_layer)
model_hybrid = Model(inputs=input_layer, outputs=output_layer)

# Compile the hybrid model
model_hybrid.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the hybrid model
model_hybrid.fit(combined_features, y_test_polarity_encoded, epochs=20, batch_size=64,  # Increase epochs and batch size
                 validation_split=0.2)

# Use the trained hybrid model to predict polarities
predicted_hybrid_polarities = model_hybrid.predict(combined_features)
predicted_hybrid_polarities_classes = np.argmax(predicted_hybrid_polarities, axis=1)

# Calculate accuracy for the hybrid model
accuracy_hybrid = accuracy_score(y_test_polarity_encoded, predicted_hybrid_polarities_classes)

# Print accuracy for the hybrid model
print("Accuracy for Hybrid Model:", accuracy_hybrid)

# Generate the classification report
report = classification_report(y_test_polarity_encoded, predicted_hybrid_polarities_classes, target_names=label_encoder_polarity.classes_)

# Print the classification report
print("Classification Report for Polarity (Hybrid Model):\n", report)

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Load your Excel dataset
data = pd.read_excel("/content/drive/MyDrive/SA/Cricket.xlsx")

# Split data into categories and sentiments
categories = data['Category'].astype(str)
polarities = data['Polarity'].astype(str)

# Convert category labels to categorical format
label_encoder_category = LabelEncoder()
y_category_encoded = label_encoder_category.fit_transform(categories)

# Use fixed 80% of data for training and 20% for testing
split_index = int(0.8 * len(categories))
X_train, X_test = categories[:split_index], categories[split_index:]
y_train, y_test = y_category_encoded[:split_index], y_category_encoded[split_index:]

# Vectorize the text data for Random Forest
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_train_rf = vectorizer.fit_transform(X_train)
X_test_rf = vectorizer.transform(X_test)

# Create the Random Forest classifier with adjusted hyperparameters
rf_model = RandomForestClassifier(n_estimators=100, max_depth=1, min_samples_split=2)

# Train the Random Forest classifier
rf_model.fit(X_train_rf, y_train)

# Use the trained Random Forest model to predict
X_test_rf_predictions = rf_model.predict(X_test_rf)

# Calculate accuracy for category classification using Random Forest
accuracy_category_rf = accuracy_score(y_test, X_test_rf_predictions)
print("Accuracy for Category Classification (Random Forest):", accuracy_category_rf)

# Generate the classification report for Random Forest
report_rf = classification_report(y_test, X_test_rf_predictions, labels=np.unique(y_test), target_names=label_encoder_category.classes_)
print("Classification Report for Category Classification (Random Forest):\n", report_rf)

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Load your Excel dataset
data = pd.read_excel("/content/drive/MyDrive/SA/Cricket.xlsx")

# Split data into categories and sentiments
categories = data['Polarity'].astype(str)
polarities = data['Polarity'].astype(str)

# Convert category labels to categorical format
label_encoder_category = LabelEncoder()
y_category_encoded = label_encoder_category.fit_transform(categories)

# Use fixed 80% of data for training and 20% for testing
split_index = int(0.8 * len(categories))
X_train, X_test = categories[:split_index], categories[split_index:]
y_train, y_test = y_category_encoded[:split_index], y_category_encoded[split_index:]

# Vectorize the text data for Random Forest
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_train_rf = vectorizer.fit_transform(X_train)
X_test_rf = vectorizer.transform(X_test)

# Create the Random Forest classifier with adjusted hyperparameters
rf_model = RandomForestClassifier(n_estimators=5, max_depth=1, min_samples_split=3)

# Train the Random Forest classifier
rf_model.fit(X_train_rf, y_train)

# Use the trained Random Forest model to predict
X_test_rf_predictions = rf_model.predict(X_test_rf)

# Calculate accuracy for category classification using Random Forest
accuracy_category_rf = accuracy_score(y_test, X_test_rf_predictions)
print("Accuracy for Category Classification (Random Forest):", accuracy_category_rf)

# Generate the classification report for Random Forest
report_rf = classification_report(y_test, X_test_rf_predictions, labels=np.unique(y_test), target_names=label_encoder_category.classes_)
print("Classification Report for Category Classification (Random Forest):\n", report_rf)

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Load your Excel dataset
data = pd.read_excel("/content/drive/MyDrive/SA/Restaurant.xlsx")

# Split data into categories and sentiments
categories = data['Category'].astype(str)
polarities = data['Polarity'].astype(str)

# Convert category labels to categorical format
label_encoder_category = LabelEncoder()
y_category_encoded = label_encoder_category.fit_transform(categories)

# Use fixed 80% of data for training and 20% for testing
split_index = int(0.8 * len(categories))
X_train, X_test = categories[:split_index], categories[split_index:]
y_train, y_test = y_category_encoded[:split_index], y_category_encoded[split_index:]

# Vectorize the text data for Random Forest
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_train_rf = vectorizer.fit_transform(X_train)
X_test_rf = vectorizer.transform(X_test)

# Create the Random Forest classifier with adjusted hyperparameters
rf_model = RandomForestClassifier(n_estimators=100, max_depth=1, min_samples_split=2)

# Train the Random Forest classifier
rf_model.fit(X_train_rf, y_train)

# Use the trained Random Forest model to predict
X_test_rf_predictions = rf_model.predict(X_test_rf)

# Calculate accuracy for category classification using Random Forest
accuracy_category_rf = accuracy_score(y_test, X_test_rf_predictions)
print("Accuracy for Category Classification (Random Forest):", accuracy_category_rf)

# Generate the classification report for Random Forest
report_rf = classification_report(y_test, X_test_rf_predictions, labels=np.unique(y_test), target_names=label_encoder_category.classes_)
print("Classification Report for Category Classification (Random Forest):\n", report_rf)

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Load your Excel dataset
data = pd.read_excel("/content/drive/MyDrive/SA/Restaurant.xlsx")

# Split data into categories and sentiments
categories = data['Polarity'].astype(str)
polarities = data['Polarity'].astype(str)

# Convert category labels to categorical format
label_encoder_category = LabelEncoder()
y_category_encoded = label_encoder_category.fit_transform(categories)

# Use fixed 80% of data for training and 20% for testing
split_index = int(0.8 * len(categories))
X_train, X_test = categories[:split_index], categories[split_index:]
y_train, y_test = y_category_encoded[:split_index], y_category_encoded[split_index:]

# Vectorize the text data for Random Forest
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_train_rf = vectorizer.fit_transform(X_train)
X_test_rf = vectorizer.transform(X_test)

# Create the Random Forest classifier with adjusted hyperparameters
rf_model = RandomForestClassifier(n_estimators=10, max_depth=1, min_samples_split=2)

# Train the Random Forest classifier
rf_model.fit(X_train_rf, y_train)

# Use the trained Random Forest model to predict
X_test_rf_predictions = rf_model.predict(X_test_rf)

# Calculate accuracy for category classification using Random Forest
accuracy_category_rf = accuracy_score(y_test, X_test_rf_predictions)
print("Accuracy for Category Classification (Random Forest):", accuracy_category_rf)

# Generate the classification report for Random Forest
report_rf = classification_report(y_test, X_test_rf_predictions, labels=np.unique(y_test), target_names=label_encoder_category.classes_)
print("Classification Report for Category Classification (Random Forest):\n", report_rf)
