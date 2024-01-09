from Animal import Herbivore,Carnivore
from Cell import water_cell,desert_cell,highland_cell,lowland_cell
from Island import Island
from BioSim import BioSim


import textwrap
       

if __name__=="__main__":

    # sample map
    geogr = """\
                WWWWWWWWWWWWWWWWWWWW
                WWWHHHWLHHWLLLHLWWWW
                WWHHHHWLLLWLLLHLHHWW
                WHHHLLLLLLLLLHHHHHHW
                WHHHHLLLLLLLLHHHHHHW
                WHHHHHLLLLLLHHHHHHHW
                WHHHHHHLLLLLHHHHHHWW
                WWWWWWHLLLLHHHDHHHDW
                WHDLWWHHLLLHHHDHHHDW
                WHLLDWWWLLLHHWDDHHLW
                WLLDDDWWWLWWWWDDDLLW
                WHDDDDHHWWWWWWWDDLLW
                WLHHLHHHHWWWWWWDDLLW
                WLHLLHHHHWWWWWDDWWLW
                WWWWLHHHHHHWWWDDWWHW
                WLLLLHHHHDDDDDDWWHHW
                WLLLLLHHHHDDDDHWDHHW
                WWLLLLLLLLHDHHHHHHWW
                WWWLLLLLLLLLLHHHHWWW
                WWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)


    # sample population for simulation
    example_pop = [{'loc': (10,10),
                   'pop': [
                        {'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range (150)
                    ]},
                    {'loc': (11,10),
                   'pop': [
                        {'species': 'Carnivore', 'age': 2, 'weight': 25} for _ in range (120)
                    ]}, 
                    {'loc': (5,18),
                   'pop': [
                        {'species': 'Carnivore', 'age': 6, 'weight': 40} for _ in range (120)
                    ]}, 
                    {'loc': (6,17),
                   'pop': [
                        {'species': 'Herbivore', 'age': 3, 'weight': 20} for _ in range (200)
                    ]},
                    {'loc': (19,4),
                   'pop': [
                        {'species': 'Herbivore', 'age': 4, 'weight': 32} for _ in range (250)
                    ]}, 
                ]


    # sample histogram plotting specification
    # max : maximum value of respective properties in histogram plot
    # delta : spacing between adjacent histograms in plot
    example_hist_specs={'fitness': {'max': 1.0, 'delta': 0.01},
                             'age': {'max': 60.0, 'delta': 1},
                             'weight': {'max': 60, 'delta': 1}}


    # setting max values of herbivores and carnivores in plot legend
    example_xmax_animals= {'Herbivore': 500, 'Carnivore': 500}


    # creating an instance of BioSim for the simulation
    sim = BioSim(geography=geogr,
                initial_animal_pop=example_pop,
                seed=101,
                hist_spec=example_hist_specs,
                xmax=example_xmax_animals,
                img_dir='results_02',
                img_base='test',
                plot=True)
    
    # sim = BioSim()

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
    sim.simulate(300)
    
    # # make mp4 movie out of the saved images
    # sim.make_movie()

    # make .avi movie from the saved images
    sim.make_movie_avi()

    # # clean/delete the saved images
    # # do NOT use this command if you wish to keep all the images saved for each year of simulation
    # sim.image_cleanup()
    
    # # if you wish to populate a cell by calling the cell functions independently
    # new_cell=highland_cell((2,2))

    # new_cell.populate_cell([{'species': "Herbivore", 'age': 5, 'weight': 20}])

    # sim.run_year_cycle()