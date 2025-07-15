import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../context/AuthContextStore';
import '../styles/Navbar.scss';

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);

  // Admin único baseado no email configurado
  const isAdmin = user?.email === 'admin@admin.com';

  return (
    <nav className="navbar">
      <Link to="/" className="logo">RagnaDB</Link>
      <div className="links">
        <Link to="/search">Buscar</Link>
        {user ? (
          <>
            <Link to="/inventory">Inventário</Link>
            <Link to="/lists">Listas</Link>
            <Link to="/account">Conta</Link>
            {isAdmin && <Link to="/admin/users">Gerenciar Usuários</Link>}
            <button onClick={logout}>Sair</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Cadastro</Link>
          </>
        )}
      </div>
    </nav>
  );
}
