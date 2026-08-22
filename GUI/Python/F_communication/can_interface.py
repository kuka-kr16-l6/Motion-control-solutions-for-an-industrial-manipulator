# import subprocess
# from PySide6.QtCore import QObject, Signal, QTimer
# from PySide6.QtSerialBus import QCanBus, QCanBusDevice, QCanBusFrame

# class CanInterface(QObject):
#     frameReceived = Signal(int, bytes)
#     errorOccurred = Signal(str)
#     busConnected = Signal()

#     BITRATE = 500000

#     def __init__(self, interface_name="can0", plugin="socketcan", parent=None):
#         super().__init__(parent)
#         self.interface_name = interface_name
#         self.plugin = plugin
#         self.device = None
#         self._connected = False

#         self._retry_timer = QTimer()
#         self._retry_timer.setInterval(1000)
#         self._retry_timer.timeout.connect(self._try_connect)

#     @property
#     def is_connected(self):
#         return self._connected

#     def connect_bus(self):
#         self._try_connect()
#         return self._connected

#     def _bring_up_interface(self):
#         try:
#             # bring down first to reset any partial/error state
#             subprocess.run(
#                 ["ip", "link", "set", self.interface_name, "down"],
#                 capture_output=True
#             )
#             result = subprocess.run(
#                 ["ip", "link", "set", self.interface_name, "up",
#                  "type", "can",
#                  "bitrate", str(self.BITRATE),
#                  "restart-ms", "0"],    # bus-off → stop, no auto-recovery
#                 capture_output=True
#             )
#             if result.returncode == 0:
#                 print(f"{self.interface_name} up at {self.BITRATE} bit/s")
#                 return True
#             else:
#                 print(f"Failed to bring up {self.interface_name}: {result.stderr.decode()}")
#                 return False
#         except Exception as e:
#             print(f"Error bringing up interface: {e}")
#             return False

#     def _bring_down_interface(self):
#         try:
#             subprocess.run(
#                 ["ip", "link", "set", self.interface_name, "down"],
#                 capture_output=True
#             )
#             print(f"{self.interface_name} brought down")
#         except Exception as e:
#             print(f"Error bringing down interface: {e}")

#     def _try_connect(self):
#         # always bring interface up fresh before attempting connection
#         if not self._bring_up_interface():
#             self._retry_timer.start()
#             return

#         device, error = QCanBus.instance().createDevice(self.plugin, self.interface_name)
#         if device is None:
#             print(f"CAN not available, retrying... ({error})")
#             self._retry_timer.start()
#             return

#         self.device = device
#         self.device.framesReceived.connect(self._on_frames_received)
#         self.device.errorOccurred.connect(self._on_error)

#         if not self.device.connectDevice():
#             print("CAN connectDevice() failed, retrying...")
#             self.device = None
#             self._retry_timer.start()
#             return

#         self._retry_timer.stop()
#         self._connected = True
#         print("CAN connected")
#         self.busConnected.emit()

#     def send_all_joints(self, joint_data: dict):
#         if not self._connected or self.device is None:
#             return
#         for joint_id, values in joint_data.items():
#             dir, position, velocity = values
#             position2 = abs(position)
#             velocity2 = abs(velocity)

#             p1 = position2 & ((1<<8)-1)
#             position2 = position2 >> 8
#             p2 = position2 & ((1<<8)-1)
#             position2 = position2 >> 8
#             p3 = position2 & ((1<<8)-1)
#             position2 = position2 >> 8
#             p4 = position2
            
#             v1 = velocity2 & ((1<<8)-1)
#             velocity2 =  velocity2 >> 8
#             v2 = velocity2

#             payload = bytes([dir, p4, p3, p2, p1, v2, v1])
            
#             print(f"Frame sent: joint={joint_id} payload={payload}")
#             result = self.device.writeFrame(QCanBusFrame(joint_id, payload))
#             print(f"Frame sent: joint={joint_id} dir={dir} pos={position} vel={velocity} success={result}")

#     def _on_frames_received(self):
#         while self.device.framesAvailable():
#             frame = self.device.readFrame()
#             self.frameReceived.emit(frame.frameId(), bytes(frame.payload()))

#     def _on_error(self, error):
#         error_str = self.device.errorString()
#         state = self.device.state()
#         print(f"CAN error: {error_str}, state: {state}")

#         # check for bus-off or disconnected state
#         if state != QCanBusDevice.ConnectedState:
#             print("CAN bus-off detected — bringing interface down, will retry...")
#             self._connected = False
#             self.device.disconnectDevice()
#             self.device = None
#             self._bring_down_interface()   # clean shutdown at OS level
#             self._retry_timer.start()      # _try_connect will bring it back up

