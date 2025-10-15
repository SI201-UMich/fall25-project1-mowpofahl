#SI 201 Project 1
# Your name: Mo Pofahl
# Your student id: 55794521
# Your email: mopofahl@umich.edu
# Worked with Zach Solomon, David Shin
# Use of AI: 


import pandas as pd

def load_data(csv_file):
    penguin_data = pd.read_csv(csv_file)
    return penguin_data

def calculate_mean_body_mass_by_sex(penguin_data):
    mean_body_mass_by_sex = penguin_data.groupby('sex')['body_mass_g'].mean().to_dict()
    return mean_body_mass_by_sex

def calculate_mean_body_mass_by_species(penguin_data):
    mean_body_mass_by_species = penguin_data.groupby('species')['body_mass_g'].mean().to_dict()
    return mean_body_mass_by_species