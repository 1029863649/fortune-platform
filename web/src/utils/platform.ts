export const isElectron = () => {
  return window.electron !== undefined
}

export const getPlatform = () => {
  if (isElectron()) {
    return 'desktop'
  }
  return 'web'
}

export const getToken = async () => {
  if (isElectron()) {
    return await window.electron.store.get('userToken')
  }
  return localStorage.getItem('token')
}

export const setToken = async (token: string) => {
  if (isElectron()) {
    await window.electron.store.set('userToken', token)
  } else {
    localStorage.setItem('token', token)
  }
} 