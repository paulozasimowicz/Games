import numpy as np
import vedo
import vtk


# --------------------------------------------------
# Parameters
# --------------------------------------------------
nx = 100   # points in x direction
ny = 100   # points in y direction
nz = 30    # points in z direction

point_size = 4

rgb_step = 5
timer_interval = 1000  # milliseconds = 1 second

sphere_radius = 0.45


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
# Create random RGB colours for each point
# --------------------------------------------------
colors = np.random.randint(
    0, 256,
    size=(n_points, 3),
    dtype=np.uint8
)


# --------------------------------------------------
# Define ball-shaped region in the centre
# --------------------------------------------------
sphere_center = np.array([0.0, 0.0, 0.0])
distances = np.linalg.norm(points - sphere_center, axis=1)

sphere_mask = distances <= sphere_radius

print(f"Number of points inside central ball: {np.sum(sphere_mask)}")


# --------------------------------------------------
# Initial colour of the central ball
# --------------------------------------------------
colors[sphere_mask] = np.array([255, 0, 0], dtype=np.uint8)  # red


# --------------------------------------------------
# Create vedo point cloud
# --------------------------------------------------
cloud = vedo.Points(points, r=point_size)


# --------------------------------------------------
# Function to apply RGB colours to the point cloud
# --------------------------------------------------
def apply_rgb_colors(actor, rgb_array):
    """
    Apply per-point RGB colours to a vedo Points actor.

    Parameters
    ----------
    actor : vedo.Points
        Point cloud actor.

    rgb_array : np.ndarray
        RGB colour array with shape (n_points, 3).
        Values must be in the range 0-255.
    """

    vtk_colors = vtk.vtkUnsignedCharArray()
    vtk_colors.SetNumberOfComponents(3)
    vtk_colors.SetName("RGBColors")

    for r, g, b in rgb_array:
        vtk_colors.InsertNextTuple3(
            int(r),
            int(g),
            int(b)
        )

    polydata = actor.dataset
    polydata.GetPointData().SetScalars(vtk_colors)
    polydata.Modified()


# Apply initial colours
apply_rgb_colors(cloud, colors)


# --------------------------------------------------
# Timer callback
# --------------------------------------------------
def update_colors(event):
    global colors

    # --------------------------------------------------
    # Keep the cube background colours fixed
    # and update only the central ball
    # --------------------------------------------------
    temp = colors[sphere_mask].astype(np.uint16)

    temp = (temp + rgb_step) % 256

    colors[sphere_mask] = temp.astype(np.uint8)

    apply_rgb_colors(cloud, colors)

    plt.render()


# --------------------------------------------------
# Create plotter
# --------------------------------------------------
plt = vedo.Plotter(
    title="Point cube with RGB ball in the centre",
    axes=1,
    bg="black"
)

plt.add_callback("timer", update_colors)

plt.show(cloud, interactive=False)

plt.timer_callback("create", dt=timer_interval)

plt.interactive()

plt.close()