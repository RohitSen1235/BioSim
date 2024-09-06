from .simulation_engine.BioSim import BioSim
import textwrap
from celery import shared_task
from pathlib import Path
from app.models import FileStorage
from django.conf import settings 

import boto3

import redis
import zlib
import pickle
import subprocess

# redis connection
cache = redis.StrictRedis(host = 'redis', port=6379, db=0)

def save_to_s3(image, filename):
    s3 = boto3.client('s3')
    s3.upload_fileobj(
        image,
        settings.AWS_STORAGE_BUCKET_NAME,
        f'{filename}',
        ExtraArgs={'ContentType': 'image/png'}
    )

@shared_task
def run_biosim(id:str,num_of_simulation_years:int=5, map:str = None):
    
    try:
        if map is None:
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
        else:
            geogr = map
            
        geogr = textwrap.dedent(geogr)


        # sample population for simulation
        example_pop = [{'loc': (5,5),
                       'pop': [
                            {'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range (150)
                        ]},
                        {'loc': (5,5),
                       'pop': [
                            {'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range (10)
                        ]}, 
                    ]


        # sample histogram plotting specification
        # max : maximum value of respective properties in histogram plot
        # delta : spacing between adjacent histograms in plot
        example_hist_specs={'fitness': {'max': 1.0, 'delta': 0.1},
                                 'age': {'max': 60.0, 'delta': 1},
                                 'weight': {'max': 60.0, 'delta': 1}}


        # setting max values of herbivores and carnivores in plot legend
        example_xmax_animals= {'Herbivore': 500, 'Carnivore': 500}

        # CURRENT_DIR = Path(__file__).resolve().parent.parent
        # creating an instance of BioSim for the simulation
        sim = BioSim(geography=geogr,
                    initial_animal_pop=example_pop,
                    seed=17,
                    hist_spec=example_hist_specs,
                    xmax=example_xmax_animals,
                    img_dir=f'plots/'+id,
                    img_base='year',
                    plot=True,
                    simulation_name = "From_Django")

        # # uncomment the below lines for setting/modifying animal parameters
        # # this is just an example for reference
        # # this is an optional step
        # sim.set_animal_parameters('Herbivore',{'w_birth': 12.0,
        #                                         'sigma_birth': 1.0,
        #                                         'beta': 0.95,
        #                                         'eta': 0.15,
        #                                         'xi':4.5})

        # below line runs the simulation
        result = sim.simulate(num_years=num_of_simulation_years)

        compress_folder(folder_path=f'plots/'+id,output_filename=f'{id}_plots.zip')

        # Create a new model instance
        file = FileStorage.objects.create(zip_file = f"/plots/{id}/{id}_plots.zip" )
        file.save()
        # Save the image to the instance's image field
        # zip_file.save(f"/plots/{id}/{id}_plots.zip")
        # # make mp4 movie out of the saved images
        # sim.make_movie()

        # # make .avi movie from the saved images
        # sim.make_movie_avi()

        # # clean/delete the saved images
        # # do NOT use this command if you wish to keep all the images saved for each year of simulation
        # sim.image_cleanup()

        # # if you wish to populate a cell by calling the cell functions independently
        # new_cell=highland_cell((2,2))

        # new_cell.populate_cell([{'species': "Herbivore", 'age': 5, 'weight': 20}])

        # sim.run_year_cycle()
        return True
    
    except Exception as e:
        print(f"run_biosim :: Exception thrown : {e}")
        return False


def StoreInCache(key,value):
    # df_compressed = zlib.compress(pickle.dumps(df))
    res = cache.set(key,value=value,ex=3600)
    if res == True:
        print(f'{key} cached')

def LoadFromCache(key):
    try:
        data = cache.get(key)
        return data
    except:
        print("Key not available in cache")

def RemoveFromCache(key):
    try:
        cache.delete(key)
    except:
        print("Key not available in cache")




@shared_task
def compress_folder(folder_path, output_filename):
    try:
        subprocess.run(['tar', '-czvf', output_filename, folder_path], check=True)
        print(f"Folder compressed successfully to {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error compressing folder: {e}")


