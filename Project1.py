# Name: Mo Pofahl
# Student ID: 55794521
# Email: mopofahl@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# Used ChatGPT for help with my unit tests and some pandas functions
#used chatgpt to help convert dictionary to a dataframe for csv output
#I also used pandas in my code as I have learned how to use it in SI261 

import pandas as pd
import unittest

#loading data
def load_data(filename):
    return pd.read_csv(filename)


#calculations
#Calculate the average body mass (g) by species and sex.
    #Uses columns: species, sex, body_mass_g
    #Returns a dictionary { (species, sex): avg_mass }
def calculate_avg_mass_by_species_sex(data):
    avg_mass = data.groupby(['species', 'sex'])['body_mass_g'].mean().round(2)
    return avg_mass.to_dict()

#Calculate average flipper length (mm) by island and species.
#Uses columns: island, species, flipper_length_mm
#Returns dictionary { (island, species): avg_flipper }
def calculate_avg_flipper_by_island_species(data):
    avg_flipper = data.groupby(['island', 'species'])['flipper_length_mm'].mean().round(2)
    return avg_flipper.to_dict()


#output
def write_results_to_csv(results, filename):
    # Convert dictionary to list of rows
    rows = []
    for (category_1, category_2), avg_value in results.items():
        rows.append([category_1, category_2, avg_value])
    
    #Creating DataFrame and write to CSV
    df = pd.DataFrame(rows, columns=["Category_1", "Category_2", "Average_Value"])
    df.to_csv(filename, index=False)
    print(f"Results written to {filename}")

# Unit tests

class TestPenguinAnalysis(unittest.TestCase):

    def setUp(self):
        self.test_data = pd.DataFrame({
            "species": ["Adelie", "Adelie", "Adelie", "Chinstrap"],
            "sex": ["Male", "Male", "Female", "Male"],
            "body_mass_g": [3500, 3700, 3300, 3800],
            "island": ["Torgersen", "Torgersen", "Dream", "Torgersen"],
            "flipper_length_mm": [180, 190, 220, 210]
        })
        
    def test_calculate_avg_mass_by_species_sex(self):
        result = calculate_avg_mass_by_species_sex(self.test_data)
        
        # the test for normal values
        self.assertEqual(result[("Adelie", "Male")], 3600.0)
        self.assertEqual(result[("Adelie", "Female")], 3300.0)
        
        # the edge case: missing body_mass_g should still be calculated 
        test_data_with_missing = self.test_data.copy()
        test_data_with_missing.loc[2, "body_mass_g"] = None  # Setting one value to None
        result = calculate_avg_mass_by_species_sex(test_data_with_missing)
        self.assertTrue(("Adelie", "Female") in result)
        
        # Edge case: group with all missing body_mass_g should produce NaN but keep key
        all_missing_mass = pd.DataFrame({
            "species": ["Adelie", "Adelie"],
            "sex": ["Male", "Female"],
            "body_mass_g": [float("nan"), float("nan")],
            "island": ["Torgersen", "Dream"],
            "flipper_length_mm": [180, 190]
        })
        result = calculate_avg_mass_by_species_sex(all_missing_mass)
        self.assertTrue(pd.isna(result[("Adelie", "Male")]))

    def test_calculate_avg_flipper_by_island_species(self):
        """Test flipper calculation."""
        result = calculate_avg_flipper_by_island_species(self.test_data)
        
        # Test for normal values
        self.assertEqual(result[("Torgersen", "Adelie")], 185.0)
        self.assertEqual(result[("Dream", "Adelie")], 220.0)

        # Edge case: missing flipper value, should still be calculated 
        test_data_with_missing = self.test_data.copy()
        test_data_with_missing.loc[2, "flipper_length_mm"] = None  # Set one value to None
        result = calculate_avg_flipper_by_island_species(test_data_with_missing)
        self.assertTrue(("Dream", "Adelie") in result)
        
        # Edge case: group with all missing flipper lengths should return NaN but keep key
        all_missing_flipper = pd.DataFrame({
            "species": ["Adelie", "Adelie"],
            "sex": ["Male", "Female"],
            "body_mass_g": [3500, 3600],
            "island": ["Torgersen", "Torgersen"],
            "flipper_length_mm": [float("nan"), float("nan")]
        })
        result = calculate_avg_flipper_by_island_species(all_missing_flipper)
        self.assertTrue(pd.isna(result[("Torgersen", "Adelie")]))

# main execution

def main():
    data = load_data("penguins.csv")

    avg_mass = calculate_avg_mass_by_species_sex(data)
    avg_flipper = calculate_avg_flipper_by_island_species(data)

    write_results_to_csv(avg_mass, "average_mass_results.csv")
    write_results_to_csv(avg_flipper, "average_flipper_results.csv")

    print("All calculations complete!")

if __name__ == "__main__":
    main()
    unittest.main()
