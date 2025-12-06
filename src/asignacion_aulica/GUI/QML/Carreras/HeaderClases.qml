import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import QML.ComponentesUI

RowLayout {
    id: visualHeader

    property alias widthVirtual: headerVirtual.width
    property alias widthCantidadDeAlumnos: headerCantidadDeAlumnos.width
    property alias widthEquipamientoNecesario: headerEquipamientoNecesario.width

    // TODO: Header selector de día

    Label {
        Layout.preferredWidth: Constantes.width_editores_horarios
        horizontalAlignment: Text.AlignHCenter
        text: "Horario"
    }

    Label {
        id: headerVirtual
        horizontalAlignment: Text.AlignHCenter
        text: "Virtual"
    }

    Label {
        id: headerCantidadDeAlumnos
        horizontalAlignment: Text.AlignHCenter
        text: "# Alumnos"
    }

    Label {
        id: headerEquipamientoNecesario
        leftPadding: 5
        rightPadding: 5
        text: "Equipamiento necesario"
    }

    // TODO: Header aula asignada

    // TODO: Header "no cambiar asignación"

    // Item { } // Espacio vacío de 2 * spacing de ancho
}
