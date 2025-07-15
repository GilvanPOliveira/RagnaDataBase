// src/pages/Register.jsx
import React, { useState } from 'react';
import { register } from '../services/api';
import { useNavigate } from 'react-router-dom';
import '../styles/Register.scss';

export default function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // agora passamos name, email e password
      await register(name, email, password);
      navigate('/login');
    } catch (err) {
      console.error(err.response || err);
      setError(
        err.response?.data?.detail ||
        'Falha ao cadastrar. Verifique seus dados.'
      );
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
            placeholder="Seu nome completo"
            required
          />
        </label>
        <label>
          E‑mail
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="email@exemplo.com"
            required
          />
        </label>
        <label>
          Senha
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="Mínimo 6 caracteres"
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
