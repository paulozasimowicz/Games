import numpy as np
import vedo
import vtk
from vtk.util.numpy_support import numpy_to_vtk


# --------------------------------------------------
# Parameters
# --------------------------------------------------
nx = 100
ny = 100
nz = 30

point_size = 4

rgb_step = 5
timer_interval = 10000  # milliseconds

sphere_radius = 0.45
sphere_center = np.array([0.0, 0.0, 0.0])


# --------------------------------------------------
# Create points inside a cube
# --------------------------------------------------
x = np.linspace(-1, 1, nx)
y = np.linspace(-1, 1, ny)
z = np.linspace(-1, 1, nz)

X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

points = np.column_stack([
    X.ravel(),
    Y.ravel(),
    Z.ravel()
])

n_points = points.shape[0]
print(f"Number of points: {n_points}")


# --------------------------------------------------
# Create random RGB colours
# --------------------------------------------------
colors = np.random.randint(
    0, 256,
    size=(n_points, 3),
    dtype=np.uint8
)


# --------------------------------------------------
# Define spherical region in the centre
# --------------------------------------------------
distances = np.linalg.norm(points - sphere_center, axis=1)
sphere_mask = distances <= sphere_radius

print(f"Points inside sphere: {np.sum(sphere_mask)}")


# --------------------------------------------------
# Initial ball colour
# --------------------------------------------------
colors[sphere_mask] = np.array([255, 0, 0], dtype=np.uint8)


# --------------------------------------------------
# Create vedo point cloud
# --------------------------------------------------
cloud = vedo.Points(points, r=point_size)


# --------------------------------------------------
# Convert NumPy RGB colours to VTK scalars
# --------------------------------------------------
vtk_colors = numpy_to_vtk(
    colors,
    deep=True,
    array_type=vtk.VTK_UNSIGNED_CHAR
)

vtk_colors.SetNumberOfComponents(3)
vtk_colors.SetName("RGBColors")

cloud.dataset.GetPointData().SetScalars(vtk_colors)
cloud.dataset.Modified()


# --------------------------------------------------
# Create plotter
# --------------------------------------------------
plt = vedo.Plotter(
    title="Point cube with animated RGB ball",
    axes=1,
    bg="black"
)


# --------------------------------------------------
# Timer callback
# --------------------------------------------------
def update_colors(event):
    global colors, vtk_colors

    # Update only the ball colours
    temp = colors[sphere_mask].astype(np.uint16)
    temp = (temp + rgb_step) % 256
    colors[sphere_mask] = temp.astype(np.uint8)

    # Update VTK colour array
    new_vtk_colors = numpy_to_vtk(
        colors,
        deep=True,
        array_type=vtk.VTK_UNSIGNED_CHAR
    )

    new_vtk_colors.SetNumberOfComponents(3)
    new_vtk_colors.SetName("RGBColors")

    cloud.dataset.GetPointData().SetScalars(new_vtk_colors)
    cloud.dataset.GetPointData().Modified()
    cloud.dataset.Modified()

    plt.render()


# --------------------------------------------------
# Show scene
# --------------------------------------------------
plt.show(cloud, interactive=False)

# Add timer callback after the window exists
plt.add_callback("timer", update_colors)

# Start timer
plt.timer_callback("create", dt=timer_interval)

plt.interactive()
plt.close()