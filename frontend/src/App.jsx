import React, { useState } from 'react'
import { Brain, Users, BarChart3, Sparkles } from 'lucide-react'
import SinglePrediction from './components/SinglePrediction'
import BatchPrediction from './components/BatchPrediction'
import Navigation from './components/Navigation'

function App() {
  const [activeTab, setActiveTab] = useState('single')

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8 animate-fade-in">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-white rounded-2xl shadow-lg">
              <Brain className="w-10 h-10 text-primary-600" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white drop-shadow-lg">
              SegmentIQ
            </h1>
          </div>
          <p className="text-white/90 text-lg max-w-2xl mx-auto">
            AI-powered customer segmentation for online learning platforms. 
            Discover behavioral personas using engagement and lifetime value data.
          </p>
        </header>

        {/* Persona Legend */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 animate-slide-up">
          <PersonaCard 
            cluster={0}
            title="🎯 The Driven Learner"
            description="High engagement, Low CLV"
            color="emerald"
          />
          <PersonaCard 
            cluster={1}
            title="💤 The Passive Payer"
            description="Low engagement, Mid CLV"
            color="amber"
          />
          <PersonaCard 
            cluster={2}
            title="🏆 The Champion"
            description="High engagement, High CLV"
            color="violet"
          />
        </div>

        {/* Navigation */}
        <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />

        {/* Main Content */}
        <main className="glass-panel rounded-2xl shadow-2xl p-6 md:p-8 animate-slide-up">
          {activeTab === 'single' ? <SinglePrediction /> : <BatchPrediction />}
        </main>

        {/* Footer */}
        <footer className="text-center text-white/70 mt-8 text-sm">
          <p>Powered by K-Means Clustering • FastAPI • React</p>
        </footer>
      </div>
    </div>
  )
}

function PersonaCard({ cluster, title, description, color }) {
  const colors = {
    emerald: 'from-emerald-400 to-emerald-600',
    amber: 'from-amber-400 to-amber-600',
    violet: 'from-violet-400 to-violet-600',
  }

  return (
    <div className="persona-card glass-panel rounded-xl p-6 text-center">
      <div className={`w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br ${colors[color]} flex items-center justify-center shadow-lg`}>
        <span className="text-2xl font-bold text-white">{cluster}</span>
      </div>
      <h3 className="font-bold text-gray-800 mb-1">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  )
}

export default App