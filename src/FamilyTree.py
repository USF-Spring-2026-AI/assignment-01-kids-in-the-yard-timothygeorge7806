from PersonFactory import PersonFactory
from collections import deque
import math
import random
import numpy as np

class FamilyTree:
    first_person_1 = None
    first_person_2 = None

    def __init__(self):
        self.first_person_1 = None
        self.first_person_2 = None

    # Build the tree
    def build_tree(self, pf):
        # Create the first two people
        self.first_person_1 = pf.get_person(1950, None, None)
        self.first_person_2 = pf.get_person(1950, None, None)
        self.first_person_1.set_spouse(self.first_person_2)
        self.first_person_2.set_spouse(self.first_person_1)

        # Create the first children and build the rest of the tree
        search_year = math.floor(int(self.first_person_1.get_birth_year())/10) * 10
        child_rate = list(pf.get_birth_and_marriage_rates().get(str(search_year)).values())[0]
        children = []
        num_children = max(0, random.randint(round(child_rate - 1.5), round(child_rate + 1.5)))
        eldest_birth_year = min(self.first_person_1.get_birth_year(), self.first_person_2.get_birth_year())
        children_floats = np.linspace(eldest_birth_year + 25, eldest_birth_year + 45, num_children)
        children_ages = [round(x) for x in children_floats]
        for child_birth_year in children_ages:
            if (child_birth_year > 2120):
                continue
            elif(num_children <= 0):
                break
            elif self.first_person_1.get_death_year() < child_birth_year and self.first_person_2.get_death_year() < child_birth_year:
                break
            child = pf.get_person(child_birth_year, 
                                  [self.first_person_1, self.first_person_2], 
                                  [self.first_person_1.get_last_name(), self.first_person_2.get_last_name()]
                                  )
            children.append(child)
        self.first_person_1.set_children(children)
        self.first_person_2.set_children(children)


    # Get the total number of people in the tree
    def person_count(self):
        visited = []
        queue = deque()
        queue.append(self.first_person_1)
        visited.append(self.first_person_1)

        while len(queue) != 0:
            current = queue.popleft()
            if current.get_spouse():
                visited.append(current.get_spouse())
            for child in current.get_children():
                if child not in visited:
                    visited.append(child)
                    queue.append(child)
        return len(visited)

    # Get and print total number of people in the tree by decade (Debug)
    def person_count_by_decade(self):
        count_by_decade = {}

        visited = []
        queue = deque()
        queue.append(self.first_person_1)
        visited.append(self.first_person_1)
        while len(queue) != 0:
            current = queue.popleft()
            birth_year_decade = math.ceil(int(current.get_birth_year())/10) * 10
            if birth_year_decade not in count_by_decade.keys():
                count_by_decade.setdefault(birth_year_decade, 1)
            else:
                count_by_decade[birth_year_decade] = count_by_decade.get(birth_year_decade) + 1
            
            if current.get_spouse():
                visited.append(current.get_spouse())
                spouse_birth_year_decade = math.ceil(int(current.get_spouse().get_birth_year())/10) * 10
                if spouse_birth_year_decade not in count_by_decade.keys():
                    count_by_decade.setdefault(spouse_birth_year_decade, 1)
                else:
                    count_by_decade[spouse_birth_year_decade] = count_by_decade.get(spouse_birth_year_decade) + 1
            for child in current.get_children():
                if child not in visited:
                    visited.append(child)
                    queue.append(child)

        # Print counts
        start_year = 1950
        total = 0
        while(start_year <= 2120):
            if start_year in count_by_decade.keys():
                total += count_by_decade.get(start_year)
            print(str(start_year) + ": " + str(total))
            start_year += 10
        return

    # Get all names that appear more than once
    def names_duplicated(self):
        name_occurences = {}

        visited = []
        queue = deque()
        queue.append(self.first_person_1)
        visited.append(self.first_person_1)
        while len(queue) != 0:
            current = queue.popleft()
            name = current.get_first_name() + " " + current.get_last_name()
            if name not in name_occurences.keys():
                name_occurences.setdefault(name, 1)
            else:
                name_occurences[name] = name_occurences.get(name) + 1
            
            if current.get_spouse():
                visited.append(current.get_spouse())
                spouse_name = current.get_spouse().get_first_name() + " " + current.get_spouse().get_last_name()
                if spouse_name not in name_occurences.keys():
                    name_occurences.setdefault(spouse_name, 1)
                else:
                    name_occurences[spouse_name] = name_occurences.get(spouse_name) + 1
            for child in current.get_children():
                if child not in visited:
                    visited.append(child)
                    queue.append(child)
        
        # Print all duplicate names
        duplicated_names = []
        for name in name_occurences.keys():
            if name_occurences[name] > 1:
                duplicated_names.append(name)
        print("There are " + str(len(duplicated_names)) + " duplicate names in the tree:")
        for name in duplicated_names:
            print("* " + name)

    # Driver
    def main(self):
        pf = PersonFactory()
        print("Reading files...")
        pf.read_files()
        print("Building family tree...")
        self.build_tree(pf)
        while(True):
            print("Are you interested in:")
            print("(T)otal number people in the tree")
            print("Total number of people in the tree by (D)ecade")
            print("(N)ames duplicated")
            print("(E)xit")
            answer = input()
            if answer == 'T':
                print(self.person_count())
            elif answer == 'D':
                self.person_count_by_decade()
            elif answer == 'N':
                self.names_duplicated()
            elif answer == 'E':
                return 0
            else:
                print("Invalid input. Please try again")



if __name__ == "__main__":
    ft = FamilyTree()
    ft.main()