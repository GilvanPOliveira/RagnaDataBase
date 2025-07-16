import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  getList,
  getListItems,
  addItemToList,
  removeItemFromList
} from '../services/api';
import '../styles/ListDetail.scss';

export default function ListDetail() {
  const { id } = useParams();
  const [list, setList] = useState(null);
  const [items, setItems] = useState([]);
  const [newItemId, setNewItemId] = useState('');
  const [newQty, setNewQty] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const l = await getList(id);
        const { items: fetchedItems } = await getListItems(id);
        if (isMounted) {
          setList(l);
          setItems(fetchedItems || []);
        }
      } catch {
        if (isMounted) setError('Erro ao carregar lista.');
      } finally {
        if (isMounted) setLoading(false);
      }
    })();
    return () => {
      isMounted = false;
    };
  }, [id]);

  async function handleAdd(e) {
    e.preventDefault();
    try {
      await addItemToList(id, newItemId, newQty);
      setNewItemId('');
      setNewQty(1);
      const { items: refreshed } = await getListItems(id);
      setItems(refreshed || []);
    } catch {
      setError('Erro ao adicionar item.');
    }
  }

  async function handleRemove(liId) {
    try {
      await removeItemFromList(id, liId);
      const { items: refreshed } = await getListItems(id);
      setItems(refreshed || []);
    } catch {
      setError('Erro ao remover item.');
    }
  }

  if (loading) return <p>Carregando…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="list-detail container">
      <h1>{list.title}</h1>
      {list.description && <p className="description">{list.description}</p>}

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
        <button type="submit">Adicionar</button>
      </form>

      {items.length === 0 ? (
        <p>Nenhum item nesta lista.</p>
      ) : (
        <ul className="items-list">
          {items.map(li => (
            <li key={li.id} className="list-item">
              <Link to={`/item/${li.item.id}`} className="item-link">
                <img src={li.item.image_url} alt={li.item.name} />
                <div className="info">
                  <strong>{li.item.name}</strong>
                  <p>Qtd: {li.quantity}</p>
                </div>
              </Link>
              <button
                className="btn-delete"
                onClick={() => handleRemove(li.id)}
              >
                ✖
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
