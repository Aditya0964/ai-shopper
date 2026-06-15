import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'
import ProductCard from '../components/ProductCard'

export default function Home() {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [selectedCategory, setSelectedCategory] = useState('')
  const [maxPrice, setMaxPrice] = useState('')
  const [search, setSearch] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchCategories()
  }, [])

  useEffect(() => {
    fetchProducts()
  }, [page, selectedCategory, maxPrice])

  const fetchCategories = async () => {
    try {
      const { data } = await api.get('/categories/')
      setCategories(data)
    } catch (err) {
      console.error(err)
    }
  }

  const fetchProducts = async () => {
    setLoading(true)
    try {
      let url = `/products/?page=${page}&limit=20`
      if (selectedCategory) url += `&category_id=${selectedCategory}`
      if (maxPrice) url += `&max_price=${maxPrice}`
      const { data } = await api.get(url)
      setProducts(data.products)
      setTotalPages(data.total_pages)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCategoryChange = (categoryId) => {
    setSelectedCategory(categoryId)
    setPage(1)
  }

  const handlePriceFilter = (e) => {
    e.preventDefault()
    setPage(1)
    fetchProducts()
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <div className="bg-gray-900 px-6 py-8 text-center">
        <h1 className="text-3xl font-bold mb-2">AI-Powered Shopping</h1>
        <p className="text-gray-400">Browse products or use the AI chat to find exactly what you need</p>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Filters */}
        <div className="flex flex-wrap gap-4 mb-8 items-center">
          {/* Category filter */}
          <select
            value={selectedCategory}
            onChange={(e) => handleCategoryChange(e.target.value)}
            className="bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-700 focus:outline-none focus:border-blue-500"
          >
            <option value="">All Categories</option>
            {categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>

          {/* Price filter */}
          <form onSubmit={handlePriceFilter} className="flex gap-2">
            <input
              type="number"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              placeholder="Max price ₹"
              className="bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-700 focus:outline-none focus:border-blue-500 w-36"
            />
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition"
            >
              Filter
            </button>
            {(selectedCategory || maxPrice) && (
              <button
                type="button"
                onClick={() => { setSelectedCategory(''); setMaxPrice(''); setPage(1); }}
                className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg transition"
              >
                Clear
              </button>
            )}
          </form>
        </div>

        {/* Products grid */}
        {loading ? (
          <div className="text-center text-gray-400 py-20">Loading products...</div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {products.map(product => (
                <ProductCard
                  key={product.id}
                  product={product}
                  onClick={() => navigate(`/products/${product.id}`)}
                />
              ))}
            </div>

            {/* Pagination */}
            <div className="flex justify-center gap-2 mt-10">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded-lg disabled:opacity-40 transition"
              >
                Previous
              </button>
              <span className="bg-gray-800 px-4 py-2 rounded-lg text-gray-400">
                Page {page} of {totalPages}
              </span>
              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded-lg disabled:opacity-40 transition"
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}