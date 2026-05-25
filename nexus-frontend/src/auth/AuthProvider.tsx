import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AuthContextType {
  isAuth: boolean;
  loading: boolean;
  user: any | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuth, setIsAuth] = useState(false);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState<any>(null);

  const login = async (email: string, password: string) => {
    setLoading(true);
    // Simular petición a API
    await new Promise(resolve => setTimeout(resolve, 500));
    // Acepta cualquier credencial por ahora
    setIsAuth(true);
    setUser({ email, name: email.split('@')[0] });
    setLoading(false);
  };

  const logout = () => {
    setIsAuth(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ isAuth, loading, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};