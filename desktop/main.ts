import { app, BrowserWindow, ipcMain } from 'electron'
import * as path from 'path'
import Store from 'electron-store'

const store = new Store()

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    title: '天机阁占卜平台',
    icon: path.join(__dirname, 'build/icon.ico')
  })

  // 在开发环境中加载本地服务器
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000')
    mainWindow.webContents.openDevTools()
  } else {
    // 在生产环境中加载打包后的前端文件
    mainWindow.loadFile(path.join(__dirname, '../web/dist/index.html'))
  }

  // 保存窗口大小和位置
  mainWindow.on('close', () => {
    store.set('windowBounds', mainWindow.getBounds())
  })
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

// IPC通信处理
ipcMain.on('get-user-token', (event) => {
  event.reply('user-token', store.get('userToken'))
})

ipcMain.on('save-user-token', (event, token) => {
  store.set('userToken', token)
}) 