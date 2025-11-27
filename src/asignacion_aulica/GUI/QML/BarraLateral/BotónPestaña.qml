import QtQuick
import QtQuick.Controls
import QtQuick.VectorImage
import QtQuick.Layouts

// El botón de una pestaña.
Button {
    required property string nombre
    id: self
    Layout.fillWidth: true
    Layout.preferredHeight: Constantes.pestaña_altura
    spacing: 0

    contentItem: RowLayout{
        spacing: 0
        Image {
            Layout.alignment: Qt.AlignCenter
            Layout.rightMargin: 10
            fillMode: Image.PreserveAspectFit
            source: assets_path + "/iconos/" + self.nombre + ".svg"
        }
        Text {
            text: self.nombre
            font.pointSize: Constantes.pestaña_texto_tamaño_pts
            color: "white"
            horizontalAlignment: Text.AlignHLeft
            verticalAlignment: Text.AlignVCenter
        }
        Item {
            Layout.fillWidth: true
        }
    }
    
    background: Rectangle {
        color: self.pressed ? Constantes.rojo_unrn_oscurísimo :
            sidebar.pestaña_actual === self.nombre || self.hovered ?
            Constantes.rojo_unrn_oscuro : Constantes.rojo_unrn

        Behavior on color {
            ColorAnimation {
                easing.type: Easing.OutQuart
            }
        }
    }
}
