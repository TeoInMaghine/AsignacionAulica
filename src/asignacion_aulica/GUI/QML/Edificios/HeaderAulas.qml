import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import QML.ComponentesUI

RowLayout {
    id: visualHeader

    property alias widthNombre: headerNombre.width
    property alias widthCapacidad: headerCapacidad.width
    property alias widthEquipamiento: headerEquipamiento.width

    BotónOrdenar {
        id: headerNombre
        labelText: "Aula"
        Layout.preferredWidth: 120 // Para que entre el texto "Sin nombre 1"
        onClicked: {
            aulas.ordenar()
        }
    }
    Label {
        id: headerCapacidad
        text: "Capacidad"
    }

    Item { } // Espacio vacío de 2 * spacing de ancho

    Label {
        id: headerEquipamiento
        leftPadding: 40
        rightPadding: 40
        text: "Equipamiento"
    }

    Item { } // Espacio vacío de 2 * spacing de ancho

    HeaderHorariosSemanales { }
}
