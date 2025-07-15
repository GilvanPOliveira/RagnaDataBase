import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from './AuthContextStore';
import { getProfile as fetchProfile } from '../services/api';

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loadingAuth, setLoadingAuth] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('jwt');
    if (!token) {
      setLoadingAuth(false);
      return;
    }
    (async () => {
      try {
        const profile = await fetchProfile();
        // Ajuste conforme seu backend: se vier dentro de { user: {...} }, desestruture abaixo
        const actual = profile.user || profile;
        setUser(actual);
      } catch {
        localStorage.removeItem('jwt');
      } finally {
        setLoadingAuth(false);
      }
    })();
  }, []);

  const loginSuccess = (token, profile) => {
    localStorage.setItem('jwt', token);
    const actual = profile.user || profile;
    setUser(actual);
    navigate('/');
  };

  const logout = () => {
    localStorage.removeItem('jwt');
    setUser(null);
    navigate('/login');
  };

  const updateUserProfile = updated => {
    setUser(updated);
  };

  return (
    <AuthContext.Provider
      value={{ user, loadingAuth, loginSuccess, logout, updateUserProfile }}
    >
      {children}
    </AuthContext.Provider>
  );
}
