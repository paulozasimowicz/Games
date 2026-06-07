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

sphere_radius = 0.45
sphere_center = np.array([0.0, 0.0, 0.0])


# --------------------------------------------------
# Create cube of points
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
print("Number of points:", n_points)


# --------------------------------------------------
# Create random RGB colours
# --------------------------------------------------
colors = np.random.randint(
    0, 256,
    size=(n_points, 3),
    dtype=np.uint8
)


# --------------------------------------------------
# Define central ball
# --------------------------------------------------
distances = np.linalg.norm(points - sphere_center, axis=1)
sphere_mask = distances <= sphere_radius
n_sphere_points = np.sum(sphere_mask)

print("Points inside central ball:", n_sphere_points)


# Set initial central ball colour
colors[sphere_mask] = np.array([255, 0, 0], dtype=np.uint8)


# --------------------------------------------------
# Create vedo point cloud
# --------------------------------------------------
cloud = vedo.Points(points, r=point_size)


# --------------------------------------------------
# Apply RGB colours
# --------------------------------------------------
def apply_colors():
    vtk_colors = numpy_to_vtk(
        colors,
        deep=True,
        array_type=vtk.VTK_UNSIGNED_CHAR
    )

    vtk_colors.SetNumberOfComponents(3)
    vtk_colors.SetName("RGBColors")

    cloud.dataset.GetPointData().SetScalars(vtk_colors)
    cloud.dataset.GetPointData().Modified()
    cloud.dataset.Modified()


apply_colors()


# --------------------------------------------------
# Create plotter
# --------------------------------------------------
plt = vedo.Plotter(
    title="RGB point cube with clickable colour controls",
    axes=1,
    bg="black",
    size=(1000, 800)
)


# --------------------------------------------------
# Button callbacks
# --------------------------------------------------
def increase_ball_rgb(button, event):
    global colors

    temp = colors[sphere_mask].astype(np.uint16)
    temp = (temp + rgb_step) % 256
    colors[sphere_mask] = temp.astype(np.uint8)

    apply_colors()
    plt.render()

    print("Button: increased central ball RGB by +5")


def randomize_ball_rgb(button, event):
    global colors

    colors[sphere_mask] = np.random.randint(
        0,
        256,
        size=(n_sphere_points, 3),
        dtype=np.uint8
    )

    apply_colors()
    plt.render()

    print("Button: randomized central ball RGB")


def reset_ball_rgb(button, event):
    global colors

    colors[sphere_mask] = np.array([255, 0, 0], dtype=np.uint8)

    apply_colors()
    plt.render()

    print("Button: reset central ball to red")


# --------------------------------------------------
# Add clickable buttons
# --------------------------------------------------
plt.add_button(
    increase_ball_rgb,
    pos=(0.18, 0.08),
    states=["RGB +5"],
    c=["white"],
    bc=["darkgreen"],
    font="courier",
    size=24,
    bold=True,
)

plt.add_button(
    randomize_ball_rgb,
    pos=(0.50, 0.08),
    states=["Random RGB"],
    c=["white"],
    bc=["darkblue"],
    font="courier",
    size=24,
    bold=True,
)

plt.add_button(
    reset_ball_rgb,
    pos=(0.82, 0.08),
    states=["Reset red"],
    c=["white"],
    bc=["darkred"],
    font="courier",
    size=24,
    bold=True,
)


# --------------------------------------------------
# Show scene
# --------------------------------------------------
plt.show(cloud, interactive=True).close()