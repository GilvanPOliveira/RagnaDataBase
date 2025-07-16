import { useState, useEffect, useContext } from 'react';
import {
  getAllUsers,
  updateUserById,
  deleteUserById,
  setUserAdminStatus
} from '../services/api';
import AuthContext from '../context/AuthContextStore';
import '../styles/AdminUsers.scss';

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState({ name: '', email: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user: currentUser } = useContext(AuthContext);

  const loadUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const raw = await getAllUsers();
      setUsers(raw.map(u => ({
        id: u.id,
        name: u.name,
        email: u.email,
        is_admin: Boolean(u.is_admin)
      })));
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

  const startEdit = u => {
    setEditingId(u.id);
    setForm({ name: u.name, email: u.email });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setForm({ name: '', email: '' });
  };

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

  const toggleAdmin = async u => {
    if (u.id === 1) return;
    try {
      await setUserAdminStatus(u.id, !u.is_admin);
      await loadUsers();
    } catch (e) {
      console.error('toggleAdmin error', e);
      setError('Erro ao alterar privilégio de admin.');
    }
  };

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
  if (error) return <p className="error">{error}</p>;

return (
  <div className="admin-users-page container">
    <h1>Gerenciar Usuários</h1>
    <table className="users-table">
      <thead>
        <tr>
          <th>Nome</th>
          <th>E-mail</th>
          <th>Permissões</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {users.map(u => (
          <tr key={u.id}>
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
                u.is_admin
                  ? <span className="badge-admin">Admin</span>
                  : <span className="badge-user">Usuário</span>
              )}
            </td>
            <td className="actions">
              {editingId === u.id ? (
                <>
                  <button onClick={() => saveEdit(u.id)}>✔️</button>
                  <button onClick={cancelEdit}>✖️</button>
                </>
              ) : (
                <>
                  
                  {u.id !== 1 && (
                    <button onClick={() => startEdit(u)}>✏️</button>
                  )}
                  {currentUser.id === 1 && u.id !== 1 && (
                    <button
                      className={u.is_admin ? "btn-remove-admin" : "btn-promote"}
                      onClick={() => toggleAdmin(u)}
                    >
                      {u.is_admin ? "⚔️" : "👑"}
                    </button>
                  )}

                  {u.id !== 1 && (
                    <button
                      className="btn-delete"
                      onClick={() => handleDelete(u.id)}
                    >
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
