// src/api/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  withCredentials: true, // important if using auth/session
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const fetchExpenses = (params = {}) => {
  return api.get('/expenses/', { params })
}


export const fetchExpenseStats = (params = {}) => {
  return api.get('/expenses/statistics/', { params })
}


export const fetchCategories = () => {
  return api.get('/categories/')
}

export default api
