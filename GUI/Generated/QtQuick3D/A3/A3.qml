import QtQuick
import QtQuick3D

Node {
    id: node
    scale.x: 55
    scale.y: 55
    scale.z: 55

    // Resources
    PrincipledMaterial {
        id: color_2_material
        objectName: "color-2"
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
            x: 10.128800392150879
            y: -0.03049900010228157
            z: -0.08893080055713654
            rotation: Qt.quaternion(-0.5, 0.5, -0.5, 0.5)
            clipNear: 0.009999999776482582
            clipFar: 100
            horizontalMagnification: 2
            verticalMagnification: 2
        }
        Node {
            id: assem2
            objectName: "Assem2"
            Model {
                id: kr16_AV300_sldasm_Part_7_1
                objectName: "KR16-AV300.sldasm-Part-7-1"
                x: 0.25999999046325684
                y: -0.11699999868869781
                z: -1.3550000190734863
                rotation: Qt.quaternion(-2.77556e-17, -4.02742e-15, 3.87729e-17, 1)
                source: "meshes/meshes_0__mesh.mesh"
                materials: [
                    color_2_material
                ]
            }
            Model {
                id: kr16_AV300_sldasm_Part_5_1_2
                objectName: "KR16-AV300.sldasm-Part-5-1-2"
                x: 0.2865000069141388
                y: -0.11699999868869781
                z: -1.2625499963760376
                rotation: Qt.quaternion(-2.77556e-17, -3.65158e-15, 1.39387e-16, 1)
                source: "meshes/meshes_1__mesh.mesh"
                materials: [
                    color_1_material
                ]
            }
            Model {
                id: kr16_AV300_sldasm_Part_5_1_3
                objectName: "KR16-AV300.sldasm-Part-5-1-3"
                x: 0.25999999046325684
                y: -0.11699999868869781
                z: -1.3550000190734863
                rotation: Qt.quaternion(-2.77556e-17, -4.02742e-15, 3.87729e-17, 1)
                source: "meshes/meshes_2__mesh.mesh"
                materials: [
                    color_1_material
                ]
            }
            Model {
                id: kr16_AV300_sldasm_Part_5_1_1
                objectName: "KR16-AV300.sldasm-Part-5-1-1"
                x: 0.27900001406669617
                y: -0.11712799966335297
                z: -1.1699700355529785
                rotation: Qt.quaternion(-2.77556e-17, -3.65158e-15, 1.39387e-16, 1)
                source: "meshes/meshes_3__mesh.mesh"
                materials: [
                    color_1_material
                ]
            }
            Model {
                id: kr16_AV300_sldasm_Part_4_1_1
                objectName: "KR16-AV300.sldasm-Part-4-1-1"
                x: 0.2659890055656433
                y: -0.11699999868869781
                z: -1.3551599979400635
                rotation: Qt.quaternion(-2.77556e-17, -3.72051e-14, 4.22424e-17, 1)
                source: "meshes/meshes_4__mesh.mesh"
                materials: [
                    color_material
                ]
            }
        }
    }

    // Animations:
}
