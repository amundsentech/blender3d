# File Type Options for Data Rendering

This repository contains a blender add on that can be used to visualize Drill Hole data based on two different file type options. The first option is a file(.CSV or .XLSX) that contains XYZ coordinates for the data, and the second option is an .XLSX file with 3 sheets conatings data that can be used to build the Drill Hole.

## File Type Option 1: XYZ Coordinates

The XYZ coordinates file contains data points in the form of x, y, and z coordinates. The file should have the following format:
| hole_id | x_utm | y_utm | z_elevation | copper | gold |
|---------|-------|-------|------- |   -------   | ------- |
| 1  | 12345 | 67890 | 1200        | 9.0    | 0.1  |
| 2  | 23456 | 78901 | 1300        | 8.0    | 0.0  |
| 3  | 34567 | 89012 | 960         | 3.0    | 0.3  |
| ...| ...   | ...   | ...         | ...    | ...  |

## File Type Option 2: XLSX File with 3 Sheets

The XLSX file contains data in three separate sheets. All three sheets must have a column containing the hole_id names. The first sheet must have UTM georeferenced locations, the second sheet must have survey information including depth, dip, and azimuth, and the third sheet must have depth and the data you are wishing to render.

The three sheets should have the following formats:

### Sheet 1: UTM Georeferenced Locations

| hole_id | x_utm | y_utm | z_elevation |
|---------|-------|-------|-------|
| hole_1  | 12345 | 67890 | 1200  |
| hole_2  | 23456 | 78901 | 1300  |
| hole_3  | 34567 | 89012 | 960   |
| ...     | ...   | ...   | ...   |

### Sheet 2: Survey Information

| hole_id | depth | dip | azimuth |
|---------|-------|-----|---------|
| 1       | 10    | 20  | 30      |
| 2       | 20    | 30  | 40      |
| 3       | 30    | 40  | 50      |
| ...     | ...   | ... | ...     |

### Sheet 3: Data

| hole_id | depth | copper | gold |
|---------|-------|------  |------|
| 1       | 10    | 5.0    | 5.0  |
| 1       | 20    | 6.0    | 5.0  |
| 1       | 30    | 7.0    | 5.0  |
| 2       | 10    | 8.0    | 5.0  |
| 2       | 30    | 10.0   |   0  |
| 2       | 30    | 10.0   | 10.0 |
| ...     | ...   | ...    | ...  |

## Usage


To use the tool in Blender, first make sure you have installed the addon by going to the "Edit" menu in the 3D viewport, selecting "Preferences", and then navigating to the "Add-ons" tab. Search for "drill hole 3d" and make sure the checkbox next to it is checked.

Next, select the 3D viewport area in Blender and press "n" to bring up the drill holle importer side menu.

In the File Importer panel, select the file you will be using, and then load the file by clicking the "Launch File Loader" button. 

Next you will be promepted to specify which format your data is in. single file or multiple files

If your file if in multiple sheets choose the multple files button and vice versa.

You will be prompted to choose the columns from each sheet or your single sheet that contain the relevant data.

Finally, choose the columns that you would like to see colored in the viewport ,the color map you would like to use and radius of the drill hole then click the "Render Drill Holes" Button button to render the data.

If you wuld like to change the colors of the data you are viewing simply change the column and click the "Render Drill Holes" Button again.
