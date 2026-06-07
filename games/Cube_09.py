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

nx = 100          # image width in points
ny = 100          # image height in points
nz = 30           # number of time-history layers

point_size = 4
frame_delay = 0.03   # approximately 30 FPS

change_threshold = 40       # larger = less sensitive
min_changed_pixels = 50     # ignore small noise changes


# --------------------------------------------------
# Open camera
# --------------------------------------------------
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    raise RuntimeError(
        "Could not open camera. Try camera_index = 1 or 2."
    )


# --------------------------------------------------
# Frame preprocessing
# --------------------------------------------------
def preprocess_frame(frame_bgr):
    """
    Convert camera frame from BGR to RGB,
    mirror it, and resize it to the point-grid resolution.
    """

    frame_bgr = cv2.flip(frame_bgr, 1)  # mirror camera like selfie view
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.resize(frame_rgb, (nx, ny), interpolation=cv2.INTER_AREA)

    return frame_rgb.astype(np.uint8)


# --------------------------------------------------
# Change detection
# --------------------------------------------------
def estimate_changed_area(frame_rgb, background_rgb, threshold=40):
    """
    Estimate changed pixels by comparing the current frame
    against the background frame.

    Returns
    -------
    area_pixels : int
        Number of changed pixels.

    change_mask : np.ndarray
        Boolean mask with shape (ny, nx).
        True means changed.
    """

    diff = np.abs(
        frame_rgb.astype(np.int16) - background_rgb.astype(np.int16)
    )

    diff_gray = np.mean(diff, axis=2)

    change_mask = diff_gray > threshold

    area_pixels = int(np.sum(change_mask))

    return area_pixels, change_mask


# --------------------------------------------------
# Read first frame
# --------------------------------------------------
ret, frame = cap.read()

if not ret:
    cap.release()
    raise RuntimeError("Could not read first frame from camera.")


frame0 = preprocess_frame(frame)


# --------------------------------------------------
# Use first frame as background
# Keep the scene empty when you start the script.
# --------------------------------------------------
background_frame = frame0.copy()


# --------------------------------------------------
# Create 3D point cube
# --------------------------------------------------
x = np.linspace(-1, 1, nx)
y = np.linspace(-1, 1, ny)
z = np.linspace(-1, 1, nz)

X, Y, Z = np.meshgrid(x, y, z, indexing="xy")

points = np.column_stack([
    X.ravel(),
    -Y.ravel(),   # flip vertically for correct camera orientation
    Z.ravel()
])

n_points = points.shape[0]

print("Number of points:", n_points)
print("Stored history duration depends on FPS.")
print(f"At ~30 FPS and nz={nz}, the cube stores about {nz / 30:.2f} seconds.")


# --------------------------------------------------
# Create initial colour volume
# Shape: (ny, nx, nz, 3)
#
# z = 0        newest frame
# z = nz - 1   oldest frame
# --------------------------------------------------
color_volume = np.repeat(
    frame0[:, :, np.newaxis, :],
    nz,
    axis=2
).astype(np.uint8)


# --------------------------------------------------
# Optional: create a change-volume for detected motion
# Shape: (ny, nx, nz)
# --------------------------------------------------
change_volume = np.zeros((ny, nx, nz), dtype=bool)


# Flatten colour array for VTK
colors = color_volume.reshape(-1, 3).copy()


# --------------------------------------------------
# Create vedo point cloud
# --------------------------------------------------
cloud = vedo.Points(points, r=point_size)


# --------------------------------------------------
# Apply RGB colours to VTK/vedo point cloud
# --------------------------------------------------
def apply_colors():
    vtk_colors = numpy_to_vtk(
        colors,
        deep=True,
        array_type=vtk.VTK_UNSIGNED_CHAR
    )

    vtk_colors.SetNumberOfComponents(3)
    vtk_colors.SetName("RGBTimeHistory")

    cloud.dataset.GetPointData().SetScalars(vtk_colors)
    cloud.dataset.GetPointData().Modified()
    cloud.dataset.Modified()


apply_colors()


# --------------------------------------------------
# Create plotter
# --------------------------------------------------
plt = vedo.Plotter(
    title="Live camera as 3D RGB time-history cube",
    axes=1,
    bg="black",
    size=(1000, 900)
)

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
# Live loop
# --------------------------------------------------
frame_counter = 0

try:
    while running:
        # Process GUI/window events
        try:
            plt.interactor.ProcessEvents()
        except Exception:
            running = False
            break

        ret, frame = cap.read()

        if not ret:
            print("Camera frame not received.")
            continue

        new_frame = preprocess_frame(frame)

        # --------------------------------------------------
        # Estimate changed pixels compared with background
        # --------------------------------------------------
        changed_pixels, change_mask = estimate_changed_area(
            new_frame,
            background_frame,
            threshold=change_threshold
        )

        if changed_pixels < min_changed_pixels:
            changed_pixels = 0
            change_mask[:, :] = False

        # --------------------------------------------------
        # Shift colour history backward in z
        # z = 0 becomes z = 1, z = 1 becomes z = 2, etc.
        # --------------------------------------------------
        color_volume[:, :, 1:, :] = color_volume[:, :, :-1, :]

        # Insert newest camera frame at the front layer
        color_volume[:, :, 0, :] = new_frame

        # --------------------------------------------------
        # Shift change history backward in z
        # --------------------------------------------------
        change_volume[:, :, 1:] = change_volume[:, :, :-1]

        # Insert newest change mask at the front layer
        change_volume[:, :, 0] = change_mask

        # --------------------------------------------------
        # Optional visual emphasis:
        # highlight changed pixels in the newest layer in red.
        #
        # Comment these two lines if you want pure camera colours only.
        # --------------------------------------------------
        highlighted_frame = color_volume[:, :, 0, :].copy()
        highlighted_frame[change_mask] = np.array([255, 0, 0], dtype=np.uint8)
        color_volume[:, :, 0, :] = highlighted_frame

        # --------------------------------------------------
        # Update VTK colour array
        # --------------------------------------------------
        colors[:] = color_volume.reshape(-1, 3)

        apply_colors()
        plt.render()

        # --------------------------------------------------
        # Print measurements
        # --------------------------------------------------
        if frame_counter % 10 == 0:
            active_layers = np.sum(np.any(change_volume, axis=(0, 1)))
            total_changed_volume = int(np.sum(change_volume))

            print(
                f"Current changed area: {changed_pixels:5d} pixels | "
                f"active history layers: {active_layers:2d}/{nz} | "
                f"changed voxels in history: {total_changed_volume:6d}"
            )

        frame_counter += 1

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