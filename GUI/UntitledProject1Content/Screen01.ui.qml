

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import UntitledProject1
import QtQuick3D
import QtQuick3D.Helpers
import Generated.QtQuick3D.Base
import Generated.QtQuick3D.A1
import Generated.QtQuick3D.A2
import Generated.QtQuick3D.A4
import Generated.QtQuick3D.A5
import Generated.QtQuick3D.A6
import Generated.QtQuick3D.A3_1
import Generated.QtQuick3D.A3
import QtQuick.Timeline 1.0

Rectangle {
    id: rectangle1
    color: Constants.backgroundColor
    property alias spinBox2WheelEnabled: ycoor.wheelEnabled
    property alias spinBoxStepSize: xcoor.stepSize
    property alias a4Y: a4.y
    
    property alias jogjoint1: jogjoint1
    property alias jogjoint2: jogjoint2
    property alias jogjoint3: jogjoint3
    property alias jogjoint4: jogjoint4
    property alias jogjoint5: jogjoint5
    property alias jogjoint6: jogjoint6

    property alias jogcartx: jogcartx
    property alias jogcarty: jogcarty
    property alias jogcartz: jogcartz
    property alias jogcartroll: jogcartroll
    property alias jogcartpitch: jogcartpitch
    property alias jogcartyaw: jogcartyaw

    property alias a1: a1
    property alias a2: a2
    property alias a3: a3
    property alias a4: a4
    property alias a5: a5
    property alias a6: a6
    property alias mouseAreaHI: mouseAreaHI

    property alias executepoint: executepoint
    property alias pointModel: pointModel

    
    width: 1024
    height: 600
    Item {
        id: __materialLibrary__
        PrincipledMaterial {
            id: principledMaterial
            objectName: "New Material"
        }
    }
    
    View3D {
        id: view3D
        x: 305
        y: 0
        width: 719
        height: 600
        camera: sceneCamera
        environment: sceneEnvironment1
        SceneEnvironment {
            id: sceneEnvironment1
            clearColor: "#ccbdbd"
            tonemapMode: SceneEnvironment.TonemapModeLinear
            backgroundMode: SceneEnvironment.Transparent
            antialiasingQuality: SceneEnvironment.High
            antialiasingMode: SceneEnvironment.NoAA
        }
        Node {
            id: scene1
            DirectionalLight {
                id: directionalLight
                x: 150
                y: 50
                z: 0
                eulerRotation.y: 90
            }
            PerspectiveCamera {
                id: sceneCamera
                x: 150
                y: 100
                eulerRotation.x: -20
                eulerRotation.y: 0
                z: 200
            }
            DirectionalLight {
                id: directionalLight1
                x: 0
                y: 50
                z: 150
            }
        }
        Base {
            id: base
            x: 0
            y: 0
            eulerRotation.y: slider.value
            z: 0
            eulerRotation.x: 270
            A1 {
                id: a1
                eulerRotation.z: 0
                z: 0.4
                A2 {
                    id: a2
                    x: 0.27
                    y: -0.08
                    z: 0.28
                    A3 {
                        id: a3
                        x: 0
                        y: -0.034
                        eulerRotation.y: 0
                        eulerRotation.z: 180
                        scale.z: 1
                        scale.y: 1
                        scale.x: 1
                        eulerRotation.x: 0
                        z: 0.68
                        A4 {
                            id: a4
                            x: -0.702
                            y: -0.117
                            eulerRotation.z: -180
                            eulerRotation.y: -0
                            scale.z: 1
                            scale.y: 1
                            scale.x: 1
                            eulerRotation.x: 0
                            z: -0.035
                            A5 {
                                id: a5
                                x: 0.268
                                y: 0.053
                                eulerRotation.y: 0
                                z: 0
                                A6 {
                                    id: a6
                                    x: 0.108
                                    y: -0.055
                                    z: 0
                                }
                            }
                        }
                    }
                }
            }
        Repeater3D {
            model: pointModel
            visible: rectangle1.state === "State2"
            delegate: Model {
                source: "#Sphere"

                scale: Qt.vector3d(0.0005,0.0005,0.0005)

                x: xaxis / 1000
                y: yaxis / 1000
                z: zaxis / 1000

                materials: DefaultMaterial {
                    diffuseColor: index === listView.currentIndex ? "red" : "blue"
                    }
            }
        }
        }

        
        SpotLight {
            id: spotlight
            x: -20
            y: 250
            eulerRotation.x: -90
            eulerRotation.y: 0
            eulerRotation.z: 0
            brightness: 1
            z: 0
        }
        Slider {
            id: slider
            opacity: 0
            visible: true
            value: 0
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 147
            anchors.rightMargin: 147
            anchors.topMargin: 176
            anchors.bottomMargin: 148
            stepSize: 1
            to: -180
            from: 180
        }
        
    }
    
    Image {
        id: home_icon
        x: 847
        y: 0
        width: 177
        height: 75
        source: "images/Home_icon.png"
        fillMode: Image.PreserveAspectFit
        
        MouseArea {
            id: mouseAreaHI
            anchors.fill: parent
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            anchors.topMargin: 0
            anchors.bottomMargin: 0
            hoverEnabled: true
            

            Connections {
                target: mouseAreaHI
                function onClicked() { jogjoint1.value = 0 }
            }            
            Connections {
                target: mouseAreaHI
                function onClicked() { jogjoint2.value = 0 }
            }
            Connections {
                target: mouseAreaHI
                function onClicked() { jogjoint3.value = 0 }
            }
            Connections {
                target: mouseAreaHI
                function onClicked() { jogjoint4.value = 0 }
            }
                Connections {
                target: mouseAreaHI
                function onClicked() { jogjoint5.value = 90 }
            }    
                Connections {
                target: mouseAreaHI
                function onClicked() { jogjoint6.value = 0 }
            }          
        }
    }
    
    Rectangle {
        id: rectangle
        x: 0
        y: 0
        width: 305
        height: 600
        opacity: 0
        visible: true
        color: "#272626"
        
        Text {
            id: text1
            y: 58
            width: 242
            height: 64
            visible: true
            color: "#fc7920"
            text: qsTr("Main Menu ")
            elide: Text.ElideNone
            font.pixelSize: 45
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            wrapMode: Text.NoWrap
            anchors.horizontalCenterOffset: -1
            anchors.horizontalCenter: parent.horizontalCenter
            styleColor: "#614b4b"
            topPadding: 0
            layer.smooth: false
            layer.mipmap: false
            layer.textureMirroring: ShaderEffectSource.NoMirroring
            focus: false
            renderType: Text.QtRendering
            font.family: "Arial"
        }
        
        Rectangle {
            id: buttonJspace
            visible: true
            color: mouseAreaJS.pressed ? "#c94e04" : mouseAreaJS.containsMouse ? "#ff7a1a" : "#f26506"
            radius: 30
            border.color: "#201f1f"
            border.width: 0
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 18
            anchors.rightMargin: 18
            anchors.topMargin: 146
            anchors.bottomMargin: 380
            antialiasing: false
            
            Text {
                id: text2
                x: 13
                y: 5
                width: 242
                height: 64
                color: "#272626"
                text: qsTr("JOG")
                elide: Text.ElideNone
                font.pixelSize: 35
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.NoWrap
                topPadding: 0
                styleColor: "#ffffff"
                renderType: Text.QtRendering
                layer.textureMirroring: ShaderEffectSource.NoMirroring
                layer.smooth: false
                layer.mipmap: false
                font.family: "Arial"
                focus: false
                anchors.horizontalCenterOffset: 0
                anchors.horizontalCenter: parent.horizontalCenter
            }
            
            MouseArea {
                id: mouseAreaJS
                visible: true
                anchors.fill: parent
                anchors.leftMargin: 1
                anchors.rightMargin: -1
                anchors.topMargin: 0
                anchors.bottomMargin: 0
                hoverEnabled: true
                
                Connections {
                    target: mouseAreaJS
                    function onClicked() { rectangle1.state = "State1" }
                }
            }
        }
        
        Rectangle {
            id: buttoncartesianspace
            visible: true
            color: mouseAreaCS.pressed ? "#c94e04" : mouseAreaCS.containsMouse ? "#ff7a1a" : "#f26506"
            radius: 30
            border.color: "#201f1f"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 18
            anchors.rightMargin: 18
            anchors.topMargin: 240
            anchors.bottomMargin: 286
            
            Text {
                id: text3
                x: 13
                y: 5
                width: 242
                height: 64
                color: "#272626"
                text: qsTr("Cartesian space")
                elide: Text.ElideNone
                font.pixelSize: 35
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.NoWrap
                topPadding: 0
                styleColor: "#ffffff"
                renderType: Text.QtRendering
                layer.textureMirroring: ShaderEffectSource.NoMirroring
                layer.smooth: false
                layer.mipmap: false
                font.family: "Arial"
                focus: false
                anchors.horizontalCenterOffset: 0
                anchors.horizontalCenter: parent.horizontalCenter
            }
            
            MouseArea {
                id: mouseAreaCS
                anchors.fill: parent
                hoverEnabled: true
                
                Connections {
                    target: mouseAreaCS
                    function onClicked() { rectangle1.state = "State2" }
                }
            }
        }
        
        Rectangle {
            id: buttonconnect2pc
            visible: true
            color: mouseAreaC2PC.pressed ? "#c94e04" : mouseAreaC2PC.containsMouse ? "#ff7a1a" : "#f26506"
            radius: 30
            border.color: "#201f1f"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 18
            anchors.rightMargin: 18
            anchors.topMargin: 334
            anchors.bottomMargin: 192
            
            Text {
                id: text4
                x: 13
                y: 5
                width: 242
                height: 64
                color: "#272626"
                text: qsTr("Connect2PC")
                elide: Text.ElideNone
                font.pixelSize: 35
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.NoWrap
                topPadding: 0
                styleColor: "#ffffff"
                renderType: Text.QtRendering
                layer.textureMirroring: ShaderEffectSource.NoMirroring
                layer.smooth: false
                layer.mipmap: false
                font.family: "Arial"
                focus: false
                anchors.horizontalCenterOffset: 0
                anchors.horizontalCenter: parent.horizontalCenter
            }
            
            MouseArea {
                id: mouseAreaC2PC
                visible: true
                anchors.fill: parent
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                anchors.topMargin: -1
                anchors.bottomMargin: 1
                hoverEnabled: true
                
                Connections {
                    target: mouseAreaC2PC
                    function onClicked() { rectangle1.state = "State3" }
                }
            }
        }
        
        Rectangle {
            id: buttontrobleshooting
            visible: true
            color: mouseAreaTS.pressed ? "#c94e04" : mouseAreaTS.containsMouse ? "#ff7a1a" : "#f26506"
            radius: 30
            border.color: "#201f1f"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 18
            anchors.rightMargin: 18
            anchors.topMargin: 422
            anchors.bottomMargin: 104
            
            Text {
                id: text5
                x: 14
                y: 5
                width: 242
                height: 64
                color: "#272626"
                text: qsTr("Trobleshooting")
                elide: Text.ElideNone
                font.pixelSize: 35
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.NoWrap
                topPadding: 0
                styleColor: "#ffffff"
                renderType: Text.QtRendering
                layer.textureMirroring: ShaderEffectSource.NoMirroring
                layer.smooth: false
                layer.mipmap: false
                font.family: "Arial"
                focus: false
                anchors.horizontalCenterOffset: 1
                anchors.horizontalCenter: parent.horizontalCenter
            }
            
            MouseArea {
                id: mouseAreaTS
                anchors.fill: parent
                anchors.leftMargin: -1
                anchors.rightMargin: 1
                anchors.topMargin: -1
                anchors.bottomMargin: 1
                clip: false
                cursorShape: Qt.ArrowCursor
                acceptedButtons: Qt.LeftButton
                hoverEnabled: true
                
                Connections {
                    target: mouseAreaTS
                    function onClicked() {
                        console.log("clicked")
                    }
                }
            }
        }
        
        Connections {
            target: rectangle
            function onActiveFocusChanged() { timeline.startFrame() }
        }
    }
    
    SwipeView {
        id: swipeView
        width: 200
        height: 200
        opacity: 0
        visible: false
        
        Item {
            Image {
                id: images
                source: "images/images.jpg"
                fillMode: Image.PreserveAspectFit
            }
        }
        
        Item {
            Image {
                id: images1
                x: -468
                y: 0
                source: "images/images1.jpg"
                fillMode: Image.PreserveAspectFit
            }
        }
        
        Item {
            Image {
                id: images3
                x: -841
                y: 70
                source: "images/images3.jpg"
                fillMode: Image.PreserveAspectFit
            }
        }
    }

    Timeline {
        id: timeline
        animations: [
            TimelineAnimation {
                id: timelineAnimation
                duration: 3000
                running: true
                loops: 1
                to: 3000
                from: 0
            }
        ]
        startFrame: 0
        endFrame: 3000
        enabled: true

        KeyframeGroup {
            target: sceneCamera
            property: "x"
            Keyframe {
                value: 150
                frame: 3000
            }
        }

        KeyframeGroup {
            target: sceneCamera
            property: "z"
            Keyframe {
                value: 0
                frame: 3000
            }
        }

        KeyframeGroup {
            target: sceneCamera
            property: "eulerRotation.y"
            Keyframe {
                value: 90
                frame: 3000
            }
        }

        KeyframeGroup {
            target: view3D
            property: "x"
            Keyframe {
                value: 375
                frame: 3000
            }
        }

        KeyframeGroup {
            target: view3D
            property: "y"
            Keyframe {
                value: 0
                frame: 3000
            }
        }

        KeyframeGroup {
            target: rectangle
            property: "opacity"
            Keyframe {
                value: 1
                frame: 3005
            }
        }

        KeyframeGroup {
            target: sceneCamera
            property: "eulerRotation"
        }
    }

    Switch {
        id: switchConnect
        opacity: 1
        visible: false
        text: qsTr("CONNECT")
    }
    
    Image {
        id: backicon
        x: 0
        y: -1
        width: 155
        height: 76
        visible: false
        source: "images/backicon-removebg-preview.png"
        fillMode: Image.PreserveAspectFit
        
        MouseArea {
            id: mouseAreaBI
            anchors.fill: parent
            
            Connections {
                target: mouseAreaBI
                function onClicked() { rectangle1.state = "" }
            }
        }
    }
    
    BusyIndicator {
        id: busyIndicator
        x: 102
        y: 235
        opacity: 0
        visible: false
    }
    
    ToolBar {
        id: toolBar
        x: 82
        y: 301
        width: 360
        opacity: 0
        visible: false
        Column{
            anchors.fill: parent
            
            ToolButton {
                id: addpoint
                text: qsTr("Add ")
                
                Connections {
                    target: addpoint
                    function onClicked()  {
                        pointModel.append({
                                            xaxis: xcoor.value,
                                            yaxis: ycoor.value,
                                            zaxis: zcoor.value,
                                            roll: rollcoor.value,
                                            pitch: pitchcoor.value,
                                            yaw: yawcoor.value
                                        })
                    }
                }
                
            }
            
            ToolButton {
                id: removepoint
                x: 0
                y: 0
                width: 92
                height: 40
                text: qsTr("Remove")
                
                Connections {
                    target: removepoint
                    function onClicked() { if (listView.currentIndex >= 0) {
                            pointModel.remove(listView.currentIndex)
                            listView.currentIndex = -1
                        }}
                }
            }
            
            ToolButton {
                id: executepoint
                x: 0
                y: 0
                width: 92
                height: 40
                text: qsTr("Execute")
            }
        }
     }
    
    Rectangle {
        id: switchbutt
        x: 115
        y: 95
        width: 200
        height: 200
        visible: false
        color: "#ffffff"
    }
    
    Rectangle {
        id: rectangle2
        x: 84
        y: 200
        width: 200
        height: 200
        visible: false
        color: "#ffffff"
        
        SpinBox {
            id: jogjoint1
            from : -120
            value : 0
            to : 120
            x: 88
            y: 16
            enabled: false
            
            Text {
                id: textjogjoint1
                text: qsTr("Joint 1")
                font.pixelSize: 18
            }
        }
        
        SpinBox {
            id: jogjoint3
            from : -210
            value : 0
            to : 60
            x: 88
            y: 108
            enabled: false
            
            Text {
                id: textjogjoint3
                text: qsTr("Joint 3")
                font.pixelSize: 18
            }
        }
        
        SpinBox {
            id: jogjoint4
            from : -180
            value : 0
            to : 180
            x: 88
            y: 155
            enabled: false
            
            Text {
                id: textjogjoint4
                text: qsTr("Joint 4")
                font.pixelSize: 18
            }
        }
        
        SpinBox {
            id: jogjoint5
            from : -120
            value : 0
            to : 120
            x: 88
            y: 201
            enabled: false
            
            Text {
                id: textjogjoint5
                text: qsTr("Joint 5")
                font.pixelSize: 18
            }
        }
        
        SpinBox {
            id: jogjoint6
            from :-180
            value : 0
            to : 180
            x: 88
            y: 247
            enabled: false
            
            Text {
                id: textjogjoint6
                text: qsTr("Joint 6 ")
                font.pixelSize: 18
            }
        }

        SpinBox {
            id: jogjoint2
            from :-65
            value : 0
            to : 120
            x: 94
            y: 72
            enabled: false

            Text {
                id: textjoint2
                text: qsTr("Joint 2 ")
                font.pixelSize: 18
            }
        }
    }
    
    SwitchDelegate {
        
        id: jointorcartesianswitch
        x: 374
        y: 105
        visible: false
        text: qsTr("JOINT")
        checked: false
        checkable: false
        enabled: false
        
        
    }

    Timeline {
        id: timeline1
        animations: [
            TimelineAnimation {
                id: timelineAnimation1
                running: false
                loops: 1
                to: 3000
                from: 0
            }
        ]
        startFrame: 0
        endFrame: 3000
        enabled: false
    }

    SpinBox {
        id: xcoor
        value : 1230
        x: 115
        y: 374
        visible: false
        enabled: false
        
        Text {
            id: text6
            text: qsTr("X(mm)")
            font.pixelSize: 20
        }
        to: 1911
        from: 705
    }
    
    SpinBox {
        id: rollcoor
        value : 0
        x: 115
        y: 445
        visible: false
        enabled: false
        
        Text {
            id: text7
            text: qsTr("ROLL(degree)")
            font.pixelSize: 20
        }
        to: 345
        from: -345
    }
    
    SpinBox {
        id: ycoor
        value : 0
        x: 290
        y: 374
        visible: false
        enabled: false
        
        Text {
            id: text8
            text: qsTr("Y(mm)")
            font.pixelSize: 20
        }
        to: 1911
        from: -1911
    }
    
    SpinBox {
        id: pitchcoor
        value : 0
        x: 290
        y: 445
        visible: false
        enabled: false
        
        Text {
            id: text9
            text: qsTr("PITCH(degree)")
            font.pixelSize: 20
        }
        to: 125
        from: -125
    }
    
    SpinBox {
        id: zcoor
        value : 1430
        x: 473
        y: 374
        visible: false
        enabled: false
        
        Text {
            id: text10
            text: qsTr("Z(mm)")
            font.pixelSize: 20
        }
        to: 2300
        from: -500
    }
    
    SpinBox {
        id: yawcoor
        value : 0
        x: 473
        y: 445
        visible: false
        enabled: false
        
        Text {
            id: text11
            text: qsTr("YAW(degree)")
            font.pixelSize: 20
        }
        to: 345
        from: -345
    }
    Row { id: row; visible: false; enabled: false; spacing: 10
        Text { width: 30
            text: "#" }
        Text { width: 30
            text: "X" }
        Text { width: 30
            text: "Y" }
        Text { width: 30
            text: "Z" }
        Text { width: 50
            text: "Roll" }
        Text { width: 50
            text: "Pitch" }
        Text { width: 50
            text: "Yaw" } }
    ListView {
        id: listView
        x: 112
        y: 105
        width: 500
        height: 200
        clip: true
        visible: false
        enabled: false
        boundsBehavior: Flickable.DragAndOvershootBounds
        interactive: false
        currentIndex: -1
        highlight: Rectangle {
            color: "#444444"
            radius: 4
            opacity: 0.6
        }
        highlightFollowsCurrentItem: true
        model: ListModel { id: pointModel }
        
        delegate: Rectangle {
            color: "transparent"
            width: ListView.view.width
            height: 30
            
            MouseArea {
                anchors.fill: parent
                onClicked: listView.currentIndex = index
            }
            
            Row {
                anchors.fill: parent
                spacing: 10
                anchors.leftMargin: 5
                anchors.verticalCenter: parent.verticalCenter
                
                Text { width: 20; text: index + 1 }
                Text { width: 35; text: xaxis }
                Text { width: 35; text: yaxis }
                Text { width: 35; text: zaxis }
                Text { width: 50; text: roll }
                Text { width: 50; text: pitch }
                Text { width: 50; text: yaw }
            }}
        
    }
    
    ComboBox {
        id: comboBox
        x: 40
        y: 301
        model: ListModel {
            ListElement { value: 1 }
            ListElement { value: 10 }
            ListElement { value: 100 }
        }
        textRole: "value"
        visible: false
        enabled: false
        
        Text {
            id: text12
            text: qsTr("Step Size")
            font.pixelSize: 18
        }
    }
    
    Text {
        id: notice
        x: 84
        y: 554
        visible: false
        text: qsTr("NOTE : r = sqrt(x**2 + y**2) >= 705mm ")
        font.pixelSize: 16
    }

    Rectangle {
        id: rectangle3
        x: 84
        y: 200
        width: 200
        height: 200
        visible: false
        color: "#ffffff"
        enabled: false
        SpinBox {
            id: jogcartx
            
            x: 88
            y: 16
            stepSize:10
            enabled: false
            Text {
                id: textjogjoint2
                text: qsTr("Joint 1")
                font.pixelSize: 18
            }
            to:1911
            from:705
        }

        SpinBox {
            id: jogcartz
            
            x: 88
            y: 108
            stepSize:10
            enabled: false
            Text {
                id: textjogjoint7
                text: qsTr("Joint 3")
                font.pixelSize: 18
            }
            to:2300
            from:-500
        }

        SpinBox {
            id: jogcartroll
            
            x: 88
            y: 155
            stepSize:10
            enabled: false
            Text {
                id: textjogjoint8
                text: qsTr("Joint 4")
                font.pixelSize: 18
            }
            to:345
            from:-345
        }

        SpinBox {
            id: jogcartpitch
            
            x: 88
            y: 201
            stepSize:10
            enabled: false
            Text {
                id: textjogjoint9
                text: qsTr("Joint 5")
                font.pixelSize: 18
            }
            to:125
            from:-125
        }

        SpinBox {
            id: jogcartyaw
            
            x: 88
            y: 247
            stepSize:10
            enabled: false
            Text {
                id: textjogjoint10
                text: qsTr("Joint 6 ")
                font.pixelSize: 18
            }
            to:345
            from:-345
        }

        SpinBox {
            id: jogcarty
            
            x: 94
            y: 72
            stepSize:10
            enabled: false
            Text {
                id: textjoint3
                text: qsTr("Joint 2 ")
                font.pixelSize: 18
            }
            to:1911
            from:-1911
        }
    }
    
    
    
    
    
    
    
    
    states: [
        
        State {
            name: "State1"
            
            PropertyChanges {
                target: view3D
                x: 305
                y: 0
            }
            
            PropertyChanges {
                target: rectangle
                x: -21
                y: -83
                visible: false
            }
            
            PropertyChanges {
                target: backicon
                x: 14
                y: 8
                width: 73
                height: 67
                visible: true
            }
            
            PropertyChanges {
                target: rectangle1
                visible: true
            }
            
            PropertyChanges {
                target: switchbutt
                x: 71
                y: 108
                width: 256
                height: 49
                visible: true
                radius: 10
            }
            
            PropertyChanges {
                target: rectangle2
                x: 71
                y: 173
                width: 256
                height: 312
                visible: !jointorcartesianswitch.checked
                radius: 10
                enabled: !jointorcartesianswitch.checked
            }
            
            PropertyChanges {
                target: jointorcartesianswitch
                x: 104
                y: 108
                width: 190
                height: 52
                visible: true
                text: jointorcartesianswitch.checked ? "CARTESIAN" : "JOINT"
                checked: false
                icon.color: "#d82222"
                enabled: true
                checkable: true
            }
            
            
            
            PropertyChanges {
                target: sceneCamera
                x: 200
                z: 0
            }
            
            PropertyChanges {
                target: jogjoint5
                x: 96
                y: 207
                enabled: true
            }
            
            PropertyChanges {
                target: jogjoint1
                x: 96
                y: 22
                enabled: true
            }
            
            PropertyChanges {
                target: jogjoint3
                x: 96
                y: 114
                enabled: true
            }
            
            PropertyChanges {
                target: jogjoint4
                x: 96
                y: 161
                enabled: true
            }
            
            PropertyChanges {
                target: jogjoint6
                x: 96
                y: 253
                enabled: true
            }
            
            PropertyChanges {
                target: textjogjoint1
                x: -77
                y: 9
                text: qsTr("Joint 1")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: textjogjoint3
                x: -76
                y: 9
                text: qsTr("Joint 3")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: textjogjoint4
                x: -77
                y: 9
                text: qsTr("Joint 4")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: textjogjoint5
                x: -76
                y: 9
                text: qsTr("Joint 5")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: textjogjoint6
                x: -76
                y: 9
                text: qsTr("Joint 6")
                font.pixelSize: 18
            }

            PropertyChanges {
                target: jogjoint2
                x: 96
                y: 68
                enabled: true
            }

            PropertyChanges {
                target: textjoint2
                x: -77
                y: 9
                text: qsTr("Joint 2")
                font.pixelSize: 18
            }

            PropertyChanges {
                target: rectangle3
                x: 71
                y: 173
                width: 256
                height: 312
                visible: jointorcartesianswitch.checked
                radius: 10
                enabled: jointorcartesianswitch.checked
            }

            PropertyChanges {
                target: jogcartx
                x: 96
                y: 22
                enabled: jointorcartesianswitch.checked
            }

            PropertyChanges {
                target: jogcartyaw
                x: 96
                y: 253
                enabled: jointorcartesianswitch.checked
            }

            PropertyChanges {
                target: jogcarty
                x: 96
                y: 68
                enabled: jointorcartesianswitch.checked
            }

            PropertyChanges {
                target: jogcartpitch
                x: 96
                y: 207
                enabled: jointorcartesianswitch.checked
            }

            PropertyChanges {
                target: jogcartroll
                x: 96
                y: 161
                enabled: jointorcartesianswitch.checked
            }

            PropertyChanges {
                target: jogcartz
                x: 96
                y: 114
                enabled: jointorcartesianswitch.checked
            }

            PropertyChanges {
                target: textjogjoint2
                x: -55
                y: 9
                text: qsTr("X")
            }

            PropertyChanges {
                target: textjogjoint7
                x: -55
                y: 9
                text: qsTr("Z")
            }

            PropertyChanges {
                target: textjoint3
                x: -55
                y: 9
                text: qsTr("Y")
            }

            PropertyChanges {
                target: textjogjoint8
                x: -63
                y: 9
                text: qsTr("Roll")
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            PropertyChanges {
                target: textjogjoint10
                x: -61
                y: 9
                text: qsTr("Yaw")
                horizontalAlignment: Text.AlignHCenter
            }

            PropertyChanges {
                target: textjogjoint9
                x: -66
                y: 9
                text: qsTr("Pitch")
                horizontalAlignment: Text.AlignHCenter
            }
        },        State {
            name: "State2"
            PropertyChanges {
                target: view3D
                x: 311
                y: 0
            }
            
            PropertyChanges {
                target: rectangle
                visible: false
            }
            
            PropertyChanges {
                target: backicon
                x: 14
                y: 8
                width: 73
                height: 67
                visible: true
            }
            
            PropertyChanges {
                target: buttoncartesianspace
                color: mouseAreaCS.pressed ? "#c94e04" : mouseAreaCS.containsMouse ? "#ff7a1a" : "#f26506"
            }
            
            PropertyChanges {
                target: toolBar
                x: 14
                y: 110
                width: 92
                height: 119
                opacity: 1
                visible: true
            }
            
           
            
            PropertyChanges {
                target: switchbutt
                visible: false
            }
            
            PropertyChanges {
                target: sceneCamera
                x: 200
                z: 0
            }
            
            PropertyChanges {
                target: listView
                x: 112
                y: 126
                width: 344
                height: 183
                visible: true
                boundsBehavior: Flickable.StopAtBounds
                enabled: true
                boundsMovement: Flickable.StopAtBounds
                interactive: true
                flickableDirection: Flickable.VerticalFlick
            }
            
            PropertyChanges {
                target: xcoor
                x: 22
                y: 406
                visible: true
                value: 1000
                stepSize: comboBox.currentValue
                spacing: 0
                wheelEnabled: false
                focusPolicy: Qt.NoFocus
                to: 1911
                from: 705
                enabled: true
            }
            
            PropertyChanges {
                target: rollcoor
                x: 22
                y: 468
                visible: true
                value: 0
                stepSize: comboBox.currentValue
                enabled: true
                to: 180
                from: -180
            }
            
            PropertyChanges {
                target: ycoor
                x: 175
                y: 406
                visible: true
                value: 1000
                stepSize: comboBox.currentValue
                to: 1911
                from: -1911
                wheelEnabled: false
                enabled: true
                layer.enabled: false
            }
            
            PropertyChanges {
                target: pitchcoor
                x: 175
                y: 468
                visible: true
                value: 0
                stepSize: comboBox.currentValue
                enabled: true
                to: 125
                from: -125
            }
            
            PropertyChanges {
                target: zcoor
                x: 327
                y: 406
                visible: true
                value: 0
                stepSize: comboBox.currentValue
                enabled: true
                to: 2300
                from: -500
            }
            
            PropertyChanges {
                target: yawcoor
                x: 327
                y: 468
                visible: true
                value: 0
                stepSize: comboBox.currentValue
                enabled: true
                to: 180
                from: -180
            }
            
            PropertyChanges {
                target: text6
                x: 0
                y: -21
                text: qsTr("X(mm)")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: text7
                x: 0
                y: -22
                text: qsTr("ROLL(degree)")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: text9
                x: 0
                y: -22
                text: qsTr("PITCH(degree)")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: text8
                x: 0
                y: -22
                text: qsTr("Y(mm)")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: text10
                x: 0
                y: -22
                text: qsTr("Z(mm)")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: text11
                x: 0
                y: -22
                text: qsTr("YAW(degree)")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: addpoint
                x: 0
                y: 0
                width: 92
                height: 40
                text: qsTr("Add ")
            }
            
            PropertyChanges {
                target: row
                x: 112
                y: 91
                visible: true
                enabled: true
            }
            
            PropertyChanges {
                target: comboBox
                x: 22
                y: 315
                width: 100
                height: 40
                visible: true
                wheelEnabled: false
                currentIndex: comboBox.currentIndex
                displayText: comboBox.currentValue
                enabled: true
                textRole: ""
            }
            
            PropertyChanges {
                target: text12
                x: 0
                y: -23
                text: qsTr("Step Size")
                font.pixelSize: 18
            }
            
            PropertyChanges {
                target: notice
                x: 22
                y: 536
                width: 334
                height: 33
                visible: true
                text: qsTr("NOTE : r = sqrt(x**2 + y**2) >= 705mm ")
                font.pixelSize: 16
            }
        },
        
        State {
            name: "State3"
            PropertyChanges {
                target: view3D
                x: 305
                y: 0
                opacity: 0
                visible: false
            }
            
            PropertyChanges {
                target: rectangle
                opacity: 0
                visible: true
            }
            
            PropertyChanges {
                target: backicon
                x: 14
                y: 8
                width: 73
                height: 67
                visible: true
            }
            
            PropertyChanges {
                target: buttoncartesianspace
                color: mouseAreaCS.pressed ? "#c94e04" : mouseAreaCS.containsMouse ? "#ff7a1a" : "#f26506"
            }
            
            PropertyChanges {
                target: swipeView
                x: 232
                y: 102
                width: 784
                height: 450
                opacity: 1
                visible: true
            }
            
            PropertyChanges {
                target: images3
                x: 214
                y: 72
                fillMode: Image.Stretch
            }
            
            PropertyChanges {
                target: images1
                x: 286
                y: 73
                horizontalAlignment: Image.AlignHCenter
                verticalAlignment: Image.AlignVCenter
                fillMode: Image.Stretch
            }
            
            PropertyChanges {
                target: images
                x: 189
                y: 29
                width: 398
                height: 363
            }
            
            PropertyChanges {
                target: home_icon
                opacity: 0
                visible: false
            }
            
            PropertyChanges {
                target: busyIndicator
                x: 123
                y: 281
                opacity: 1
                visible: switchConnect.checked
                running: switchConnect.checked
            }
            
            PropertyChanges {
                target: switchConnect
                x: 77
                y: 192
                width: 151
                height: 77
                opacity: 1
                visible: true
                text: qsTr("CONNECT")
            }
            
            PropertyChanges {
                target: switchbutt
                visible: false
            }
        }
    ]
}

/*##^##
Designer {
    D{i:0}D{i:3;cameraSpeed3d:4;cameraSpeed3dMultiplier:1}D{i:5;cameraSpeed3d:4;cameraSpeed3dMultiplier:1}
D{i:7}D{i:27}
}
##^##*/

