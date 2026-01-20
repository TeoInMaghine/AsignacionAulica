import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

RowLayout {
    required property var clase

    spacing: Constantes.spacing_horario

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
    }
}
