import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electron', {
  store: {
    get: (key: string) => ipcRenderer.invoke('electron-store-get', key),
    set: (key: string, val: any) => ipcRenderer.invoke('electron-store-set', key, val),
    delete: (key: string) => ipcRenderer.invoke('electron-store-delete', key)
  },
  ipcRenderer: {
    send: (channel: string, data: any) => ipcRenderer.send(channel, data),
    on: (channel: string, func: Function) => ipcRenderer.on(channel, (event, ...args) => func(...args))
  }
}) 