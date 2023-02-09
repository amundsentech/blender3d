import bpy, csv
with open("your file.csv") as f:
    reader = csv.reader(f)
    for i, data in enumerate(reader):
        
        # This skips the firt row of the CSV, because it is a header row
        if i==0: continue
    
        # This makes temp variables from each row in your import, many ways to do this in Python
        # note! cell counts start at 0 in computer language, not 1 !
        x = data[0] # number of your X column
        y = data[1] # number of your Y column
        z = data[2] # number of your Z column
        azimuth = data[3] # number of your azimuth column
        dip = data[4] # number of your dip column
        length = data[5] # number of your interval length in meters
        att = data[6] # number of the column that contains the data you want
        
        # Placeholder for the X,Y,Z coordinates
        coords = ( float(x), float(y), float(z) )
        
        # Placeholder for the rotation attrubute, about the (X,Y,Z) axis, in RADIANS
        rotate = ( float(0.0), float(radians(dip)), float(radians(azimuth)) )
        
        # Sets the 3D properties of a SPHERE or CYLINDER from the values above, comment the chosen line
        #bpy.ops.mesh.primitive_uv_sphere_add( location = coords )
        bpy.ops.mesh.primitive_cylinder_add(location = coords, rotation = rotate, radius=.05, depth=length, cap_ends=True)

        # This sets the material to use on the sphere you just created
        material = bpy.data.materials["The name of your material aka style file"]
        bpy.context.object.data.materials.append(material)

        # Creates the custom color value (the following example assumes range 0-100 for a percent column eg 0-10)
        bpy.context.object["color"] = att / 100
