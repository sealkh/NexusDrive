from pathlib import Path

# Main settings
DEBUG_MODE = True
RESOURCES_DIR = Path(__file__).parent

# Window options
WINDOW = {
    'width': 1280,
    'height': 720,
    'title': "Voxel Sphere Raymarching",
    'fullscreen': False,
    'vsync': False
}

# Shaders config
SHADERS = {
    'vertex': RESOURCES_DIR / 'shaders' / 'vertex.glsl',
    'fragment': RESOURCES_DIR / 'shaders' / 'fragment.glsl',
    'uniforms': ['u_res']  #, 'u_voxels']
}

# Voxels config
VOXELS = {
    'grid_size': 64,
    'sphere_radius': 30,
    'texture_unit': 0
}