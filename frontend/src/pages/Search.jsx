import { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { searchItems } from '../services/api';
import '../styles/Search.scss';

export default function Search() {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const initialTerm = params.get('term') || '';

  const [term, setTerm] = useState(initialTerm);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (initialTerm) runSearch(initialTerm);
  }, [initialTerm]);

  async function runSearch(q) {
    setLoading(true);
    setError(null);
    try {
      const { results } = await searchItems(q, 1, 20);
      setResults(results || []);
    } catch {
      setError('Erro ao buscar itens.');
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    const q = term.trim();
    if (!q) return;
    runSearch(q);
  }

  return (
    <div className="search-page container">
      <h1>Buscar Itens</h1>
      <form className="search-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Digite o nome do item"
          value={term}
          onChange={e => setTerm(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Buscando…' : 'Buscar'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      <ul className="results-list">
        {results.length > 0 ? (
          results.map(item => (
            <li key={item.id} className="result-item">
              <Link to={`/item/${item.id}`}>
                <img
                  src={`https://static.divine-pride.net/images/items/item/${item.id}.png`}
                  alt={item.name}
                  loading="lazy"
                  width={64}
                  height={64}
                />
                <div>
                  <strong>{item.name}</strong>
                  <p>Preço NPC: -- </p>
                </div>
              </Link>
            </li>
          ))
        ) : (
          !loading && <p>Nenhum item encontrado.</p>
        )}
      </ul>
    </div>
  );
}
