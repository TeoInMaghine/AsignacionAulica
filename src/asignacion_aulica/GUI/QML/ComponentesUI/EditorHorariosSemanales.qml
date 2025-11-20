import QtQuick
import QtQuick.Layouts

Repeater {
    id: repeater
    required property var entidad

    // Días de la semana
    model: [
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo"
    ]

    EditorRangoHorario {
        // Este modelData es del Repeater, no del model de ListView...
        required property string modelData
        entidad: repeater.entidad
        díaDeLaSemana: modelData

        Layout.preferredWidth: Constantes.width_columna_horario
        Layout.alignment: Qt.AlignCenter
    }
}
