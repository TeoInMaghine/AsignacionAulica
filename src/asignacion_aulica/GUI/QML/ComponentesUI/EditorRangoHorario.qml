import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    required property var entidad
    required property string sufijoRol

    readonly property string rolDeHorarioInicio:
        "horario_inicio_" + sufijoRol
    readonly property string rolDeHorarioFin:
        "horario_fin_" + sufijoRol

    readonly property int textFieldWidth : 45
    readonly property int textFieldPadding : 2
    spacing: 2

    // TODO: Fix. También, horario de edificio si el del aula == None (y engrisar también).
    // TODO: Agregar botón (que se pueda deshabilitar si se usa este componente
    // en la lista de clases) para resetear el horario al del edificio (por
    // ejemplo con un ícono tipo 🔄), solo interactuable si el usuario cambió
    // el horario.

    EditorHorario {
        Layout.preferredWidth: textFieldWidth
        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: entidad[rolDeHorarioInicio]
        onEditingFinished: {
            entidad[rolDeHorarioInicio] = text
        }
    }
    EditorHorario {
        Layout.preferredWidth: textFieldWidth
        Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: entidad[rolDeHorarioFin]
        onEditingFinished: {
            entidad[rolDeHorarioFin] = text
        }
    }
}
