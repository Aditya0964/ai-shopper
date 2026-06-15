import { Link, useNavigate } from 'react-router-dom'
import useAuthStore from '../store/authStore'

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-gray-900 text-white px-6 py-4 flex items-center justify-between sticky top-0 z-50">
      <Link to="/" className="text-xl font-bold text-blue-400">
        🛍️ AI Shopper
      </Link>

      <div className="flex items-center gap-6">
        <Link to="/" className="hover:text-blue-400 transition">Home</Link>

        {isAuthenticated ? (
          <>
            <Link to="/cart" className="hover:text-blue-400 transition">🛒 Cart</Link>
            <Link to="/orders" className="hover:text-blue-400 transition">Orders</Link>
            <span className="text-gray-400 text-sm">{user?.name || 'User'}</span>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-sm transition"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:text-blue-400 transition">Login</Link>
            <Link
              to="/register"
              className="bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded text-sm transition"
            >
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}