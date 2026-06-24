import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

ColumnLayout {
    anchors.fill: parent
    anchors.margins: 15
    spacing: 20
    
    Botonera {
        indexCarrera: selector.indexCarrera
        onImportaciónHecha: {
            materias.model.resetModel()
            // TODO: Resetear ComboBoxCarrera de alguna forma
        }
    }

    SelectorYEditorDeCarrera {
        id: selector
        onCarreraChanged: {
            materias.model.resetModel()
        }
    }

    Materias {
        id: materias
        enabled: selector.hayCarreraSeleccionada
        indexCarrera: selector.indexCarrera
    }
}
