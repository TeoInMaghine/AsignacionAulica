import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import QML.ComponentesUI

RowLayout {
    id: visualHeader

    property alias widthCantidadDeAlumnos: headerCantidadDeAlumnos.width
    property alias widthEquipamiento: headerEquipamiento.width

    // TODO: Header selector de día

    // TODO: Header rango horario clase

    // TODO: Header "es virtual"

    Label {
        id: headerCantidadDeAlumnos
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "# Alumnos"
    }

    Label {
        id: headerEquipamiento
        leftPadding: 40
        rightPadding: 40
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Equipamiento"
    }

    // TODO: Header aula asignada

    // TODO: Header "no cambiar asignación"

    // Item { } // Espacio vacío de 2 * spacing de ancho
}
