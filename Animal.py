from dataclasses import dataclass,field
from abc import ABC,abstractmethod
import random as random
from math import e


def q(sign,x,x_half,phi):
    """Mathematical function to be used for calculating fitness"""
    return 1.0/(1.0+e**(sign*phi*(x-x_half)))


@dataclass
class Animal(ABC):
    """
    Abstract class for Representing Animals.
    **Subclasses**:
    - Herbivore class
    - Carnivore class
    """
    age: int 
    weight: float
    fitness: float = 0.0
    has_moved : bool = False

    def __str__(self) -> str:
        str_representation=f"{self.__class__.__name__} \tage:{self.age} \twt:{round(self.weight,3)} \tft:{round(self.fitness,4)} \tmig:{self.has_moved}"
        return str_representation
        

    def __lt__(self,other):
        """
        Defining lesser than (<) operator for sorting
        """
        return self.fitness < other.fitness


    @classmethod
    def set_parameters(cls,new_parameters):
        """
        This function will set/reset the parameters for animals
        """
        for key in new_parameters:
            if key not in cls.p:
                raise KeyError("Invalid key name: " + key)

        for key in cls.p:
            if key in new_parameters:
                if new_parameters[key] < 0:
                    raise ValueError("Parameter must be positive")
                cls.p.update(new_parameters)


    @classmethod
    def get_parameters(cls):
        """
        Returns the parameters of the given animal type
        """
        return cls.p


    def Compute_fitness(self)->float:
        """Computes fitness of the animal"""

        age_component= q(+1,self.age,self.p['a_half'],self.p['phi_age'])
        weight_component= q(-1,self.weight,self.p['w_half'],self.p['phi_weight'])
        self.fitness=age_component*weight_component
        return self.fitness

    def birth_weight(self)->float:
        """
        Birth weight of new born baby is drawn from gaussian distribution
        Birth weight is not a property of animal ( its natures decision I guess)
        """
        birth_weight =random.gauss(self.p['w_birth'],self.p['sigma_birth'])
        return birth_weight

    def reproduce(self,n_same_species)->bool:
        """
        Animals can reproduce only if there are >=2 members of the same species in the give cell
        -probabillity of birth => min(1, self.p['gamma']*self._fitness*(num_same_species-1))
        -
        """
        # computing probability of reproduction
        prob_of_reproduction=self.p['gamma']*self.fitness*(n_same_species-1)
        # evaluating self weight condition for giving birth
        if self.weight < self.p['zeta']*(self.p['w_birth']+self.p['sigma_birth']):
            return False, None

        elif 0 <prob_of_reproduction<1:
            if random.random() < prob_of_reproduction:
                give_birth = True
            else:
                give_birth = False

        elif prob_of_reproduction >=1:
            give_birth= True

        else:
            give_birth= False

        if give_birth:
            # computing the birth weight
            birth_weight=self.birth_weight()
            # checking if birth weight of baby is more than the parents weight
            if birth_weight < self.weight:
                # updating weight loss of parent
                self.weight-=self.p['xi']*birth_weight
                # re-evaluating fitness of parent
                self.Compute_fitness()

                return True,birth_weight
            else:
                return False, None

        return False, None

    def migrate(self)->bool:
        """
        Checking if the given animal will migrate
        """
        self.Compute_fitness()
        # computing probability of migration
        probability_of_migration=self.p['mu']*self.fitness
        # setting migration status randomly
        if random.random() < probability_of_migration:
            return True
        else:
            return False

    def aging(self):
        """Incrementing the age of animals"""
        self.age+=1

    def natural_weight_loss(self):
        """
        Animals naturally loose weight each year based on parameter 'eta'
        """
        # Updating self weight after weight loss
        self.weight -=self.weight*self.p['eta']
        # re evaluating fitness
        self.Compute_fitness()

    def evaluate_death(self)->bool:
        """
        Checks is the animal is dead or alive
        if dead :remove from simulation
        if alive : keep it still part of simulation
        """
        fitness=self.Compute_fitness()
        death= False
        if self.weight <= 0:
            death=True
        else:
            death_probability=self.p['omega']*(1-fitness)
            if random.random() < death_probability:
                death= True
    
        return death

    @abstractmethod
    def eat_food(self):
        """
        this is an abstract method for animals eating
        """
    
    
