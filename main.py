# from dataclasses import dataclass,field
# from abc import ABC,abstractmethod
from Animal import Herbivore,Carnivore
from Cell import Cell,Cell_Type
from Island import Island
from BioSim import BioSim


import textwrap
       

if __name__=="__main__":

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
    # geogr ="""\
    #           WWW
    #           WLW
    #           WWW"""
    # geogr = textwrap.dedent(geogr)

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

    
    # Interface class Structure for inistantiating simulation
    # sim = BioSim(geogr, ini_herbs + ini_carns, seed=1,
    #              hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
    #                          'age': {'max': 60.0, 'delta': 2},
    #                          'weight': {'max': 60, 'delta': 2}},
    #              cmax_animals={'Herbivore': 200, 'Carnivore': 50},
    #              img_dir='results',
    #              img_base='sample')

  
    example_hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}}

    example_cmax_animals= {'Herbivore': 200, 'Carnivore': 50}

    # print(f"from main.py\n{geogr}")
    # creating an instance of simulation using the interface class
    sim = BioSim(geography=geogr,
                initial_animal_pop=example_pop,
                seed=19,
                hist_spec=example_hist_specs,
                cmax=example_cmax_animals,
                img_dir='results',
                img_base='test',
                plot=True)
    
    # print(sim.island)

    # sim.get_animal_parameters('Herbivore')
    # sim.set_animal_parameters('Herbivore',{'w_birth': 8.0,
    #                                         'sigma_birth': 1.5,
    #                                         'beta': 0.95,
    #                                         'eta': 0.15,
    #                                         'xi':4.5})
    # sim.get_animal_parameters('Herbivore')

    # sim.get_landscape_parameters('H')

    # sim.set_landscape_parameters('H',{'f_max':500.0})

    # sim.get_landscape_parameters('H')

    sim.simulate(25)
    # sim.make_movie()
    sim.make_movie_avi()