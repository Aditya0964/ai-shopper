import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api/axios'
import useAuthStore from '../store/authStore'

function ReviewsSection({ productId }) {
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchReviews()
  }, [productId])

  const fetchReviews = async () => {
    try {
      const { data } = await api.get(`/products/${productId}/reviews`)
      setReviews(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="mt-10 text-gray-400 text-sm">Loading reviews...</div>
  if (reviews.length === 0) return <div className="mt-10 text-gray-400 text-sm">No reviews yet.</div>

  return (
    <div className="mt-10 bg-gray-900 rounded-xl p-6">
      <h2 className="text-lg font-semibold mb-4">Customer Reviews ({reviews.length})</h2>
      <div className="space-y-4">
        {reviews.map(review => (
          <div key={review.id} className="border-b border-gray-800 pb-4">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-yellow-400 text-sm">
                {'⭐'.repeat(review.rating)}
              </span>
              <span className="text-gray-500 text-xs">{review.created_at?.split('T')[0]}</span>
            </div>
            <p className="text-gray-400 text-sm">{review.body}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function ProductDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [quantity, setQuantity] = useState(1)
  const [adding, setAdding] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchProduct()
  }, [id])

  const fetchProduct = async () => {
    try {
      const { data } = await api.get(`/products/${id}`)
      setProduct(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    setAdding(true)
    try {
      await api.post(`/cart/?product_id=${product.id}&quantity=${quantity}`)
      setMessage('Added to cart successfully!')
      setTimeout(() => setMessage(''), 3000)
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Failed to add to cart')
    } finally {
      setAdding(false)
    }
  }

  if (loading) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
      Loading...
    </div>
  )

  if (!product) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center text-white">
      Product not found
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-950 text-white px-6 py-10">
      <div className="max-w-5xl mx-auto">
        <button
          onClick={() => navigate(-1)}
          className="text-gray-400 hover:text-white mb-6 flex items-center gap-2 transition"
        >
          ← Back
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          {/* Image */}
          <div className="bg-gray-900 rounded-xl p-6 flex items-center justify-center min-h-64">
            {product.image_url ? (
              <img
                src={product.image_url}
                alt={product.name}
                className="max-h-80 object-contain"
                onError={(e) => { e.target.src = 'https://via.placeholder.com/300x300?text=No+Image' }}
              />
            ) : (
              <span className="text-gray-600">No image available</span>
            )}
          </div>

          {/* Details */}
          <div className="flex flex-col gap-4">
            <span className="text-blue-400 text-sm">{product.category?.name}</span>
            <h1 className="text-2xl font-bold">{product.name}</h1>

            <div className="flex items-center gap-4">
              <span className="text-3xl font-bold text-blue-400">₹{product.price}</span>
              <span className="text-yellow-400">⭐ {product.avg_rating}</span>
            </div>

            <div className="text-sm text-gray-400">
              {product.stock > 0
                ? <span className="text-green-400">✓ In Stock ({product.stock} available)</span>
                : <span className="text-red-400">Out of Stock</span>
              }
            </div>

            {/* Quantity */}
            <div className="flex items-center gap-3">
              <span className="text-gray-400 text-sm">Quantity:</span>
              <button
                onClick={() => setQuantity(q => Math.max(1, q - 1))}
                className="bg-gray-800 hover:bg-gray-700 w-8 h-8 rounded-lg transition"
              >
                -
              </button>
              <span className="w-8 text-center">{quantity}</span>
              <button
                onClick={() => setQuantity(q => Math.min(product.stock, q + 1))}
                className="bg-gray-800 hover:bg-gray-700 w-8 h-8 rounded-lg transition"
              >
                +
              </button>
            </div>

            {/* Add to cart */}
            {message && (
              <div className={`px-4 py-2 rounded-lg text-sm ${message.includes('success') ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`}>
                {message}
              </div>
            )}

            <button
              onClick={handleAddToCart}
              disabled={adding || product.stock === 0}
              className="bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-medium transition disabled:opacity-50"
            >
              {adding ? 'Adding...' : '🛒 Add to Cart'}
            </button>
          </div>
        </div>

        {/* Description */}
        {product.description && (
          <div className="mt-10 bg-gray-900 rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4">About this product</h2>
            <p className="text-gray-400 text-sm leading-relaxed whitespace-pre-line">
              {product.description}
            </p>
          </div>
        )}
      </div>

      {/* Reviews */}
      <ReviewsSection productId={id} />
    </div>
  )
}