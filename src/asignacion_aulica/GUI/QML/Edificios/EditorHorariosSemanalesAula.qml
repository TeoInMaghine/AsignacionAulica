import QtQuick
import QtQuick.Layouts
import QML.ComponentesUI

Repeater {
    id: repeater
    required property var edificio
    required property var aula

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

    EditorRangoHorarioAula {
        // Este modelData es del Repeater, no del model de ListView...
        required property string modelData
        rolHorarioInicio: "horario_inicio_" + modelData
        rolHorarioFin: "horario_fin_" + modelData
        rolHorarioCerrado: "horario_cerrado_" + modelData
        rolAulaTieneHorarioPropio: "horario_es_propio_" + modelData
        edificio: repeater.edificio
        aula: repeater.aula

        Layout.preferredWidth: Constantes.width_columna_horario
        Layout.alignment: Qt.AlignCenter
    }
}
