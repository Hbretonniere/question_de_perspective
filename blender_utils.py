import bpy


def full_screen():
    context = bpy.context.copy()

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            context['area'] = area
            bpy.ops.screen.screen_full_area(context, use_hide_panels=True)
            bpy.context.space_data.show_gizmo = False
            bpy.context.space_data.overlay.show_overlays = False


def starting_position():

    for a in bpy.context.screen.areas:
        if a.type == 'VIEW_3D':
            a.spaces[0].region_3d.view_matrix[0] = [0.946, -0.2319, 0.0, -4.67]
            a.spaces[0].region_3d.view_matrix[1] = [0.0296, 10, 0.99, 3.6]
            a.spaces[0].region_3d.view_matrix[2] = [-0.3205, 0.94, 0.091, -40]
            a.spaces[0].region_3d.view_matrix[3] = [0, 0, 0, 1]
            a.spaces[0].region_3d.view_rotation = [-0.12, -0.10, 0.66, 0.72]
            a.spaces[0].region_3d.view_distance = 5
            break
    c = {}
    c['area'] = a
    c["space_data"] = a.spaces.active
    c['region'] = a.regions[-1]

    bpy.ops.view3d.walk(c, 'INVOKE_DEFAULT')

