from io import BytesIO
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from app import utils

from celery import shared_task

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.views.static import serve
import os
import zipfile
import glob
import uuid
import json

from pathlib import Path

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

        task_result = utils.run_biosim.delay(id=sim_id,num_of_simulation_years=sim_years,map=map_str)



        return JsonResponse({'task_id':task_result.id,
                             'sim_id':sim_id})


# @require_GET
# @csrf_exempt
# def download_result(request,sim_id):
    
#     # Specify the folder path where the .png files are stored
#     folder_path = os.path.join("vol","plots", sim_id)

#     print(f"folder path : {folder_path}")

#     # Create a BytesIO buffer to store the zip file
#     zip_buffer = zipfile.ZipFile(file=os.path.join(folder_path, f"{sim_id}_plots.zip"), mode='w')

#     try:
#         # Loop through all files in the specified folder with .png extension
#         for root, dirs, files in os.walk(folder_path):
#             for file in files:
#                 if file.lower().endswith('.png'):
#                     file_path = os.path.join(root, file)
#                     # Add each file to the zip buffer
#                     zip_buffer.write(file_path, os.path.relpath(file_path, folder_path))

#         # Close the zip buffer
#         zip_buffer.close()

#         # Serve the zip file for download
#         zip_file_path = os.path.join(folder_path, f"{sim_id}_plots.zip")
#         response = HttpResponse(serve(request, os.path.basename(zip_file_path), os.path.dirname(zip_file_path)))
#         response['Content-Disposition'] = f'attachment; filename="{sim_id}_plots.zip"'
#         return response
#     except Exception as e:
#         # Handle exceptions as needed
#         return HttpResponse(f"Error: {str(e)}", status=500)

@require_GET
@csrf_exempt

def download_result(request, sim_id):
    BASE_DIR = Path(__file__).resolve().parent.parent
    # Specify the folder path where the .png files are stored
    folder_path = os.path.join("plots", sim_id)
    # folder_path = Path.joinpath('plots',sim_id)
    # print(f"Folder path: {folder_path}")

    # # Create a BytesIO buffer to store the zip file
    # zip_buffer = zipfile.ZipFile(file=os.path.join(folder_path, f"{sim_id}_plots.zip"), mode='w')

    try:
        # Loop through all files in the specified folder with .png extension
        png_files_found = False
        # for root, dirs, files in os.walk(folder_path):
        #     for file in files:
        #         if file.lower().endswith('.png'):
        #             file_path = os.path.join(root, file)
        #             # Add each file to the zip buffer
        #             zip_buffer.write(file_path, os.path.relpath(file_path, folder_path))
        #             print(f"processing file: {file_path}")
        #             # utils.save_to_s3(file_path,file)
        #             png_files_found = True
        # utils.compress_folder(folder_path,f"{sim_id}_plots.zip")
        
        # Check if any PNG files were found
        if not png_files_found:
            return HttpResponse("No PNG files found in the specified folder.", status=404)


        print("ZIP file created successfully.")

        # # Create a ZIP file on the file system
        # zip_file_path = os.path.join(folder_path, f"{sim_id}_plots.zip")
        # with open(zip_file_path, 'wb') as zip_file:
        #     zip_file.write(zip_buffer.getvalue())

        # zip_buffer.write(f"{sim_id}_plots.zip")

        # Serve the zip file for download
        # zip_buffer = zipfile.ZipFile(file=os.path.join(folder_path, f"{sim_id}_plots.zip"), mode='r')
        # response = HttpResponse(zip_buffer, content_type='application/zip')

        response = FileResponse(open(Path.joinpath(folder_path, f"{sim_id}_plots.zip"), 'rb'), content_type='application/zip')
        # Set the Content-Disposition header to prompt a file download
        response['Content-Disposition'] = f'attachment; filename="{sim_id}_plots.zip"'
        # Close the zip buffer
        # zip_buffer.close()
        # response = HttpResponse({"Results saved to S3 bucket"})
        return response
    except Exception as e:
        # Handle exceptions as needed
        print(f"Error: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)
