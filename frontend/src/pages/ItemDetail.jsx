import { useEffect, useState } from "react";
import { useParams, useLocation, Link } from "react-router-dom";
import { api } from "../services/api";
import { BRANCHES, iconUrl, allowedIdSet } from "../utils/classIcons";

import "../styles/ItemDetail.scss";

export default function ItemDetail() {
  const { id } = useParams();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const term = queryParams.get("term");

  const [item, setItem] = useState(null);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    api.get(`/item/${id}`).then((res) => setItem(res.data));
  }, [id]);

  if (!item) return <p className="loading">Carregando…</p>;

  const allowedIds = allowedIdSet(item);

  return (
    <div className="item-detail">
      <div className="card">
        <h1 className="title">
          {item.image_icon && (
            <img src={item.image_icon} alt={item.name} className="item-icon" />
          )}
          {item.name || `Item ${item.id}`}{" "}
          <span className="item-id">#{item.id}</span>
        </h1>

        <div className="item-content">
          <div className="item-image">
            {item.image_collection && (
              <img
                src={item.image_collection}
                alt=""
                className="collection-img"
              />
            )}
          </div>
          <div className="item-info">
            <p className="description">{item.description}</p>
            <p className="details">
              Peso: {item.weight || "?"} | Slots: {item.slots || "?"} | Ataque:{" "}
              {item.attack || "?"}
            </p>

            <div className="actions">
              <div className="quantity">
                <button onClick={() => setQuantity((q) => Math.max(1, q - 1))}>-</button>
                <span>{quantity}</span>
                <button onClick={() => setQuantity((q) => q + 1)}>+</button>
              </div>
              <button className="btn">Adicionar ao Inventário</button>
              <button className="btn">Adicionar à Lista</button>
            </div>
          </div>
        </div>

        <div className="job-grid">
          <h2>Classes que podem equipar:</h2>
          <table>
            <tbody>
              {BRANCHES[0].stages.map((_, rowIdx) => (
                <tr key={rowIdx}>
                  {BRANCHES.map((br) => (
                    <td key={br.key} className="job-cell">
                      <div className="job-icons">
                        {br.stages[rowIdx].map(({ id, name }) => {
                          const enabled = allowedIds.has(id);
                          return (
                            <div key={id} className="job-icon-wrapper">
                              <img
                                src={iconUrl(id, enabled)}
                                alt={name}
                                title={name}
                                className={`job-icon ${enabled ? "" : "disabled"}`}
                              />
                              <span className="job-label">{name}</span>
                            </div>
                          );
                        })}
                      </div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <Link to={`/search?term=${term || ""}`} className="back-link">
          ← Voltar
        </Link>
      </div>
    </div>
  );
}
