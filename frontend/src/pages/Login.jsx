import { useState, useContext } from 'react';
import { login, getProfile } from '../services/api';
import AuthContext from '../context/AuthContextStore';
import '../styles/Login.scss';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { loginSuccess } = useContext(AuthContext);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const { access_token } = await login(email, password);
      localStorage.setItem('jwt', access_token);
      const profile = await getProfile();
      loginSuccess(access_token, profile);
    } catch {
      setError('E‑mail ou senha inválidos.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit} className="login-form">
        <label>E‑mail<input type="email" value={email} onChange={e => setEmail(e.target.value)} required/></label>
        <label>Senha<input type="password" value={password} onChange={e => setPassword(e.target.value)} required/></label>
        <button type="submit" disabled={loading}>{loading ? 'Entrando…' : 'Entrar'}</button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
);
}
