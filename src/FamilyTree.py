from PersonFactory import PersonFactory

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

        # TODO: Implement Child Logic Here
        # For testing, create one child and hardcode first person names (REMOVE BEFORE FINAL SUBMISSION)
        self.first_person_1.set_first_name("Desmond")
        self.first_person_1.set_last_name("Original")
        self.first_person_1.set_gender("male")
        self.first_person_2.set_first_name("Molly")
        self.first_person_2.set_last_name("Original")
        self.first_person_2.set_gender("female")
        child = pf.get_person(1985, 
                              [self.first_person_1, self.first_person_2], 
                              [self.first_person_1.get_last_name(), self.first_person_2.get_last_name()]
                              )
        self.first_person_1.set_children([child])
        self.first_person_2.set_children([child])

    
    # TODO: Implement CLI and Relevant Traversal Functions
    # Driver
    def main(self):
        pf = PersonFactory()
        print("Reading files...")
        pf.read_files()
        print("Building family tree...")
        self.build_tree(pf)
        print("Are you interested in:")
        print("(T)otal number people in the tree")
        print("Total number of people in the tree by (D)ecade")
        print("(N)ames duplicated")
        answer = input()

        # Remove
        print(answer)



if __name__ == "__main__":
    ft = FamilyTree()
    ft.main()