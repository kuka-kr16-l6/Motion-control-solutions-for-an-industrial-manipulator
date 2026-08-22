import QtQuick
import QtQuick3D

Node {
    id: node

    // Resources
    PrincipledMaterial {
        id: color_2_material
        objectName: "color-2"
        baseColor: "#ff003333"
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
    PrincipledMaterial {
        id: color_material
        objectName: "color"
        baseColor: "#ffff7f00"
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
            x: 0.19200199842453003
            y: -6.675270080566406
            z: 0.6999030113220215
            rotation: Qt.quaternion(0.733528, 0.678998, 0.0282059, -0.0101537)
            scale.x: 1
            scale.y: 1
            scale.z: 1
            clipNear: 0.009999999776482582
            clipFar: 100
            horizontalMagnification: 2
            verticalMagnification: 2
        }
        Node {
            id: assem1
            objectName: "Assem1"
            Model {
                id: kr16_AV300_sldasm_Part_2_1_1
                objectName: "KR16-AV300.sldasm-Part-2-1-1"
                x: -0.00014515500515699387
                y: 4.161279775871662e-06
                z: -0.3971039950847626
                source: "meshes/meshes_0__mesh.mesh"
                materials: [
                    color_2_material
                ]
            }
            Model {
                id: kr16_AV300_sldasm_Part_8_1_1
                objectName: "KR16-AV300.sldasm-Part-8-1-1"
                x: -0.00014515500515699387
                y: 0.0001803799968911335
                z: -0.396916002035141
                source: "meshes/meshes_1__mesh.mesh"
                materials: [
                    color_1_material
                ]
            }
            Model {
                id: kr16_AV300_sldasm_Part_15_2
                objectName: "KR16-AV300.sldasm-Part-15-2"
                z: -0.3969230055809021
                source: "meshes/meshes_2__mesh.mesh"
                materials: [
                    color_material
                ]
            }
        }
    }

    // Animations:
}
