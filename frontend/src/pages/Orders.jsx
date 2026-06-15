import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

export default function Orders() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    try {
      const { data } = await api.get('/orders/')
      setOrders(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const statusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-900 text-yellow-300',
      paid: 'bg-blue-900 text-blue-300',
      shipped: 'bg-purple-900 text-purple-300',
      delivered: 'bg-green-900 text-green-300',
      cancelled: 'bg-red-900 text-red-300'
    }
    return colors[status] || 'bg-gray-800 text-gray-300'
  }

  if (loading) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
      Loading orders...
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-950 text-white px-6 py-10">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold mb-8">Your Orders</h1>

        {orders.length === 0 ? (
          <div className="text-center text-gray-400 py-20">
            <p className="text-lg mb-4">No orders yet</p>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg transition"
            >
              Start Shopping
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            {orders.map(order => (
              <div key={order.id} className="bg-gray-900 rounded-xl p-6">
                {/* Order header */}
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Order ID</p>
                    <p className="text-sm font-mono text-gray-300">{order.id}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColor(order.status)}`}>
                    {order.status.toUpperCase()}
                  </span>
                </div>

                {/* Order items */}
                <div className="space-y-2 mb-4">
                  {order.order_items.map(item => (
                    <div key={item.id} className="flex justify-between text-sm">
                      <span
                        className="text-gray-400 hover:text-blue-400 cursor-pointer transition line-clamp-1 flex-1"
                        onClick={() => navigate(`/products/${item.product_id}`)}
                        >
                        {item.product_name || item.product_id}
                        </span>
                      <span className="text-gray-500 mx-4">x{item.quantity}</span>
                      <span className="text-white">₹{item.unit_price}</span>
                    </div>
                  ))}
                </div>

                {/* Order footer */}
                <div className="border-t border-gray-800 pt-4 flex justify-between items-center">
                  <span className="text-gray-500 text-sm">
                    {order.created_at?.split('T')[0]}
                  </span>
                  <span className="text-blue-400 font-bold text-lg">
                    ₹{order.total_amount.toFixed(2)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}