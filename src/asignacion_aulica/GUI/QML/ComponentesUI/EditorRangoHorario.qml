import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    required property var entidad
    required property string rolDeHorarioInicio
    required property string rolDeHorarioFin

    spacing: Constantes.spacing_horario

    // Dependiendo de si el rango horario está abierto o cerrado, se muestran o
    // esconden ciertos elementos
    property bool cerrado: entidad[rolDeHorarioInicio] == entidad[rolDeHorarioFin]

    // Editores de horarios que se muestran cuando el rango horario está abierto
    readonly property int textFieldPadding : 2
    EditorHorario {
        id: horarioInicio
        visible: !cerrado

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: entidad[rolDeHorarioInicio]
        onEditingFinished: {
            entidad[rolDeHorarioInicio] = text
        }
    }
    EditorHorario {
        id: horarioFin
        visible: !cerrado

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        text: entidad[rolDeHorarioFin]
        onEditingFinished: {
            entidad[rolDeHorarioFin] = text
        }
    }

    // Elemento que se muestra cuando el rango horario está cerrado
    Label {
        visible: cerrado

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

    // Se puede cerrar el rango horario editando los horarios para que sean
    // iguales, pero la única forma de abrir el rango horario es con este botón
    Candado {
        Layout.preferredWidth: Constantes.width_horario_sideButtons
        Layout.preferredHeight: Constantes.width_horario_sideButtons

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
