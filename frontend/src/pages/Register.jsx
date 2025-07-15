import { useState } from 'react';
import { register } from '../services/api';
import { useNavigate } from 'react-router-dom';
import '../styles/Register.scss';

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await register(email, password);
      navigate('/login');
    } catch {
      setError('Falha ao cadastrar. Tente outro e‑mail.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="register-page container">
      <h1>Cadastro de Conta</h1>
      <form className="register-form" onSubmit={handleSubmit}>
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
          Senha
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Cadastrando…' : 'Cadastrar'}
        </button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}
