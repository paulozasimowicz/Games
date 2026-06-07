import time
import cv2
import numpy as np
import vedo
import vtk
from vtk.util.numpy_support import numpy_to_vtk


# --------------------------------------------------
# Parameters
# --------------------------------------------------
camera_index = 0

nx = 100
ny = 100
nz = 30

point_size = 4
frame_delay = 0.03  # seconds, approximately 30 FPS


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
    cap.release()
    raise RuntimeError("Could not read from camera.")


# --------------------------------------------------
# Preprocess first camera frame
# --------------------------------------------------
frame = cv2.flip(frame, 1)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = cv2.resize(frame, (nx, ny), interpolation=cv2.INTER_AREA)


# --------------------------------------------------
# Create 3D point cube
# --------------------------------------------------
x = np.linspace(-1, 1, nx)
y = np.linspace(-1, 1, ny)
z = np.linspace(-1, 1, nz)

X, Y, Z = np.meshgrid(x, y, z, indexing="xy")

points = np.column_stack([
    X.ravel(),
    -Y.ravel(),   # keeps camera orientation correct
    Z.ravel()
])

n_points = points.shape[0]
print("Number of points:", n_points)


# --------------------------------------------------
# Convert 2D camera image into 3D colour volume
# --------------------------------------------------
def frame_to_3d_colors(frame_rgb):
    """
    Takes a 2D RGB camera frame with shape (ny, nx, 3)
    and copies each pixel colour through all z-layers.

    Output shape:
    (ny * nx * nz, 3)
    """

    colour_volume = np.repeat(
        frame_rgb[:, :, np.newaxis, :],
        nz,
        axis=2
    )

    return colour_volume.reshape(-1, 3).astype(np.uint8)


colors = frame_to_3d_colors(frame)


# --------------------------------------------------
# Create vedo point cloud
# --------------------------------------------------
cloud = vedo.Points(points, r=point_size)


# --------------------------------------------------
# Apply RGB colours to point cloud
# --------------------------------------------------
def apply_colors():
    vtk_colors = numpy_to_vtk(
        colors,
        deep=True,
        array_type=vtk.VTK_UNSIGNED_CHAR
    )

    vtk_colors.SetNumberOfComponents(3)
    vtk_colors.SetName("CameraRGB3D")

    cloud.dataset.GetPointData().SetScalars(vtk_colors)
    cloud.dataset.GetPointData().Modified()
    cloud.dataset.Modified()


apply_colors()


# --------------------------------------------------
# Create plotter
# --------------------------------------------------
plt = vedo.Plotter(
    title="Live camera mapped to 3D RGB point cube",
    axes=1,
    bg="black",
    size=(1000, 900)
)


# --------------------------------------------------
# Show scene
# --------------------------------------------------
plt.show(cloud, interactive=False)


# --------------------------------------------------
# Close-window control
# --------------------------------------------------
running = True


def stop_program(obj=None, event=None):
    global running
    running = False
    print("Close requested.")


try:
    plt.interactor.AddObserver("ExitEvent", stop_program)
    plt.interactor.AddObserver("DeleteEvent", stop_program)
except Exception as e:
    print("Could not attach close callback:", e)


# --------------------------------------------------
# Live camera loop
# --------------------------------------------------
try:
    while running:
        try:
            plt.interactor.ProcessEvents()
        except Exception:
            running = False
            break

        ret, frame = cap.read()

        if not ret:
            print("Camera frame not received.")
            continue

        # Mirror camera
        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize to point grid resolution
        frame = cv2.resize(frame, (nx, ny), interpolation=cv2.INTER_AREA)

        # Convert camera frame to 3D colour cube
        colors[:] = frame_to_3d_colors(frame)

        apply_colors()
        plt.render()

        time.sleep(frame_delay)

except KeyboardInterrupt:
    print("Stopped manually with Ctrl+C.")

finally:
    running = False

    if cap is not None:
        cap.release()

    try:
        plt.close()
    except Exception:
        pass

    print("Camera released. Program closed.")