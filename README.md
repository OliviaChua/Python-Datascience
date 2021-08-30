# Overview

This is a set of real world data science tasks completed using the Python Pandas library.

# Project Organization

    workspace/
    │
    ├── data/               <- The original, immutable data dump.
    │
    ├── figures/            <- Figures saved by scripts or notebooks.
    │
    ├── notebooks/          <- Jupyter notebooks. 
    │
    ├── output/             <- Manipulated data, logs, etc.
    │
    ├── tests/              <- Unit tests.
    │
    ├── practice/           <- Python module with source code of this project.
    
    ./
    │
    ├── Makefile            <- Makefile with shortcut commands to run project
    │
    └── README.md           <- The top-level README for developers using this project.

# Setup

To run this project, just do `make run` then open the generated URL of the Jupyter Notebook.

Once you are in the dedicated URL, just click `work > notebooks > Analysis.ipynb`

# Reference

- The idea of the project structure is from this [tutorial](https://godatadriven.com/blog/write-less-terrible-code-with-jupyter-notebook/).


- All of the data files are from this [repository](https://github.com/KeithGalli/Pandas-Data-Science-Tasks). This repo goes with [this video](https://youtu.be/eMOA1pPVUc4) on "Solving real world data science videos with Python Pandas!". 

-----

Here is some information on that video.

In this video we use Python Pandas & Python Matplotlib to analyze and answer business questions about 12 months worth of sales data. The data contains hundreds of thousands of electronics store purchases broken down by month, product type, cost, purchase address, etc. 

We start by cleaning our data. Tasks during this section include:
- Drop NaN values from DataFrame
- Removing rows based on a condition
- Change the type of columns (to_numeric, to_datetime, astype)

Once we have cleaned up our data a bit, we move the data exploration section. In this section we explore 5 high level business questions related to our data:
- What was the best month for sales? How much was earned that month?
- What city sold the most product?
- What time should we display advertisemens to maximize the likelihood of customer’s buying product?
- What products are most often sold together?
- What product sold the most? Why do you think it sold the most?

To answer these questions we walk through many different pandas & matplotlib methods. They include:
- Concatenating multiple csvs together to create a new DataFrame (pd.concat)
- Adding columns
- Parsing cells as strings to make new columns (.str)
- Using the .apply() method
- Using groupby to perform aggregate analysis
- Plotting bar charts and lines graphs to visualize our results
- Labeling our graphs
