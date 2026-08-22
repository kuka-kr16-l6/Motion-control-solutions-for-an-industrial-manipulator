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

    // Nodes:
    Node {
        id: root
        objectName: "ROOT"
        OrthographicCamera {
            id: current_camera
            objectName: "current"
            x: -1.655500054359436
            y: 2.6808600425720215
            z: -0.0394412986934185
            rotation: Qt.quaternion(0.68161, -0.682108, -0.194087, 0.180187)
            scale.x: 1
            scale.y: 1
            scale.z: 1
            clipNear: 0.009999999776482582
            clipFar: 100
            horizontalMagnification: 2
            verticalMagnification: 2
        }
        Node {
            id: assem2
            objectName: "Assem2"
            Model {
                id: kr16_AV300_sldasm_Part_16_1
                objectName: "KR16-AV300.sldasm-Part-16-1"
                x: -0.9620000123977661
                z: -1.3200000524520874
                source: "meshes/meshes_0__mesh.mesh"
                materials: [
                    color_material
                ]
            }
        }
    }

    // Animations:
}
