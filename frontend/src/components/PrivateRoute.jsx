import { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import AuthContext from '../context/AuthContextStore';

export default function PrivateRoute() {
  const { user, loadingAuth } = useContext(AuthContext);

  if (loadingAuth) return <p>Carregando autenticação…</p>;
  if (!user) return <Navigate to="/login" replace />;

  return <Outlet />;
}
