import QtQuick
import QtQuick3D

Node {
    id: node
    scale.x: 54
    scale.y: 54
    scale.z: 54

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
            x: -5.110189914703369
            y: -3.2677299976348877
            z: 3.1877400875091553
            rotation: Qt.quaternion(0.715154, 0.483973, -0.223216, -0.452216)
            scale.x: 1
            scale.y: 1
            scale.z: 1
            clipNear: 0.009999999776482582
            clipFar: 100
            horizontalMagnification: 2
            verticalMagnification: 2
        }
        Model {
            id: kr16_AV300_sldasm_Part_1_1
            objectName: "KR16-AV300.sldasm-Part-1-1"
            source: "meshes/meshes_0__mesh.mesh"
            materials: [
                color_material
            ]
        }
    }

    // Animations:
}
