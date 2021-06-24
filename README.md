# **Control-Map-Reader**

Control Map Reader is a script for creating an image out of an FRC driver & operator buttons layout.

## How to use:
1. Create a .txt file with the name of the layout.<p>
2. The file should follow this exact [format](control_maps/BaseBlankFormat.txt):<p>
    ```
    Name= Blank
    Robot= Blank

    Driver=
    A:
    B:
    X:
    Y:
    D_UP:
    D_DOWN:
    D_LEFT:
    D_RIGHT:
    RT:
    LT:
    RB:
    LB:
    START:
    BACK:
    LS:
    RS:
    LSB:
    RSB:

    Operator=
    A:
    B:
    X:
    Y:
    D_UP:
    D_DOWN:
    D_LEFT:
    D_RIGHT:
    RT:
    LT:
    RB:
    LB:
    START:
    BACK:
    LS:
    RS:
    LSB:
    RSB:
    ```
3. Fill each btn for it's task (e.g ``` D_UP: Shoot```).<p>
**NOTE:** Be abstract with the action description so the image wont look be overwhelming.<p>
 
4. Run the Batch file (Change the directory before).<p>

5. In the folder [map_views](map_views) you will get a folder named after the ```Robot``` and an inner folder named after the layout ```name```,<p>
    inside those foldes you will find 2 images one for the driver and one for the operator

## **FOR XBOX CONTROLLERS ONLY**
