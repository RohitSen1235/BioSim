from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import run_biosim

import uuid
import os

def index(request):
    content={}
    return render(request,"biosim_world.html",context=content)

def run_simulation(request):
        
    uid = str(uuid.uuid4().hex)[0:6]
    # # run in sync
    # result = run_biosim()
    
    # run async
    task_result = run_biosim.delay(id=uid,num_of_simulation_years=10)
    
    # if result:
    #     response = 200
    # else:
    #     response = 400

    # return HttpResponse(content={response : "Simulation Completed"})

    return JsonResponse({'task_id':task_result.id})