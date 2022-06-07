from dataclasses import dataclass, field
from typing import List
from Cell import Cell,Cell_Type, desert_cell, highland_cell, lowland_cell


@dataclass
class Island():

    
    map: Cell = field(default_factory=list)
    size: tuple = field(init=False)
    


    def __str__(self) -> str:
        """
        str representation of the island
        """
        representation=f"Island Size:{self.size}\n"
        for cell in self.map:
            representation+=f"{cell.location}\t\tneigh:{cell.neighbours}\tTyp:{cell.type}\tf_max:{cell.f_max}\tn_herbs:{cell.count_herbivores()}\tn_carns:{cell.count_carnivores()}\n"
        return representation
        
    @classmethod
    def from_map_str(cls,map_str):
        """
        creates all the cells that make up the island from the string representation
        """

        Temp_map=[]
        valid_cell_types=['W','L','H','D']
        map_list=map_str.split()
        n_cols=len(map_list[0])
        n_rows=len(map_list)

        cls.size=(n_rows,n_cols)

        # checking for map inconsistency
        for i in range(1,n_rows):
            if len(map_list[i-1])!=len(map_list[i]):
                raise ValueError(f"Inconsistent Map!! all rows must be of same length")


        for i in range(0,n_rows):
            for j in range(0,n_cols):

                # checking boundary cells
                if map_list[0][j] !='W' or map_list[i][0]!='W' or map_list[-1][j]!='W' or map_list[i][-1]!='W' :

                    raise ValueError(f"Boundary cells need to be of type water (W): type {map_list[i][j]} not valid at ({i+1},{j+1})")

                # checking for invalid cell type type
                elif map_list[i][j] not in valid_cell_types:

                    raise ValueError(f"Cell type is not valid : type '{map_list[i][j]}' at ({i+1},{j+1}) is Undefined")

                else:
                    # finding neighbours for all cells which are not of type water
                    # naighbours are valid only if neighbours themself are also not of type water

                    # container to hold neighbours of current cell 
                    cell_neighbours=[]

                    if map_list[i][j] != 'W':
                        
                        cell_north=(i,j+1) if i>0 and map_list[i-1][j] !='W' else None
                        if cell_north is not None:
                            cell_neighbours.append(cell_north)

                        cell_south=(i+2,j+1) if i<n_rows-1 and map_list[i+1][j] !='W' else None
                        if cell_south is not None:
                            cell_neighbours.append(cell_south)

                        cell_west =(i+1,j) if j>0 and map_list[i][j-1] !='W' else None
                        if cell_west is not None:
                            cell_neighbours.append(cell_west) 
                            
                        cell_east =(i+1,j+2) if j<n_cols-1 and map_list[i][j+1] !='W' else None
                        if cell_east is not None:
                            cell_neighbours.append(cell_east)

                    if map_list[i][j] == 'D':
                        # creating cell of type desert
                        Temp_map.append(desert_cell.from_map_char((i+1,j+1),neighbours=cell_neighbours))  
                    
                    elif map_list[i][j] == 'L':
                        # creating cell of type lowland
                        Temp_map.append(lowland_cell.from_map_char((i+1,j+1),neighbours=cell_neighbours))  

                    elif map_list[i][j] == 'H':
                        # creating cell of type highland
                        Temp_map.append(highland_cell.from_map_char((i+1,j+1),neighbours=cell_neighbours))  
                    
        
        return cls(Temp_map)

    
    def set_island_str_representation(self,map_str):
        """
        setting string representation of map
        """
        self.map_str_representation=map_str

    
    def populate_island(self,population_dict):
        """
        creates all the initial animals in the island from population dictionary 
        """
        if type(population_dict) == list:
            for dict in population_dict:

                for cell in self.map:

                    if dict['loc']== cell.location: 
                        cell.populate_cell(dict['pop'])

        else:
            raise ValueError(f"population_dict should be a list of dicts! this input was of type:{type(population_dict)}")
        
    
    def grow_fodder(self):
        """
        Grows fodder for the herbivores to consume
        Once every year
        """
        for cell in self.map:
            cell.grow_fodder()
        

    def feeding(self):
        """
        Feeding happens in an order
        1)All Herbivores(in random order) consume fodder
        2)All Carnivores(in random order) Hunt and kill Herbivores from least fittest to most fittest 
        """
        # Feeding all the herbivores
        for cell in self.map:
            if len(cell.herbivores) !=0:
                # print(cell.herbivores)
                cell.feed_herbivore()

        all_herbivores=[]
        # sorting the herbivores according to fitness
        for cell in self.map:
            for herb in cell.herbivores:
                all_herbivores.append(herb)

        sorted_herbivores=sorted(all_herbivores, key=lambda herb: herb.fitness)
        # print(sorted_herbivores)
        
        # feeding all the carnivores
        for cell in self.map:
            if len(sorted_herbivores)!=0 and len(cell.carnivores) !=0:
                updated_list=cell.feed_carnivore(sorted_herbivores)
                sorted_herbivores=updated_list

        herbs_killed=len(all_herbivores)-len(sorted_herbivores)

        return herbs_killed


    def reproduction(self):
        """
        this function represents the mating season in the simulation
        """
        new_herbs=0
        new_carns=0
        for cell in self.map:
            n_H,n_C=cell.animals_reproduce()
            new_herbs+=n_H
            new_carns+=n_C

        return new_herbs,new_carns


    def migration(self):
        """
        computes all the migrations and updates all the cells 
        """
        migrating_animals_list=[]
        n_migrations=0
        for cell in self.map:
            # get list(dict) of migrating animals in each cell
            migrating_animals_list=cell.migrate_animals()
            
            if migrating_animals_list is not None:

                n_migrations+=len(migrating_animals_list)
                # each dict represents one animal which migrated
                # {'loc':chosen_cell,'species':'Carnivore'/'herbivore', 'age': carn.age ,'weight':carn.weight}
                for dict in migrating_animals_list:
                    # match cell location and add the animal to that cell
                    for target_cell in self.map:
                        if target_cell.location == dict.get('loc'):
                            target_cell.add_animal(dict)
                        

        return n_migrations       


    def reset_migration(self):
        """
        reseting migration information for all animals in island
        """
        for cell in self.map:
            for herb in cell.herbivores:
                herb.has_moved=False

            for carn in cell.carnivores:
                carn.has_moved=False

    
    def aging(self):
        """
        increases the age of all animals by one year
        """
        for cell in self.map:
            cell.increment_age_of_animals()


    def animals_loose_weight(self):
        """
        Weight lose step of simulation
        """
        for cell in self.map:
            cell.weight_loss()


    def animals_die(self):
        """
        computes the death probability of all animals and removes the dead animals from the simulation for the next year
        """
        for cell in self.map:
            if (cell.count_herbivores() + cell.count_carnivores()) != 0:
                (dead_herbivores,dead_carnivores)=cell.animal_death()

                
    def num_animals(self):
        """
        Returns total number of animals present in the island
        """
        return self.num_herbs() + self.num_carns()


    def num_herbs(self):
        """
        returns number of herbivores
        """
        n_herbs=0
        for cell in self.map:
            num=len(cell.herbivores)
            if num  !=0:
                n_herbs+=num
        
        return n_herbs


    def num_carns(self):
        """
        returns number of carnivores
        """
        n_carns=0
        for cell in self.map:
            num=len(cell.carnivores)
            if num  !=0:
                n_carns+=num
        
        return n_carns


    # def update_pop_matrix(self):
    #     """
    #     Population matrix is used to plot the heat map of animal population
    #     """
        
    #     for cell in self.map:
    #         if cell.type is not Cell_Type.water:
    #             row=cell.location[0]-1
    #             col=cell.location[1]-1
    #             # print(f"{cell.location}:[{row},{col}]")
    #             self.herbivore_pop_matrix[row][col]=cell.count_herbivores()
    #             self.carnivore_pop_matrix[row][col]=cell.count_carnivores()
    #     #         herb_pop_matrix[row][col]=cell.count_herbivores()
    #     # print(herb_pop_matrix)

    def animal_weights(self):
        """
        returns weights of all herbivores and carnivores in list
        """
        herb_weights=[]
        carn_weights=[]

        for cell in self.map:
            for herb in cell.herbivores:
                herb_weights.append(herb.weight)
            for carn in cell.carnivores:
                carn_weights.append(carn.weight)   

        if not herb_weights:
            return [carn_weights]

        elif not carn_weights:
            return [herb_weights]
        
        else:
            return [herb_weights,carn_weights]


    def animal_ages(self):
        """
        returns ages of all herbivores and carnivores in list
        """
        herb_ages=[]
        carn_ages=[]

        for cell in self.map:
            for herb in cell.herbivores:
                herb_ages.append(herb.age)
            for carn in cell.carnivores:
                carn_ages.append(carn.age)   

        if not herb_ages:
            return [carn_ages]

        elif not carn_ages:
            return [herb_ages]
        
        else:
            return [herb_ages,carn_ages]

    
    def animal_fitnesses(self):
        """
        returns ages of all herbivores and carnivores in list
        """
        herb_fitnesses=[]
        carn_fitnesses=[]

        for cell in self.map:
            for herb in cell.herbivores:
                herb_fitnesses.append(herb.fitness)
            for carn in cell.carnivores:
                carn_fitnesses.append(carn.fitness)   

        if not herb_fitnesses:
            return [carn_fitnesses]

        elif not carn_fitnesses:
            return [herb_fitnesses]
        
        else:
            return [herb_fitnesses,carn_fitnesses]