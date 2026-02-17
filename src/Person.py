class Person:
    # Person attributes
    birth_year = 0
    death_year = 0
    first_name = ""
    last_name = ""
    gender = ""
    # Person object
    spouse = None

    # List of Person objects
    children = []
    parents = []

    # Constructor to initialize a Person with default or provided values
    def __init__(self, first_name="", last_name="", birth_year=0, death_year=0,gender="not set"):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.spouse = None
        self.children = []
        self.parents = []
        self.gender = gender

    # --- Accessors (getters) ---

    # Returns the birth year of this person
    def get_birth_year(self):
        return self.birth_year

    # Returns the death year of this person
    def get_death_year(self):
        return self.death_year

    # Returns the first name of this person
    def get_first_name(self):
        return self.first_name

    # Returns the last name of this person
    def get_last_name(self):
        return self.last_name

    # Returns the spouse (Person object) of this person, or None if unmarried
    def get_spouse(self):
        return self.spouse

    # Returns the list of children (Person objects) of this person
    def get_children(self):
        return self.children
    
    def get_parents(self):
        return self.parents
    
    def get_gender(self):
        return self.gender

    # --- Mutators (setters) ---

    # Sets the birth year of this person
    def set_birth_year(self, birth_year):
        self.birth_year = birth_year

    # Sets the death year of this person
    def set_death_year(self, death_year):
        self.death_year = death_year

    # Sets the first name of this person
    def set_first_name(self, first_name):
        self.first_name = first_name

    # Sets the last name of this person
    def set_last_name(self, last_name):
        self.last_name = last_name

    # Sets the spouse (Person object) of this person
    def set_spouse(self, spouse):
        self.spouse = spouse

    # Sets the list of children (Person objects) of this person
    def set_children(self, children):
        self.children = children

    def set_parents(self, parents):
        self.parents = parents
    
    def set_gender(self, gender):
        self.gender = gender