import cv2
import pytesseract
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np


# Function to preprocess the image
def preprocess_image(image_path):
    try:
        # Read the image
        image = cv2.imread(image_path)

        # Debugging: Confirm the image path and its existence
        if image is None:
            raise FileNotFoundError(f"Failed to load image: {image_path}. Check if the file exists and the path is correct.")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to enhance poorly lit areas
        enhanced_image = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Apply GaussianBlur for noise reduction
        denoised_image = cv2.GaussianBlur(enhanced_image, (5, 5), 0)

        return denoised_image
    except Exception as e:
        print(f"Error in preprocessing image {image_path}: {e}")
        raise


# Function to perform OCR with advanced settings
def perform_ocr(image_path):
    try:
        # Preprocess the image
        processed_image = preprocess_image(image_path)

        # Perform OCR using pytesseract
        custom_config = r'--oem 3 --psm 6 --dpi 300'  # High dpi for better accuracy
        text = pytesseract.image_to_string(processed_image, config=custom_config)

        return text
    except Exception as e:
        print(f"Error during OCR for image {image_path}: {e}")
        raise


# Function to write the OCR output to a text file (Notepad or plain text)
def write_to_file(text, output_path):
    try:
        with open(output_path, 'a', encoding='utf-8') as file:  # 'a' for appending to the file
            file.write(text)
            file.write("\n\n")  # Add space between different image outputs
        print(f"Output successfully written to {output_path}")
    except Exception as e:
        print(f"Error writing to file {output_path}: {e}")


# Function to generate the next sequential file name (e.g., 1.txt, 2.txt, etc.)
def generate_sequential_filename(directory):
    try:
        # Get a list of all files in the directory with .txt extension
        existing_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

        # Find the highest number in the existing files and increment it
        highest_number = 0
        for file in existing_files:
            try:
                # Extract the number from the file name
                number = int(file.split('.')[0])
                highest_number = max(highest_number, number)
            except ValueError:
                continue  # If the file name doesn't have a valid number, skip it

        # Generate the next sequential file name
        return os.path.join(directory, f"{highest_number + 1}.txt")
    except Exception as e:
        print(f"Error generating filename: {e}")
        raise


# Function to open the file dialog and select multiple image files
def select_image_files():
    try:
        # Create a Tkinter root window but keep it hidden
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Open the file dialog to select multiple image files
        file_paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[("All Files", "*.*")]
        )

        # Check if the user selected any files
        if not file_paths:
            print("No files selected.")
        else:
            print(f"Files selected: {file_paths}")

        return file_paths
    except Exception as e:
        print(f"Error in file selection: {e}")
        return []


# Main function to demonstrate OCR functionality
def main():
    try:
        # Ask the user to select multiple image files via the file dialog
        image_paths = select_image_files()

        # Check if no files were selected
        if not image_paths:
            print("No files selected. Exiting program.")
            return

        # Get the current directory for saving the output
        directory = os.getcwd()  # Current working directory

        # Ensure the directory exists (to avoid errors while saving)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Generate the next sequential file name (1.txt, 2.txt, etc.)
        output_filename = generate_sequential_filename(directory)

        # Process each image and append the results to the same text file
        for image_path in image_paths:
            try:
                # Perform OCR and get the main extracted text
                text = perform_ocr(image_path)

                # Write the OCR results (main text) to the generated file name
                write_to_file(text, output_filename)
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

        print(f"All OCR results have been written to {output_filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
