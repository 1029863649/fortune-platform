import { autoUpdater } from 'electron-updater'
import { app, BrowserWindow, ipcMain } from 'electron'

export function initAutoUpdater(mainWindow: BrowserWindow) {
  autoUpdater.autoDownload = false

  autoUpdater.on('checking-for-update', () => {
    mainWindow.webContents.send('update-message', '检查更新中...')
  })

  autoUpdater.on('update-available', (info) => {
    mainWindow.webContents.send('update-available', info)
  })

  autoUpdater.on('update-not-available', () => {
    mainWindow.webContents.send('update-not-available')
  })

  autoUpdater.on('error', (err) => {
    mainWindow.webContents.send('update-error', err)
  })

  autoUpdater.on('download-progress', (progressObj) => {
    mainWindow.webContents.send('download-progress', progressObj)
  })

  autoUpdater.on('update-downloaded', () => {
    mainWindow.webContents.send('update-downloaded')
  })

  // 检查更新
  ipcMain.on('check-for-update', () => {
    autoUpdater.checkForUpdates()
  })

  // 开始下载
  ipcMain.on('start-download', () => {
    autoUpdater.downloadUpdate()
  })

  // 安装更新
  ipcMain.on('install-update', () => {
    autoUpdater.quitAndInstall()
  })
} 