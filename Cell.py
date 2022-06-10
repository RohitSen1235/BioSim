from abc import ABC,abstractmethod
from Animal import Herbivore,Carnivore
import random as random
from math import e


class Cell(ABC):
    """
    This class represents one unit cell of the island
    """
   
    
    @classmethod
    def set_cell_parameter(cls,new_parameter):

            if new_parameter['f_max'] < 0:
                raise ValueError("Parameter must be positive")
            else:
                cls.p=new_parameter

    @classmethod
    def get_cell_parameter(cls):
        """
        This function returns the parameter of selected cell type
        - cell type should be either 'H' or 'L' 
        """
        return cls.p
    
    @abstractmethod
    def from_map_char(cls,location,char_cell_type,neighbours):
        """
        This is  an abstract function for creating cells of different types
        -the actual implementation for each type SHOULD be present in all the respective derived classes
        """

        

    @abstractmethod
    def populate_cell(self,animal_dict):
        """
        populating the cell with animals as specified in the input dict
        """


    def grow_fodder(self):
        """
        depending on the type of cell the maximumm fodder possible is grown
        """
        self.f_max=self.p.get('f_max')
    
    
    def increment_age_of_animals(self):
        """
        Incrementing the age of animals in the cell
        """
        for herb in self.herbivores:
            herb.aging()
        for carn in self.carnivores:
            carn.aging()


    def feed_herbivore(self):
        """
        Feeding Herbivores
        """
        random.shuffle(self.herbivores)
        for herb in self.herbivores:
            herb.eat_food(self)
            herb.Compute_fitness()


    def feed_carnivore(self,sorted_herbivores):
        """
        Feeding Carnivores
        """
        # carnivores feeding
        random.shuffle(self.carnivores)
        for carn in self.carnivores:
            killed_herbivores=carn.eat_food(sorted_herbivores)
            carn.Compute_fitness()
            # print(f"prey killed by {carn} loc:{self.location} >> {len(killed_herbivores)}")
            # removing killed herbivores
            for herb in killed_herbivores:
                sorted_herbivores.remove(herb)

        return sorted_herbivores


    def animals_reproduce(self):
        """
        Animals reproduce is there are more than one of the same species in a given cell
        """
        new_herbivores=[]
        new_carnivores=[]
        n_herbs=self.count_herbivores()
        n_carns=self.count_carnivores()

        for herb in self.herbivores:
            had_offspring,birth_weight=herb.reproduce(n_herbs)

            if had_offspring:
                new_herbivores.append(Herbivore(age=0,weight=birth_weight))
        
        for carn in self.carnivores:
            had_offspring,birth_weight=carn.reproduce(n_carns)

            if had_offspring:
                new_carnivores.append(Carnivore(age=0,weight=birth_weight))

        self.carnivores += new_carnivores
        self.herbivores += new_herbivores

        return len(self.herbivores),len(self.carnivores)


    def migrate_animals(self):
        """
        Moves the animals qualified for migration from present cell to neighbouring cells selected randomly
        """
        migrating_animals_list=[]
        if len(self.neighbours) != 0:
            for herb in self.herbivores:
                if not herb.has_moved and herb.migrate():
                    chosen_cell=random.choice(self.neighbours)
                    migration_dict={'loc':chosen_cell,'species':'Herbivore', 'age': herb.age ,'weight':herb.weight}
                    migrating_animals_list.append(migration_dict)
                    self.herbivores.remove(herb)

            for carn in self.carnivores:
                if not carn.has_moved and carn.migrate():
                    chosen_cell=random.choice(self.neighbours)
                    migration_dict={'loc':chosen_cell,'species':'Carnivore', 'age': carn.age ,'weight':carn.weight}
                    migrating_animals_list.append(migration_dict)
                    self.carnivores.remove(carn)

            if len(migrating_animals_list)!=0:
                return migrating_animals_list
            else:
                return None
        else:
            return None


    def add_animal(self,dict):
        """
        moving migrated animals to respective cell
        """
        if type(self) is not type(water_cell):

            if dict['species']=='Herbivore':

               self.herbivores.append(Herbivore(dict['age'],dict['weight'],has_moved=True))
            
            elif dict['species']=='Carnivore':
               
               self.carnivores.append(Carnivore(dict['age'],dict['weight'],has_moved=True))

            else :
                raise ValueError (f"Species NOT Defined")   
            
        else:
               
            raise ValueError (f"Animals can NOT be place in Water, double check location : {self.location} ")


    def weight_loss(self):
        """
        yearly natural weight loss
        """
        for herb in self.herbivores:
            herb.natural_weight_loss()

        for carn in self.carnivores:
            carn.natural_weight_loss()


    def animal_death(self):
        """
        Checking for death of animals due to natural causes
        """
        dead_herbivores=[]
        dead_carnivores=[]
        for herb in self.herbivores:
            if herb.evaluate_death():
                dead_herbivores.append(herb)
                self.herbivores.remove(herb)

        for carn in self.carnivores:
            if carn.evaluate_death():
                dead_carnivores.append(carn)
                self.carnivores.remove(carn)

        return (dead_herbivores,dead_carnivores)


    def count_herbivores(self)->int:
        """ 
        returns the number of herbivores present in the cell
        """
        return len(self.herbivores)


    def count_carnivores(self)->int:
        """
        returns the number of carnivores present in the cell
        """
        return len(self.carnivores)


