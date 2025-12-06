import QtQuick
import QtQuick.Layouts
import QML.ComponentesUI

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

    EditorRangoHorarioEdificio {
        // Este modelData es del Repeater, no del model de ListView...
        required property string modelData
        rolHorarioInicio: "horario_inicio_" + modelData
        rolHorarioFin: "horario_fin_" + modelData
        rolHorarioCerrado: "horario_cerrado_" + modelData
        entidad: repeater.entidad

        Layout.preferredWidth: Constantes.width_columna_horario
        Layout.alignment: Qt.AlignCenter
    }
}
