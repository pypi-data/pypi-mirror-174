![logo_azul](https://user-images.githubusercontent.com/64251090/199361725-4915b720-6e80-4e23-9342-e0ce48b58c7a.jpg)
-----------------

# Izandescriptive: powerful PyPi data analysis package 
[![PyPI Latest Release](https://img.shields.io/pypi/v/izandescriptive.svg)](https://pypi.org/project/izandescriptive/)
[![License](https://img.shields.io/pypi/l/izandescriptive.svg)](https://github.com/ceciliabilbao/izandescriptive/blob/main/LICENSE)

## What is it?

**Izandescriptive** is a PyPi library that provides fast and easy to undersand data
analysis. It aims to speed up the exploratory analysis process. It performs different graphs of the numerical variables in a single function called **graphic()**.

## Main Features

Here are just a few of the things that *izandescriptive* does well:

- Easy handling of reading csv.
- Selects numerical variables from the dataframe.
- Creates histograms, raincloud graphs and a heatmap graph.

### Class desc_analysis():

You can define the following class name desc_analysis

### Attributes

This class will have an attibute called *data*

- data : this attribute reads a csv and selects the numeric variables

### Methods

- graphic : The class desc_analysis has one method *graphic*. This method will take an argument wich is *data* defined in the previous attribute.

### Dependencies

- [pandas](https://pandas.pydata.org/)
- [turtle](https://docs.python.org/3/library/turtle.html)
- [ptitprince](https://github.com/pog87/PtitPrince)
- [seaborn](https://seaborn.pydata.org/)
- [matplotlib](https://matplotlib.org/)

## Using the library

### Installation

``` pip install izandescriptive ```

### Import

``` from izandescriptive import class_descriptives```

### Intance attributes and init the method

``` c1=desc_analysis('example.csv') ```

``` c1.graphic() ```

## Example

This would be the result of the desc_analysis class.

##### Histograms

![image](https://user-images.githubusercontent.com/64251072/197811387-d3f2e3f0-d28d-4332-ae28-fe35685f82be.png)

##### Raincloud

![image](https://user-images.githubusercontent.com/64251072/197811919-e4f5801a-07d0-4d27-af8d-ee427e882943.png)

##### Heatmap

![image](https://user-images.githubusercontent.com/64251072/197812131-81e48d49-ed32-4dc5-8328-e4980d4448fb.png)

## Where to get the library
The library is currently hosted on PyPi at:
https://pypi.org/project/izandescriptive/
