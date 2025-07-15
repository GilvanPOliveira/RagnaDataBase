import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// ——————————————————————————————
// Auth
// ——————————————————————————————
export async function ping() {
  // verifica se o servidor está vivo
  const res = await api.get('/auth/ping');
  return res.data;
}

export async function register(email, password) {
  const res = await api.post('/auth/register', { email, password });
  return res.data;
}

export async function login(email, password) {
  const res = await api.post('/auth/login', { email, password });
  return res.data;
}

// ——————————————————————————————
// Usuário
// ——————————————————————————————
export async function getProfile() {
  // retorna dados do usuário logado
  const res = await api.get('/users/me');
  return res.data;
}

export async function updateProfile(data) {
  // data pode ter { name, email, ... }
  const res = await api.put('/users/me', data);
  return res.data;
}

// ——————————————————————————————
// Busca de Itens
// ——————————————————————————————
export async function searchItems(name, page = 1, per_page = 10) {
  const res = await api.get('/search', {
    params: { name, page, per_page }
  });
  return res.data;
}

export async function getItemById(id) {
  const res = await api.get(`/item/${id}`);
  return res.data;
}

// ——————————————————————————————
// Inventário
// ——————————————————————————————
export async function getInventoryList() {
  const res = await api.get('/inventory/list');
  return res.data;
}

export async function addInventoryItem(item_id, quantity, price) {
  const res = await api.post('/inventory', {
    item_id,
    quantity,
    price
  });
  return res.data;
}

export async function updateInventoryItem(inventoryId, updates) {
  // updates: { quantity?, price? }
  const res = await api.put(`/inventory/${inventoryId}`, updates);
  return res.data;
}

export async function deleteInventoryItem(inventoryId) {
  const res = await api.delete(`/inventory/${inventoryId}`);
  return res.data;
}

// ——————————————————————————————
// Listas
// ——————————————————————————————
export async function getLists() {
  const res = await api.get('/lists');
  return res.data;
}

export async function createList(title, description) {
  const res = await api.post('/lists', { title, description });
  return res.data;
}

export async function getList(listId) {
  const res = await api.get(`/lists/${listId}`);
  return res.data;
}

export async function updateList(listId, updates) {
  // updates: { title?, description? }
  const res = await api.put(`/lists/${listId}`, updates);
  return res.data;
}

export async function deleteList(listId) {
  const res = await api.delete(`/lists/${listId}`);
  return res.data;
}

export async function getListItems(listId) {
  const res = await api.get(`/lists/${listId}/items`);
  return res.data;
}

export async function addItemToList(listId, item_id, quantity = 1) {
  const res = await api.post(`/lists/${listId}/items`, {
    item_id,
    quantity
  });
  return res.data;
}

export async function removeItemFromList(listId, itemId) {
  const res = await api.delete(`/lists/${listId}/items/${itemId}`);
  return res.data;
}