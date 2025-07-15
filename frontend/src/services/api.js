// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// Interceptor: anexa o JWT a todas as requisições
api.interceptors.request.use(config => {
  const token = localStorage.getItem('jwt');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// — Auth —

// Pinga o servidor
export async function ping() {
  const res = await api.get('/auth/ping');
  return res.data;
}

// Faz login e retorna { access_token }
export async function login(email, password) {
  const res = await api.post('/auth/login', { email, password });
  return res.data;
}

// Cadastra um usuário (nome, e‑mail, senha)
export async function register(name, email, password) {
  const res = await api.post('/auth/register', { name, email, password });
  return res.data;
}

// — Usuário —

// Retorna perfil do usuário logado
export async function getProfile() {
  const res = await api.get('/users/me');
  return res.data;
}

// Atualiza perfil (name, email, password opcional)
export async function updateProfile(data) {
  // data deverá ter: { name, email, current_password, new_password? }
  const res = await api.patch('/users/me', data);
  return res.data;
}

// Exclui a conta do usuário logado, requer a senha atual
export async function deleteAccount(password) {
  // axios.delete não aceita `data` no 2º parâmetro, então passamos tudo em config
  const res = await api.delete('/users/me', {
    data: { password }
  });
  return res.data;
}

// — Admin: usuários —

// Lista todos os usuários (admin)
export async function getAllUsers() {
  const res = await api.get('/users');
  return res.data; // espera { users: [...] } ou diretamente [...]
}

// Atualiza dados de um usuário pelo ID
export async function updateUserById(id, data) {
  // data: { name?, email?, is_admin? }
  const res = await api.patch(`/users/${id}`, data);
  return res.data;
}

// Remove um usuário pelo ID
export async function deleteUserById(id) {
  const res = await api.delete(`/users/${id}`);
  return res.data;
}

// Promove usuário a admin
export async function promoteUser(userId) {
  // usa o endpoint POST /users/{userId}/promote
  // passa um body vazio para evitar 400 Bad Request
  const res = await api.post(`/users/${userId}/promote`, {});
  return res.data;
}

// — Itens —

// Busca itens por nome
export async function searchItems(name, page = 1, per_page = 10) {
  const res = await api.get('/search', {
    params: { name, page, per_page }
  });
  return res.data;
}

// Busca detalhes de item por ID
export async function getItemById(id) {
  const res = await api.get(`/item/${id}`);
  return res.data;
}

// — Inventário —

// Lista o inventário do usuário
export async function getInventoryList() {
  const res = await api.get('/inventory/list');
  return res.data;
}

// Adiciona item ao inventário
export async function addInventoryItem(item_id, quantity, price) {
  const res = await api.post('/inventory', { item_id, quantity, price });
  return res.data;
}

// Atualiza item do inventário
export async function updateInventoryItem(inventoryId, updates) {
  const res = await api.put(`/inventory/${inventoryId}`, updates);
  return res.data;
}

// Remove item do inventário
export async function deleteInventoryItem(inventoryId) {
  const res = await api.delete(`/inventory/${inventoryId}`);
  return res.data;
}

// — Listas —

// Lista todas as listas
export async function getLists() {
  const res = await api.get('/lists');
  return res.data;
}

// Cria nova lista
export async function createList(title, description) {
  const res = await api.post('/lists', { title, description });
  return res.data;
}

// Busca dados de uma lista
export async function getList(listId) {
  const res = await api.get(`/lists/${listId}`);
  return res.data;
}

// Atualiza lista
export async function updateList(listId, updates) {
  const res = await api.put(`/lists/${listId}`, updates);
  return res.data;
}

// Remove lista
export async function deleteList(listId) {
  const res = await api.delete(`/lists/${listId}`);
  return res.data;
}

// Itens dentro de uma lista
export async function getListItems(listId) {
  const res = await api.get(`/lists/${listId}/items`);
  return res.data;
}

// Adiciona item a uma lista
export async function addItemToList(listId, item_id, quantity = 1) {
  const res = await api.post(`/lists/${listId}/items`, {
    item_id,
    quantity
  });
  return res.data;
}

// Remove item de uma lista
export async function removeItemFromList(listId, itemId) {
  const res = await api.delete(`/lists/${listId}/items/${itemId}`);
  return res.data;
}
