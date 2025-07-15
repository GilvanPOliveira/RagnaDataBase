import { useEffect, useState } from 'react';
import {
  getInventoryList,
  addInventoryItem,
  updateInventoryItem,
  deleteInventoryItem,
} from '../services/api';
import '../styles/Inventory.scss';

export default function Inventory() {
  const [items, setItems] = useState([]);
  const [newItemId, setNewItemId] = useState('');
  const [newQty, setNewQty] = useState(1);
  const [newPrice, setNewPrice] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function loadInventory() {
    setLoading(true);
    setError(null);
    try {
      const data = await getInventoryList();
      setItems(data.items || []);
    } catch {
      setError('Falha ao carregar inventário.');
    } finally {
      setLoading(false);
    } 
  }

  useEffect(() => {
    loadInventory();
  }, []);

  async function handleAdd(e) {
    e.preventDefault();
    try {
      await addInventoryItem(newItemId, newQty, newPrice);
      setNewItemId('');
      setNewQty(1);
      setNewPrice(0);
      loadInventory();
    } catch {
      setError('Erro ao adicionar item.');
    }
  }

  async function handleUpdate(id, qty, price) {
    try {
      await updateInventoryItem(id, { quantity: qty, price });
      loadInventory();
    } catch {
      setError('Erro ao atualizar item.');
    }
  }

  async function handleDelete(id) {
    try {
      await deleteInventoryItem(id);
      loadInventory();
    } catch {
      setError('Erro ao remover item.');
    }
  }

  if (loading) return <p>Carregando inventário…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="inventory-page container">
      <h1>Meu Inventário</h1>

      <form className="add-form" onSubmit={handleAdd}>
        <input
          type="text"
          placeholder="ID do item"
          value={newItemId}
          onChange={e => setNewItemId(e.target.value)}
          required
        />
        <input
          type="number"
          min="1"
          placeholder="Quantidade"
          value={newQty}
          onChange={e => setNewQty(+e.target.value)}
          required
        />
        <input
          type="number"
          min="0"
          placeholder="Preço"
          value={newPrice}
          onChange={e => setNewPrice(+e.target.value)}
          required
        />
        <button type="submit">Adicionar</button>
      </form>

      <ul className="inventory-list">
        {items.map(inv => (
          <li key={inv.id} className="inventory-item">
            <span className="info">
              <strong>{inv.item.name}</strong> (#{inv.item.id})
              — Qty: 
              <input
                type="number"
                min="1"
                value={inv.quantity}
                onChange={e => handleUpdate(inv.id, +e.target.value, inv.price)}
              />
              — Price: 
              <input
                type="number"
                min="0"
                value={inv.price}
                onChange={e => handleUpdate(inv.id, inv.quantity, +e.target.value)}
              />
            </span>
            <button className="btn-delete" onClick={() => handleDelete(inv.id)}>
              ✖
            </button>
          </li>
        ))}
      </ul>
    </div>
);
}
