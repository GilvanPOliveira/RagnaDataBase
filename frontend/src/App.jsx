import { Routes, Route, Navigate } from 'react-router-dom';
import AuthProvider from './context/AuthProvider';
import PrivateRoute from './components/PrivateRoute';
import Navbar from './components/Navbar';

import Home from './pages/Home';
import Login from './pages/Login';
import Search from './pages/Search';
import ItemDetail from './pages/ItemDetail';
import Inventory from './pages/Inventory';
import Lists from './pages/Lists';
import ListDetail from './pages/ListDetail';
import Register from './pages/Register';
import Profile  from './pages/Profile';

export default function App() {
  return (
    <AuthProvider>
      <Navbar />
      <Routes>
        {/* públicas */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* privadas */}
        <Route element={<PrivateRoute />}>
          <Route path="/search" element={<Search />} />
          <Route path="/item/:id" element={<ItemDetail />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/lists" element={<Lists />} />
          <Route path="/lists/:id" element={<ListDetail />} />
          <Route path="/account"   element={<Profile />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
);
}
