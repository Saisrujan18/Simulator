const { app, BrowserWindow } = require('electron')
const path = require('path')
var requirejs=require('requirejs')

try {
	require('electron-reloader')(module)
  } catch (_) {}


function createWindow () 
{
	const win = new BrowserWindow({
    	width: 800,
    	height: 600,
    	minHeight: 600,
    	minWidth: 800,
    	webPreferences: {
      		preload: path.join(__dirname, 'preload.js'),
      		nodeIntegration: true,
			contextIsolation: false,
			enableRemoteModule: true,
		}
  	})
  	win.loadFile('index.html')
}

app.whenReady().then(() => {
  	createWindow()
	app.on('activate', () => {
    	if (BrowserWindow.getAllWindows().length === 0) {
     	 	createWindow()
    	}
  	})
})

app.on('window-all-closed', () => {
  	if (process.platform !== 'darwin') {
    	app.quit()
 	}
})