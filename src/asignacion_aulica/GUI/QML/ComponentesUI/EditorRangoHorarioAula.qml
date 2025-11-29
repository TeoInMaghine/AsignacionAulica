import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    required property var entidad_padre
    required property var entidad
    required property string rolDeHorarioInicio
    required property string rolDeHorarioFin

    spacing: Constantes.spacing_horario

    // Dependiendo de si el rango horario está abierto o cerrado, se muestran o
    // esconden ciertos elementos
    property bool cerrado: entidad[rolDeHorarioInicio] ?
                            entidad[rolDeHorarioInicio] == entidad[rolDeHorarioFin] :
                            entidad_padre[rolDeHorarioInicio] == entidad_padre[rolDeHorarioFin]

    // TODO: Agregar botón (que se pueda deshabilitar si se usa este componente
    // en la lista de clases) para resetear el horario al del edificio (por
    // ejemplo con un ícono tipo 🔄), solo interactuable si el usuario cambió
    // el horario.

    // Editores de horarios que se muestran cuando el rango horario está abierto
    readonly property int textFieldPadding : 2
    EditorHorario {
        id: horarioInicio
        visible: !cerrado

        Layout.preferredWidth: Constantes.width_horario_textField
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
        id: horarioFin
        visible: !cerrado

        Layout.preferredWidth: Constantes.width_horario_textField
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

    // Elemento que se muestra cuando el rango horario está cerrado
    Label {
        visible: cerrado

        // Ocupa el mismo espacio que los editores de horarios
        Layout.preferredWidth: horarioInicio.Layout.preferredWidth + spacing + horarioFin.Layout.preferredWidth
        Layout.preferredHeight: horarioInicio.height

        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        // Des-enfatizar texto cuando se usa el horario de la entidad padre
        color: entidad[rolDeHorarioInicio] ? palette.dark : palette.mid
        font.bold: true
        text: "CERRADO"

        background: Rectangle {
            border.width: 1
            border.color: horarioInicio.palette.mid
        }
    }

    // Se puede cerrar el rango horario editando los horarios para que sean
    // iguales, pero la única forma de abrir el rango horario es con este botón
    Candado {
        Layout.preferredWidth: Constantes.width_horario_sideButtons
        Layout.preferredHeight: Constantes.width_horario_sideButtons

        // Des-enfatizar candado cuando se usa el horario de la entidad padre
        opacity: entidad[rolDeHorarioInicio] ? 1.0 : 0.5
        checked: cerrado
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
