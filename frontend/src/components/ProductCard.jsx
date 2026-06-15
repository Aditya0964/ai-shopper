export default function ProductCard({ product, onClick }) {
  return (
    <div
      onClick={onClick}
      className="bg-gray-900 rounded-xl overflow-hidden cursor-pointer hover:scale-105 transition-transform duration-200 border border-gray-800 hover:border-blue-500"
    >
      {/* Image */}
      <div className="h-48 bg-gray-800 flex items-center justify-center overflow-hidden">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="h-full w-full object-contain p-2"
            onError={(e) => { e.target.src = 'https://via.placeholder.com/200x200?text=No+Image' }}
          />
        ) : (
          <span className="text-gray-600 text-sm">No image</span>
        )}
      </div>

      {/* Info */}
      <div className="p-4">
        <h3 className="text-white text-sm font-medium line-clamp-2 mb-2 min-h-[2.5rem]">
          {product.name}
        </h3>

        <div className="flex items-center justify-between">
          <span className="text-blue-400 font-bold text-lg">₹{product.price}</span>
          <span className="text-yellow-400 text-sm">⭐ {product.avg_rating}</span>
        </div>

        <div className="mt-2 text-xs text-gray-500">
          {product.category?.name}
        </div>
      </div>
    </div>
  )
}