import sys
import numpy as np
from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from autogen.settings import setup_qt_environment
from F_JOG_joint.quintic_traj import trajectory
from F_JOG_joint.forward_kinem import F_K
from F_communication.can_interface import CanInterface
from F_JOG_cartesian.main_JOG_cart import cart_calc
from F_JOG_cartesian.robot import robotRobot
from F_CART_._main_cart_ import Bcart_calc

class Backend(QObject):
    # joint signals
    joint1AngleChanged = Signal()
    joint2AngleChanged = Signal()
    joint3AngleChanged = Signal()
    joint4AngleChanged = Signal()
    joint5AngleChanged = Signal()
    joint6AngleChanged = Signal()

    # cartesian signals
    cartXChanged     = Signal()
    cartYChanged     = Signal()
    cartZChanged     = Signal()
    cartRollChanged  = Signal()
    cartPitchChanged = Signal()
    cartYawChanged   = Signal()

    IKErrorOccurred = Signal(str)
    canStatusChanged = Signal()

    MAX_VELOCITY     = 500
    MAX_ACCELERATION = 340000 / (3**2)
    TIME_STEPS       = 100
    DEBOUNCE_DELAY   = 150

    def __init__(self):
        super().__init__()
        self.can = CanInterface("can0")
        print("CAN connected:", self.can.connect_bus())
        self._can_status = "disconnected"
        self.can.statusChanged.connect(self._on_can_status)
        self.robot = robotRobot()

        self._current_joints = [0.0, 0.0, 0.0, 0.0, 90.0, 0.0]    # degrees

        fk = F_K(self._current_joints)
        self._current_cart = list(fk)      # [x_mm, y_mm, z_mm, roll_deg, pitch_deg, yaw_deg]
        # ────────────────────────────────────────────

        # previous positions for delta CAN sending
        self._prev_joint_pos = [0.0] * 6
        self._prev_cart_pos  = [0.0] * 6
        self._prev_bcart_pos = [0.0] * 6
        self._bcart_steps = None
        # guard flags
        self._updating_from_playback = False
        self._updating_from_fk       = False

        # pending targets
        self._pending_joints = {}
        self._pending_cart   = {}

        # joint debounce
        self._debounce_timer = QTimer()
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.timeout.connect(self._execute_joint_trajectory)

        # cart debounce
        self._cart_debounce_timer = QTimer()
        self._cart_debounce_timer.setSingleShot(True)
        self._cart_debounce_timer.timeout.connect(self._execute_cart_trajectory)

        # joint playback timer
        self._joint_playback_timer = QTimer()
        self._joint_playback_timer.timeout.connect(self._joint_playback_step)
        self._joint_playback_index = 0
        self._joint_playback_pos   = None
        self._joint_playback_vel   = None

        # cart playback timer
        self._cart_playback_timer = QTimer()
        self._cart_playback_timer.timeout.connect(self._cart_playback_step)
        self._cart_playback_index = 0
        self._cart_playback_pos   = None
        self._cart_playback_vel   = None

        # bcart playback timer
        self._bcart_playback_timer = QTimer()
        self._bcart_playback_timer.timeout.connect(self._bcart_playback_step)
        self._bcart_playback_index = 0
        self._bcart_playback_pos   = None
        self._bcart_playback_vel   = None

    # ─────────────────────────────────────────────
    # QML → BACKEND SLOTS
    # ─────────────────────────────────────────────

    @Slot(int, float)
    def jointChanged(self, joint, angle):
        if self._updating_from_playback:
            return
        self._pending_joints[joint] = angle
        self._debounce_timer.start(self.DEBOUNCE_DELAY)

    @Slot(int, float)
    def posChanged(self, axis, value):
        if self._updating_from_fk:
            return
        self._pending_cart[axis] = value
        self._cart_debounce_timer.start(self.DEBOUNCE_DELAY)

    # ─────────────────────────────────────────────
    # JOINT TRAJECTORY
    # ─────────────────────────────────────────────

    def _execute_joint_trajectory(self):
        current = list(self._current_joints)
        target = [
            self._pending_joints.get(j, current[j - 1])
            for j in range(1, 7)
        ]
        self._pending_joints.clear()

        if all(abs(c - t) < 0.001 for c, t in zip(current, target)):
            return

        traj = trajectory(
            current, target,
            start_velocity=0, end_velocity=0,
            start_acceleration=0, end_acceleration=0,
            max_acceleration=self.MAX_ACCELERATION,
            max_velocity=self.MAX_VELOCITY,
            time_steps_=self.TIME_STEPS
        )
        all_pos, all_vel, _ = traj.Quintic_trajectory()
        duration = traj.compute_time()
        # print("pos", all_pos)
        # max_val = 0
        # prev= 0 
        # all_pos = np.array(all_pos)
        # for i,p in enumerate(all_pos[5]):
        #     delta = all_pos[5][i] - prev
            
        #     delta_int = int(delta )
        #     if abs(delta_int) > max_val:
        #         max_val = abs(delta_int)
        # print("max_val:", max_val)
        self._joint_playback_pos   = all_pos
        self._joint_playback_vel   = all_vel
        self._joint_playback_index = 0
        self._prev_joint_pos       = list(current)

        interval_ms = max(1, int((duration / self.TIME_STEPS) * 1000))
        self._cart_playback_timer.stop()
        self._joint_playback_timer.start(interval_ms)

    def _joint_playback_step(self):
        # guard at entry
        if self._joint_playback_pos is None or \
        self._joint_playback_index >= len(self._joint_playback_pos[0]):
            self._joint_playback_timer.stop()
            return

        idx = self._joint_playback_index
        joint_data = {}

        self._updating_from_playback = True

        for i in range(6):
            joint_id  = i + 1
            pos_val   = self._joint_playback_pos[i][idx]
            vel_val   = self._joint_playback_vel[i][idx]
            delta     = pos_val - self._prev_joint_pos[i]
            self._prev_joint_pos[i] = pos_val
            direction = 1 if delta > 0 else 0

            self._current_joints[i] = pos_val
            self._emit_joint(joint_id, pos_val)
            
            delta_int = int(delta * 10000.0)
            # if i ==4:
            #     print("delta_int:", delta_int)
            # print ("max_val", delta_int)
            # delta  = np.array(delta_int)
            # max_val = np.max(np.abs(delta))
            # print("delta_int:", max_val)
            joint_data[joint_id] = [direction, abs(delta_int), abs(int(vel_val))]

        self._updating_from_playback = False
        self.can.send_all_joints(joint_data)
        self._joint_playback_index += 1
        if self._joint_playback_index >= len(self._joint_playback_pos[0]):
            # print ("loop joint current ",self._current_joints )

            self._joint_playback_timer.stop()
            self._sync_cart_from_joints()
    # ─────────────────────────────────────────────
    # CART TRAJECTORY
    # ─────────────────────────────────────────────

    def _execute_cart_trajectory(self):
        current_cart = list(self._current_cart)
        target_cart = [
            self._pending_cart.get(i + 1, current_cart[i])
            for i in range(6)
        ]
        self._pending_cart.clear()

        if all(abs(c - t) < 0.0001 for c, t in zip(current_cart, target_cart)):
            return

        try:
            # spinbox units: mm/deg → cart_calc units: m/rad
            current_m = [
                current_cart[0] / 1000.0,
                current_cart[1] / 1000.0,
                current_cart[2] / 1000.0,
                np.deg2rad(current_cart[3])  ,
                np.deg2rad(current_cart[4])  ,
                np.deg2rad(current_cart[5])  ,
            ]
            target_m = [
                target_cart[0] / 1000.0,
                target_cart[1] / 1000.0,
                target_cart[2] / 1000.0,
                np.deg2rad(target_cart[3]),
                np.deg2rad(target_cart[4]),
                np.deg2rad(target_cart[5]),
            ]
            # print("current_pos_before_trajectory:", current_m)
            # print("current_joints_before_trajectory:", self._current_joints)
            theta_p, vel_joint_p, time__, time_steps = cart_calc(current_m, np.deg2rad(self._current_joints), target_m)
            # print ("cart_calc returned:", theta_p)
            if theta_p is None or vel_joint_p is None:
                raise ValueError("NO IK solution found")
            # theta_p: (time_steps, 6) degrees
            # vel_joint_p: (time_steps, 6) deg/s with gear ratio

            self._cart_playback_pos   = [theta_p[:, i] for i in range(6)]
            self._cart_playback_vel   = [vel_joint_p[:, i] for i in range(6)]
            self._cart_playback_index = 0
            self._prev_cart_pos       = list(self._current_joints)
            # print("prev joint", self._prev_cart_pos)
            interval_ms =  int((time__ / time_steps) * 1000)
            self._joint_playback_timer.stop()
            self._cart_playback_timer.start(interval_ms)

            # store target as new current cart — in mm/deg (spinbox units)
            self._current_cart = list(target_cart)
            # print ("after motion", self._current_cart)
        except Exception as e:
            self._current_cart = F_K(np.deg2rad(self._prev_cart_pos))
            self._emit_cart()
            self.IKErrorOccurred.emit(str(e))
            print(f"Cartesian trajectory error: {e}")

    def _cart_playback_step(self):
        # guard at entry — prevents stale timer fire from accessing out-of-bounds index
        if self._cart_playback_pos is None or \
        self._cart_playback_index >= len(self._cart_playback_pos[0]):
            self._cart_playback_timer.stop()
            return

        idx = self._cart_playback_index
        joint_data = {}

        self._updating_from_playback = True

        for i in range(6):
            joint_id  = i + 1
            pos_val   = self._cart_playback_pos[i][idx]
            vel_val   = self._cart_playback_vel[i][idx]
            delta     = pos_val - self._prev_cart_pos[i]
            self._prev_cart_pos[i] = pos_val
            direction = 1 if delta > 0 else 0

            self._current_joints[i] = pos_val
            self._emit_joint(joint_id, pos_val)

            delta_int = int(delta * 10000.0)
            joint_data[joint_id] = [direction, abs(delta_int), abs(int(vel_val))]

        self._updating_from_playback = False
        self.can.send_all_joints(joint_data)
        
        self._cart_playback_index += 1
        if self._cart_playback_index >= len(self._cart_playback_pos[0]):
            # print("loop cart current ",self._current_joints )
            self._cart_playback_timer.stop()
            # sync cart from actual FK after playback — fixes the sync issue
            # self._sync_cart_from_joints()
            self._emit_cart()
    
    @Slot(list)
    def executeMultipoint(self, points):

        positions = np.asarray(points, dtype=float)
        positions[:, 0:3] /= 1000.0   # mm → m
        # print (" position",positions)
        current_cart = np.array(F_K(np.deg2rad(self._current_joints)), dtype=float) 

        positions = np.vstack((current_cart/1000, positions))
        try:
            theta, vel, steps = Bcart_calc(positions[:, 0:3])
            print ("vel",vel)
            # print("Bcart_calc returned:", theta, "points, vel shape:", vel, "steps:", steps)
            # theta: (n, 6) joint angles in degrees
            # vel:   (n, 6) joint velocities in deg/s
            # steps: total time or time array
            # print ("velocity", vel)
            self._bcart_playback_pos   = [theta[:, i] for i in range(6)]
            self._bcart_playback_vel   = [vel[:, i]   for i in range(6)]
            self._bcart_playback_index = 0
            self._prev_bcart_pos       = list(self._current_joints)
            
            steps = np.asarray(steps, dtype=float) * 1000.0
            self._bcart_steps = steps
            
            # compute interval
            self._bcart_playback_timer.setSingleShot(True)
            self._joint_playback_timer.stop()
            self._cart_playback_timer.stop()
            self._bcart_playback_timer.start(int(self._bcart_steps[0]))

            # stop other timers before starting
            self._joint_playback_timer.stop()
            self._cart_playback_timer.stop()
            

        except Exception as e:
            print(f"Bcart trajectory error: {e}")

    def _bcart_playback_step(self):
        if self._bcart_playback_pos is None or \
        self._bcart_playback_index >= len(self._bcart_playback_pos[0]):
            self._bcart_playback_timer.stop()
            return

        idx        = self._bcart_playback_index
        joint_data = {}

        self._updating_from_playback = True

        for i in range(6):
            joint_id  = i + 1
            pos_val   = self._bcart_playback_pos[i][idx]
            vel_val   = self._bcart_playback_vel[i][idx]
            delta     = pos_val - self._prev_bcart_pos[i]
            self._prev_bcart_pos[i] = pos_val
            direction = 1 if delta > 0 else 0

            self._current_joints[i] = pos_val
            self._emit_joint(joint_id, pos_val)

            delta_int = int(delta * 10000)
            joint_data[joint_id] = [direction, abs(delta_int), abs(int(vel_val))]

        self._updating_from_playback = False
        self.can.send_all_joints(joint_data)

        self._bcart_playback_index += 1

        if self._bcart_playback_index >= len(self._bcart_playback_pos[0]):
            # finished
            self._bcart_playback_timer.stop()
            self._sync_cart_from_joints()
        else:
            # schedule next step with its own interval
            next_interval = int(self._bcart_steps[self._bcart_playback_index]-self._bcart_steps[self._bcart_playback_index-1])
            print(f" interval: {next_interval} ms")
            self._bcart_playback_timer.start(next_interval)
    
    # ─────────────────────────────────────────────
    # SYNC HELPERS
    # ─────────────────────────────────────────────

    def _sync_cart_from_joints(self):
        """After joint move: compute FK and update cart state + spinboxes."""
        try:
            self._updating_from_fk = True
            self._current_joints = np.array(self._current_joints, dtype=float)
            self._current_joints[np.abs(self._current_joints) < 1e-6] = 0.0
            x,y,z,roll,pitch,yaw = F_K(np.deg2rad(self._current_joints))  # returns mm, degrees directly
            self._current_cart = [x,y,z,roll,pitch,yaw]
            # self._current_cart = np.array(self._current_cart, dtype=float)
            # self._current_cart[np.abs(self._current_cart) < 1e-3] = 0.0
            # print("update joint:", self._current_joints)
            # print("update pos:", self._current_cart)
            self._emit_cart()
        except Exception as e:
            print(f"FK sync error: {e}")
        finally:
            self._updating_from_fk = False

    def _emit_joint(self, joint_id, value):
        """Update QML property for one joint."""
        setattr(self, f"_joint{joint_id}Angle", value)
        getattr(self, f"joint{joint_id}AngleChanged").emit()

    def _emit_cart(self):
        """Push current_cart to QML properties."""
        self.cartXChanged.emit()
        self.cartYChanged.emit()
        self.cartZChanged.emit()
        self.cartRollChanged.emit()
        self.cartPitchChanged.emit()
        self.cartYawChanged.emit()

    def _get_angle(self, joint):
        return self._current_joints[joint - 1]

    def _on_can_status(self, status):
        self._can_status = status
        self.canStatusChanged.emit()
    
    
    # ─────────────────────────────────────────────
    # JOINT PROPERTIES
    # ─────────────────────────────────────────────

    def get_joint1Angle(self): return self._current_joints[0]
    def get_joint2Angle(self): return self._current_joints[1]
    def get_joint3Angle(self): return self._current_joints[2]
    def get_joint4Angle(self): return self._current_joints[3]
    def get_joint5Angle(self): return self._current_joints[4]
    def get_joint6Angle(self): return self._current_joints[5]
    def get_canStatus(self): return self._can_status

    _joint1Angle = 0.0
    _joint2Angle = 0.0
    _joint3Angle = 0.0
    _joint4Angle = 0.0
    _joint5Angle = 0.0
    _joint6Angle = 0.0

    joint1Angle = Property(float, get_joint1Angle, notify=joint1AngleChanged)
    joint2Angle = Property(float, get_joint2Angle, notify=joint2AngleChanged)
    joint3Angle = Property(float, get_joint3Angle, notify=joint3AngleChanged)
    joint4Angle = Property(float, get_joint4Angle, notify=joint4AngleChanged)
    joint5Angle = Property(float, get_joint5Angle, notify=joint5AngleChanged)
    joint6Angle = Property(float, get_joint6Angle, notify=joint6AngleChanged)
    canStatus = Property(str, get_canStatus, notify=canStatusChanged)

    # ─────────────────────────────────────────────
    # CARTESIAN PROPERTIES
    # ─────────────────────────────────────────────

    def get_cartX(self):     return self._current_cart[0]
    def get_cartY(self):     return self._current_cart[1]
    def get_cartZ(self):     return self._current_cart[2]
    def get_cartRoll(self):  return self._current_cart[3]
    def get_cartPitch(self): return self._current_cart[4]
    def get_cartYaw(self):   return self._current_cart[5]

    cartX     = Property(float, get_cartX,     notify=cartXChanged)
    cartY     = Property(float, get_cartY,     notify=cartYChanged)
    cartZ     = Property(float, get_cartZ,     notify=cartZChanged)
    cartRoll  = Property(float, get_cartRoll,  notify=cartRollChanged)
    cartPitch = Property(float, get_cartPitch, notify=cartPitchChanged)
    cartYaw   = Property(float, get_cartYaw,   notify=cartYawChanged)


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)
    setup_qt_environment(engine)
    if not engine.rootObjects():
        sys.exit(-1)
    ex = app.exec()
    del engine
    return ex


if __name__ == "__main__":
    sys.exit(main())