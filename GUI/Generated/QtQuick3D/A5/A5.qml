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
            x: -0.5489550232887268
            y: -1.520509958267212
            z: -0.1396619975566864
            rotation: Qt.quaternion(0.663828, 0.72382, -0.156387, -0.104696)
            scale.x: 1
            scale.y: 1
            scale.z: 1
            clipNear: 0.009999999776482582
            clipFar: 100
            horizontalMagnification: 2
            verticalMagnification: 2
        }
        Node {
            id: assem7
            objectName: "Assem7"
            Model {
                id: kr16_AV300_sldasm_Part_17_1_1
                objectName: "KR16-AV300.sldasm-Part-17-1-1"
                x: -1.2300000190734863
                y: -0.05299999937415123
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
