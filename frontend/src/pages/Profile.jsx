// src/pages/Profile.jsx
import React, { useContext, useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import AuthContext from '../context/AuthContextStore';
import { updateProfile, deleteAccount } from '../services/api';
import '../styles/Profile.scss';

export default function Profile() {
  const { user, loadingAuth, logout, updateUserProfile } = useContext(AuthContext);

  // Hooks no topo
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [deletePassword, setDeletePassword] = useState('');
  const [deleting, setDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState(null);

  // Preenche com dados atuais
  useEffect(() => {
    if (!loadingAuth && user) {
      setName(user.name || '');
      setEmail(user.email || '');
    }
  }, [loadingAuth, user]);

  if (loadingAuth) return <p>Carregando perfil…</p>;
  if (!user) return <Navigate to="/login" replace />;

  const initials = (user.name || '')
    .split(' ')
    .map(w => w[0])
    .join('')
    .slice(0, 2)
    .toUpperCase() || 'U';

  // Salvar alterações de perfil
  async function handleSave(e) {
    e.preventDefault();
    setSaving(true);
    setError(null);

    const payload = {};
    if (name !== user.name) payload.name = name;
    if (email !== user.email) payload.email = email;

    // Se trocar senha, exige senha atual
    if (newPassword.trim()) {
      if (!currentPassword.trim()) {
        setError('Informe sua senha atual para alterar a senha.');
        setSaving(false);
        return;
      }
      payload.current_password = currentPassword;
      payload.new_password = newPassword;
    }

    if (!Object.keys(payload).length) {
      alert('Nenhuma alteração para salvar.');
      setSaving(false);
      return;
    }

    try {
      const updated = await updateProfile(payload);
      updateUserProfile(updated);
      setCurrentPassword('');
      setNewPassword('');
      alert('Dados atualizados com sucesso!');
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao salvar alterações.');
    } finally {
      setSaving(false);
    }
  }

  // Excluir conta
  async function handleDelete(e) {
    e.preventDefault();
    if (!deletePassword.trim()) {
      setDeleteError('Informe sua senha para excluir a conta.');
      return;
    }
    if (!window.confirm('Tem certeza? Esta ação é irreversível.')) return;

    setDeleting(true);
    setDeleteError(null);

    try {
      await deleteAccount(deletePassword);
      alert('Conta excluída com sucesso.');
      logout();
    } catch (err) {
      setDeleteError(err.response?.data?.detail || 'Erro ao excluir conta.');
    } finally {
      setDeleting(false);
    }
  }

  return (
    <div className="profile-page container">
      <div className="profile-header">
        <div className="avatar">{initials}</div>
        <div className="user-info">
          <h1>{user.name}</h1>
          <p>{user.email}</p>
        </div>
      </div>

      <div className="profile-content">
        {/* Editar Perfil */}
        <section className="card edit-card">
          <h2>Editar Perfil</h2>
          <form onSubmit={handleSave}>
            <label>
              Nome
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                required
              />
            </label>

            <label>
              E‑mail
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
              />
            </label>

            <label>
              Senha Atual (necessária para trocar senha)
              <input
                type="password"
                value={currentPassword}
                onChange={e => setCurrentPassword(e.target.value)}
                placeholder="Sua senha atual"
              />
            </label>

            <label>
              Nova Senha
              <input
                type="password"
                value={newPassword}
                onChange={e => setNewPassword(e.target.value)}
                placeholder="Deixe em branco para manter"
              />
            </label>

            <button type="submit" disabled={saving}>
              {saving ? 'Salvando…' : 'Salvar Alterações'}
            </button>
            {error && <p className="error">{error}</p>}
          </form>
        </section>

        {/* Excluir Conta */}
        <section className="card delete-card">
          <h2>Excluir Conta</h2>
          <p className="warning">
            Esta ação é irreversível. Todos os seus dados serão apagados.
          </p>
          <form onSubmit={handleDelete}>
            <label>
              Senha Atual
              <input
                type="password"
                value={deletePassword}
                onChange={e => setDeletePassword(e.target.value)}
                placeholder="Digite sua senha"
                required
              />
            </label>
            <button type="submit" disabled={deleting}>
              {deleting ? 'Excluindo…' : 'Excluir Conta'}
            </button>
            {deleteError && <p className="error">{deleteError}</p>}
          </form>
        </section>
      </div>
    </div>
  );
}
