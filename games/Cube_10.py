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

point_size_full = 4
point_size_change = 5

frame_delay = 0.03   # approximately 30 FPS

change_threshold = 40       # larger = less sensitive
min_changed_pixels = 50     # ignore small noise changes

# Options:
# "camera" = changed points keep their camera RGB colour
# "red"    = changed points are shown in red
change_display_mode = "camera"


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
    frame_bgr = cv2.flip(frame_bgr, 1)  # mirror camera
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.resize(frame_rgb, (nx, ny), interpolation=cv2.INTER_AREA)
    return frame_rgb.astype(np.uint8)


# --------------------------------------------------
# Change detection
# --------------------------------------------------
def estimate_changed_area(frame_rgb, background_rgb, threshold=40):
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

# First frame is used as the background.
# Start the script with no moving object in the view.
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
    -Y.ravel(),
    Z.ravel()
])

n_points = points.shape[0]

print("Number of points:", n_points)
print(f"At ~30 FPS and nz={nz}, the cube stores about {nz / 30:.2f} seconds.")


# --------------------------------------------------
# Create initial colour volume
# Shape: (ny, nx, nz, 3)
# --------------------------------------------------
color_volume = np.repeat(
    frame0[:, :, np.newaxis, :],
    nz,
    axis=2
).astype(np.uint8)


# --------------------------------------------------
# Create change volume
# Shape: (ny, nx, nz)
# True = changed point
# False = unchanged point
# --------------------------------------------------
change_volume = np.zeros((ny, nx, nz), dtype=bool)


# --------------------------------------------------
# Flatten colour arrays for VTK
# --------------------------------------------------
colors_full = color_volume.reshape(-1, 3).copy()

colors_change = np.zeros_like(colors_full, dtype=np.uint8)


# --------------------------------------------------
# Create vedo point clouds
# --------------------------------------------------
cloud_full = vedo.Points(points, r=point_size_full)
cloud_change = vedo.Points(points, r=point_size_change)


# --------------------------------------------------
# Apply RGB colours to a vedo actor
# --------------------------------------------------
def apply_colors(actor, rgb_array, scalar_name):
    vtk_colors = numpy_to_vtk(
        rgb_array,
        deep=True,
        array_type=vtk.VTK_UNSIGNED_CHAR
    )

    vtk_colors.SetNumberOfComponents(3)
    vtk_colors.SetName(scalar_name)

    actor.dataset.GetPointData().SetScalars(vtk_colors)
    actor.dataset.GetPointData().Modified()
    actor.dataset.Modified()


apply_colors(cloud_full, colors_full, "FullRGBHistory")
apply_colors(cloud_change, colors_change, "ChangedRGBHistory")


# --------------------------------------------------
# Create two plotter windows
# --------------------------------------------------
plt_full = vedo.Plotter(
    title="Full live camera RGB time-history cube",
    axes=1,
    bg="black",
    size=(900, 800),
    pos=(50, 50),
)

plt_change = vedo.Plotter(
    title="Only changing points",
    axes=1,
    bg="black",
    size=(900, 800),
    pos=(1000, 50),
)


# --------------------------------------------------
# Show both windows
# --------------------------------------------------
plt_full.show(cloud_full, interactive=False)
plt_change.show(cloud_change, interactive=False)


# --------------------------------------------------
# Close-window control
# --------------------------------------------------
running = True


def stop_program(obj=None, event=None):
    global running
    running = False
    print("Close requested.")


for plotter in [plt_full, plt_change]:
    try:
        plotter.interactor.AddObserver("ExitEvent", stop_program)
        plotter.interactor.AddObserver("DeleteEvent", stop_program)
    except Exception as e:
        print("Could not attach close callback:", e)


# --------------------------------------------------
# Build changed-only colours
# --------------------------------------------------
def build_changed_only_colors():
    """
    Creates the colour array for the second window.

    Unchanged points are black.
    Changed points are either:
    - original camera colour, or
    - red, depending on change_display_mode.
    """

    flat_change_mask = change_volume.reshape(-1)
    flat_rgb = color_volume.reshape(-1, 3)

    output = np.zeros_like(flat_rgb, dtype=np.uint8)

    if change_display_mode == "red":
        output[flat_change_mask] = np.array([255, 0, 0], dtype=np.uint8)

    else:
        output[flat_change_mask] = flat_rgb[flat_change_mask]

    return output


# --------------------------------------------------
# Main live loop
# --------------------------------------------------
frame_counter = 0

try:
    while running:
        # Process both GUI windows
        try:
            plt_full.interactor.ProcessEvents()
            plt_change.interactor.ProcessEvents()
        except Exception:
            running = False
            break

        ret, frame = cap.read()

        if not ret:
            print("Camera frame not received.")
            continue

        new_frame = preprocess_frame(frame)

        # --------------------------------------------------
        # Detect changed pixels against the background
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
        # Shift RGB history backward in z
        # z=0 newest, z=1 previous, z=2 older, ...
        # --------------------------------------------------
        color_volume[:, :, 1:, :] = color_volume[:, :, :-1, :]
        color_volume[:, :, 0, :] = new_frame

        # --------------------------------------------------
        # Shift change history backward in z
        # --------------------------------------------------
        change_volume[:, :, 1:] = change_volume[:, :, :-1]
        change_volume[:, :, 0] = change_mask

        # --------------------------------------------------
        # Update first window: full RGB history
        # --------------------------------------------------
        colors_full[:] = color_volume.reshape(-1, 3)

        apply_colors(
            cloud_full,
            colors_full,
            "FullRGBHistory"
        )

        # --------------------------------------------------
        # Update second window: only changed points
        # --------------------------------------------------
        colors_change[:] = build_changed_only_colors()

        apply_colors(
            cloud_change,
            colors_change,
            "ChangedRGBHistory"
        )

        # --------------------------------------------------
        # Render both windows
        # --------------------------------------------------
        plt_full.render()
        plt_change.render()

        # --------------------------------------------------
        # Print measurements
        # --------------------------------------------------
        if frame_counter % 10 == 0:
            active_layers = int(np.sum(np.any(change_volume, axis=(0, 1))))
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
        plt_full.close()
    except Exception:
        pass

    try:
        plt_change.close()
    except Exception:
        pass

    print("Camera released. Program closed.")