import numpy as np
import vedo
import vtk


# --------------------------------------------------
# Parameters
# --------------------------------------------------
nx = 100   # number of points in x direction
ny = 100   # number of points in y direction
nz = 30    # number of points in z direction
point_size = 4

rgb_step = 5          # RGB increase per update
timer_interval = 1000 # milliseconds = 1 second


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
# Scale: 0 to 255
# --------------------------------------------------
colors = np.random.randint(
    0, 256,
    size=(n_points, 3),
    dtype=np.uint8
)


# --------------------------------------------------
# Create vedo Points object
# --------------------------------------------------
cloud = vedo.Points(points, r=point_size)


# --------------------------------------------------
# Function to apply RGB colours to the point cloud
# --------------------------------------------------
def apply_rgb_colors(actor, rgb_array):
    """
    Apply per-point RGB colours to a vedo Points actor.
    rgb_array must have shape (n_points, 3) and dtype uint8.
    """

    vtk_colors = vtk.vtkUnsignedCharArray()
    vtk_colors.SetNumberOfComponents(3)
    vtk_colors.SetName("RGBColors")

    for r, g, b in rgb_array:
        vtk_colors.InsertNextTuple3(int(r), int(g), int(b))

    polydata = actor.dataset
    polydata.GetPointData().SetScalars(vtk_colors)
    polydata.Modified()


apply_rgb_colors(cloud, colors)


# --------------------------------------------------
# Timer callback
# --------------------------------------------------
def update_colors(event):
    global colors

    # Option 1: increase all RGB channels by 5
    colors = colors.astype(np.uint16)
    colors = (colors + rgb_step) % 256
    colors = colors.astype(np.uint8)

    apply_rgb_colors(cloud, colors)

    plt.render()


# --------------------------------------------------
# Plotter
# --------------------------------------------------
plt = vedo.Plotter(
    title="RGB point cube",
    axes=1,
    bg="black"
)

plt.add_callback("timer", update_colors)

plt.show(cloud, interactive=False)

# Create timer after showing scene
plt.timer_callback("create", dt=timer_interval)

plt.interactive()
plt.close()