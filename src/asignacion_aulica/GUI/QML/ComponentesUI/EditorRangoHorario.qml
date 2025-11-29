import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    property var entidad_padre
    required property var entidad
    required property string rolDeHorarioInicio
    required property string rolDeHorarioFin

    spacing: Constantes.spacing_horario

    // TODO: Agregar botón (que se pueda deshabilitar si se usa este componente
    // en la lista de clases) para resetear el horario al del edificio (por
    // ejemplo con un ícono tipo 🔄), solo interactuable si el usuario cambió
    // el horario.

    readonly property int textFieldPadding : 2
    EditorHorario {
        Layout.preferredWidth: Constantes.width_horario_textField
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
        Layout.preferredWidth: Constantes.width_horario_textField
        Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        // Des-enfatizar texto cuando se usa el horario de la entidad padre
        color: entidad[rolDeHorarioFin] ? palette.dark : palette.mid
        // Si no se especifica el horario, mostrar el de la entidad padre
        text: entidad[rolDeHorarioFin] ?
              entidad[rolDeHorarioFin] :
              entidad_padre[rolDeHorarioFin]
        onEditingFinished: {
            entidad[rolDeHorarioFin] = text
        }
    }

    Candado {
        Layout.preferredWidth: Constantes.width_horario_sideButtons
        Layout.preferredHeight: Constantes.width_horario_sideButtons
        Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter

        checked: entidad[rolDeHorarioInicio] ?
                 entidad[rolDeHorarioInicio] == entidad[rolDeHorarioFin] :
                 entidad_padre[rolDeHorarioInicio] == entidad_padre[rolDeHorarioFin]
        onClicked: {
            if (checked) {
                // Cerrar
                entidad[rolDeHorarioInicio] = "00:00"
                entidad[rolDeHorarioFin] = "00:00"
            } else {
                // Abrir
                entidad[rolDeHorarioInicio] = "00:00"
                entidad[rolDeHorarioFin] = "24:00"
            }
        }
    }
}