#         self.errorOccurred.emit(error_str)

#     def disconnect_bus(self):
#         if self.device:
#             self.device.disconnectDevice()
#         self._connected = False

import subprocess
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtSerialBus import QCanBus, QCanBusDevice, QCanBusFrame


class CanInterface(QObject):
    frameReceived  = Signal(int, bytes)
    errorOccurred  = Signal(str)
    busConnected   = Signal()
    statusChanged  = Signal(str)   # ADD — "disconnected" | "connected" | "sending"

    BITRATE = 500000

    def __init__(self, interface_name="can0", plugin="socketcan", parent=None):
        super().__init__(parent)
        self.interface_name = interface_name
        self.plugin         = plugin
        self.device         = None
        self._connected     = False

        self._retry_timer = QTimer()
        self._retry_timer.setInterval(1000)
        self._retry_timer.timeout.connect(self._try_connect)

        # ADD — resets LED from "sending" back to "connected" after short pulse
        self._send_reset_timer = QTimer()
        self._send_reset_timer.setSingleShot(True)
        self._send_reset_timer.setInterval(120)   # blink duration ms
        self._send_reset_timer.timeout.connect(
            lambda: self.statusChanged.emit("connected")
        )

    @property
    def is_connected(self):
        return self._connected

    def connect_bus(self):
        self._try_connect()
        return self._connected

    def _bring_up_interface(self):
        try:
            subprocess.run(
                ["ip", "link", "set", self.interface_name, "down"],
                capture_output=True
            )
            result = subprocess.run(
                ["ip", "link", "set", self.interface_name, "up",
                 "type", "can",
                 "bitrate", str(self.BITRATE),
                 "restart-ms", "0"],
                capture_output=True
            )
            if result.returncode == 0:
                print(f"{self.interface_name} up at {self.BITRATE} bit/s")
                return True
            else:
                print(f"Failed to bring up {self.interface_name}: {result.stderr.decode()}")
                return False
        except Exception as e:
            print(f"Error bringing up interface: {e}")
            return False

    def _bring_down_interface(self):
        try:
            subprocess.run(
                ["ip", "link", "set", self.interface_name, "down"],
                capture_output=True
            )
            print(f"{self.interface_name} brought down")
        except Exception as e:
            print(f"Error bringing down interface: {e}")

    def _try_connect(self):
        if not self._bring_up_interface():
            self._retry_timer.start()
            return

        device, error = QCanBus.instance().createDevice(self.plugin, self.interface_name)
        if device is None:
            print(f"CAN not available, retrying... ({error})")
            self._retry_timer.start()
            return

        self.device = device
        self.device.framesReceived.connect(self._on_frames_received)
        self.device.errorOccurred.connect(self._on_error)

        if not self.device.connectDevice():
            print("CAN connectDevice() failed, retrying...")
            self.device = None
            self._retry_timer.start()
            return

        self._retry_timer.stop()
        self._connected = True
        print("CAN connected")
        self.busConnected.emit()
        self.statusChanged.emit("connected")   # ADD

    def send_all_joints(self, joint_data: dict):
        if not self._connected or self.device is None:
            return

        # ADD — pulse LED to "sending", reset after 120ms
        self.statusChanged.emit("sending")
        self._send_reset_timer.start()

        for joint_id, values in joint_data.items():
            dir, position, velocity = values
            position2 = abs(position)
            velocity2 = abs(velocity)

            p1 = position2 & ((1 << 8) - 1); position2 >>= 8
            p2 = position2 & ((1 << 8) - 1); position2 >>= 8
            p3 = position2 & ((1 << 8) - 1); position2 >>= 8
            p4 = position2

            v1 = velocity2 & ((1 << 8) - 1); velocity2 >>= 8
            v2 = velocity2

            payload = bytes([dir, p4, p3, p2, p1, v2, v1])
            self.device.writeFrame(QCanBusFrame(joint_id, payload))

    def _on_frames_received(self):
        while self.device.framesAvailable():
            frame = self.device.readFrame()
            self.frameReceived.emit(frame.frameId(), bytes(frame.payload()))

    def _on_error(self, error):
        error_str = self.device.errorString()
        state     = self.device.state()
        print(f"CAN error: {error_str}, state: {state}")

        if state != QCanBusDevice.ConnectedState:
            print("CAN bus-off — bringing interface down, will retry...")
            self._connected = False
            self.device.disconnectDevice()
            self.device = None
            self._bring_down_interface()
            self._retry_timer.start()
            self.statusChanged.emit("disconnected")   # ADD

        self.errorOccurred.emit(error_str)

    def disconnect_bus(self):
        if self.device:
            self.device.disconnectDevice()
        self._connected = False
        self.statusChanged.emit("disconnected")   # ADD