import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getItemById } from '../services/api';
import '../styles/ItemDetail.scss';

export default function ItemDetail() {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await getItemById(id);
        setItem(data);
      } catch {
        setError('Erro ao carregar item.');
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  if (loading) return <p>Carregando…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="item-detail container">
      <h1>{item.name} (#{item.id})</h1>
      <div className="detail-header">
        <img src={item.image_url} alt={item.name} />
        <div className="stats">
          <p><strong>Descrição:</strong> {item.description}</p>
          <p><strong>Preço NPC:</strong> {item.buy_price_npc} / {item.sell_price_npc}</p>
          {item.weapon_level != null && <p><strong>Nível da Arma:</strong> {item.weapon_level}</p>}
          {item.slots != null && <p><strong>Slots:</strong> {item.slots}</p>}
          <p><strong>Equipável por:</strong> {item.equips_jobs.join(', ')}</p>
          <p><strong>Classe:</strong> {item.equips_classes.join(', ')}</p>
        </div>
      </div>
      <section className="sold-by">
        <h2>Vendido por NPCs</h2>
        {item.sold_by.length > 0 ? (
          <ul>{item.sold_by.map((s,i) => (
            <li key={i}>{s.npc_name} ({s.map}) – Preço: {s.price}</li>
          ))}</ul>
        ) : <p>Nenhum NPC vende este item.</p>}
      </section>
      <section className="drops">
        <h2>Dropado por Monstros</h2>
        {item.drops.length > 0 ? (
          <ul>{item.drops.map((d,i) => (
            <li key={i}>{d.monster_name} ({d.map}) – {d.drop_rate}%</li>
          ))}</ul>
        ) : <p>Não há informações de drop.</p>}
      </section>
    </div>
);
}
