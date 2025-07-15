import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from './AuthContextStore';
import { getProfile } from '../services/api';

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
        const profile = await getProfile();
        setUser(profile);
      } catch {
        localStorage.removeItem('jwt');
      } finally {
        setLoadingAuth(false);
      }
    })();
  }, []);

  const loginSuccess = (token, profile) => {
    localStorage.setItem('jwt', token);
    setUser(profile);
    navigate('/');
  };

  const logout = () => {
    localStorage.removeItem('jwt');
    setUser(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loadingAuth, loginSuccess, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
