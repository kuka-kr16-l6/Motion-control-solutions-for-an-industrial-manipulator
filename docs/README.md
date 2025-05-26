## 📘 Project Documentation: Robotic Arm Embedded Firmware (ESP32 + Modbus RTU)

### 1. 📄 Introduction

This document serves as a comprehensive guide for understanding and maintaining the embedded firmware developed for a robotic arm using ESP32 microcontrollers with ESP-IDF and Modbus RTU protocol. It is intended for future developers who will work on or extend the current system.

### 2. 🧠 System Architecture

* **Block Diagram**: A high-level diagram showing ESP32s controlling individual joints, communicating with a central master (PC or Raspberry Pi) over RS-485.
* **Microcontroller Setup**: Each ESP32 acts as a Modbus RTU slave controlling one motor/joint.
* **Master-Slave Hierarchy**: The master sends commands over RS-485. Each slave listens to its ID and acts accordingly.

### 3. 🔧 Hardware Setup

* **Components**: ESP32 (3x), RS-485 transceivers (e.g., MAX485), motors (servo/stepper), motor drivers, power supply, Raspberry Pi (or PC) as master.
* **Connections**: ESP32 UART to MAX485, motor driver to GPIO, power lines as per motor specs.

### 4. 🧑‍💻 Software Setup

* **Development Tools**: ESP-IDF (vX.Y), VS Code with IDF extension, Ubuntu 22.04.
* **Flashing**: Use `idf.py build` and `idf.py -p /dev/ttyUSBx flash`.
* **Debugging**: UART logs via `idf.py monitor`.

### 5. 📂 Project Structure

```
firmware/
├── main/
│   ├── modbus_slave.c
│   ├── motor_control.c
│   └── main.c
├── CMakeLists.txt
├── sdkconfig
└── components/
```

* `main.c`: Initializes system, handles Modbus.
* `modbus_slave.c`: Implements Modbus RTU slave logic.
* `motor_control.c`: Receives parsed data and controls motors.

### 6. 📡 Modbus RTU Protocol Usage

* **Slave IDs**: One per joint (1, 2, 3...)
* **Registers**:

  * `0x00`: Target angle (degrees)
  * `0x01`: Direction (0: CW, 1: CCW)
  * `0x02`: Delay (ms)
* **Master Flow**: Writes values to these registers, slave reads and executes.

### 7. 🧠 Control Logic

* **Receive**: Slave receives holding register values.
* **Parse**: Values parsed and validated.
* **Execute**: Motor control logic drives motor to target with specified delay.

### 8. 🧪 Testing & Debugging

* **Tools**: Modbus master simulator (e.g., Modbus Poll or Python script)
* **Check UART logs**: Ensure correct packet parsing and motor movement.
* **Common Issues**:

  * Incorrect slave ID
  * Wiring errors
  * Modbus timeout

### 9. 📈 Future Work

* Add feedback sensors
* Implement watchdog timer
* Modularize configuration (e.g., JSON over serial)

### 10. 🧾 Appendix

* **Glossary**:

  * RTU: Remote Terminal Unit
  * CW: Clockwise
  * CCW: Counter-Clockwise
* **References**:

  * [ESP-IDF Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/)
  * [Modbus RTU Protocol](https://modbus.org/)

