// src/pages/Inventory.jsx
import React, { useEffect, useState } from 'react';
import {
  getInventoryList,
  addInventoryItem,
  updateInventoryItem,
  deleteInventoryItem
} from '../services/api';
import '../styles/Inventory.scss';

export default function Inventory() {
  const [items, setItems] = useState([]);
  const [newItemId, setNewItemId] = useState('');
  const [newQty, setNewQty] = useState(1);
  const [newPrice, setNewPrice] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const { items } = await getInventoryList();
      setItems(items || []);
    } catch {
      setError('Erro ao carregar inventário.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  async function handleAdd(e) {
    e.preventDefault();
    try {
      await addInventoryItem(newItemId, newQty, newPrice);
      setNewItemId(''); setNewQty(1); setNewPrice(0);
      load();
    } catch {
      setError('Erro ao adicionar.');
    }
  }

  async function handleUpdate(id, qty, price) {
    try {
      await updateInventoryItem(id, { quantity: qty, price });
      load();
    } catch {
      setError('Erro ao atualizar.');
    }
  }

  async function handleDelete(id) {
    try {
      await deleteInventoryItem(id);
      load();
    } catch {
      setError('Erro ao remover.');
    }
  }

  if (loading) return <p>Carregando…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="inventory-page container">
      <h1>Meu Inventário</h1>
      <form onSubmit={handleAdd} className="add-form">
        <input placeholder="ID do item" value={newItemId} onChange={e => setNewItemId(e.target.value)} required/>
        <input type="number" min="1" value={newQty} onChange={e => setNewQty(+e.target.value)} required/>
        <input type="number" min="0" value={newPrice} onChange={e => setNewPrice(+e.target.value)} required/>
        <button type="submit">Adicionar</button>
      </form>
      <ul className="inventory-list">
        {items.map(inv => (
          <li key={inv.id} className="inventory-item">
            <span>
              {inv.item.name} (#{inv.item.id}) 
              Qty:<input type="number" value={inv.quantity} onChange={e => handleUpdate(inv.id, +e.target.value, inv.price)}/>
              Price:<input type="number" value={inv.price} onChange={e => handleUpdate(inv.id, inv.quantity, +e.target.value)}/>
            </span>
            <button onClick={() => handleDelete(inv.id)}>✖</button>
          </li>
        ))}
      </ul>
    </div>
);
}
