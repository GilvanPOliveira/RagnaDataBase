// src/pages/AdminUsers.jsx
import React, { useState, useEffect } from 'react';
import {
  getAllUsers,
  updateUserById,
  deleteUserById
} from '../services/api';
import '../styles/AdminUsers.scss';

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({ name: '', email: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carrega e normaliza lista de usuários, garantindo que is_admin exista
  const loadUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllUsers();
      const raw = Array.isArray(data) ? data : data.users || [];
      // Se o backend usar outro campo, adicione aqui: u.isAdmin ?? u.admin
      const list = raw.map(u => ({
        ...u,
        is_admin: Boolean(u.is_admin),
      }));
      setUsers(list);
    } catch (e) {
      console.error('loadUsers error', e);
      setError('Falha ao carregar usuários.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  // Inicia edição inline de nome e e‑mail
  const startEdit = u => {
    setEditingId(u.id);
    setForm({ name: u.name, email: u.email });
  };

  // Cancela edição
  const cancelEdit = () => {
    setEditingId(null);
    setForm({ name: '', email: '' });
  };

  // Salva alterações de nome e e‑mail
  const saveEdit = async id => {
    try {
      await updateUserById(id, form);
      await loadUsers();
      cancelEdit();
    } catch (e) {
      console.error('saveEdit error', e);
      setError('Erro ao salvar alterações.');
    }
  };

  // Alterna permissão de admin via PATCH /users/{id}
  const toggleAdmin = async u => {
    if (u.id === 1) return; // super‑admin imune
    try {
      await updateUserById(u.id, { is_admin: !u.is_admin });
      await loadUsers();
    } catch (e) {
      console.error('toggleAdmin error', e);
      setError('Erro ao alterar permissão de admin.');
    }
  };

  // Exclui usuário (exceto super‑admin)
  const handleDelete = async id => {
    if (id === 1) return;
    if (!window.confirm('Excluir este usuário?')) return;
    try {
      await deleteUserById(id);
      await loadUsers();
    } catch (e) {
      console.error('handleDelete error', e);
      setError('Erro ao excluir usuário.');
    }
  };

  if (loading) return <p>Carregando usuários…</p>;
  if (error)   return <p className="error">{error}</p>;

  return (
    <div className="admin-users-page container">
      <h1>Gerenciar Usuários</h1>
      <table className="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>E‑mail</th>
            <th>Admin?</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>

              <td>
                {editingId === u.id ? (
                  <input
                    type="text"
                    value={form.name}
                    onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
                  />
                ) : (
                  u.name
                )}
              </td>

              <td>
                {editingId === u.id ? (
                  <input
                    type="email"
                    value={form.email}
                    onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
                  />
                ) : (
                  u.email
                )}
              </td>

              <td>
                {u.id === 1 ? (
                  <span className="badge-admin">Super Admin</span>
                ) : (
                  <button
                    className={`btn-admin-toggle ${u.is_admin ? 'admin' : 'user'}`}
                    onClick={() => toggleAdmin(u)}
                  >
                    {u.is_admin ? 'Despromover' : 'Tornar Admin'}
                  </button>
                )}
              </td>

              <td className="actions">
                {editingId === u.id ? (
                  <>
                    <button onClick={() => saveEdit(u.id)}>💾</button>
                    <button onClick={cancelEdit}>✖️</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => startEdit(u)}>✏️</button>
                    {u.id !== 1 && (
                      <button className="btn-delete" onClick={() => handleDelete(u.id)}>
                        🗑️
                      </button>
                    )}
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
