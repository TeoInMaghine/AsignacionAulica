import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    required property var entidad
    required property string rolHorarioInicio
    required property string rolHorarioFin
    required property string rolHorarioCerrado

    spacing: Constantes.spacing_horario

    // Editores de horarios que se muestran cuando el rango horario está abierto
    readonly property int textFieldPadding : 2
    EditorHorario {
        id: horarioInicio
        visible: !entidad[rolHorarioCerrado]

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: entidad[rolHorarioInicio]
        onEditingFinished: {
            entidad[rolHorarioInicio] = text
        }
        onChangeText: function(newText) {
            entidad[rolHorarioInicio] = newText
        }
    }
    EditorHorario {
        id: horarioFin
        visible: !entidad[rolHorarioCerrado]

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: entidad[rolHorarioFin]
        onEditingFinished: {
            entidad[rolHorarioFin] = text
        }
        onChangeText: function(newText) {
            entidad[rolHorarioFin] = newText
        }
    }

    // Elemento que se muestra cuando el rango horario está cerrado
    Label {
        visible: entidad[rolHorarioCerrado]

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

        checked: entidad[rolHorarioCerrado]
        onClicked: entidad[rolHorarioCerrado] = checked
    }
}
