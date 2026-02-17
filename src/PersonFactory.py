from Person import Person
import pandas as pd
import random
import math
import numpy as np

class PersonFactory:
    life_expectancy = {}
    gender_name_probability = {}
    first_names = {}
    last_names = {}
    birth_and_marriage_rates = {}

    # Constructor to initialize the PersonFactory with an empty life expectancy dictionary
    def __init__(self):
        self.life_expectancy = {}
        self.gender_name_probability = {}
        self.first_names = {}
        self.last_names = {}
        self.birth_and_marriage_rates = {}

    def read_files(self):
        # Get life expectancy by year
        df = pd.read_csv("life_expectancy.csv")
        self.life_expectancy = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

        # Get gender probability by decade
        df = pd.read_csv("gender_name_probability.csv")
        for _, row in df.iterrows():
            decade = row["decade"].rstrip("s")
            if decade not in self.gender_name_probability:
                self.gender_name_probability[decade] = {}
            self.gender_name_probability[decade][row["gender"]] = row["probability"]

        # Read first names
        df = pd.read_csv("first_names.csv")
        for _, row in df.iterrows():
            decade = row["decade"].rstrip("s")
            gender = row["gender"]
            if decade not in self.first_names:
                self.first_names[decade] = {}
            if gender not in self.first_names[decade]:
                self.first_names[decade][gender] = []
            self.first_names[decade][gender].append((row["name"], row["frequency"]))
        
        # Read last names and rank to probability
        df = pd.read_csv("rank_to_probability.csv", header=None)
        rank_to_probability = {rank + 1: prob for rank, prob in enumerate(df.iloc[0])}

        df = pd.read_csv("last_names.csv")
        for _, row in df.iterrows():
            decade = row["Decade"].rstrip("s")
            if decade not in self.last_names:
                self.last_names[decade] = []
            self.last_names[decade].append((row["LastName"], rank_to_probability[row["Rank"]]))

        # Read birth and marriage rates
        df = pd.read_csv("birth_and_marriage_rates.csv")
        for _, row in df.iterrows():
            decade = row["decade"].rstrip("s")
            if decade not in self.birth_and_marriage_rates:
                self.birth_and_marriage_rates[decade] = {}
            self.birth_and_marriage_rates[decade][row["marriage_rate"]] = row["birth_rate"]

    
    # Construct a person
    def get_person(self, year_born, parents, ancestor_last_names):
        person = Person()
        person.set_birth_year(int(year_born))
        # Generate death year
        year_died = year_born + random.randint(int(self.life_expectancy.get(year_born)) - 10, int(self.life_expectancy.get(year_born)) + 10)
        person.set_death_year(year_died)

        # Set parents
        if parents:
            person.set_parents(parents)
        
        # Convert birth year into valid dict key
        search_year = math.floor(int(year_born) / 10) * 10

        # Get gender based on probability
        gender_list = ['male', 'female']
        weights = [self.gender_name_probability.get(str(search_year)).get('male'), self.gender_name_probability.get(str(search_year)).get('female')]
        gender = random.choices(gender_list, weights=weights, k=1)[0]
        person.set_gender(gender)

        # Get first name using frequency
        names, name_weights = zip(*self.first_names.get(str(search_year)).get(gender))
        first_name = random.choices(names, weights=name_weights, k=1)[0]
        person.set_first_name(first_name)

        # Get last name
        if ancestor_last_names is not None: # Should only return true if descended from the first two people
            person.set_last_name(random.choice(ancestor_last_names))
        else:
            names, name_weights = zip(*self.last_names.get(str(search_year)))
            last_name = random.choices(names, weights=name_weights,k=1)[0]
            person.set_last_name(last_name)

        # Get Partner
        prob_partner = list(self.birth_and_marriage_rates.get(str(search_year)).keys())[0]
        
        has_partner = random.random() < prob_partner
        partner = None
        if has_partner and parents is not None: # Change later
            partner_year_born = year_born + random.randint(-10,10)
            partner = self._create_partner(partner_year_born)
            person.set_spouse(partner)
            partner.set_spouse(person)

        # Get Children
        if parents is not None: # If not one of the two original people
            child_rate = list(self.birth_and_marriage_rates.get(str(search_year)).values())[0]
            children = []
            # Get number of children
            num_children = 0
            if partner:
                num_children = max(0, random.randint(round(child_rate - 1.5), round(child_rate + 1.5)))
            else: 
                num_children = max(0, random.randint(round(child_rate - 1.5), round(child_rate + 1.5)) - 1)

            # Get ages of children
            eldest_birth_year = 0
            if partner:
                eldest_birth_year = min(year_born, partner.get_birth_year())
            else:
                eldest_birth_year = year_born

            children_floats = np.linspace(eldest_birth_year + 25, eldest_birth_year + 45, num_children)
            children_ages = [round(x) for x in children_floats]

            # Create children and add to parents' lists
            for child_birth_year in children_ages:
                if child_birth_year > 2120:
                    continue
                elif num_children <= 0:
                    break
                elif year_died < child_birth_year:
                    if partner and partner.get_death_year() < child_birth_year:
                        break
                    elif not partner:
                        break
                child_parents = [person, partner] if partner else [person]
                child = self.get_person(child_birth_year, child_parents, ancestor_last_names)
                children.append(child)
            person.set_children(children)
            if partner:
                partner.set_children(children)

        return person

    # Create a partner with basic attributes only
    def _create_partner(self, year_born):
        year_born = int(year_born)
        partner = Person()
        partner.set_birth_year(year_born)

        # Death year
        life_exp = self.life_expectancy.get(year_born)
        if life_exp is not None:
            partner.set_death_year(
                year_born + random.randint(int(life_exp) - 10, int(life_exp) + 10)
            )

        # Decade key
        search_year = str(math.floor(year_born / 10) * 10)

        # Gender
        gender_list = ['male', 'female']
        weights = [self.gender_name_probability.get(str(search_year)).get('male'), self.gender_name_probability.get(str(search_year)).get('female')]
        gender = random.choices(gender_list, weights=weights, k=1)[0]
        partner.set_gender(gender)

        # First name
        name_data = self.first_names[search_year][gender]
        names, name_weights = zip(*name_data)
        partner.set_first_name(random.choices(names, weights=name_weights, k=1)[0])

        # Last name from last_names.csv (partner is never a direct descendant)
        last_name_data = self.last_names[search_year]
        ln_names, ln_weights = zip(*last_name_data)
        partner.set_last_name(random.choices(ln_names, weights=ln_weights, k=1)[0])

        return partner

