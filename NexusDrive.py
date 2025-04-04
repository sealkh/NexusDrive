from config import WINDOW, SHADERS, VOXELS
from voxels.render_core import VoxelEngineCore

app = VoxelEngineCore(
    window_config=WINDOW,
    shader_config=SHADERS,
    voxel_config=VOXELS
)

app.run()