// src/pages/Home.jsx
import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../context/AuthContextStore';
import '../styles/Home.scss';

export default function Home() {
  const { user } = useContext(AuthContext);

  // único admin pelo e‑mail
  const isAdmin = user?.email === 'admin@admin.com';

  return (
    <div className="home-page container">
      <div className="hero">
        <h1>Bem‑vindo ao RagnaDataBase</h1>
        <p>Encontre, organize e gerencie seus itens de forma prática.</p>
      </div>
      <nav className="home-nav">
        <Link to="/search" className="card">
          🔍 <span>Buscar Itens</span>
        </Link>
        {user ? (
          <>
            <Link to="/inventory" className="card">
              🎒 <span>Meu Inventário</span>
            </Link>
            <Link to="/lists" className="card">
              📋 <span>Minhas Listas</span>
            </Link>
            <Link to="/account" className="card">
              👤 <span>Minha Conta</span>
            </Link>
            {isAdmin && (
              <Link to="/admin/users" className="card admin-card">
                ⚙️ <span>Gerenciar Usuários</span>
              </Link>
            )}
          </>
        ) : (
          <>
            <Link to="/login" className="card">
              🔑 <span>Login</span>
            </Link>
            <Link to="/register" className="card">
              ✍️ <span>Cadastro</span>
            </Link>
          </>
        )}
      </nav>
    </div>
);
}
