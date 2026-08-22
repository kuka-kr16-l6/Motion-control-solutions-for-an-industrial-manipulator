import numpy as np

def compute_tangents(points):
    """Compute unit tangent vectors using finite differences."""
    n = len(points)
    tangents = np.zeros((n, 3))
    for i in range(n):
        if i == 0:
            t = points[1] - points[0]
        elif i == n - 1:
            t = points[-1] - points[-2]
        else:
            t = points[i + 1] - points[i - 1]
        norm = np.linalg.norm(t)
        tangents[i] = t / norm if norm > 1e-10 else (tangents[i-1] if i > 0 else np.array([1.0, 0.0, 0.0]))
    return tangents


def double_reflection(points, tangents, init_reference):
    """
    Direct NumPy translation of the doubleReflection algorithm from Wang et al.
    
    Args:
        points:         np.array (n, 3)
        tangents:       np.array (n, 3) — unit tangent at each point
        init_reference: np.array (3,)   — initial reference/normal vector

    Returns:
        frames: list of (r, s, t) tuples — reference, bitangent, tangent
    """
    n = len(points)
    assert n == len(tangents)

    def make_frame(reference, tangent):
        """Gram-Schmidt: make reference orthogonal to tangent, compute bitangent."""
        t = tangent / np.linalg.norm(tangent)
        # project reference onto tangent and subtract (Gram-Schmidt)
        r = reference - np.dot(reference, t) * t
        r_norm = np.linalg.norm(r)
        r = r / r_norm if r_norm > 1e-10 else np.array([0.0, 1.0, 0.0])
        s = np.cross(t, r)
        s /= np.linalg.norm(s)
        return r, s, t

    # initial frame
    r0, s0, t0 = make_frame(init_reference, tangents[0])
    frames = [(r0, s0, t0)]

    for i in range(n - 1):
        r_i, s_i, t_i = frames[i]

        # FIRST REFLECTION — reflect across plane perpendicular to v1
        v1 = points[i + 1] - points[i]
        c1 = np.dot(v1, v1)

        if c1 < 1e-12:
            # points coincide — carry frame forward
            r_next, s_next, t_next = make_frame(r_i, tangents[i + 1])
            frames.append((r_next, s_next, t_next))
            continue

        ref_L = r_i - (2.0 / c1) * np.dot(v1, r_i) * v1      # R1 * r_i
        tan_L = t_i - (2.0 / c1) * np.dot(v1, t_i) * v1      # R1 * t_i

        # SECOND REFLECTION — align tan_L with tangents[i+1]
        v2 = tangents[i + 1] - tan_L
        c2 = np.dot(v2, v2)

        if c2 < 1e-12:
            ref_next = ref_L
        else:
            ref_next = ref_L - (2.0 / c2) * np.dot(v2, ref_L) * v2   # R2 * ref_L

        # enforce continuity — prevent N sign flip
        if np.dot(ref_next, r_i) < 0:
            ref_next = -ref_next

        r_next, s_next, t_next = make_frame(ref_next, tangents[i + 1])
        frames.append((r_next, s_next, t_next))

    return frames

def rotation_matrix_to_rpy(R):
    """
    Numerically robust ZYX extraction directly from rotation matrix.
    Uses atan2 with full row/column to avoid division by cos(pitch).
    """
    # pitch — use full atan2 form instead of arcsin for better conditioning
    pitch =  np.arctan2(-R[2, 0], np.sqrt(R[0, 0]**2 + R[1, 0]**2))

    cos_pitch = np.sqrt(R[0, 0]**2 + R[1, 0]**2)  # already computed above

    if cos_pitch > 1e-6:
        # use full row elements — avoids dividing by cos_pitch directly
        roll = np.arctan2(R[2, 1], R[2, 2])
        yaw  = np.arctan2(R[1, 0], R[0, 0])
    else:
        # genuine gimbal lock at pitch = ±90°
        roll = 0.0
        if pitch > 0:
            yaw = np.arctan2(R[0, 1], R[1, 1])
        else:
            yaw = -np.arctan2(R[0, 1], R[1, 1])

    return roll, pitch, yaw




