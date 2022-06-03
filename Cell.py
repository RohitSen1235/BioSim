from dataclasses import dataclass, field
from queue import Empty

from pkg_resources import empty_provider
from Animal import Herbivore,Carnivore
import random as random
from math import e

# importing enum for enumerations
import enum
 
# creating enumerations using class
class Cell_Type(enum.Enum):
    water = 1
    desert = 2
    highland = 3
    lowland = 4

@dataclass
class Cell:
    """
    This class represents one unit cell of the island
    """
    location: tuple 
    type: Cell_Type
    neighbours: tuple = field(default_factory=list)
    f_max : float = 0.0
    herbivores: Herbivore = field(default_factory=list)
    carnivores: Carnivore = field(default_factory=list)
    
    p={
        'W': {'f_max':0.0},
        'L': {'f_max':800.0},
        'H': {'f_max':300.0},
        'D': {'f_max':0.0}
    }

    @classmethod
    def set_cell_parameter(cls,cell_type,new_parameter):

            if cell_type in ['H','L']:
                if new_parameter['f_max'] < 0:
                    raise ValueError("Parameter must be positive")
                else:
                    cls.p.update({cell_type:new_parameter})
            else:
                raise ValueError(f"parameters of cell type:{cell_type} can not be modified only 'H' and 'L' are allowed ")
    
    @classmethod
    def get_cell_parameter(cls,cell_type):
        
        if cell_type in ['H','L']:
            return cls.p[cell_type]
    
    @classmethod
    def from_map_char(cls,location,char_cell_type,neighbours):
        """
        This function creates the cells of various types according to the 
        """
        # creating a cell of water type
        if char_cell_type =='W':
            return cls(location=location,type=Cell_Type.water,neighbours=neighbours)
        # creating a cell of Lowland type
        elif char_cell_type =='L':
            return cls(location=location,type=Cell_Type.lowland,neighbours=neighbours,f_max=cls.p['L'])
        # creating a cell of Highland type
        elif char_cell_type =='H':
            return cls(location=location,type=Cell_Type.highland,neighbours=neighbours,f_max=cls.p['H'])
        # creating a cell of Desert type
        else:
            return cls(location=location,type=Cell_Type.desert,neighbours=neighbours)


    def populate_cell(self,animal_dict):
        """
        populating the cell with animals as specified in the input dict"""
        for dict in animal_dict:
            if self.type is not Cell_Type.water:
                if dict['species']=='Herbivore':
                    self.herbivores.append(Herbivore(dict['age'],dict['weight']))
                elif dict['species']=='Carnivore':
                    self.carnivores.append(Carnivore(dict['age'],dict['weight']))
            else:
                raise ValueError (f"Animals can NOT be place in Water, double check location : {self.location} ")

        # for herb in self.herbivores:
        #     herb.Compute_fitness()
        # for carn in self.carnivores:
        #     carn.Compute_fitness()

        for animal in self.herbivores+self.carnivores:
            animal.Compute_fitness()


    def grow_fodder(self):
        """
        depending on the type of cell the maximumm fodder possible is grown
        """
        if self.type == Cell_Type.lowland:
            self.f_max=800.0
        elif self.type ==Cell_Type.highland:
            self.f_max=300.0
        else:
            self.f_max=0
    
    
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
        if self.type is not Cell_Type.water:

            if dict['species']=='Herbivore':

               self.herbivores.append(Herbivore(dict['age'],dict['weight'],has_moved=True))
            
            elif dict['species']=='Carnivore':
               
               self.carnivores.append(Carnivore(dict['age'],dict['weight'],has_moved=True))
            
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