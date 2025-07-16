import { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import AuthContext from '../context/AuthContextStore';

export default function AdminRoute() {
  const { user, loadingAuth } = useContext(AuthContext);

  if (loadingAuth) return <p>Carregando…</p>;
  if (!user) return <Navigate to="/login" replace />;

  if (!user.is_admin && user.id !== 1) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
