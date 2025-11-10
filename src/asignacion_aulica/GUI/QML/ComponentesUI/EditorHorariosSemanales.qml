import QtQuick
import QtQuick.Layouts

Repeater {
    // Roles de horarios
    model: [
        "horario_lunes",
        "horario_martes",
        "horario_miércoles",
        "horario_jueves",
        "horario_viernes",
        "horario_sábado",
        "horario_domingo"
    ]

    EditorRangoHorario {
        // Este modelData es del Repeater, no del model de ListView...
        required property string modelData
        rolDeHorario: modelData
        Layout.preferredWidth: Constantes.width_columna_horario
        Layout.alignment: Qt.AlignCenter
    }
}
