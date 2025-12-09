import QtQuick
import QtQuick.Controls

// Referencia:
// https://doc.qt.io/qt-6/qml-qtquick-textinput.html#inputMask-prop
TextFieldConEnter {
    // Define qué caracteres "deja pasar". Hace la edición más fluída, ya
    // que hace avanzar el cursor cuando corresponde (por ejemplo, al
    // ingresar un dígito o para saltear el ":").
    inputMask: "99:99"
    maximumLength: 5 // Duh
    // Valida que el texto sea una hora válida (por ejemplo, no podés
    // ingresar "30:00" o "24:01", pero sí "08:33" o "24:00")
    validator: RegularExpressionValidator {
        regularExpression: /^(([0-1][0-9]|2[0-3]):([0-5][0-9])|(24:00))$/
    }
    // Poner cursor al principio al ganar focus
    onActiveFocusChanged: {
        if (activeFocus) cursorPosition = 0
    }

    // Sobre-escribir comportamientos al presionar teclas de borrado.
    // Sino no hacen nada o resultan en comportamiento inválido al
    // seleccionar texto.
    Keys.onPressed: (event) => {
        switch (event.key) {
            // Reemplaza el dígito previo al cursor por 0 y mueve el cursor
            // a la izquierda.
            case Qt.Key_Backspace:
                event.accepted = true

                if (cursorPosition == 0) break

                var index = cursorPosition - 1
                if (text[index] == ":") index-- // Para no intentar borrar el ":"
                // NOTA: (posiblemente) por la configuración que tenemos insert
                // funciona no-intuitivamente, por eso no es necesario usar
                // remove.
                insert(index, "0")
                cursorPosition = index

                break
            // Trata a las horas y minutos como campos separados.
            // Elimina el dígito siguiente al cursor, mueve a la derecha el
            // cursor y agrega un cero a la izquierda del número del campo.
            case Qt.Key_Delete:
                event.accepted = true

                if (cursorPosition == maximumLength) break

                var index = cursorPosition
                // Como son sólo 4 casos y tienen excepciones entre sí, los manejo individualmente
                switch (index) {
                    case 0:
                        insert(0, "0")
                        break
                    case 1:
                        insert(1, text[0])
                        index++ // Para que el cursor se mueva después del ":"
                        break
                    case 3:
                        insert(3, "0")
                        break
                    case 4:
                        insert(4, text[3])
                        break
                    default:
                        // cursorPosition != 2 sí o sí por la configuración que
                        // tenemos, así que este caso no puede ocurrir!
                        console.error("Este índice no debería ser posible: " + index)
                        break
                }
                cursorPosition = index + 1

                break
        }
    }

    // Para teclados virtuales, probablemente no lo necesitemos pero no está de más
    inputMethodHints: Qt.ImhDigitsOnly
}
