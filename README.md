# Object Localization Using Round Trip Propagation Time Measurements

This application is a demonstration of the results in [this paper](https://ieeexplore.ieee.org/abstract/document/4542689?casa_token=anrYO5PKXesAAAAA:DJEadLwcF02fw9-zX2Jg-g8BGwdtXagcvIczKT7XP-4Uyy-O4Qz8HxzLCEWlTgDNF5FNr3CXeNXl), with two dimensions in consideration. It simulates a UWB radar system with 4 transcievers and 1 reciever used to localize an object.

Based on user input, 2-d coordinates are generated as they would have been received by the radar system. Then, 3 approximation methods (Direct calculation, Least-squares, Taylor series) used to produce the resulting trajectories are compared.

![Screenshot](/assets/readme-img.png)

## How to use the program

1. Download the executable from releases and run it

2. Input the object trajectory by drawing in the **input** window

3. Click **SAVE** to save the trajectory
   
   - Click **CLEAR** to delete all data and start over

4. See the **output** window for the results

To run this as a python script:

1. Build a conda environemnt from `environment.yml`
   
   ```bash
   conda env create --name envname --file=environment.yml
   ```

2. Run the script
   
   ```bash
   python __main__.py
   ```

## Dependencies

- Python 3.9.7
- Matplotlib 3.3.4
- Numpy 1.21.2
- Pyqt5 5.15.6
- All dependencies listed in `environment.yml`
