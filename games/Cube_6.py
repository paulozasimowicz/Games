import time
import cv2
import numpy as np
import vedo
import vtk
from vtk.util.numpy_support import numpy_to_vtk


# --------------------------------------------------
# Parameters
# --------------------------------------------------
camera_index = 0   # default webcam. Try 1 or 2 if it does not open.

nx = 100
ny = 100

point_size = 8
frame_delay = 0.03  # seconds, about 30 FPS


# --------------------------------------------------
# Open camera
# --------------------------------------------------
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    raise RuntimeError(
        "Could not open camera. Try changing camera_index to 1 or 2."
    )


# --------------------------------------------------
# Read first camera frame
# --------------------------------------------------
ret, frame = cap.read()

if not ret:
    raise RuntimeError("Could not read from camera.")


# --------------------------------------------------
# Convert first frame to RGB and resize
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
    -Y.ravel(),              # negative Y so camera image is not upside down
    np.zeros(nx * ny)
])

n_points = points.shape[0]
print("Number of points:", n_points)


# --------------------------------------------------
# Convert camera pixels to point colours
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
    vtk_colors.SetName("CameraRGB")

    cloud.dataset.GetPointData().SetScalars(vtk_colors)
    cloud.dataset.GetPointData().Modified()
    cloud.dataset.Modified()


apply_colors()


# --------------------------------------------------
# Create plotter
# --------------------------------------------------
plt = vedo.Plotter(
    title="Live camera mapped to RGB point grid",
    axes=1,
    bg="black",
    size=(900, 900)
)

plt.show(cloud, interactive=False)


# --------------------------------------------------
# Live camera loop
# --------------------------------------------------
try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Camera frame not received.")
            continue

        # Optional: mirror camera like a selfie view
        frame = cv2.flip(frame, 1)

        # OpenCV uses BGR, vedo/VTK colours should be RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize camera frame to match the point grid
        frame = cv2.resize(frame, (nx, ny), interpolation=cv2.INTER_AREA)

        # Update point colours from camera pixels
        colors[:] = frame.reshape(-1, 3).astype(np.uint8)

        apply_colors()
        plt.render()

        time.sleep(frame_delay)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    cap.release()
    plt.close()