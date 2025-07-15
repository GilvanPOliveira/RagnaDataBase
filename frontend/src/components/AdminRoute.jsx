import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import AuthContext from '../context/AuthContextStore';

export default function AdminRoute() {
  const { user, loadingAuth } = useContext(AuthContext);

  if (loadingAuth) return <p>Carregando…</p>;
  if (!user) return <Navigate to="/login" replace />;

  // Mesma lógica do Navbar
  if (user.email !== 'admin@admin.com') {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