@dataclass
class Herbivore(Animal):
    """
    derived class for representing Herbivores
    """

    p = {  # Dictionary of parameters belonging to the Herbivore class
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.6,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0
    }

    # def set_parameters(self,parameters):
    #     """This function will set/reset the parameters for animals"""
    #     for param, value in parameters.items():
    #         if param in self.p.keys():
    #             self.p[param]=value
    #         else:
    #             raise ValueError(f"The parameter {param} is not defined")
                

    def eat_food(self,cell):
        """
        Herbivore will try to eat enough fodder,
        if not enough fodder present in cell it will consume what is left

        -weight will increase after food consumption
        -fitness will be affected, hence need to be re-evaluated
        """
        # amount of food required
        food_required=self.p['F']

        # if surpless food available in cell
        if food_required<=cell.f_max:
            self.weight+=self.p['beta']*food_required
            cell.f_max-= food_required

        # if not enough food present in cell
        else:
            self.weight += self.p['beta']*cell.f_max
            cell.f_max=0

        self.Compute_fitness()

@dataclass
class Carnivore(Animal):
    """derived class for representing Carnivores"""

    p = {  # Dictionary containing default parameter values for Carnivore class
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 40.0,
        "phi_age": 0.3,
        "w_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.8,
        "F": 50.0,
        "DeltaPhiMax": 10.0
    }

    # def set_parameters(self,parameters):
    #     """This function will set/reset the parameters for animals"""
    #     for param, value in parameters.items():
    #         if param in self.p.keys():
    #             self.p[param]=value
    #         else:
    #             raise ValueError(f"The parameter {param} is not defined")

    def eat_food(self,sorted_herbivores):
        """
        Carnivores feed on herbivores, and they can feed on herbivores anywhere in the Environment ( not restricted by cell )
        -They start killing prey from the weekest to the strongest 
        -require sorted list of herbivores in the entire environment as input

        """
        # Container to store killed prey
        herbivore_killed=[]
        # food required and initial food consumed
        food_consumed=0
        food_required=self.p['F']
        # computing initial fitness
        fitness=self.Compute_fitness()

        # itrating through the sorted list of herbivores in the environment
        for herbivore in sorted_herbivores:
            # carnivore kills prey only if food consumed is less than food required
            if food_consumed< food_required:
                # computing fitness delta
                fitness_delta = fitness-herbivore.fitness
                # can not kill prey if fitness is less than prey
                if fitness_delta<=0:
                    kill_prey =False
                # there is a chance of killing prey if fitness delta is positive but less than max fitness delta 
                elif 0 < fitness_delta < self.p['DeltaPhiMax']:
                    kill_prob =fitness_delta/self.p['DeltaPhiMax']
                    # simulating chance using random number generator
                    if random.random() <= kill_prob:
                        kill_prey=True
                    else:
                        kill_prey=False
                # if fitness delta is >= max fitness delta => assured kill
                else:
                    kill_prey=True

                # if prey is killed the, need to update total food consumed and add the killed herbivore to list of killed herbivores
                if kill_prey:
                    food_consumed+= herbivore.weight
                    herbivore_killed.append(herbivore)
            
            else:
                # continues the steps until the carnivore has consumed required amount of food
                continue

            
        # Animal only eat what they require, they can not consume more than what is required
        if food_consumed>self.p['F']:
            food_consumed=self.p['F']
        # Updating self weight after food consumption
        self.weight += food_consumed*self.p['beta']

        return herbivore_killed

