from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .utils import run_biosim
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.views.static import serve
import os
import zipfile

import uuid
import json

def index(request):
    content={}
    return render(request,"biosim_world.html",context=content)

@csrf_exempt
def run_simulation(request):

    if request.method == "POST":

        received_data = json.loads(request.body)
        
        print(f"{received_data}")

        sim_years = int(received_data.get('n_years'))
        map_str = received_data.get('map')
        name = received_data.get('prj_name')
        uid = str(uuid.uuid4().hex)[0:4]

        sim_id = name + "_" + uid

        if sim_years == None or map_str == None or name == None :
            return JsonResponse({'error': 'Parmeter values are None', 
                                 'task_id': None})

        task_result = run_biosim.delay(id=sim_id,num_of_simulation_years=sim_years,map=map_str)



        return JsonResponse({'task_id':task_result.id,
                             'sim_id':sim_id})


@require_GET
@csrf_exempt
def download_result(request,sim_id):
    
    # Specify the folder path where the .png files are stored
    folder_path = os.path.join("vol","plots", sim_id)

    print(f"folder path : {folder_path}")

    # Create a BytesIO buffer to store the zip file
    zip_buffer = zipfile.ZipFile(file=os.path.join(folder_path, f"{sim_id}_plots.zip"), mode='w')

    try:
        # Loop through all files in the specified folder with .png extension
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.png'):
                    file_path = os.path.join(root, file)
                    # Add each file to the zip buffer
                    zip_buffer.write(file_path, os.path.relpath(file_path, folder_path))

        # Close the zip buffer
        zip_buffer.close()

        # Serve the zip file for download
        zip_file_path = os.path.join(folder_path, f"{sim_id}_plots.zip")
        response = HttpResponse(serve(request, os.path.basename(zip_file_path), os.path.dirname(zip_file_path)))
        response['Content-Disposition'] = f'attachment; filename="{sim_id}_plots.zip"'
        return response
    except Exception as e:
        # Handle exceptions as needed
        return HttpResponse(f"Error: {str(e)}", status=500)
