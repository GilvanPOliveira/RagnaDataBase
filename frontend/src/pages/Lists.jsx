import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  getLists,
  createList,
  deleteList
} from '../services/api';
import '../styles/Lists.scss';

export default function Lists() {
  const [lists, setLists] = useState([]);
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function loadLists() {
    setLoading(true);
    setError(null);
    try {
      const data = await getLists();
      setLists(data.lists || []);
    } catch {
      setError('Falha ao carregar listas.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadLists();
  }, []);

  async function handleCreate(e) {
    e.preventDefault();
    if (!newTitle.trim()) return;
    try {
      await createList(newTitle, newDesc);
      setNewTitle('');
      setNewDesc('');
      loadLists();
    } catch {
      setError('Erro ao criar lista.');
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Remover esta lista?')) return;
    try {
      await deleteList(id);
      loadLists();
    } catch {
      setError('Erro ao remover lista.');
    }
  }

  if (loading) return <p>Carregando listas…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="lists-page container">
      <h1>Minhas Listas</h1>

      <form className="create-form" onSubmit={handleCreate}>
        <input
          type="text"
          placeholder="Título da lista"
          value={newTitle}
          onChange={e => setNewTitle(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Descrição (opcional)"
          value={newDesc}
          onChange={e => setNewDesc(e.target.value)}
        />
        <button type="submit">Criar Lista</button>
      </form>

      {lists.length === 0 ? (
        <p>Nenhuma lista criada ainda.</p>
      ) : (
        <ul className="lists-list">
          {lists.map(lst => (
            <li key={lst.id} className="list-item">
              <Link to={`/lists/${lst.id}`}>
                <strong>{lst.title}</strong>
                {lst.description && <p>{lst.description}</p>}
              </Link>
              <button
                className="btn-delete"
                onClick={() => handleDelete(lst.id)}
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