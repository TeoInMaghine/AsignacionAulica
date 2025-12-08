import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

RowLayout {
    required property var edificio
    required property string rolHorarioInicio
    required property string rolHorarioFin
    required property string rolHorarioCerrado

    spacing: Constantes.spacing_horario

    // Editores de horarios que se muestran cuando el rango horario está abierto
    readonly property int textFieldPadding : 2
    EditorHorario {
        id: horarioInicio
        visible: !edificio[rolHorarioCerrado]

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: edificio[rolHorarioInicio]
        onEditingFinished: {
            edificio[rolHorarioInicio] = text
        }
        onChangeText: function(newText) {
            edificio[rolHorarioInicio] = newText
        }
    }
    EditorHorario {
        id: horarioFin
        visible: !edificio[rolHorarioCerrado]

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: edificio[rolHorarioFin]
        onEditingFinished: {
            edificio[rolHorarioFin] = text
        }
        onChangeText: function(newText) {
            edificio[rolHorarioFin] = newText
        }
    }

    // Elemento que se muestra cuando el rango horario está cerrado
    Label {
        visible: edificio[rolHorarioCerrado]

        // Ocupa el mismo espacio que los editores de horarios
        Layout.preferredWidth: Constantes.width_editores_horarios
        Layout.preferredHeight: horarioInicio.height

        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.bold: true
        text: "Cerrado"

        background: Rectangle {
            border.width: 1
            border.color: horarioInicio.palette.mid
        }
    }

    Candado {
        Layout.preferredWidth: Constantes.width_horario_sideButtons
        Layout.preferredHeight: Constantes.width_horario_sideButtons

        checked: edificio[rolHorarioCerrado]
        onClicked: edificio[rolHorarioCerrado] = checked
    }
}
