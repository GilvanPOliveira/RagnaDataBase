import { useState, useEffect, useContext } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { searchItems } from '../services/api';
import AuthContext from '../context/AuthContextStore';
import '../styles/Search.scss';

export default function Search() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  const [name, setName] = useState('');
  const [results, setResults] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const perPage = 20;
  const [quantities, setQuantities] = useState({});

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const term = params.get('name') || '';
    if (term) {
      setName(term);
      setPage(1);
      runSearch(term, 1);
    }
  }, [location.search]);

  async function runSearch(q, pageNumber = 1) {
    setLoading(true);
    setError(null);
    try {
      if (!isNaN(q)) {
        // Busca por ID se for número
        const response = await fetch(`http://localhost:8000/item/${q}`);
        if (!response.ok) throw new Error('Item não encontrado.');
        const item = await response.json();
        setResults([item]);
        setTotal(1);
      } else {
        // Busca por nome com paginação
        const { results, total } = await searchItems(q, pageNumber, perPage);
        setResults(results || []);
        setTotal(total || 0);
      }
    } catch {
      setError('Erro ao buscar itens.');
      setResults([]);
      setTotal(0);
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

  function handleQuantityChange(id, delta) {
    setQuantities(prev => ({
      ...prev,
      [id]: Math.max(0, (prev[id] || 0) + delta)
    }));
  }

  function handleAddToInventory(id) {
    const quantity = quantities[id] || 0;
    alert(`Adicionar ${quantity} unidades do item ${id} ao inventário`);
  }

  function handleAddToList(id) {
    const quantity = quantities[id] || 0;
    alert(`Adicionar ${quantity} unidades do item ${id} à lista`);
  }

  const totalPages = Math.ceil(total / perPage);

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
                  src={`https://static.divine-pride.net/images/items/collection/${item.id}.png`}
                  alt={item.name}
                  loading="lazy"
                  width={64}
                  height={64}
                />
              </Link>
              <div>
                <strong>{item.name}</strong>
                {user && (
                  <div className="quantity-controls">
                    <button onClick={() => handleQuantityChange(item.id, -1)}>-</button>
                    <input
                      type="number"
                      value={quantities[item.id] || 0}
                      onChange={(e) =>
                        setQuantities(prev => ({
                          ...prev,
                          [item.id]: Math.max(0, parseInt(e.target.value) || 0)
                        }))
                      }
                    />
                    <button onClick={() => handleQuantityChange(item.id, 1)}>+</button>
                  </div>
                )}
                {user && (
                  <div className="actions">
                    <button onClick={() => handleAddToInventory(item.id)}>Adicionar ao Inventário</button>
                    <button onClick={() => handleAddToList(item.id)}>Adicionar à Lista</button>
                  </div>
                )}
              </div>
            </li>
          ))
        ) : (
          !loading && <p>Nenhum item encontrado.</p>
        )}
      </ul>

      {totalPages > 1 && (
        <div className="pagination-footer">
          <span>Total de resultados: {total}</span>
          <div className="pagination">
            {Array.from({ length: totalPages }, (_, i) => (
              <button
                key={i + 1}
                onClick={() => handlePageChange(i + 1)}
                disabled={page === i + 1}
              >
                {i + 1}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
