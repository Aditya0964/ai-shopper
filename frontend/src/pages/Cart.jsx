import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

export default function Cart() {
  const [cart, setCart] = useState([])
  const [loading, setLoading] = useState(true)
  const [placing, setPlacing] = useState(false)
  const [message, setMessage] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchCart()
  }, [])

  const fetchCart = async () => {
    try {
      const { data } = await api.get('/cart/')
      setCart(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleRemove = async (itemId) => {
    try {
      await api.delete(`/cart/${itemId}`)
      setCart(cart.filter(item => item.id !== itemId))
    } catch (err) {
      console.error(err)
    }
  }

  const handleUpdateQuantity = async (itemId, quantity) => {
    try {
      await api.put(`/cart/${itemId}?quantity=${quantity}`)
      if (quantity <= 0) {
        setCart(cart.filter(item => item.id !== itemId))
      } else {
        setCart(cart.map(item =>
          item.id === itemId
            ? { ...item, quantity, subtotal: item.product_price * quantity }
            : item
        ))
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handlePlaceOrder = async () => {
    setPlacing(true)
    try {
      await api.post('/orders/')
      setCart([])
      setMessage('Order placed successfully!')
      setTimeout(() => navigate('/orders'), 2000)
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Failed to place order')
    } finally {
      setPlacing(false)
    }
  }

  const total = cart.reduce((sum, item) => sum + item.subtotal, 0)

  if (loading) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
      Loading cart...
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-950 text-white px-6 py-10">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold mb-8">Your Cart</h1>

        {message && (
          <div className={`px-4 py-3 rounded-lg mb-6 text-sm ${message.includes('success') ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`}>
            {message}
          </div>
        )}

        {cart.length === 0 ? (
          <div className="text-center text-gray-400 py-20">
            <p className="text-lg mb-4">Your cart is empty</p>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg transition"
            >
              Continue Shopping
            </button>
          </div>
        ) : (
          <>
            <div className="space-y-4 mb-8">
              {cart.map(item => (
                <div key={item.id} className="bg-gray-900 rounded-xl p-4 flex items-center gap-4">
                  {/* Image */}
                  <img
                    src={item.image_url || 'https://via.placeholder.com/80'}
                    alt={item.product_name}
                    className="w-20 h-20 object-contain bg-gray-800 rounded-lg"
                    onError={(e) => { e.target.src = 'https://via.placeholder.com/80' }}
                  />

                  {/* Details */}
                  <div className="flex-1">
                    <h3 className="text-sm font-medium line-clamp-2">{item.product_name}</h3>
                    <p className="text-blue-400 font-bold mt-1">₹{item.product_price}</p>
                  </div>

                  {/* Quantity controls */}
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                      className="bg-gray-800 hover:bg-gray-700 w-8 h-8 rounded-lg transition"
                    >
                      -
                    </button>
                    <span className="w-8 text-center">{item.quantity}</span>
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                      className="bg-gray-800 hover:bg-gray-700 w-8 h-8 rounded-lg transition"
                    >
                      +
                    </button>
                  </div>

                  {/* Subtotal */}
                  <div className="text-right min-w-20">
                    <p className="font-bold">₹{item.subtotal}</p>
                    <button
                      onClick={() => handleRemove(item.id)}
                      className="text-red-400 hover:text-red-300 text-xs mt-1 transition"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Order summary */}
            <div className="bg-gray-900 rounded-xl p-6">
              <div className="flex justify-between items-center mb-4">
                <span className="text-gray-400">Total ({cart.length} items)</span>
                <span className="text-2xl font-bold text-blue-400">₹{total.toFixed(2)}</span>
              </div>
              <button
                onClick={handlePlaceOrder}
                disabled={placing}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-medium transition disabled:opacity-50"
              >
                {placing ? 'Placing order...' : 'Place Order'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}   