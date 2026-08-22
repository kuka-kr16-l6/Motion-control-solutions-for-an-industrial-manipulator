import QtQuick
import QtQuick3D

Node {
    id: node

    // Resources
    PrincipledMaterial {
        id: color_material
        objectName: "color"
        baseColor: "#ffff7f00"
        roughness: 0.18000000715255737
        alphaMode: PrincipledMaterial.Opaque
    }
    PrincipledMaterial {
        id: color_1_material
        objectName: "color-1"
        baseColor: "#ff003333"
        roughness: 0.18000000715255737
        alphaMode: PrincipledMaterial.Opaque
    }

    // Nodes:
    Node {
        id: root
        objectName: "ROOT"
        OrthographicCamera {
            id: current_camera
            objectName: "current"
            x: 3.784600019454956
            y: -2.9461700916290283
            z: -8.72819995880127
            rotation: Qt.quaternion(0.162319, 0.966601, 0.0495123, 0.19205)
            scale.x: 0.999999
            scale.y: 1
            scale.z: 1
            clipNear: 0.009999999776482582
            clipFar: 100
            horizontalMagnification: 2
            verticalMagnification: 2
        }
        Node {
            id: assem8
            objectName: "Assem8"
            Model {
                id: kr16_AV300_sldasm_Part_7_1_1
                objectName: "KR16-AV300.sldasm-Part-7-1-1"
                x: -0.11699999868869781
                y: 1.3550000190734863
                z: -0.25999999046325684
                rotation: Qt.quaternion(0.5, 0.5, -0.5, 0.5)
                source: "meshes/meshes_0__mesh.mesh"
                materials: [
                    color_material
                ]
            }
            Model {
                id: kr16_AV300_sldasm_Part_6_1_1
                objectName: "KR16-AV300.sldasm-Part-6-1-1"
                x: -0.11699999868869781
                y: 1.3550000190734863
                z: -0.25999999046325684
                rotation: Qt.quaternion(0.5, 0.5, -0.5, 0.5)
                source: "meshes/meshes_1__mesh.mesh"
                materials: [
                    color_1_material
                ]
            }
            Model {
                id: kr16_AV300_sldasm_Part_6_1_2
                objectName: "KR16-AV300.sldasm-Part-6-1-2"
                x: -0.11687199771404266
                y: 1.4475799798965454
                z: -0.26750001311302185
                rotation: Qt.quaternion(-0.5, -0.5, 0.5, -0.5)
                source: "meshes/meshes_2__mesh.mesh"
                materials: [
                    color_1_material
                ]
            }
            Model {
                id: kr16_AV300_sldasm_Part_6_1_3
                objectName: "KR16-AV300.sldasm-Part-6-1-3"
                x: -0.11687199771404266
                y: 1.5400300025939941
                z: -0.2409999966621399
                rotation: Qt.quaternion(0.5, 0.5, -0.5, 0.5)
                source: "meshes/meshes_3__mesh.mesh"
                materials: [
                    color_1_material
                ]
            }
        }
    }

    // Animations:
}
