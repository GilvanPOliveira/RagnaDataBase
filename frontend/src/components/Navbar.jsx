import { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import AuthContext from '../context/AuthContextStore';
import '../styles/Navbar.scss';

import searchIcon from '../assets/items.png';      
import inventoryIcon from '../assets/inventory.png'; 
import listsIcon from '../assets/lists.png';      
import profileIcon from '../assets/status.png';   
import adminIcon from '../assets/config.png';     
import logoutIcon from '../assets/logout.png';    
import loginIcon from '../assets/login.png';      
import registerIcon from '../assets/register.png';
import logoIcon from '../assets/ragnadatabase.png';


export default function Navbar() {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav className="navbar container">
      <NavLink to="/" className="navbar-brand">
        <img src={logoIcon} alt="RagnaDataBase" className="nav-brand-icon" title='RagnaDataBase' />
      </NavLink>

      <div className="navbar-links">
        {user ? (
          <>
            <NavLink to="/search" className="nav-link">
              <img src={searchIcon} alt="Buscar Itens" title="Buscar Itens" className="nav-icon" />
            </NavLink>
            <NavLink to="/inventory" className="nav-link">
              <img src={inventoryIcon} alt="Inventário"  title="Inventário" className="nav-icon" />
            </NavLink>
            <NavLink to="/lists" className="nav-link">
              <img src={listsIcon} alt="Listas"  title="Listas" className="nav-icon" />
            </NavLink>

            <NavLink to="/account" className="nav-link">
              <img src={profileIcon} alt="Minha Conta"  title="Minha Conta" className="nav-icon" />
            </NavLink>

            {user.is_admin && (
              <NavLink to="/admin/users" className="nav-link">
                <img src={adminIcon} alt="Gerenciar Usuários" title="Gerenciar Usuários" className="nav-icon" />
              </NavLink>
            )}

            <button onClick={logout} className="nav-button">
              <img src={logoutIcon} alt="Sair" title="Sair" className="nav-icon" />
            </button>
          </>
        ) : (
          <>
            <NavLink to="/login" className="nav-link">
              <img src={loginIcon} alt="Login" title="Login" className="nav-icon" />
            </NavLink>
            <NavLink to="/register" className="nav-link">
              <img src={registerIcon} alt="Cadastro" title="Cadastro"  className="nav-icon" />
            </NavLink>
          </>
        )}
      </div>
    </nav>
  );
}
