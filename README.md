# Demeter

This project is part of the 3rd semester of the IT4BI Master's program at Universitat Politècnica de Catalunya. The expected outcome of the project is a recipe recommendation system.

#### Instructions to download and run the project

1. First, make sure you have Python 2.7+ ,MongoDB and Divolte Collector 0.4.1  installed in your machine
2. Clone this repository to your machine by either using [GitHub's Client for Windows] or by typing the following in the command line (make sure you working directory is the folder where you want the project to be in):
` git clone https://github.com/larissaleite/Demeter.git `
3. In the bin directory divolte-collector-0.4.1 run:
 		` ./bin/divolte-collector `
4. In the directory containing the project, run:
` pip install -r requirements.txt `
5. Run the project:
` python run.py `
6. Enter `http://localhost:5000` on the web browser

To load the dataset into MongoDB, just execute:

 `python data/data-collector-edamam.py`
 `python data/data-collector-yummly.py`
 `python data/data-collector-spoonacular.py`
