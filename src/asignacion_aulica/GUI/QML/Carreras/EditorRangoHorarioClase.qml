import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

RowLayout {
    required property var clase

    spacing: Constantes.spacing_horario

    // Editores de horarios que se muestran cuando el rango horario está abierto
    readonly property int textFieldPadding : 2
    EditorHorario {
        id: horarioInicio

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: clase.horario_inicio
        onEditingFinished: {
            clase.horario_inicio = text
        }
        onChangeText: function(newText) {
            clase.horario_inicio = newText
        }
    }
    EditorHorario {
        id: horarioFin

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: clase.horario_fin
        onEditingFinished: {
            clase.horario_fin = text
        }
        onChangeText: function(newText) {
            clase.horario_fin = newText
        }
    }
}
