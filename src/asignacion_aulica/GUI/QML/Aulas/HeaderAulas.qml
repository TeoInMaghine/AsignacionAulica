import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

RowLayout {
    id: visualHeader

    required property int leftPadding
    required property int verticalPadding

    property alias widthNombre : headerNombre.width
    property alias widthCapacidad : headerCapacidad.width
    property alias widthEquipamiento : headerEquipamiento.width

    Layout.alignment: Qt.AlignHCenter
    Layout.topMargin: verticalPadding
    Layout.bottomMargin: verticalPadding

    Label {
        id: headerNombre
        // Tiene que aplicarse acá el "leftPadding" en vez de en el RowLayout en sí
        Layout.leftMargin: parent.leftPadding
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Nombre"
    }
    Label {
        id: headerCapacidad
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Capacidad"
    }

    Item { } // Espacio vacío de 2 * spacing de ancho

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
        Label {
            Layout.preferredWidth: Constantes.width_columna_horario
            horizontalAlignment: Text.AlignHCenter

            required property string modelData
            text: modelData
        }
    }

    Item { } // Espacio vacío de 2 * spacing de ancho

    Label {
        id: headerEquipamiento
        leftPadding: 50
        rightPadding: 50
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Equipamiento"
    }

    Button {
        text: "Ordenar"
        highlighted: hovered
        onClicked: {
            aulas.ordenar()
        }
    }
}
