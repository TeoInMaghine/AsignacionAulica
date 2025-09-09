import QtQuick
import QtQuick.Controls
import Custom

TableView {
    anchors.fill: parent
    columnSpacing: 1
    rowSpacing: 1
    clip: true

    model: Table {
    }

    selectionModel: ItemSelectionModel {}

    delegate: Rectangle {
        implicitWidth: 100
        implicitHeight: 50
        Text {
            text: display
        }

       TableView.editDelegate: TextField {
           anchors.fill: parent
               text: display
               horizontalAlignment: TextInput.AlignHCenter
               verticalAlignment: TextInput.AlignVCenter
               Component.onCompleted: selectAll()

               TableView.onCommit: {
                   display = text
               }
       }
    }
}
