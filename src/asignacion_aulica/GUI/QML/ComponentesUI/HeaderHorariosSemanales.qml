import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Repeater {
    model: [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo"
    ]
    RowLayout {
        required property string modelData

        Layout.preferredWidth: Constantes.width_columna_horario

        Label {
            Layout.preferredWidth: Constantes.width_columna_horario
                                   - Constantes.width_horario_sideButtons
                                   - Constantes.spacing_horario
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft

            horizontalAlignment: Text.AlignHCenter
            text: modelData
        }
    }
}
