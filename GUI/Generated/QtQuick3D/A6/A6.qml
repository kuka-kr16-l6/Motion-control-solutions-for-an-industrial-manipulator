import QtQuick
import QtQuick3D

Node {
    id: node

    // Resources
    PrincipledMaterial {
        id: color_material
        objectName: "color"
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
            x: -0.287308007478714
            y: 0.0013302599545568228
            z: 0.40479201078414917
            rotation: Qt.quaternion(0.951825, 0.0135591, -0.299796, -0.0629908)
            scale.x: 1
            scale.y: 1
            scale.z: 1
            clipNear: 0.009999999776482582
            clipFar: 100
            horizontalMagnification: 2
            verticalMagnification: 2
        }
        Node {
            id: assem6
            objectName: "Assem6"
            Model {
                id: kr16_AV300_sldasm_Part_13_1_1
                objectName: "KR16-AV300.sldasm-Part-13-1-1"
                x: -1.3387999534606934
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
