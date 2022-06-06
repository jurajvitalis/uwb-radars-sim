# Target localization using UWB radars

This application simulates an UWB radar system with 4 transcievers and 1 recievers used to localize a target. Based on user input, it generates 2-d coordinates as they would have been received from the radar system.

Then, 3 approximation methods used for target localization (Direct calculation, Least-squares, Taylor series) are compared.

![Screenshot](/assets/readme-img.png)

## How to use the program

1. ```bash
   python __main__.py
   ```

2. Input the target trajectory in the **input** window

3. Click **SAVE** to save the trajectory

   - Click **CLEAR** to delete all data

4. Open the **output** window to see the results

## Dependencies

Project is created with:

- Python 3.9.7
- Matplotlib 3.3.4
- Numpy 1.21.2
- Pyqt5 5.15.6

## Todo

- File I/O
