// main.js

const { app, BrowserWindow } = require("electron")

// 创建窗口
function createWindow() {
    let win = new BrowserWindow({
        width: 1400,
        height: 900
    })
    // 加载 "templates/flask_welcome.html"
    win.loadURL("http://127.0.0.1:5000/")
}

// 使用 python-shell 调用 engine.py
const {PythonShell}  = require("python-shell")
PythonShell.run(
	"app.py", null, function (err, results) {
        if (err) throw err
        console.log('engine.py is running')
        console.log('results', results)
    }
)

const electron = require('electron')
const Menu = electron.Menu
Menu.setApplicationMenu(null)

// 启动
app.on("ready", createWindow)