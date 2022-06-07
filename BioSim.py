from dataclasses import dataclass,field
from distutils.log import error
from gettext import npgettext
from Animal import Herbivore,Carnivore
from Cell import Cell,Cell_Type, highland_cell, lowland_cell, water_cell
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
_DEFAULT_GRAPHICS_NAME = "BioSim"
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
    img_dir:str ="results"
    img_base:str ="sample" 
    img_fmt:str ="png"
    _num_herbs: int = field(init=False,default_factory=0)
    _num_carns: int = field(init=False,default_factory=0)
    herbivore_pop_matrix: list = field(init=False,default_factory=list)
    carnivore_pop_matrix: list = field(init=False,default_factory=list)

    def __init__(self,geography,initial_animal_pop=[],seed=0,num_years=1,ymax=None,xmax=None,hist_spec=None,plot=True,img_dir='results',img_base='sample',img_years=1) -> None:
        """
        constructor for BioSim object
        """
        # generating map/geography of island
        if geography is None:
            # specifying defaule geometry if none specified
            default_geography = """WWW\nWLW\nWWW"""
            self.island=Island.from_map_str(default_geography)
            self.map_str_representation = default_geography
        
        # checking if map geography is string type 
        elif type(geography)==str:
            #  generating map usnig specified geometry 
            self.island=Island.from_map_str(geography)
            # print(f"island: {self.island}")
            self.map_str_representation = geography
        
        else:
            raise ValueError(F"Map geography shoudld be of type str!")

        # populating the island with initial population
        self.island.populate_island(population_dict=initial_animal_pop)
        # max y-axis limit for plots 
        self.ymax=ymax
        # max x-axis limit for plots
        self.xmax=xmax
        # setting random seed 
        self.random_seed=seed
        # setting histogram plotting specifications
        self.hist_spec=hist_spec
        # current year in simulation
        self._year = 0
        # total num of years to eb simulated
        self._year_target = num_years
        # interval for visualization
        self.vis_years=1
        # enable disable plotting
        self._plot_bool=plot
        # instantiating plotting object
        self._plot: Plotting = None
        # setting directory for saving images
        self.img_dir=img_dir
        # setting base name for images that will be saved
        self.img_base=img_base
        # initializing population matrix for herbivores and carnivores
        self.herbivore_pop_matrix = [[0 for _ in range(self.island.size[1])] for _ in range(self.island.size[0])]
        self.carnivore_pop_matrix = [[0 for _ in range(self.island.size[1])] for _ in range(self.island.size[0])]
        # estimating number of herbivores and number of carnivores in the simulation
        self._num_herbs=self.island.num_herbs()
        self._num_carns=self.island.num_carns()


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
        if landscape == 'H':
            highland_cell.set_cell_parameter(new_parameter=param)

        elif landscape =='L':
            lowland_cell.set_cell_parameter(new_parameter=param)

        else:
            raise ValueError(f"parameters of cell type:{landscape} can not be modified only 'H' and 'L' are allowed to be modified")
    

    def get_landscape_parameters(self,landscape):
        """
        get f_max for the specified cell type
        """
        if landscape=='H':
            param=highland_cell.get_cell_parameter()

        if landscape=='L':
            param=lowland_cell.get_cell_parameter()

        print(param)


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
        self.island.feeding()
        # Mating season
        self.island.reproduction()
        # Migration season
        self.island.migration()
        # animals aging
        self.island.aging()
        # natural weight loss
        self.island.animals_loose_weight()
        # natural death of animals
        self.island.animals_die()

        self._year +=1


    def simulate(self,num_years,vis_years=1,img_years=None):
        """
        This function runs the simulation or the specified number of years
        -num_years: num of years to run the simulation
        -vis_years: interval of saving image, 
                    vis_years =1 i.e. plot is saved every simulation year(default)
                    vis_years =2 => plot will be saved every 2 simulation years
        -img_years: plot will be saved only on multiples of img_years
        """
        # setting random seed
        random.seed(self.random_seed)
        # make the directory for saving plots is it doesn't already exist
        self.make_dir()
        # starting clock
        start_time = time.time()
        # setting target number of years for simulation and plotting
        self._year_target += num_years
        # checking if plotting is enabled in this instance of simulation
        if  self._plot_bool and self._plot is None:
            # instantiating object for plotting
            self._plot = Plotting(Island= self.island,                              # assign the island to be simulated 
                                map_str = self.map_str_representation,              # input string for making the island
                                herbivore_pop_matrix = self.herbivore_pop_matrix,   # population matrix for herbivores
                                carnivore_pop_matrix = self.carnivore_pop_matrix,   # population matrix for carnivores
                                num_herbivores=self._num_herbs,                     # tracing num of herbivores
                                num_carnivores=self._num_carns,                     # tracking num of carnivores
                                xmax=self.xmax,                                     # setting max x axis for plots
                                ymax=self.ymax,                                     # setting max y axis for plots
                                hist_specs=self.hist_spec,                          # predefined specification for plotting of histograms
                                image_dir=self.img_dir)                             # directory for storing images
            
            #  updating population matrix for plotting current stats
            self.update_pop_matrix()
            self._plot.init_plot(num_years)
            self._plot.y_herb[self._year] = self._num_herbs
            self._plot.y_carn[self._year] = self._num_carns
        
        # checking is plotting parameters are already specified
        elif self._plot_bool:
            self._plot.set_x_axis(self._year_target)
            self._plot.y_herb += [np.nan for _ in range(num_years)]
            self._plot.y_carn += [np.nan for _ in range(num_years)]

        # running life cycle for num_years specified 
        for _ in range(num_years):

            # running life cycle
            self.run_year_cycle()

            # Results are printed if visualization is disabled 
            if not self._plot_bool:  
                print(f"Year: {self._year}")
                print(f"Total animal count: {self.island.num_animals()}")
                print("Species count: 'Herbivore' : {} 'Carnivore' : {}".format(self.island.num_herbs(),self.island.num_carns()))

            # if visualization is enabled
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
        # end clock
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
            if type(cell) is not type(water_cell):
                row=cell.location[0]-1
                col=cell.location[1]-1
                self.herbivore_pop_matrix[row][col]=cell.count_herbivores()
                self.carnivore_pop_matrix[row][col]=cell.count_carnivores()


    def make_dir(self):
        """
        This function creates directory for storing results if the specified directory is not already present in the current working directory
        - the name of directory created will be same as the 'img_dir' parameter specified at the time of initialising the BioSim object
        """
        cwd =os.getcwd()
        # print(cwd)
        dir_path=path.join(cwd,self.img_dir)
        # print(dir_path)

        dir_exists = os.path.isdir(str(dir_path)) 

        if not dir_exists:
            os.mkdir(self.img_dir)


    def image_cleanup(self):
        """
        Removes created image files after movie is rendered.
        """

        cwd =os.getcwd()
        # print(cwd)
        dir_path=path.join(cwd,self.img_dir)
        # print(dir_path)
        files = glob.glob(dir_path+"/*")
        for f in files:
            os.remove(f)


    def make_movie_avi(self):

        if self._plot_bool:
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
        else:
            print ("plotting is Disabled for this simulation video NOT created, set param: plot = True, to enable plotting")