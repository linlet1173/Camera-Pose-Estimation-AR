import cv2 as cv
import numpy as np

# === Calibration Data ===
K = np.array([
    [2137.63718, 0, 550.773459],
    [0, 2138.19531, 978.379842],
    [0, 0, 1]
])
dist_coeff = np.array([0.226712813, -1.31541165, 0.00347213231, -0.0000459365739, 3.56670726])

# === Chessboard Info ===
board_pattern = (8, 6)  # inner corners
board_cellsize = 30.0   # mm

# === 3D Line Definitions for L, I, N ===
def get_letter_lines(base_x, depth=10):
    def cube_lines(p1, p2):
        """Create 3D box edges between two points defining a cuboid"""
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        # 8 corners of a cuboid
        corners = [
            (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1),
            (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2)
        ]
        # edges to draw
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # bottom face
            (4, 5), (5, 6), (6, 7), (7, 4),  # top face
            (0, 4), (1, 5), (2, 6), (3, 7)   # verticals
        ]
        return [[corners[i], corners[j]] for i, j in edges]

    # Each line is now a cuboid instead of a flat line
    L = cube_lines((0, 0, 0), (10, 90, depth)) + cube_lines((0, 0, 0), (30, 10, depth))
    I = cube_lines((10, 0, 0), (20, 90, depth)) + \
        cube_lines((0, 0, 0), (30, 10, depth)) + \
        cube_lines((0, 90, 0), (30, 90, depth))
    # N with two vertical cubes + one diagonal line (not cube)
    N_verticals = cube_lines((0, 0, 0), (10, 90, depth)) + cube_lines((30, 0, 0), (40, 90, depth))
    N_diagonal = [[(0, 0, 0), (40, 90, depth)]]  # thin 3D line

    N = N_verticals + N_diagonal


    def shift(letter, shift_x):
        return [[(x + shift_x, y, z) for (x, y, z) in line] for line in letter]

    return shift(L, base_x) + shift(I, base_x + 50) + shift(N, base_x + 110)


letter_lines = get_letter_lines(0, depth=10)
letter_lines = [np.array(line, dtype=np.float32) for line in letter_lines]


# === Chessboard Object Points ===
objp = np.zeros((board_pattern[0] * board_pattern[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:board_pattern[0], 0:board_pattern[1]].T.reshape(-1, 2)
objp *= board_cellsize

# === Load the Video ===
import os
video_path = os.path.expanduser("~/Desktop/computer vision/cv assignments/chessboard.avi")
cap = cv.VideoCapture(video_path)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# === Output Video Writer (Optional) ===
frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv.CAP_PROP_FPS)
out = cv.VideoWriter('ar_object.avi', cv.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    success, corners = cv.findChessboardCorners(gray, board_pattern, None)

    if success:
        corners_refined = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        ret, rvec, tvec = cv.solvePnP(objp, corners_refined, K, dist_coeff)

        for line3d in letter_lines:
            pts_2d, _ = cv.projectPoints(line3d, rvec, tvec, K, dist_coeff)
            pt1 = tuple(np.int32(pts_2d[0].ravel()))
            pt2 = tuple(np.int32(pts_2d[1].ravel()))
            cv.line(frame, pt1, pt2, (0, 0, 255), 3)

        R, _ = cv.Rodrigues(rvec)
        cam_pos = (-R.T @ tvec).flatten()
        info = f'Camera XYZ: [{cam_pos[0]:.1f}, {cam_pos[1]:.1f}, {cam_pos[2]:.1f}]'
        cv.putText(frame, info, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        cv.drawChessboardCorners(frame, board_pattern, corners_refined, success)

    cv.imshow("AR Object", frame)
    out.write(frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()