def extract_continuous_rpy(frames):
    """
    Extract RPY from frames while enforcing continuity between consecutive frames.
    Compares each result against previous and picks the equivalent representation
    that minimizes angular change.
    """
    n = len(frames)
    orientations_rad = np.zeros((n, 3))

    for i, (r, s, t) in enumerate(frames):
        R = np.column_stack([t, r, s])
        roll, pitch, yaw = rotation_matrix_to_rpy(R)
        orientations_rad[i] = [roll, pitch, yaw]

        if i > 0:
            prev = orientations_rad[i - 1]
            curr = orientations_rad[i]

            # for each angle, check if flipping by ±2π reduces the jump
            for col in range(3):
                diff = curr[col] - prev[col]
                if diff > np.pi:
                    orientations_rad[i, col] -= 2 * np.pi
                elif diff < -np.pi:
                    orientations_rad[i, col] += 2 * np.pi

            # handle the ±180° roll/yaw swap specifically
            # if both roll and yaw jumped by ~180°, flip both back
            roll_jump = abs(orientations_rad[i, 0] - prev[0])
            yaw_jump  = abs(orientations_rad[i, 2] - prev[2])

            if roll_jump > np.deg2rad(90) and yaw_jump > np.deg2rad(90):
                # switch to equivalent representation
                orientations_rad[i, 0] -= np.sign(orientations_rad[i, 0] - prev[0]) * np.pi
                orientations_rad[i, 2] -= np.sign(orientations_rad[i, 2] - prev[2]) * np.pi

    return orientations_rad


def compute_rmf(points, timesteps=None, init_reference=None):
    points = np.array(points, dtype=float)
    n = len(points)
    assert n >= 2

    tangents = compute_tangents(points)

    if init_reference is None:
        T0 = tangents[0]
        init_reference = np.array([0.0, 1.0, 0.0]) if abs(T0[0]) < 0.9 \
                         else np.array([0.0, 1.0, 0.0])

    frames = double_reflection(points, tangents, init_reference)
    # for i in range(len(frames)-1):
    #     r1, s1, t1 = frames[i]
    #     r2, s2, t2 = frames[i+1]

    #     R1 = np.column_stack([t1, r1, s1])
    #     R2 = np.column_stack([t2, r2, s2])

    #     Rrel = R1.T @ R2

    #     angle = np.degrees(
    #         np.arccos(
    #             np.clip((np.trace(Rrel)-1)/2, -1.0, 1.0)
    #         )
    #     )

    #     print(i, angle)
    # replace this:
    orientations_rad = np.array([
        rotation_matrix_to_rpy(np.column_stack([T, N, B]))
        for T, N, B in frames
    ])
    for col in range(3):
        orientations_rad[:, col] = np.unwrap(orientations_rad[:, col])

    # with this:
    orientations_rad = extract_continuous_rpy(frames)
    # no unwrap needed — continuity already enforced above

    orientations = np.array(orientations_rad)

    # ── angular velocity and acceleration ─────────────────────────────
    if timesteps is not None:
        timesteps = np.array(timesteps, dtype=float)
        assert len(timesteps) == n

        ang_velocities = np.zeros((n, 3))
        ang_accs       = np.zeros((n, 3))

        for i in range(n):
            if i == 0:
                dt = timesteps[1] - timesteps[0]
                dO = orientations[1] - orientations[0]
            elif i == n - 1:
                dt = timesteps[-1] - timesteps[-2]
                dO = orientations[-1] - orientations[-2]
            else:
                dt = timesteps[i + 1] - timesteps[i - 1]
                dO = orientations[i + 1] - orientations[i - 1]
            ang_velocities[i] = dO / dt if dt > 1e-10 else np.zeros(3)

        for i in range(n):
            if i == 0:
                dt = timesteps[1] - timesteps[0]
                dV = ang_velocities[1] - ang_velocities[0]
            elif i == n - 1:
                dt = timesteps[-1] - timesteps[-2]
                dV = ang_velocities[-1] - ang_velocities[-2]
            else:
                dt = timesteps[i + 1] - timesteps[i - 1]
                dV = ang_velocities[i + 1] - ang_velocities[i - 1]
            ang_accs[i] = dV / dt if dt > 1e-10 else np.zeros(3)

        return orientations, ang_velocities, ang_accs, frames

    return orientations, None, None, frames