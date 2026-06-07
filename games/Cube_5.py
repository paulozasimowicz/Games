import time
import cv2
import numpy as np
import vedo
import vtk
from vtk.util.numpy_support import numpy_to_vtk


# --------------------------------------------------
# Parameters
# --------------------------------------------------
video_path = "your_video.mp4"   # change this to your video path

nx = 100
ny = 100

point_size = 8
frame_delay = 0.03  # seconds, about 30 FPS


# --------------------------------------------------
# Open video
# --------------------------------------------------
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {video_path}")


# --------------------------------------------------
# Read first frame
# --------------------------------------------------
ret, frame = cap.read()

if not ret:
    raise RuntimeError("Could not read first frame from video.")


# --------------------------------------------------
# Convert first frame to RGB and resize to 100 x 100
# OpenCV reads video as BGR, so convert to RGB
# --------------------------------------------------
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = cv2.resize(frame, (nx, ny), interpolation=cv2.INTER_AREA)


# --------------------------------------------------
# Create 2D point grid
# --------------------------------------------------
x = np.linspace(-1, 1, nx)
y = np.linspace(-1, 1, ny)

X, Y = np.meshgrid(x, y, indexing="xy")

points = np.column_stack([
    X.ravel(),
    Y.ravel(),
    np.zeros(nx * ny)
])

n_points = points.shape[0]
print("Number of points:", n_points)


# --------------------------------------------------
# Convert image pixels to point colours
# --------------------------------------------------
colors = frame.reshape(-1, 3).astype(np.uint8)


# --------------------------------------------------
# Create vedo point cloud
# --------------------------------------------------
cloud = vedo.Points(points, r=point_size)


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
    title="Video mapped to RGB point grid",
    axes=1,
    bg="black",
    size=(900, 900)
)

plt.show(cloud, interactive=False)


# --------------------------------------------------
# Animation loop
# --------------------------------------------------
while True:
    ret, frame = cap.read()

    # Restart video when it reaches the end
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize frame to match point grid
    frame = cv2.resize(frame, (nx, ny), interpolation=cv2.INTER_AREA)

    # Update point colours
    colors[:] = frame.reshape(-1, 3).astype(np.uint8)

    apply_colors()
    plt.render()

    time.sleep(frame_delay)