import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    required property string rolDeHorario

    readonly property int textFieldWidth : 45
    readonly property int textFieldPadding : 2
    spacing: 2

    // TODO: Fix. También, horario de edificio si el del aula == None (y engrisar también).
    // Dudas:
    // - ¿Queremos que por ejemplo puedas customizar el horario de
    // inicio para un aula, pero también dejar el de fin con el valor del
    // edificio?
    // - ¿Tendría el usuario una forma de expresar explícitamente que el
    // horario del aula use el horario del edificio, después de haber editado
    // el campo por primera vez?
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
