import bpy

bpy.types.Scene.file_path = bpy.props.StringProperty(
        name="File Path",
        description="Enter the  file path to load",
        subtype='FILE_PATH'
    )

bpy.types.Scene.Column_ops : bpy.props.EnumProperty(
        name='Column_ops',
        description="Options of columns to use",
        default=10,
    )

bpy.types.Scene.Sheet_ops : bpy.props.EnumProperty(
        name="Sheet_name",
        description="Options of columns to use",
        default=10,
    )

# bpy.types.Scene.Collar_col : bpy.props.EnumProperty(
#         name="Collar_col",
#         description="Choose Collar column",
#         default=10,
#     )
# bpy.types.Scene.x : bpy.props.EnumProperty(
#         name="x",
#         description="Choose X column",
#         default=10,

#     )
# bpy.types.Scene.y : bpy.props.EnumProperty(
#         name="y",
#         description="Choose Y column",
#         default=10,

#     )
# bpy.types.Scene.z : bpy.props.EnumProperty(
#         name="z",
#         description="Choose Z column",
#         default=10,

#     )
# bpy.types.Scene.Render_col : bpy.props.EnumProperty(
#         name="Render_col",
#         description="Choose a column to render",
#         default=10,
#     )