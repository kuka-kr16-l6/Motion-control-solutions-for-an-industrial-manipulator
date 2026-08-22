import QtQuick
import QtQuick.Controls
import UntitledProject1

Window {
    width: mainScreen.width
    height: mainScreen.height
    visibility: "FullScreen"
    visible: true
    title: "UntitledProject1"

    Screen01 {
        id: mainScreen

        anchors.centerIn: parent
        // Real-looking CAN status LED — top left corner
        Item {
            id: canLed
            x: 700
            y: 35
            width: 15
            height: 15
            z: 100   // always on top

            // ── outer bezel ──────────────────────────────
            Rectangle {
                anchors.fill: parent
                radius: width / 2
                color: "#111111"
                border.color: "#333333"
                border.width: 2

                // ── LED body ─────────────────────────────
                Rectangle {
                    id: ledBody
                    anchors.centerIn: parent
                    width: parent.width - 4
                    height: parent.height - 4
                    radius: width / 2

                    color: {
                        if (backend.canStatus === "sending")  return "#00ff44"
                        if (backend.canStatus === "connected") return "#00cc33"
                        return "#660000"
                    }

                    // glow ring — simulates LED halo
                    Rectangle {
                        anchors.centerIn: parent
                        width: parent.width + 8
                        height: parent.height + 8
                        radius: width / 2
                        color: "transparent"
                        border.width: 3
                        border.color: {
                            if (backend.canStatus === "sending")   return "#00ff4480"
                            if (backend.canStatus === "connected") return "#00cc3340"
                            return "#66000040"
                        }
                        z: -1
                    }

                    // ── inner dark shadow at bottom ───────
                    Rectangle {
                        anchors.bottom: parent.bottom
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.bottomMargin: 1
                        width: parent.width - 4
                        height: (parent.height - 4) / 2
                        radius: width / 2
                        color: Qt.rgba(0, 0, 0, 0.25)
                    }

                    // ── specular highlight (top-left) ─────
                    Rectangle {
                        x: 4
                        y: 3
                        width: parent.width * 0.38
                        height: parent.height * 0.28
                        radius: width / 2
                        color: Qt.rgba(1, 1, 1, 0.55)
                    }

                    // ── smaller secondary highlight ───────
                    Rectangle {
                        x: 7
                        y: 6
                        width: parent.width * 0.18
                        height: parent.height * 0.14
                        radius: width / 2
                        color: Qt.rgba(1, 1, 1, 0.30)
                    }

                    // ── opacity animation for blink ───────
                    opacity: backend.canStatus === "sending" ? 1.0 : 0.85
                    Behavior on opacity {
                        NumberAnimation { duration: 80 }
                    }
                    Behavior on color {
                        ColorAnimation { duration: 80 }
                    }
                }
            }

            // ── tooltip label ─────────────────────────────
            Text {
                anchors.right: parent.left
                anchors.rightMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                text: {
                    if (backend.canStatus === "sending")   return "CONNECTED"
                    if (backend.canStatus === "connected") return "CONNECTED"
                    return "DISCONNECTED"
                }
                color: {
                    if (backend.canStatus === "sending")   return "#595959"
                    if (backend.canStatus === "connected") return '#595959'
                    return '#595959'
                }
                font.pixelSize: 12
                font.family: "Arial"
                font.bold: true
            }
        }
        Connections {
            target: mainScreen.jogjoint1
            function onValueChanged() {
                backend.jointChanged(1, mainScreen.jogjoint1.value)
            }}
        Connections {
            target: mainScreen.jogjoint2
            function onValueChanged() {
                backend.jointChanged(2, mainScreen.jogjoint2.value)
            }}
        Connections {
            target: mainScreen.jogjoint3
            function onValueChanged() {
                backend.jointChanged(3, mainScreen.jogjoint3.value)
            }}
        Connections {
            target: mainScreen.jogjoint4
            function onValueChanged() {
                backend.jointChanged(4, mainScreen.jogjoint4.value)
            }}
        Connections {
            target: mainScreen.jogjoint5
            function onValueChanged() {
                backend.jointChanged(5, mainScreen.jogjoint5.value)
            }}
        Connections {
            target: mainScreen.jogjoint6
            function onValueChanged() {
                backend.jointChanged(6, mainScreen.jogjoint6.value)
            }}
        Connections {
            target: mainScreen.jogcartx
            function onValueChanged() {
                backend.posChanged(1, mainScreen.jogcartx.value)
            }}
        Connections {
            target: mainScreen.jogcarty
            function onValueChanged() {
                backend.posChanged(2, mainScreen.jogcarty.value)
            }}
        Connections {
            target: mainScreen.jogcartz
            function onValueChanged() {
                backend.posChanged(3, mainScreen.jogcartz.value)
            }}
        Connections {
            target: mainScreen.jogcartroll
            function onValueChanged() {
                backend.posChanged(4, mainScreen.jogcartroll.value)
            }}
        Connections {
            target: mainScreen.jogcartpitch
            function onValueChanged() {
                backend.posChanged(5, mainScreen.jogcartpitch.value)
            }}
        Connections {
            target: mainScreen.jogcartyaw
            function onValueChanged() {
                backend.posChanged(6, mainScreen.jogcartyaw.value)
            }}
        Connections {
            target: mainScreen.executepoint

            function onClicked() {

                var points = [];

                for (var i = 0; i < mainScreen.pointModel.count; ++i){
                    
                    var p = mainScreen.pointModel.get(i);

                    points.push([
                        p.xaxis,
                        p.yaxis,
                        p.zaxis,
                        p.roll,
                        p.pitch,
                        p.yaw
                    ]);
                }
                backend.executeMultipoint(points);
            }}
        // add inside Screen01 block, after existing Connections

        Connections {
            target: backend
            function onIKErrorOccurred(message) {
                console.log("Received:", message)
                errorPopup.errorText = message
                errorPopup.open()
            }
        }

        // popup — add at the same level as Screen01, inside Window
        
        Binding {
            target: mainScreen.a1
            property: "eulerRotation.z"
            value: backend.joint1Angle
            }
        Binding {
            target: mainScreen.a2
            property: "eulerRotation.y"
            value: backend.joint2Angle
            }
        Binding {
            target: mainScreen.a3
            property: "eulerRotation.y"
            value: backend.joint3Angle
            }
        Binding {
            target: mainScreen.a4
            property: "eulerRotation.x"
            value: backend.joint4Angle
            }
        Binding {
            target: mainScreen.a5
            property: "eulerRotation.y"
            value: backend.joint5Angle
            }
        Binding {
            target: mainScreen.a6
            property: "eulerRotation.x"
            value: backend.joint6Angle
            }
        // Joint Bindings — update spinboxes when trajectory runs
        Binding {
            target: mainScreen.jogjoint1
            property: "value"
            value: backend.joint1Angle
            when: !mainScreen.jogjoint1.activeFocus
        }
        Binding {
            target: mainScreen.jogjoint2
            property: "value"
            value: backend.joint2Angle
            when: !mainScreen.jogjoint2.activeFocus
        }
        Binding {
            target: mainScreen.jogjoint3
            property: "value"
            value: backend.joint3Angle
            when: !mainScreen.jogjoint3.activeFocus
        }
        Binding {
            target: mainScreen.jogjoint4
            property: "value"
            value: backend.joint4Angle
            when: !mainScreen.jogjoint4.activeFocus
        }
        Binding {
            target: mainScreen.jogjoint5
            property: "value"
            value: backend.joint5Angle
            when: !mainScreen.jogjoint5.activeFocus
        }
        Binding {
            target: mainScreen.jogjoint6
            property: "value"
            value: backend.joint6Angle
            when: !mainScreen.jogjoint6.activeFocus
        }

        // Cartesian Bindings — update spinboxes when FK runs after joint move
        // or when Cartesian trajectory completes
        Binding {
            target: mainScreen.jogcartx
            property: "value"
            value: backend.cartX
            when: !mainScreen.jogcartx.activeFocus
        }
        Binding {
            target: mainScreen.jogcarty
            property: "value"
            value: backend.cartY
            when: !mainScreen.jogcarty.activeFocus
        }
        Binding {
            target: mainScreen.jogcartz
            property: "value"
            value: backend.cartZ
            when: !mainScreen.jogcartz.activeFocus
        }
        Binding {
            target: mainScreen.jogcartroll
            property: "value"
            value: backend.cartRoll
            when: !mainScreen.jogcartroll.activeFocus
        }
        Binding {
            target: mainScreen.jogcartpitch
            property: "value"
            value: backend.cartPitch
            when: !mainScreen.jogcartpitch.activeFocus
        }
        Binding {
            target: mainScreen.jogcartyaw
            property: "value"
            value: backend.cartYaw
            when: !mainScreen.jogcartyaw.activeFocus
        }
        Component.onCompleted: {
            console.log("a1 exists?", mainScreen.a1)
            console.log("jogjoint1 exists?", mainScreen.jogjoint1)}

    }
    
    Popup {
            id: errorPopup
            property string errorText: ""

            onOpened: console.log("Popup opened")
            onClosed: console.log("Popup closed")
            anchors.centerIn: parent
            width: 400
            height: 150
            modal: true
            closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

            background: Rectangle {
                color: "#272626"
                radius: 12
                border.color: "#f26506"
                border.width: 2
            }

            Column {
                anchors.centerIn: parent
                spacing: 16

                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "⚠ No IK Solution"
                    color: "#f26506"
                    font.pixelSize: 20
                    font.family: "Arial"
                    font.bold: true
                }

                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: errorPopup.errorText
                    color: "#ffffff"
                    font.pixelSize: 14
                    font.family: "Arial"
                    wrapMode: Text.WordWrap
                    width: 360
                    horizontalAlignment: Text.AlignHCenter
                }

                Rectangle {
                    anchors.horizontalCenter: parent.horizontalCenter
                    width: 100
                    height: 36
                    radius: 8
                    color: dismissArea.pressed ? "#c94e04" :
                        dismissArea.containsMouse ? "#ff7a1a" : "#f26506"

                    Text {
                        anchors.centerIn: parent
                        text: "OK"
                        color: "#272626"
                        font.pixelSize: 16
                        font.family: "Arial"
                    }

                    MouseArea {
                        id: dismissArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: errorPopup.close()
                    }
                }
            }
        }

}

