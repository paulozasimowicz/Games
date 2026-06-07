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

nx = 100          # width  of each frame in points
ny = 100          # height of each frame in points
nz = 30           # number of time-history layers in depth

point_size = 4
frame_delay = 0.03   # about 30 FPS


# --------------------------------------------------
# Open camera
# --------------------------------------------------
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    raise RuntimeError(
        "Could not open camera. Try camera_index = 1 or 2."
    )


# --------------------------------------------------
# Read first frame
# --------------------------------------------------
ret, frame = cap.read()

if not ret:
    cap.release()
    raise RuntimeError("Could not read first frame from camera.")


# --------------------------------------------------
# Frame preprocessing function
# --------------------------------------------------
def preprocess_frame(frame_bgr):
    frame_bgr = cv2.flip(frame_bgr, 1)  # mirror view
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.resize(frame_rgb, (nx, ny), interpolation=cv2.INTER_AREA)
    return frame_rgb.astype(np.uint8)


frame0 = preprocess_frame(frame)


# --------------------------------------------------
# Create 3D point cube
# shape will correspond to volume shape (ny, nx, nz)
# --------------------------------------------------
x = np.linspace(-1, 1, nx)
y = np.linspace(-1, 1, ny)
z = np.linspace(-1, 1, nz)

X, Y, Z = np.meshgrid(x, y, z, indexing="xy")

points = np.column_stack([
    X.ravel(),
    -Y.ravel(),   # flip vertically so image is visually correct
    Z.ravel()
])

n_points = points.shape[0]
print("Number of points:", n_points)


# --------------------------------------------------
# Create colour volume
# volume[y, x, z, rgb]
# front layer z=0 = newest frame
# back layers = older frames
# --------------------------------------------------
color_volume = np.repeat(
    frame0[:, :, np.newaxis, :],
    nz,
    axis=2
).astype(np.uint8)


# Flattened colour array used by VTK
colors = color_volume.reshape(-1, 3).copy()


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
    vtk_colors.SetName("RGBHistory")

    cloud.dataset.GetPointData().SetScalars(vtk_colors)
    cloud.dataset.GetPointData().Modified()
    cloud.dataset.Modified()


apply_colors()


# --------------------------------------------------
# Create plotter
# --------------------------------------------------
plt = vedo.Plotter(
    title="Live camera as 3D time-history RGB cube",
    axes=1,
    bg="black",
    size=(1000, 900)
)

plt.show(cloud, interactive=False)


# --------------------------------------------------
# Close handling
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
# Main live loop
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
            continue

        new_frame = preprocess_frame(frame)

        # --------------------------------------------------
        # Shift history backward in z
        # z=0 is newest, z=1 previous, z=2 older, ...
        # --------------------------------------------------
        color_volume[:, :, 1:, :] = color_volume[:, :, :-1, :]

        # Insert newest frame at front
        color_volume[:, :, 0, :] = new_frame

        # Flatten for VTK
        colors[:] = color_volume.reshape(-1, 3)

        apply_colors()
        plt.render()

        time.sleep(frame_delay)

except KeyboardInterrupt:
    print("Stopped with Ctrl+C.")

finally:
    running = False
    cap.release()
    try:
        plt.close()
    except Exception:
        pass
    print("Camera released. Program closed.")