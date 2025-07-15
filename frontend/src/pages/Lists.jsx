// src/pages/Lists.jsx
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getLists, createList, deleteList } from '../services/api';
import '../styles/Lists.scss';

export default function Lists() {
  const [lists, setLists] = useState([]);
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const { lists } = await getLists();
      setLists(lists || []);
    } catch {
      setError('Erro ao carregar listas.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  async function handleCreate(e) {
    e.preventDefault();
    try {
      await createList(title, desc);
      setTitle(''); setDesc('');
      load();
    } catch {
      setError('Erro ao criar lista.');
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Remover?')) return;
    try {
      await deleteList(id);
      load();
    } catch {
      setError('Erro ao remover.');
    }
  }

  if (loading) return <p>Carregando…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="lists-page container">
      <h1>Minhas Listas</h1>
      <form onSubmit={handleCreate} className="create-form">
        <input placeholder="Título" value={title} onChange={e => setTitle(e.target.value)} required/>
        <input placeholder="Descrição" value={desc} onChange={e => setDesc(e.target.value)}/>
        <button type="submit">Criar</button>
      </form>
      <ul className="lists-list">
        {lists.map(l => (
          <li key={l.id}>
            <Link to={`/lists/${l.id}`}>{l.title}</Link>
            <button onClick={() => handleDelete(l.id)}>✖</button>
          </li>
        ))}
      </ul>
    </div>
);
}
