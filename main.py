# from dataclasses import dataclass,field
# from abc import ABC,abstractmethod
from Animal import Herbivore,Carnivore
from Cell import Cell,water_cell,desert_cell,highland_cell,lowland_cell
from Island import Island
from BioSim import BioSim


import textwrap
       

if __name__=="__main__":

    # sample map
    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHLLLLWWLLLLLLLWW
               WWHHLLLLLLLWWLLLLLLLW
               WWHHLLLLLLLWWLLLLLLLW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDWWLLLLLWWW
               WHHHHDDDDDDLLLLWWWWWW
               WWHHHHDDDDDDLWWWWWWWW
               WWHHHHDDDDDLLLWWWWWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHDDDDDDLLLLWWWWWW
               WWHHHHDDDDDLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWHHHHHHWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)


    # sample population for simulation
    example_pop = [{'loc': (10,10),
                   'pop': [
                        {'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range (150)
                    ]},
                    {'loc': (10,10),
                   'pop': [
                        {'species': 'Carnivore', 'age': 2, 'weight': 25} for _ in range (20)
                    ]}, 
                    {'loc': (3,8),
                   'pop': [
                        {'species': 'Carnivore', 'age': 12, 'weight': 45} for _ in range (15)
                    ]}, 
                    {'loc': (2,9),
                   'pop': [
                        {'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range (20)
                    ]} 
                ]


    # sample histogram plotting specification
    # max : maximum value of respective properties in histogram plot
    # delta : spacing between adjacent histograms in plot
    example_hist_specs={'fitness': {'max': 1.0, 'delta': 0.01},
                             'age': {'max': 60.0, 'delta': 1},
                             'weight': {'max': 60, 'delta': 1}}


    # setting max values of herbivores and carnivores in plot legend
    example_xmax_animals= {'Herbivore': 200, 'Carnivore': 50}


    # creating an instance of BioSim for the simulation
    sim = BioSim(geography=geogr,
                initial_animal_pop=example_pop,
                seed=19,
                hist_spec=example_hist_specs,
                xmax=example_xmax_animals,
                img_dir='results',
                img_base='test',
                plot=True)
    

    # # uncomment the below lines for setting/modifying animal parameters
    # # this is just an example for reference
    # # this is an optional step
    # sim.set_animal_parameters('Herbivore',{'w_birth': 8.0,
    #                                         'sigma_birth': 1.5,
    #                                         'beta': 0.95,
    #                                         'eta': 0.15,
    #                                         'xi':4.5})


    # # uncomment the below line for setting/modifying the landscape parameter, f_max for highland and lowland
    # # this is just and example for reference 
    # # this is an optional step
    # sim.set_landscape_parameters('H',{'f_max':500.0})

    # below line runs the simulation
    # sim.simulate(5)
    
    # # make mp4 movie out of the saved images
    # sim.make_movie()

    # # make .avi movie from the saved images
    # sim.make_movie_avi()

    # # clean/delete the saved images
    # # do NOT use this command if you wish to keep all the images saved for each year of simulation
    # sim.image_cleanup()

    new_cell=highland_cell((2,2))

    new_cell.populate_cell([{'species': "Herbivore", 'age': 5, 'weight': 20}])