import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: visualHeader

    required property int leftPadding
    required property int verticalPadding

    property alias widthNombre : headerNombre.width
    property alias widthCapacidad : headerCapacidad.width
    // Si la resolución de dependencias de Qt funciona, esto no se recalcula al
    // menos que cambien los anchos de los horarios...
    property int widthHorario : Math.max(...horarios.children.map(c => c.width))

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

    RowLayout {
        id: horarios
        spacing: parent.spacing
        uniformCellSizes: true

        Repeater {
            model: ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            Label {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                required property string modelData
                text: modelData
            }
        }
    }

    Button {
        height: horarios.height
        text: "Ordenar"
        onClicked: {
            aulas.ordenar()
        }
    }
}
