import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './AuthProvider';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';

export default function ProtectedRoute() {
  const { isAuth, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner fullscreen label="Verifying session..." />;
  }

  return isAuth ? <Outlet /> : <Navigate to="/login" replace />;
}