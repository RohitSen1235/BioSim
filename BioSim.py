from dataclasses import dataclass,field
from gettext import npgettext
from Animal import Herbivore,Carnivore
from Cell import Cell,Cell_Type
from Island import Island
from visualization import Plotting

import cv2
import numpy as np
import glob

import random as random
import numpy as np
import time
import os
import subprocess
from os import path

_FFMPEG_BINARY = "ffmpeg"

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join("./", "data")
_DEFAULT_GRAPHICS_NAME = "biosim"
_DEFAULT_MOVIE_FORMAT = "mp4"  # alternatives: mp4, gif


@dataclass
class BioSim:
    """
    This is the Interface class for setting up the simulation by providing various simulation parameters
    """
    island:Island
    map_str_representation: str
    random_seed:int
    hist_spec:dict
    vis_years:int
    _year: int
    _ymax: int
    _cmax: int
    _year_target: int 
    _plot_bool: bool
    _plot: Plotting
    img_dir:str ="./result"
    img_base:str ="sample" 
    img_fmt:str ="png"
    _num_herbs: int = field(init=False,default_factory=0)
    _num_carns: int = field(init=False,default_factory=0)
    herbivore_pop_matrix: list = field(init=False,default_factory=list)
    carnivore_pop_matrix: list = field(init=False,default_factory=list)

    def __init__(self,geography,initial_animal_pop=[],seed=0,num_years=1,ymax=None,cmax=None,hist_spec=None,plot=True,img_dir='results',img_base='sample',img_years=1) -> None:
        """
        constructor for BioSim object
        """
        # generating map/geography of island
        if geography is None:
            # specifying defaule geometry if none specified
            default_geography = """WWW\nWLW\nWWW"""
            self.island=Island.from_map_str(default_geography)
            self.map_str_representation = default_geography
            
        elif type(geography)==str:
            #  generating map usnig specified geometry 
            self.island=Island.from_map_str(geography)
            # print(f"island: {self.island}")
            self.map_str_representation = geography
        
        else:
            raise ValueError(F"Map geography shoudld be of type str!")

        self.island.populate_island(population_dict=initial_animal_pop)
        # 
        self.ymax=ymax
        # 
        self.cmax=cmax
        # setting random seed 
        self.random_seed=seed
        # 
        self.hist_spec=hist_spec
        # 
        self._year = 0
        self._year_target = num_years
        self.vis_years=1
        self._plot_bool=plot
        self._plot: Plotting = None
        self.img_dir=img_dir
        # 
        self.img_base=img_base

        self.herbivore_pop_matrix = [[0 for _ in range(self.island.size[1])] for _ in range(self.island.size[0])]
        self.carnivore_pop_matrix = [[0 for _ in range(self.island.size[1])] for _ in range(self.island.size[0])]

        self._num_herbs=self.island.num_herbs()
        self._num_carns=self.island.num_carns()

        # print(f"from BioSim constructor\n{self.island.map_str_representation}")
        
        # generating initial animal population


    def set_animal_parameters(self,species,params):
        """
        Set parameters for animal species.

        -param species: String, name of animal species
        -param params: Dict with valid parameter specification for species
        """
        if species=='Herbivore':
            Herbivore.set_parameters(new_parameters=params) 

        elif species=='Carnivore':
            Carnivore.set_parameters(new_parameters=params)

        else:
            raise ValueError(f"Undefined Species type :{species}")


    def get_animal_parameters(self,species):
        """
        get parameters of the specified species type
        """     
        parameter=None

        if species=='Herbivore':
            parameter=Herbivore.get_parameters()
            # print(parameter)

        elif species =='Carnivore':
            parameter=Carnivore.get_parameters()
            # print(parameter)

        else:
            raise ValueError(f"Undefined Species type :{species}")


    def set_landscape_parameters(self, landscape, param):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        Cell.set_cell_parameter(cell_type=landscape,new_parameter=param)


    def get_landscape_parameters(self,landscape):
        """
        get f_max for the specified cell type
        """
        f_max=Cell.get_cell_parameter(cell_type=landscape)
        # print(f_max)

    def add_population(self,population_dict):
        """
        Additing Polulation to existing island
        """
        self.populate_island(population_dict)

    def run_year_cycle(self):
        """
        Running life cycle of one year
        """
        self.island.reset_migration()
        # Food growing season
        self.island.grow_fodder()
        # Animals Feeding
        print(f"Herbs hunted : {self.island.feeding()}")
        # Mating season
        print(f"num of new animals: {self.island.reproduction()}")
        # Migration season
        print(f"num of migrations: {self.island.migration()}")
        # animals aging
        self.island.aging()
        # natural weight loss
        self.island.animals_loose_weight()
        # natural death of animals
        self.island.animals_die()

        self._year +=1


    def simulate(self,num_years,vis_years=1,img_years=None):
        
        random.seed(self.random_seed)
        start_time = time.time()
        self._year_target += num_years
        # print(f"from Biosim.Simulate:\n{self.island.map_str_representation}")
        if  self._plot_bool and self._plot is None:

            self._plot = Plotting(Island= self.island,
                                map_str = self.map_str_representation,
                                herbivore_pop_matrix = self.herbivore_pop_matrix,
                                carnivore_pop_matrix = self.carnivore_pop_matrix,
                                num_herbivores=self._num_herbs,
                                num_carnivores=self._num_carns, 
                                cmax=self.cmax, 
                                ymax=self.ymax, 
                                hist_specs=self.hist_spec,
                                image_dir=self.img_dir)

            self.update_pop_matrix()
            self._plot.init_plot(num_years)
            self._plot.y_herb[self._year] = self._num_herbs
            self._plot.y_carn[self._year] = self._num_carns

        elif self._plot_bool:
            self._plot.set_x_axis(self._year_target)
            self._plot.y_herb += [np.nan for _ in range(num_years)]
            self._plot.y_carn += [np.nan for _ in range(num_years)]

        for _ in range(num_years):

            # running life cycle
            self.run_year_cycle()

            if not self._plot_bool:  # Results are printed if visualization is disabled r
                print(f"Year: {self._year}")
                print(f"Total animal count: {self.island.num_animals()}")
                print("Species count: 'Herbivore' : {} 'Carnivore' : {}".format(self.island.num_hrebs(),self.island.num_carns()))

            if self._plot_bool:
                self._plot.y_herb[self._year] = self.island.num_herbs()
                self._plot.y_carn[self._year] = self.island.num_carns()
                if self._year % vis_years == 0:
                    self.update_pop_matrix()
                    self._plot.update_plot()

                if self.img_base is not None:
                    if img_years is None:
                        if self._year % vis_years == 0:
                            self._plot.save_graphics(self.img_base, self.img_fmt)

                    else:
                        if self._year % img_years == 0:
                            self._plot.save_graphics(self.img_base, self.img_fmt)
            
        finish_time = time.time()

        print("Simulation complete.")
        print("Elapsed time: {:.6} seconds".format(finish_time - start_time))


    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Creates MPEG4 movie from visualization images saved.
        """

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == "mp4":
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call(
                    [
                        _FFMPEG_BINARY,
                        "-i",
                        "{}_%05d.png".format(self.img_base),
                        "-y",
                        "-profile:v",
                        "baseline",
                        "-level",
                        "3.0",
                        "-pix_fmt",
                        "yuv420p",
                        "{}.{}".format(self.img_base, movie_fmt),
                    ]
                )
            except subprocess.CalledProcessError as err:
                raise RuntimeError("ERROR: ffmpeg failed with: {}".format(err))
        else:
            raise ValueError("Unknown movie format: " + movie_fmt)

    def update_pop_matrix(self):
        """
        Population matrix is used to plot the heat map of animal population
        """
        for cell in self.island.map:
            if cell.type is not Cell_Type.water:
                row=cell.location[0]-1
                col=cell.location[1]-1
                # print(f"{cell.location}:[{row},{col}]")
                self.herbivore_pop_matrix[row][col]=cell.count_herbivores()
                self.carnivore_pop_matrix[row][col]=cell.count_carnivores()
        #         herb_pop_matrix[row][col]=cell.count_herbivores()
        # print(herb_pop_matrix)

    def image_cleanup(self):
        """Removes created image files after movie is rendered."""
        pass

    def make_movie_avi(self):

        img_array = []
        file_list= glob.glob(f"{self.img_dir}/*.png")
        for file in sorted(file_list):
            img = cv2.imread(file)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)

        out = cv2.VideoWriter(f"{self.img_base}.avi",cv2.VideoWriter_fourcc(*'DIVX'),15, size)
 
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()