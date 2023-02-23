import bpy, csv
with open("your file.csv") as f:
    reader = csv.reader(f)
    for i, data in enumerate(reader):
        
        # This skips the firt row of the CSV, because it is a header row
        if i==0: continue
    
        # This makes temp variables from each row in your import, many ways to do this in Python
        # note! cell counts start at 0 in computer language, not 1 !
        x = data[0] # if your X data is the first column, change if needed
        y = data[1] # if your Y data is the second column, change if needed
        z = data[2] # if your Z data is the third column, change if needed
        att = data[3] # or whatever the number of the column is that contains the data you want [12, 13, whatever]
        
        # This sets the 3D location of the object to values from the above
        bpy.ops.mesh.primitive_uv_sphere_add( location = ( float(x), float(y), float(z) ) )
        
        # This sets the material to use on the sphere you just created
        material = bpy.data.materials["The name of your material aka style file"]
        bpy.context.object.data.materials.append(material)
        sphere=bpy.context.object()

        # This creates the custom color value (the following example assumes range 0-100 for a percent column eg 0-100)
        bpy.context.object["color"] = float(att) / 100
