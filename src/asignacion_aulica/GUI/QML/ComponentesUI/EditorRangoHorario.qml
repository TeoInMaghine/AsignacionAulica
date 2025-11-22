import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    property var entidad_padre
    required property var entidad
    required property string rolDeHorarioInicio
    required property string rolDeHorarioFin

    readonly property int textFieldWidth : 45
    readonly property int textFieldPadding : 2
    spacing: 2

    // TODO: Agregar botón (que se pueda deshabilitar si se usa este componente
    // en la lista de clases) para resetear el horario al del edificio (por
    // ejemplo con un ícono tipo 🔄), solo interactuable si el usuario cambió
    // el horario.

    EditorHorario {
        Layout.preferredWidth: textFieldWidth
        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        // Des-enfatizar texto cuando se usa el horario de la entidad padre
        color: entidad[rolDeHorarioInicio] ? palette.dark : palette.mid
        // Si no se especifica el horario, mostrar el de la entidad padre
        text: entidad[rolDeHorarioInicio] ?
              entidad[rolDeHorarioInicio] :
              entidad_padre[rolDeHorarioInicio]
        onEditingFinished: {
            entidad[rolDeHorarioInicio] = text
        }
    }
    EditorHorario {
        Layout.preferredWidth: textFieldWidth
        Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        // Des-enfatizar texto cuando se usa el horario de la entidad padre
        color: entidad[rolDeHorarioFin] ? palette.dark : palette.mid
        // Si la no se especifica el horario, mostrar el de la entidad padre
        text: entidad[rolDeHorarioFin] ?
              entidad[rolDeHorarioFin] :
              entidad_padre[rolDeHorarioFin]
        onEditingFinished: {
            entidad[rolDeHorarioFin] = text
        }
    }
}
