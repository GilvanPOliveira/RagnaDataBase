import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContextStore';
import '../styles/Home.scss';

import logoIcon from '../assets/logo.png';
import inventoryIcon from '../assets/inventory.png';
import listsIcon from '../assets/lists.png';
import profileIcon from '../assets/status.png';
import adminIcon from '../assets/config.png';

export default function Home() {
  const { user } = useContext(AuthContext);
  const isAdmin = Boolean(user?.is_admin) || user?.id === 1;
  const [name, setName] = useState('');
  const navigate = useNavigate();

  function onSearch(e) {
    e.preventDefault();
    const q = name.trim();
    if (!q) return;
    navigate(`/search?name=${encodeURIComponent(q)}`);
  }

  return (
    <div className="home-page container">
      <div className="hero">
        <img src={logoIcon} alt="RagnaDataBase" className="logo" />
        <h1>Bem-vindo ao RagnaDataBase</h1>
        <p>Encontre, organize e gerencie seus itens de forma prática.</p>

        <form className="home-search" onSubmit={onSearch}>
          <input
            type="text"
            placeholder="Digite o nome do item"
            value={name}
            onChange={e => setName(e.target.value)}
          />
          <button type="submit">Buscar</button>
        </form>
      </div>

      {user && (
        <nav className="home-nav">
          <LinkCard to="/inventory" icon={inventoryIcon} label="Meu Inventário" />
          <LinkCard to="/lists"     icon={listsIcon}     label="Minhas Listas" />
          <LinkCard to="/account"   icon={profileIcon}   label="Minha Conta" />
          {isAdmin && (
            <LinkCard to="/admin/users" icon={adminIcon} label="Gerenciar Usuários" admin />
          )}
        </nav>
      )}
    </div>
  )
}

function LinkCard({ to, icon, label, admin }) {
  return (
    <a href={to} className={`card${admin ? ' admin-card' : ''}`}>
      <img src={icon} alt={label} className="card-icon" />
      <span>{label}</span>
    </a>
  );
}
