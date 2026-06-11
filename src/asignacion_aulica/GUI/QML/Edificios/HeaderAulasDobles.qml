import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import QML.ComponentesUI

RowLayout {
    id: visualHeader

    BotónOrdenar {
        labelText: "Aula grande"
        Layout.preferredWidth: Constantes.width_editor_aula
        onClicked: {
            aulasDobles.ordenar()
        }
    }

    Item { width: 10 } // Espacio vacío, separar aula grande de las chicas

    RowLayout {
        Layout.preferredWidth:
            2*Constantes.width_editor_aula + visualHeader.spacing

        Label {
            Layout.preferredWidth: 2*Constantes.width_editor_aula
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft

            horizontalAlignment: Text.AlignHCenter
            text: "Aulas chicas"
        }
    }
}
