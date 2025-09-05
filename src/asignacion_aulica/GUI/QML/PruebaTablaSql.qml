// import Qt.labs.qmlmodels
import QtQuick
import QtQuick.Controls
import IDontKnowMan

TableView {
    anchors.fill: parent
    columnSpacing: 1
    rowSpacing: 1
    clip: true

    model: OurTableBitch {
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
                   // 'display = text' is short-hand for:
                   // let index = TableView.view.index(row, column)
                   // TableView.view.model.setData(index, "display", text)
               }
       }
    }
}
