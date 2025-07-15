import { useContext, useState, useEffect } from 'react';
import AuthContext from '../context/AuthContextStore';
import { getProfile, updateProfile } from '../services/api';
import '../styles/Profile.scss';

export default function Profile() {
  const { logout } = useContext(AuthContext);
  const [form, setForm] = useState({ name: '', email: '' });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await getProfile();
        setForm({ name: data.name || '', email: data.email });
      } catch {
        setError('Não foi possível carregar dados.');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  async function handleSave(e) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await updateProfile(form);
      alert('Dados atualizados!');
    } catch {
      setError('Falha ao salvar.');
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <p>Carregando seus dados…</p>;

  return (
    <div className="profile-page container">
      <h1>Minha Conta</h1>
      <form className="profile-form" onSubmit={handleSave}>
        <label>
          Nome
          <input
            type="text"
            value={form.name}
            onChange={e => setForm({ ...form, name: e.target.value })}
            required
          />
        </label>
        <label>
          E‑mail
          <input
            type="email"
            value={form.email}
            onChange={e => setForm({ ...form, email: e.target.value })}
            required
          />
        </label>
        <button type="submit" disabled={saving}>
          {saving ? 'Salvando…' : 'Salvar Alterações'}
        </button>
        {error && <p className="error">{error}</p>}
      </form>
      <button className="btn-logout" onClick={logout}>
        Sair da Conta
      </button>
    </div>
  );
}