# derived class representing water cells
class water_cell(Cell):

    def __init__(self,loc=(1,1),neigh=[]):
        """cnstructor for water cell"""
        self.location=loc
        self.neighbours=neigh
        self.f_max=0.0
        self.herbivores=[]
        self.carnivores=[]

    # property of water type cell
    p={'f_max':0.0}

    # creating a cell of type water
    @classmethod
    def from_map_char(cls,location,neighbours):
        """
        This function creates the cells of type water
        """
        return cls(location,neighbours)

    # populating cell
    def populate_cell(self,animal_dict):
        """
        Can not populate cel of type water
        """
        raise ValueError (f"Animals can NOT be place in Water, please double check location : {self.location} ")

# derived class representing desert cells
class desert_cell(Cell):

    def __init__(self,loc=(1,1),neigh=[]):
        """cnstructor for desert cell"""
        self.location=loc
        self.neighbours=neigh
        self.f_max=0.0
        self.herbivores=[]
        self.carnivores=[]


    # property of water type cell
    p={'f_max':0.0}

    # creating a cell of type desert
    @classmethod
    def from_map_char(cls,location,neighbours):
        """
        This function creates the cells of type desert
        """
        return cls(location,neighbours)

    # populating cell
    def populate_cell(self,animal_dict):
        """
        populating the cell with animals as specified in the input dict
        """
        for dict in animal_dict:
            if dict['species']=='Herbivore':
                self.herbivores.append(Herbivore(dict['age'],dict['weight']))
            elif dict['species']=='Carnivore':
                self.carnivores.append(Carnivore(dict['age'],dict['weight']))    

# derived class representing lowland cells
class lowland_cell(Cell):

    def __init__(self,loc=(1,1),neigh=[]):
        """cnstructor for lowland cell"""
        self.location=loc
        self.neighbours=neigh
        self.f_max=0.0
        self.herbivores=[]
        self.carnivores=[]


    # property of water type cell
    p={'f_max':800.0}


    # creating a cell of type lowland
    @classmethod
    def from_map_char(cls,location,neighbours):
        """
        This function creates the cells of type lowland
        """
        return cls(location,neighbours)

    # populating cell
    def populate_cell(self,animal_dict):
        """
        populating the cell with animals as specified in the input dict
        """
        for dict in animal_dict:
            if dict['species']=='Herbivore':
                self.herbivores.append(Herbivore(dict['age'],dict['weight']))
            elif dict['species']=='Carnivore':
                self.carnivores.append(Carnivore(dict['age'],dict['weight']))    
   

# derived class representing highland cells
class highland_cell(Cell):

    def __init__(self,loc=(1,1),neigh=[]):
        """cnstructor for highland cell"""
        self.location=loc
        self.neighbours=neigh
        self.f_max=0.0
        self.herbivores=[]
        self.carnivores=[]



    # property of water type cell
    p={'f_max':300.0}


    # creating a cell of type highland
    @classmethod
    def from_map_char(cls,location,neighbours):
        """
        This function creates the cells of type highland 
        """
        return cls(location,neighbours)

    # populating cell
    def populate_cell(self,animal_dict):
        """
        populating the cell with animals as specified in the input dict
        """
        for dict in animal_dict:
            if dict['species']=='Herbivore':
                self.herbivores.append(Herbivore(dict['age'],dict['weight']))
            elif dict['species']=='Carnivore':
                self.carnivores.append(Carnivore(dict['age'],dict['weight']))    
