import { Link } from 'react-router-dom';
import "../styles/Home.scss"

export default function Home() {
  return (
    <div className="container">
      <h1>RagnaDataBase</h1>
 
      <nav>
        <ul className="nav-list">
          <li><Link to="/search">🔍 Buscar Itens</Link></li>
          <li><Link to="/inventory">🎒 Meu Inventário</Link></li>
          <li><Link to="/lists">📋 Minhas Listas</Link></li>
          <li><Link to="/login">🔑 Login</Link></li>
        </ul>
      </nav>
    </div>
  );
}
