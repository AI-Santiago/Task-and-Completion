import bpy

def create_cube():
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 2))
    cube = bpy.context.active_object

    # blue
    mat = bpy.data.materials.new(name="BlueMaterial")
    mat.use_nodes = False
    mat.diffuse_color = (0.0, 0.0, 1.0, 1.0)
    cube.data.materials.append(mat)

    bpy.ops.object.shade_smooth()

    # rigid body effect
    bpy.ops.rigidbody.objects_add(type='ACTIVE')
#    cube.rigid_body.kinematic = True  #is better not to use it 
    cube.location.z = 2  # Set initial height

    return cube


def animate_cube(cube, num_bounces):
    start_frame = 1
    frame_step = 50
    height = 2

    for bounce in range(num_bounces):
        # key frame
        cube.location.z = height
        cube.keyframe_insert(data_path="location", index=2, frame=start_frame)

        cube.location.z = 0.5
        cube.keyframe_insert(data_path="location", index=2, frame=start_frame + frame_step)

        cube.location.z = height
        cube.keyframe_insert(data_path="location", index=2, frame=start_frame + 2 * frame_step)

        start_frame += 2 * frame_step  # to begin
        height *= 0.5  # to be lower, just a simple try

    # still
    cube.location.z = 0.5
    cube.keyframe_insert(data_path="location", index=2, frame=start_frame + 3 * frame_step)

def setup_scene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # light can be better
    bpy.ops.object.light_add(type='SUN', radius=1, location=(5, 5, 5))

    # delete, but seem useless
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    
    #Add a new ground and set it as a rigid body
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    ground = bpy.context.active_object
    bpy.ops.rigidbody.objects_add(type='PASSIVE')  # rigid body effect
    ground.rigid_body.type = 'PASSIVE'
    ground.animation_data_clear()


def main():
    setup_scene()
    cube = create_cube()
    animate_cube(cube, num_bounces=3)  # 3 bounces

    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 150  # total animation frames
    bpy.ops.screen.animation_play()

if __name__ == "__main__":
    main()
