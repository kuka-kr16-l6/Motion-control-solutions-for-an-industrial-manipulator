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
            x: -7.143139839172363
            y: 4.817920207977295
            z: 0.68510502576828
            rotation: Qt.quaternion(-0.381754, -0.291555, 0.625368, 0.614959)
            scale.x: 1
            scale.y: 1
            scale.z: 1
            clipNear: 0.009999999776482582
            clipFar: 100
            horizontalMagnification: 2
            verticalMagnification: 2
        }
        Node {
            id: assem3
            objectName: "Assem3"
            Model {
                id: kr16_AV300_sldasm_Part_14_1
                objectName: "KR16-AV300.sldasm-Part-14-1"
                x: -0.25999999046325684
                y: 0.08299999684095383
                z: -0.675000011920929
                source: "meshes/meshes_0__mesh.mesh"
                materials: [
                    color_material
                ]
            }
        }
    }

    // Animations:
}
