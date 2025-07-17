import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../services/api";
import {
  BRANCHES,
  iconUrl,
} from "../utils/classIcons";
import "../styles/ItemDetail.scss";

/* ---------- mapa ID → ramo ---------- */
const ID_TO_BRANCH = (() => {
  const m = new Map();
  BRANCHES.forEach((br) =>
    br.stages.flat().forEach((id) => id !== undefined && m.set(id, br.key))
  );
  return m;
})();

export default function ItemDetail() {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    api
      .get(`/item/${id}`)
      .then((r) => setItem(r.data))
      .catch(() => setItem(null))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p className="loading">Carregando…</p>;
  if (!item) return <p className="no-results">Item não encontrado.</p>;

  const allowedIds = new Set(item.allowed_classes ?? []);

  return (
    <div className="item-detail-page">
      <h1 className="item-title">
        <img src={item.image_icon} alt="" className="item-icon" />
        {item.name} <span className="item-id">#{item.id}</span>
      </h1>

      <div className="item-body">
        <div className="item-info">
          <p>{item.description}</p>
          <ul className="item-stats">
            <li>Peso: {item.weight}</li>
            <li>Slots: {item.slots}</li>
            <li>Ataque: {item.attack}</li>
            <li>Defesa: {item.defense ?? "-"}</li>
            <li>Nível Necessário: {item.requiredLevel ?? "-"}</li>
            <li>Preço NPC: {item.price ?? "-"}</li>
          </ul>
        </div>

        <table className="job-grid">
          <tbody>
            {BRANCHES[0].stages.map((_, rowIdx) => (
              <tr key={rowIdx}>
                {BRANCHES.map((br) => (
                  <td key={br.key} className="job-cell">
                    <div className="job-cell-icons">
                      {br.stages[rowIdx].map((iconId) => {
                        const enabled = allowedIds.has(iconId);
                        return (
                          <img
                            key={iconId}
                            src={iconUrl(iconId, enabled)}
                            className={enabled ? "job-icon" : "job-icon disabled"}
                            title={br.pt}
                            alt=""
                          />
                        );
                      })}
                    </div>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>

        {item.image_collection && (
          <img src={item.image_collection} alt="" className="collection-img" />
        )}
      </div>

      <Link to="/" className="back-link">← Voltar</Link>
    </div>
  );
}
