import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

RowLayout {
    required property int indexCarrera
    required property int indexMateria
    required property int indexClase
    
    SelectorDeEdificioConAulas{
        id: selectorEdificio
    }

    SelectorDeAula{
        indexEdificio: selectorEdificio.indexEdificioSeleccionado
    }
}
