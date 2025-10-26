import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    required property string rolDeHorario

    readonly property int textFieldWidth : 45
    readonly property int textFieldPadding : 2
    spacing: 2

    // TODO: Fix. También, horario de edificio si el del aula == None (y engrisar también).
    // TODO: Agregar botón (que se pueda deshabilitar si se usa este componente
    // en la lista de clases) para resetear el horario al del edificio (por
    // ejemplo con un ícono tipo 🔄), solo interactuable si el usuario cambió
    // el horario.
    // property string horarioInicio : aula[rolDeHorario][0]
    // property string horarioFin : aula[rolDeHorario][1]
    property string horarioInicio : "00:00"
    property string horarioFin : "24:00"

    EditorHorario {
        Layout.preferredWidth: textFieldWidth
        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: horarioInicio
        onEditingFinished: {
            horarioInicio = text
        }
    }
    EditorHorario {
        Layout.preferredWidth: textFieldWidth
        Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: horarioFin
        onEditingFinished: {
            horarioFin = text
        }
    }
}
