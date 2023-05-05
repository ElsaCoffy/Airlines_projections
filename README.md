Predict Air Traffic by routes
============================
<h2> Global concept </h2>

The idea is to produce two main products : 
- One is a series of notebook allowing to explore the dataset, and train models on said dataset
- Second is to create a streamlit apps allowing to access the result of the forecasting model set-up at with the notebook in a user friendly interface. We are forecasting the total number of passenger, with a granularity of the day, as a function of the route looked at.


<h2> Project Organization </h2 >
------------

    ├── LICENSE
    ├── README.md          <- Top-level README for developers using this project.
    |
    ├── data               <- Directory to store data (not pushed to Git)
    ├── notebooks          <- Jupyter notebooks. Contains the training for the forecasting model,              
    |                         data-exploration notebook 
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with 'pipreqs --force .'
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        ├── app.py         <- Code of the application
        ├── models         <- Modeling data for the forecast application.
        └── data           <- Dataset used by the application

--------

<p><small>Project based on the <a target="_blank" href="http://git.equancy.io/tools/cookiecutter-data-science-project/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
