import wx;
import socketio;
from sound import Sound;
from cytolk import tolk;

class UserDialog(wx.TextEntryDialog):
    def __init__(self, parent, message, caption='Nombre de usuario', value=wx.EmptyString):
        super(UserDialog, self).__init__(parent, message, caption, value, style=wx.TextEntryDialogStyle|wx.OK|wx.CANCEL)
        self.dialogClosed = False
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        self.dialogClosed = True
        event.Skip()

class MainWindow(wx.Frame):
    def __init__(self,*args, tolkInstance,**kw):
        super(MainWindow, self).__init__(*args,**kw);
        self.tolk=tolkInstance;
        self.userName='';
        userDialog = UserDialog(self, 'Ingrese su nombre de usuario:', 'Nombre de usuario')
        while not self.userName and not userDialog.dialogClosed:
            result = userDialog.ShowModal()
            if result == wx.ID_OK:
                self.userName = userDialog.GetValue().strip()
                if not self.userName:
                    wx.MessageBox('Es necesario proporcionar un nombre de usuario.', 'Error', wx.OK | wx.ICON_ERROR)
                else:
                    userDialog.Destroy()
                    self.setupMainWindow()
                    self.connectSocket(userNameP=self.userName)
            else:
                userDialog.Destroy()
                self.Destroy()

        self.Bind(wx.EVT_CLOSE, self.onClose)


    def setupMainWindow(self):
        self.panel=wx.Panel(self);
        caja=wx.BoxSizer(wx.VERTICAL);
        labelChat=wx.StaticText(self.panel,label='&Chat');
        caja.Add(labelChat,0,wx.ALL,5);
        self.chatBox=wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER);
        self.chatBox.Bind(wx.EVT_TEXT_ENTER, self.sendMethod);
        caja.Add(self.chatBox,0,wx.ALL,5);
        self.sendButton=wx.Button(self.panel, label='&Enviar');
        self.sendButton.Bind(wx.EVT_BUTTON, self.sendMethod);
        caja.Add(self.sendButton,0,wx.ALL,5);
        caja2=wx.BoxSizer(wx.VERTICAL);
        self.mensajesLista=wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL);
        self.mensajesLista.InsertColumn(0, 'Mensajes');
        caja2.Add(self.mensajesLista,0,wx.ALL,5);
        self.panel.SetSizer(caja);
        self.panel.SetSizer(caja2);
        #socketIo
        self.io=socketio.Client();
        self.io.on('mensaje',self.insertMensajes);
        self.io.on('msgconexion', self.connectSocketNotification);
        self.io.on('msgdesconexion', self.disconnectSocketNotification);


    sound=Sound();

    def connectSocketNotification(self,data):
        self.sound.connectSound();
        self.tolk.speak(data);
        self.mensajesLista.Append([data]);


    def disconnectSocketNotification(self,data):
        self.sound.disconnectSound();
        self.tolk.speak(data);
        self.mensajesLista.Append([data]);

    def connectSocket(self, userNameP):
        try:
            self.io.connect('http://localhost:3000');
            mensajeConexion=f'{userNameP} se conectó';
            self.io.emit('msgconexion',mensajeConexion);
        except Exception as e:
            wx.MessageBox(f'Error al conectar al servidor: {str(e)}', 'Error de conexión', wx.OK | wx.ICON_ERROR)
            self.Destroy()


    def sendMethod(self,event):
        if not self.userName:
            wx.MessageBox('Es necesario proporcionar un nombre de usuario.', 'Error', wx.OK | wx.ICON_ERROR);
        else:
            mensaje = self.chatBox.GetValue().strip();
            if mensaje:
                mensajeTexto=f'{self.userName}: {self.chatBox.GetValue()}';
                self.io.emit('mensaje', mensajeTexto);
                self.chatBox.SetValue('');

    def insertMensajes(self,mensaje):
        self.mensajesLista.Append([mensaje]);
        self.tolk.speak(mensaje);
        self.sound.chatSound();

    def disconnectSocket(self):
        mensajeDesconexion = f'{self.userName} se desconectó';
        self.io.emit('msgdesconexion', mensajeDesconexion);


    def onClose(self,event):
        self.disconnectSocket();
        self.Destroy();


with tolk.tolk():
    app=wx.App();
    mainWindow=MainWindow(None, title='Chat simple',tolkInstance=tolk);
    mainWindow.Show();
    app.MainLoop();
