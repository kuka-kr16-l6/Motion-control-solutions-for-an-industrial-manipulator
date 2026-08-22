

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

Rectangle {
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor
    property alias a4Y: a4.y

    Item {
        id: __materialLibrary__
        PrincipledMaterial {
            id: principledMaterial
            objectName: "New Material"
        }
    }

    View3D {
        id: view3D
        x: 760
        y: 91
        width: 1008
        height: 891
        environment: sceneEnvironment1
        SceneEnvironment {
            id: sceneEnvironment1
            antialiasingQuality: SceneEnvironment.High
            antialiasingMode: SceneEnvironment.MSAA
        }

        Node {
            id: scene1
            DirectionalLight {
                id: directionalLight
                z: 10
                eulerRotation.y: 90
            }

            PerspectiveCamera {
                id: sceneCamera1
                x: 150
                y: 50
                eulerRotation.y: 90
                z: 0
            }
        }

        Base {
            id: base
            x: 0
            y: 0
            eulerRotation.y: 0
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
                    eulerRotation.y: 0
                    z: 0.28

                    A3_1 {
                        id: a3_1
                        x: 0
                        y: -0.04
                        eulerRotation.y: 90
                        eulerRotation.z: 270
                        eulerRotation.x: 0
                        z: 0.68

                        A4 {
                            id: a4
                            x: -0.117
                            y: 0.035
                            eulerRotation.y: 0
                            eulerRotation.z: 90
                            eulerRotation.x: 90
                            z: 0.7

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
        }

        A3 {
            id: a3
            x: -100
            y: -50
            eulerRotation.z: 180
            eulerRotation.y: 0
            eulerRotation.x: -90
            z: 50
        }
    }

    Rectangle {
        id: rectangle
        x: 103
        y: 107
        width: 325
        height: 859
        color: "#ffffff"
    }
}

/*##^##
Designer {
    D{i:0}D{i:3;cameraSpeed3d:10;cameraSpeed3dMultiplier:1}D{i:5;cameraSpeed3d:10;cameraSpeed3dMultiplier:1}
}
##^##*/

