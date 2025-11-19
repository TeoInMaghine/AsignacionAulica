import QtQuick.Controls

// Es igual que un TextField, pero pierde foco al apretar enter.
TextField {
    id: self
    
    onAccepted: {
        self.focus = false
    }
}
