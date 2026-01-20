import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import QML.ComponentesUI

RowLayout {
    id: visualHeader

    property alias widthDía: headerDía.width
    property alias widthVirtual: headerVirtual.width
    property alias widthCantidadDeAlumnos: headerCantidadDeAlumnos.width
    property alias widthEquipamientoNecesario: headerEquipamientoNecesario.width

    Label {
        id: headerDía
        leftPadding: 50
        rightPadding: 50
        horizontalAlignment: Text.AlignHCenter
        text: "Día"
    }

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

    RowLayout {
        Layout.preferredWidth: Constantes.width_columna_aula_asignada

        Label {
            Layout.preferredWidth: Constantes.width_editores_aula_asignada
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft

            horizontalAlignment: Text.AlignHCenter
            text: "Aula asignada"
        }
    }
}
