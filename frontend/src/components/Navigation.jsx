import React from 'react'
import { User, Users } from 'lucide-react'

function Navigation({ activeTab, setActiveTab }) {
  return (
    <div className="flex justify-center mb-6">
      <div className="bg-white/20 backdrop-blur-md rounded-xl p-1 flex gap-1">
        <button
          onClick={() => setActiveTab('single')}
          className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
            activeTab === 'single'
              ? 'bg-white text-primary-700 shadow-lg'
              : 'text-white hover:bg-white/10'
          }`}
        >
          <User className="w-4 h-4" />
          Single Prediction
        </button>
        <button
          onClick={() => setActiveTab('batch')}
          className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
            activeTab === 'batch'
              ? 'bg-white text-primary-700 shadow-lg'
              : 'text-white hover:bg-white/10'
          }`}
        >
          <Users className="w-4 h-4" />
          Batch Processing
        </button>
      </div>
    </div>
  )
}

export default Navigation