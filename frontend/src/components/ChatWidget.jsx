import { useState, useRef, useEffect } from 'react'
import api from '../api/axios'

function FormattedMessage({ text }) {
  const lines = text.split('\n')
  return (
    <div className="space-y-1">
      {lines.map((line, i) => {
        const formatted = line
          .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
          .replace(/\*(.*?)\*/g, '<strong>$1</strong>')

        // Numbered or bullet product item
        if (/^[\*\-\d]+[\.\)]?\s/.test(line.trim())) {
          const clean = line.replace(/^[\*\-\d]+[\.\)]\s*/, '').trim()
          const formattedClean = clean
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')

          // Check if it has price info inline
          if (clean.includes('Price:') || clean.includes('₹')) {
            const parts = clean.split('|')
            return (
              <div key={i} className="mt-2 bg-gray-900 rounded-lg p-2 border border-gray-700">
                {parts.map((part, j) => {
                  const t = part.trim()
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.*?)\*/g, '<strong>$1</strong>')
                  if (j === 0) return (
                    <p key={j} className="text-white text-xs font-medium mb-1"
                      dangerouslySetInnerHTML={{ __html: t }} />
                  )
                  if (t.startsWith('Price:') || t.includes('₹')) return (
                    <span key={j} className="text-blue-400 text-xs font-bold mr-2"
                      dangerouslySetInnerHTML={{ __html: t }} />
                  )
                  if (t.startsWith('Rating:')) return (
                    <span key={j} className="text-yellow-400 text-xs mr-2"
                      dangerouslySetInnerHTML={{ __html: t }} />
                  )
                  if (t.startsWith('ID:')) return (
                    <span key={j} className="text-gray-600 text-xs"
                      dangerouslySetInnerHTML={{ __html: t }} />
                  )
                  return <span key={j} className="text-xs mr-2"
                    dangerouslySetInnerHTML={{ __html: t }} />
                })}
              </div>
            )
          }

          return (
            <div key={i} className="mt-1 ml-1 text-xs"
              dangerouslySetInnerHTML={{ __html: `• ${formattedClean}` }} />
          )
        }

        // Price line standalone
        if (line.trim().startsWith('Price:')) {
          return (
            <div key={i} className="flex flex-wrap gap-2 text-xs mt-1 ml-2">
              {line.split('|').map((part, j) => {
                const t = part.trim()
                if (t.startsWith('Price:')) return (
                  <span key={j} className="text-blue-400 font-bold">{t}</span>
                )
                if (t.startsWith('Rating:')) return (
                  <span key={j} className="text-yellow-400">{t}</span>
                )
                if (t.startsWith('ID:')) return (
                  <span key={j} className="text-gray-600 text-xs">{t}</span>
                )
                return <span key={j}>{t}</span>
              })}
            </div>
          )
        }

        if (!line.trim()) return <div key={i} className="h-1" />

        return (
          <p key={i} className="text-xs leading-relaxed"
            dangerouslySetInnerHTML={{ __html: formatted }} />
        )
      })}
    </div>
  )
}

export default function ChatWidget() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hi! I\'m your AI shopping assistant 🛍️ Ask me to find products, compare items, or add things to your cart!' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', text: userMessage }])
    setLoading(true)

    try {
      const { data } = await api.post('/chat/', { message: userMessage })
      setMessages(prev => [...prev, { role: 'assistant', text: data.response }])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: 'Sorry, something went wrong. Please try again.'
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Chat window */}
      {open && (
        <div className="mb-4 w-80 bg-gray-900 rounded-2xl shadow-2xl border border-gray-700 flex flex-col overflow-hidden"
          style={{ height: '480px' }}>

          {/* Header */}
          <div className="bg-blue-600 px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-lg">🤖</span>
              <div>
                <p className="text-white text-sm font-medium">AI Shopping Assistant</p>
                <p className="text-blue-200 text-xs">Powered by Gemini + RAG</p>
              </div>
            </div>
            <button
              onClick={() => setOpen(false)}
              className="text-white hover:text-blue-200 transition text-lg"
            >
              ✕
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] px-3 py-2 rounded-xl text-sm ${
                    msg.role === 'user'
                        ? 'bg-blue-600 text-white rounded-br-none'
                        : 'bg-gray-800 text-gray-200 rounded-bl-none'
                    }`}>
                    <FormattedMessage text={msg.text} />
                    </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-800 text-gray-400 px-3 py-2 rounded-xl text-sm rounded-bl-none">
                  Thinking...
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="p-3 border-t border-gray-700 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me anything..."
              disabled={loading}
              className="flex-1 bg-gray-800 text-white text-sm px-3 py-2 rounded-lg border border-gray-700 focus:outline-none focus:border-blue-500 disabled:opacity-50"
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg transition disabled:opacity-50"
            >
              ➤
            </button>
          </div>
        </div>
      )}

      {/* Toggle button */}
      <button
        onClick={() => setOpen(!open)}
        className="bg-blue-600 hover:bg-blue-700 text-white w-14 h-14 rounded-full shadow-lg flex items-center justify-center text-2xl transition hover:scale-110"
      >
        {open ? '✕' : '🤖'}
      </button>
    </div>
  )
}