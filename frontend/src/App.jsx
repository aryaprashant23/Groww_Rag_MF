import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import './index.css'
import ShaderBackground from './ShaderBackground'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (queryText = null) => {
    const text = queryText || input
    if (!text.trim()) return

    const newMessages = [...messages, { role: 'user', content: text }]
    setMessages(newMessages)
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8001/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: text }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      
      setMessages([...newMessages, { role: 'assistant', content: data.answer }])
    } catch (error) {
      setMessages([...newMessages, { role: 'assistant', content: 'Sorry, I encountered an error connecting to the server. Ensure the FastAPI backend is running.' }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleClearChat = () => {
    setMessages([])
  }

  const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'short',
    day: 'numeric'
  });

  return (
    <>
      <ShaderBackground />
      <div className="app-container">
        {/* TopNavBar */}
        <header className="header">
          <div className="header-left">
            <span className="material-symbols-outlined header-icon">trending_up</span>
            <h1 className="header-title">Mutual Fund Assistant</h1>
          </div>
          <div className="header-right">
            <div className="disclaimer-badge">
              <span className="material-symbols-outlined disclaimer-icon">warning</span>
              <span className="disclaimer-text">Facts-only. No investment advice.</span>
            </div>
            <button className="clear-chat-btn" onClick={handleClearChat}>
              <span className="material-symbols-outlined clear-chat-icon">delete_sweep</span>
              Clear Chat
            </button>
          </div>
        </header>

        {/* Chat Area */}
        <main className="chat-container">
          <div className="timestamp">
            Today, {currentDate}
          </div>

          {messages.length === 0 && (
            <div className="message-wrapper">
              <div className="ai-avatar">
                <span className="material-symbols-outlined ai-avatar-icon">smart_toy</span>
              </div>
              <div className="chat-bubble-ai markdown-content">
                <p>Hello! I am the Mutual Fund Assistant. I can help you retrieve factual information from fund documents, fact sheets, and historical NAV data.</p>
                <p style={{marginTop: '0.75rem', fontSize: '14px', color: 'var(--on-surface-variant)'}}>Example queries:</p>
                <ul>
                  <li>"What is the exit load for HDFC Mid-Cap Opportunities?"</li>
                  <li>"Compare the 3-year trailing returns of Parag Parikh Flexi Cap vs Benchmark."</li>
                </ul>
              </div>
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-wrapper ${msg.role}`}>
              {msg.role === 'assistant' && (
                <div className="ai-avatar">
                  <span className="material-symbols-outlined ai-avatar-icon">smart_toy</span>
                </div>
              )}
              <div className={`markdown-content ${msg.role === 'assistant' ? 'chat-bubble-ai' : 'chat-bubble-user'}`}>
                {msg.role === 'assistant' ? (
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                ) : (
                  msg.content
                )}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message-wrapper typing-wrapper">
              <div className="ai-avatar">
                <span className="material-symbols-outlined ai-avatar-icon">smart_toy</span>
              </div>
              <div className="typing-bubble">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          )}
          <div className="chat-spacer"></div>
          <div ref={messagesEndRef} />
        </main>

        {/* Input Area */}
        <footer className="footer">
          {/* Quick Actions */}
          <div className="quick-actions">
            <button 
              className="action-btn" 
              onClick={() => handleSend("What is the NAV of Nippon India small cap?")} 
              disabled={isLoading}
            >
              Check NAV
            </button>
            <button 
              className="action-btn" 
              onClick={() => handleSend("What is the exit load for the Nippon India Small Cap fund?")} 
              disabled={isLoading}
            >
              Exit Load
            </button>
            <button 
              className="action-btn" 
              onClick={() => handleSend("Is this a good fund to invest in?")} 
              disabled={isLoading}
            >
              Subjective Query
            </button>
          </div>

          {/* Input Box */}
          <div className="input-container-inner">
            <input 
              id="chat-input" 
              className="chat-input" 
              placeholder="Ask about any mutual fund..." 
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleSend();
                }
              }}
              disabled={isLoading}
            />
            <button 
              id="send-btn" 
              className="send-btn group"
              onClick={() => handleSend()} 
              disabled={isLoading || !input.trim()}
            >
              <span className="material-symbols-outlined send-icon">send</span>
            </button>
          </div>
          
          <div className="footer-disclaimer">
            <span>AI can make mistakes. Verify important factual data.</span>
          </div>
        </footer>
      </div>
    </>
  )
}

export default App
