# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 20:28:23 2025

@author: Russell Engle
@model: chatGPT-4o
"""

from genderize import Genderize


class Gender:
    def __init__(self, api_key=None):
        """
        Initialize the Gender class with an optional API key for Genderize.io.
        """
        self.api_key = api_key
        self.genderize = Genderize(api_key=api_key) if api_key else Genderize()

    def predict(self, names):
        """
        Predicts gender for a first name string or list of first name strings.

        Args:
            names (string): first name (string)
            names (list): List of first names

        Returns:
            list of dict: Each dict contains name, gender, probability, and count
        """
        try:
            if isinstance(names, str):
                results = self.genderize.get1(names)
                return results
            elif isinstance(names, list):
                results = self.genderize.get(names)
                return results
            else:
                raise TypeError("Input must be a string or a list of strings")
        except Exception as e:
            print(f"[ERROR] Failed to fetch gender data: {e}")
            return []


def display_gender_predictions(predictions):
    """
    Display name-gender prediction results in a formatted table.

    Parameters:
        predictions (list of dict): Each dict should contain keys 'name', and optionally 'gender', 'probability', and 'count'.
    """
    for result in predictions:
        name = result['name']
        gender = result.get('gender', 'unknown')
        probability = result.get('probability', 0)
        count = result.get('count', 0)
        print(f"Name: {name:<10} | Gender: {gender:<7} | Probability: {probability:.2f} | Sample Size: {count}")


def main():
    # Instantiate the Gender class (without API key for free use)
    gender_predictor = Gender()

    # Test names
    names = ['Alice', 'Chie', 'John', 'Taylor', 'Jordan', 'Chen', 'Sasha', 'Sean', 'Sterling']

    # Get predictions
    rse = gender_predictor.predict("Russell")
    print(rse)

    predictions = gender_predictor.predict(names)
    display_gender_predictions(predictions)

"""
    # Display results
    for result in predictions:
        name = result['name']
        gender = result.get('gender', 'unknown')
        probability = result.get('probability', 0)
        count = result.get('count', 0)
        print(f"Name: {name:<10} | Gender: {gender:<7} | Probability: {probability:.2f} | Sample Size: {count}")
"""

if __name__ == "__main__":
    main()
