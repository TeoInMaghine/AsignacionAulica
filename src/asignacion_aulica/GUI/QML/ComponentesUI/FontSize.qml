import QtQuick

pragma Singleton

/** Constantes para unificar los tamaños de fuente en todos lados.
    Todos los tamaños están expresados en puntos.
*/
QtObject {
    readonly property int base: 12 // También definido en main.py
    readonly property int medium: 15
    readonly property int big: 17
    readonly property int bigger: 20
    readonly property int huge: 28
}
