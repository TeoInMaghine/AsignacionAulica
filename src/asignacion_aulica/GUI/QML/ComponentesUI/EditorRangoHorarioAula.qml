import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    required property var edificio
    required property var aula
    required property string rolHorarioInicio
    required property string rolHorarioFin
    required property string rolHorarioCerrado
    required property string rolAulaTieneHorarioPropio

    readonly property bool horarioCerrado: aula[rolAulaTieneHorarioPropio] ?
                                           aula[rolHorarioCerrado] :
                                           edificio[rolHorarioCerrado]

    spacing: Constantes.spacing_horario

    // TODO: Agregar botón (que se pueda deshabilitar si se usa este componente
    // en la lista de clases) para resetear el horario al del edificio (por
    // ejemplo con un ícono tipo 🔄), solo interactuable si el usuario cambió
    // el horario.

    // Editores de horarios que se muestran cuando el rango horario está abierto
    readonly property int textFieldPadding : 2
    EditorHorario {
        id: horarioInicio
        visible: !horarioCerrado

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        // Des-enfatizar texto cuando se usa el horario del edificio
        color: aula[rolAulaTieneHorarioPropio] ? palette.dark : palette.mid
        // Si no se especifica el horario, mostrar el del edificio
        text: aula[rolAulaTieneHorarioPropio] ?
              aula[rolHorarioInicio] :
              edificio[rolHorarioInicio]
        onEditingFinished: {
            aula[rolHorarioInicio] = text
        }
        onChangeText: function(newText) {
            aula[rolHorarioInicio] = newText
        }
    }
    EditorHorario {
        id: horarioFin
        visible: !horarioCerrado

        Layout.preferredWidth: Constantes.width_editor_horario
        leftPadding: textFieldPadding
        rightPadding: textFieldPadding

        // Des-enfatizar texto cuando se usa el horario del edificio
        color: aula[rolAulaTieneHorarioPropio] ? palette.dark : palette.mid
        // Si no se especifica el horario, mostrar el del edificio
        text: aula[rolAulaTieneHorarioPropio] ?
              aula[rolHorarioFin] :
              edificio[rolHorarioFin]
        onEditingFinished: {
            aula[rolHorarioFin] = text
        }
        onChangeText: function(newText) {
            aula[rolHorarioFin] = newText
        }
    }

    // Elemento que se muestra cuando el rango horario está cerrado
    Label {
        visible: horarioCerrado

        // Ocupa el mismo espacio que los editores de horarios
        Layout.preferredWidth: Constantes.width_editores_horarios
        Layout.preferredHeight: horarioInicio.height

        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        // Des-enfatizar texto cuando se usa el horario del edificio
        color: aula[rolAulaTieneHorarioPropio] ? palette.dark : palette.mid
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

        // Des-enfatizar candado cuando se usa el horario del edificio
        opacity: aula[rolAulaTieneHorarioPropio] ? 1.0 : 0.5
        checked: horarioCerrado
        onClicked: aula[rolHorarioCerrado] = checked
    }
}
