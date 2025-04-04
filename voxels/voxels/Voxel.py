class Voxel:
    def __init__(self, size, x, y, z, parent=None):
        self.size = size  # Voxel size
        self.x = x  # Voxel coordinates
        self.y = y
        self.z = z
        self.parent = parent  # Parent voxel
        self.children = None  # Children (will be created when needed)
        self.matter1 = None  # Primary material
        self.matter2 = None  # Secondary material, can be None
        self.fraction = None  # Volume of Matter1 in the voxel

    def get_id(self):
        """Create a unique ID for the voxel"""
        return (self.size, self.x, self.y, self.z)

    def __repr__(self):
        return f"Voxel({self.size}, {self.x}, {self.y}, {self.z})"


class VoxelMatter:
    def __init__(self, pressure=None, temperature=None, matter=None):
        self.pressure = pressure
        self.temperature = temperature
        self.matter = matter if matter else "Vacuum"


# Dictionary to store voxels
voxel_map = {}


def calculate_voxel_id(size, x, y, z):
    """Calculate a unique ID for the voxel"""
    return (size, x, y, z)


def get_voxel(size, x, y, z):
    """Retrieve a voxel from the dictionary or create a new one if not found"""
    voxel_id = calculate_voxel_id(size, x, y, z)
    if voxel_id in voxel_map:
        return voxel_map[voxel_id]
    else:
        # Find the parent and split it into 8 children if it exists
        parent = None
        if size < 24:  # If it's not the root size, look for the parent
            parent_id = calculate_voxel_id(size + 1, x // 2, y // 2, z // 2)
            parent = voxel_map.get(parent_id)
        new_voxel = Voxel(size, x, y, z, parent)
        voxel_map[voxel_id] = new_voxel
        return new_voxel


def create_subvoxels(voxel):
    """Split the parent voxel into 8 parts"""
    if voxel.children is None:
        voxel.children = []
        # Split the parent into 8 children
        for dx in [0, 1]:
            for dy in [0, 1]:
                for dz in [0, 1]:
                    child_voxel = Voxel(
                        voxel.size - 1, voxel.x * 2 + dx, voxel.y * 2 + dy, voxel.z * 2 + dz, parent=voxel
                    )
                    voxel.children.append(child_voxel)
                    voxel_map[child_voxel.get_id()] = child_voxel


def find_neighbor(voxel, offset_x, offset_y, offset_z):
    """Find a neighboring voxel with the given offset"""
    return get_voxel(voxel.size, voxel.x + offset_x, voxel.y + offset_y, voxel.z + offset_z)


# Example usage

# Build the voxel hierarchy
root_voxel = get_voxel(24, 0, 0, 0)  # Root voxel
print(f"Root Voxel ID: {root_voxel.get_id()}")

# Split the root voxel into 8 children
create_subvoxels(root_voxel)

# Get a neighboring voxel
neighbor_voxel = find_neighbor(root_voxel, 1, 0, 0)
print(f"Neighbor Voxel: {neighbor_voxel.get_id()}")
