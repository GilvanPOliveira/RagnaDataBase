import { useState } from 'react';
import { searchItems } from '../services/api';
import { Link } from 'react-router-dom';
import '../styles/Search.scss';

export default function Search() {
  const [term, setTerm] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSearch(e) {
    e.preventDefault();
    if (!term.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await searchItems(term, 1, 20);
      setResults(data.items || []);
    } catch {
      setError('Erro ao buscar itens.');
    } finally {
      setLoading(false);
    }
  }
 
  return (
    <div className="search-page container">
      <h1>Buscar Itens</h1>

      <form className="search-form" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Digite o nome do item"
          value={term}
          onChange={e => setTerm(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Buscando…' : 'Buscar'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      <ul className="results-list">
        {results.map(item => (
          <li key={item.id} className="result-item">
            <Link to={`/item/${item.id}`}>
              <img src={item.image_url} alt={item.name} />
              <div>
                <strong>{item.name}</strong>
                <p>Preço NPC: {item.sell_price_npc}</p>
              </div>
            </Link>
          </li>
        ))}
      </ul>

      {results.length === 0 && !loading && (
        <p>Nenhum item encontrado. Tente outro termo.</p>
      )}
    </div>
);
}
