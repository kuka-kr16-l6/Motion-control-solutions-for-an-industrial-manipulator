import QtQuick
import QtQuick.Controls
import QtQuick3D
import UntitledProject1

ApplicationWindow {
    visible: true
    width: 1366
    height: 768

    // load the UI file as a component
    Screen01 {
        id: ui
        anchors.fill: parent
        
        
}
    

    MouseArea {
        anchors.fill: ui.home_icon
        onClicked: {
            if (ui.rectangle1.view3D.scene1 && ui.rectangle1.view3D.scene1.sceneCamera) {
                console.log("Camera exists")
                ui.rectangle1.view3D.scene1.sceneCamera.position = Qt.vector3d(150,50,0)
                ui.rectangle1.view3D.scene1.sceneCamera.eulerRotation = Qt.vector3d(0,90,0)
            } else {
                console.log("Camera not ready yet")
            }
        }
    }
}