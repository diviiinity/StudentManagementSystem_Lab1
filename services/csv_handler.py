import csv
import os


class CSVHandler:

    @staticmethod
    def load_data(file_path):
        """Load data from a CSV file and return a list of dictionaries."""
        data = []

        # If file doesn't exist, return empty list
        if not os.path.exists(file_path):
            return data

        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        return data

    @staticmethod
    def save_data(file_path, data, fieldnames):
        """Save a list of dictionaries to a CSV file."""
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)