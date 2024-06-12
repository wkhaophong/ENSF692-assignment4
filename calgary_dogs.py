# calgary_dogs.py
# AUTHOR NAME
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.
import pandas as pd

def analyze_data(data, breed):
    # Masking operation to filter data for the selected breed
    breed_data = data[data.index.get_level_values('Breed').str.upper() == breed.upper()]
    
    # Grouping by Year
    grouped_data = breed_data.groupby(level='Year')

    # Multi-index slicing
    idx = pd.IndexSlice

    # Find all years where the selected breed was listed in the top breeds
    years = breed_data.index.get_level_values('Year').unique()
    years_str = " ".join(str(year) for year in years)
    print(f"The {breed.upper()} was found in the top breeds for years: {years_str}")

    #Print total register
    total_registrations = breed_data['Total'].sum()
    print(f"There have been {total_registrations} {breed} dogs registered total.")

    # Group by Year and calculate total registrations for each year
    for year, year_data in grouped_data:
        # Multi-index slicing to filter data for the current year
        year_data = year_data.loc[idx[year, :], :]
        year_registrations = year_data['Total'].sum()
        total_registrations_all_breeds = data.loc[idx[year, :], 'Total'].sum()
        percentage = (year_registrations / total_registrations_all_breeds) * 100
        print(f"The {breed} was {percentage:.6f}% of top breeds in {year}")

     # Calculate percentage of registrations out of total across all years
    total_registrations_all_years = data['Total'].sum()
    total_percentage = (total_registrations / total_registrations_all_years) * 100
    print(f"The {breed} was {total_percentage:.6f}% of top breeds across all years.")

    # Count the occurrences of each month for the selected breed
    month_counts = breed_data['Month'].value_counts()

    # Find the maximum count
    max_counts = month_counts.max()
    #print(max_counts)
    popular_months = month_counts[month_counts == max_counts].index.tolist()
    popular_months.sort()
    print("Most popular month(s) for {} dogs: {}".format(breed, " ".join(popular_months)))


def main():
    # Import data here
    data = pd.read_excel('CalgaryDogBreeds.xlsx')
    print("ENSF 692 Dogs of Calgary")

    # Convert 'Breed' column to uppercase for consistency
    data["Breed"] = data["Breed"].str.upper()

    # Set multi-index with Year and Breed
    data.set_index(['Year', 'Breed'], inplace=True)

    # User input stage
    while True:
        try:
            breed_input = input("Please enter a dog breed: ").strip().upper()
            if breed_input not in data.index.get_level_values('Breed'):
                raise KeyError("Dog breed not found in the data. Please try again.")
        
            analyze_data(data, breed_input)
            break
        except KeyError as e:
            print(e)

if __name__ == '__main__':
    main()