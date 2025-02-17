import pandas as pd
import random
from faker import Faker
import numpy as np

def make_fake_database(columns,multiple={},n=30):
    
    fake = Faker()
    Faker.seed(42)  # Ensures repeatability
    random.seed(42)

    # Generate 30 fake employees
    data = []
    for _ in range(30):

        name = fake.first_name()
        surname = fake.last_name()
        nationality = fake.country()

        column_names = ['name','surname','nationality']

        data.append([name, surname, nationality])

        for key in columns.keys():
            
            if key in multiple.keys():
                column = ", ".join(random.sample(columns[key], random.randint(multiple[key][0], multiple[key][1])))
            else:
                column = random.choice(columns[key])  

            data[-1].append(column)
            column_names.append(key)

    # Create DataFrame
    df = pd.DataFrame(data, columns=column_names)

    return df

def add_missing_data(df,missing_percentage=0.2,opt=2):
    
    df_missing = df.copy()

    if opt == 1:
        for col in df_missing.columns:
            df_missing.loc[df_missing.sample(frac=missing_percentage).index,col] = np.nan
    elif opt == 2:
        # Creating mask with True or False (with a certain percent of True) with the same shape of the DataFrame
        mask = np.random.choice([True, False], size=df_missing.shape, p=[missing_percentage, 1-missing_percentage])
        df_missing[mask] = np.nan
        
    return df_missing


if __name__ == "__main__":
    columns = {
        'roles': ["Librarian", "Archivist", "Cataloguer", "Research Assistant", "Digital Preservationist"],
        'skills': ["Data Management", "Rare Book Handling", "Coding", "Multilingual Research", "Metadata Tagging", "Customer Service", "AI-based Cataloging", "3D Printing"],
        'planets': ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    }

    df_raw = make_fake_database(columns=columns,multiple={'skills':(1,4)},n=30)

    df = add_missing_data(df=df_raw, missing_percentage=0.1)

    # Save to CSV
    df.to_csv("library_employees.csv", index=False)