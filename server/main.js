const express= require('express');
const http=require('http');
const socketIo=require('socket.io');
const morgan= require('morgan');
const app=express();
const server=http.createServer(app);
const io=socketIo(server);
const cors=require('cors');


//evento connection
io.on('connection',(socket)=>{
    //evento mensaje conexion
    socket.on('msgconexion',(msg)=>{
        console.log(msg);
        io.emit('msgconexion',msg);
    });
    //evento mensaje desconexion
    socket.on('msgdesconexion',(msg)=>{
        console.log(msg);
        socket.broadcast.emit('msgdesconexion',msg);
    });
    //evento para enviar un mensaje
    socket.on('mensaje',(mensaje)=>{
        console.log(mensaje);
        //El método emit recive como argumento una string del nombre del evento, y el objeto que se pasó como argumento del callback en socket.on
        io.emit('mensaje',mensaje);
    });
});



app.use(morgan('dev'));
app.use(cors());
app.get('/socket.io',(req,res)=>{
    res.send('hi');
});

const port=3000;
//En lugar de app se deve inicializar la instancia server ya que es donde está escuchando socket
server.listen(port,()=>{
console.log(`Servidor en el puerto ${port}`)
});
