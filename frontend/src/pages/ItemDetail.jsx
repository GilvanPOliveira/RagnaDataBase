import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/ItemDetail.scss';

export default function ItemDetail() {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchItem() {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://localhost:8000/item/${id}`);
        if (!response.ok) throw new Error('Item não encontrado.');
        const data = await response.json();
        setItem(data);
      } catch {
        setError('Erro ao carregar o item.');
      } finally {
        setLoading(false);
      }
    }
    fetchItem();
  }, [id]);

  if (loading) return <p className="loading">Carregando...</p>;
  if (error) return <p className="error">{error}</p>;
  if (!item) return null;

  return (
    <div className="item-detail container">
      <h1>{item.name}</h1>

      <img
        src={`https://static.divine-pride.net/images/items/collection/${item.id}.png`}
        alt={item.name}
        className="item-image"
        width={96}
        height={96}
      />

      <p className="description">{item.description}</p>

      <ul className="item-info">
        <li>Tipo: {item.type || '-'}</li>
        <li>Categoria: {item.subtype || '-'}</li>
        <li>Força de Ataque: {item.attack || '-'}</li>
        <li>Defesa: {item.defense || '-'}</li>
        <li>Propriedade: {item.property || '-'}</li>
        <li>Peso: {item.weight || '-'}</li>
        <li>Slots: {item.slots || '-'}</li>
        <li>Nível da arma: {item.weapon_level || '-'}</li>
        <li>Nível necessário: {item.required_level || '-'}</li>
        <li>Classes: {item.classes || '-'}</li>
        <li>Preço NPC: {item.npc_price || '-'}</li>
        <li>Adicionado em: {item.added_date || '-'}</li>
      </ul>

      <h2>Vendido por NPC</h2>
      <ul className="sold-by">
        {item.sold_by && item.sold_by.length > 0 ? (
          item.sold_by.map((npc, index) => (
            <li key={index}>
              {npc.name || 'Unknown'} - {npc.map || '-'} - {npc.price || '-'} zeny
            </li>
          ))
        ) : (
          <li>Nenhum NPC encontrado.</li>
        )}
      </ul>
    </div>
  );
}
