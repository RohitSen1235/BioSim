#!/bin/bash

celery -A BioSim worker -l INFO &
celery -A BioSim beat -l INFO