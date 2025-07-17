import { useState, useEffect } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { searchItems, getItemById } from '../services/api';
import '../styles/Search.scss';

export default function Search() {
  const location = useLocation();
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const term = params.get('name') || '';
    if (term) {
      setName(term);
      setPage(1);
      runSearch(term, 1);
    }
  }, [location.search]);

  async function runSearch(q, pageNumber) {
    setLoading(true);
    setError(null);
    try {
      if (/^\d+$/.test(q)) {
        const item = await getItemById(q);
        setResults(item ? [item] : []);
        setTotalPages(1);
      } else {
        const { results, total } = await searchItems(q, pageNumber, 20);
        setResults(results || []);
        setTotalPages(Math.ceil((total || 0) / 20));
      }
    } catch {
      setError('Erro ao buscar itens.');
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    const q = name.trim();
    if (!q) return;
    navigate(`/search?name=${encodeURIComponent(q)}`);
  }

  function handlePageChange(newPage) {
    setPage(newPage);
    runSearch(name, newPage);
  }

  return (
    <div className="search-page container">
      <h1>Buscar Itens</h1>
      <form className="search-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Digite o nome ou ID do item"
          value={name}
          onChange={e => setName(e.target.value)}
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

      {totalPages > 1 && (
        <div className="pagination">
          <button
            disabled={page === 1 || loading}
            onClick={() => handlePageChange(page - 1)}
          >
            Página Anterior
          </button>
          <span>Página {page} de {totalPages}</span>
          <button
            disabled={page === totalPages || loading}
            onClick={() => handlePageChange(page + 1)}
          >
            Próxima Página
          </button>
        </div>
      )}
    </div>
  );
}
