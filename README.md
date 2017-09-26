# Automatic Semantic Search Engine for Suitable Standards 

## Getting started

Clone this repository and then build the docker image from the main folder of ASSESS as follows:

> docker build -t assessimage . -f docker/Dockerfile

Run the docker container as follows:

> docker run -p 5000:5000 -it assessimage bash

Start the web application as follows:

> python webapp.py

Open `http://0.0.0.0:5000` with your web browser and then upload a SoW to extract standard references and suitable standards.
