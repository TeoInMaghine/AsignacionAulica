import QtQuick
import QtQuick.Layouts

Repeater {
    id: repeater
    property var entidad_padre
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
        rolDeHorarioInicio: "horario_inicio_" + modelData
        rolDeHorarioFin: "horario_fin_" + modelData
        entidad_padre: repeater.entidad_padre
        entidad: repeater.entidad

        Layout.preferredWidth: Constantes.width_columna_horario
        Layout.alignment: Qt.AlignCenter
    }
}
