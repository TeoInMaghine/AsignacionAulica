import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

RowLayout {
    id: visualHeader

    property alias widthNombre: headerNombre.width
    property alias widthCapacidad: headerCapacidad.width
    property alias widthEquipamiento: headerEquipamiento.width

    Button {
        id: headerNombre
        contentItem: RowLayout {
            spacing: 0
            Label {
                Layout.alignment: Qt.AlignCenter
                text: "Aula"
                color: headerNombre.highlighted ? headerNombre.palette.brightText
                                                : headerNombre.palette.buttonText
            }
            Image {
                Layout.alignment: Qt.AlignCenter
                fillMode: Image.PreserveAspectFit
                source: assets_path + "/iconos/Ordenar.svg"
            }
        }
        highlighted: hovered
        onClicked: {
            aulas.ordenar()
        }
    }
    Label {
        id: headerCapacidad
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Capacidad"
    }

    Item { } // Espacio vacío de 2 * spacing de ancho

    HeaderHorariosSemanales { }

    Item { } // Espacio vacío de 2 * spacing de ancho

    Label {
        id: headerEquipamiento
        leftPadding: 50
        rightPadding: 50
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
        text: "Equipamiento"
    }
}
