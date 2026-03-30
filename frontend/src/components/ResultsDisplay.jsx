import React from 'react'
import { User, DollarSign, Clock, MapPin, Radio, Award } from 'lucide-react'

const PERSONA_DETAILS = {
  0: {
    name: 'The Driven Learner',
    emoji: '🎯',
    color: 'emerald',
    description: 'Highly engaged students who consume lots of content but generate lower revenue. Focus on upselling premium courses.',
    traits: ['High watch time', 'Cost-conscious', 'Self-motivated'],
  },
  1: {
    name: 'The Passive Payer',
    emoji: '💤',
    color: 'amber',
    description: 'Students who pay but rarely engage. At risk of churning. Re-engagement campaigns recommended.',
    traits: ['Low engagement', 'Recurring revenue', 'Needs motivation'],
  },
  2: {
    name: 'The Champion',
    emoji: '🏆',
    color: 'violet',
    description: 'Your most valuable customers. High engagement and high CLV. VIP treatment and referral programs.',
    traits: ['Power user', 'High value', 'Brand advocate'],
  },
}

function ResultsDisplay({ result, compact = false }) {
  const persona = PERSONA_DETAILS[result.cluster]

  if (compact) {
    return (
      <div className={`flex items-center justify-between p-3 rounded-lg border cluster-badge-${result.cluster}`}>
        <div className="flex items-center gap-3">
          <span className="text-2xl">{persona.emoji}</span>
          <div>
            <div className="font-semibold text-sm">{persona.name}</div>
            <div className="text-xs opacity-75">Cluster {result.cluster}</div>
          </div>
        </div>
        <div className="text-right text-sm">
          <div>{result.minutes_watched.toLocaleString()} min</div>
          <div>${result.clv.toFixed(2)}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="animate-slide-up">
      <div className={`rounded-2xl p-6 border-2 bg-gradient-to-br from-${persona.color}-50 to-white border-${persona.color}-200`}>
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <div className={`w-20 h-20 rounded-full bg-${persona.color}-100 flex items-center justify-center text-4xl shadow-inner`}>
            {persona.emoji}
          </div>
          <div>
            <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium bg-${persona.color}-100 text-${persona.color}-800 mb-2`}>
              <Award className="w-4 h-4" />
              Cluster {result.cluster}
            </div>
            <h3 className={`text-2xl font-bold text-${persona.color}-900`}>
              {persona.name}
            </h3>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <StatCard 
            icon={<Clock className="w-5 h-5" />}
            label="Minutes Watched"
            value={result.minutes_watched.toLocaleString()}
            color={persona.color}
          />
          <StatCard 
            icon={<DollarSign className="w-5 h-5" />}
            label="Lifetime Value"
            value={`$${result.clv.toFixed(2)}`}
            color={persona.color}
          />
          <StatCard 
            icon={<MapPin className="w-5 h-5" />}
            label="Region"
            value={result.region}
            color={persona.color}
          />
          <StatCard 
            icon={<Radio className="w-5 h-5" />}
            label="Channel"
            value={result.channel}
            color={persona.color}
          />
        </div>

        {/* Description */}
        <div className={`p-4 rounded-xl bg-${persona.color}-100/50 border border-${persona.color}-200`}>
          <p className="text-gray-700 mb-3">{persona.description}</p>
          <div className="flex flex-wrap gap-2">
            {persona.traits.map((trait, idx) => (
              <span 
                key={idx}
                className={`px-3 py-1 rounded-full text-xs font-medium bg-${persona.color}-200 text-${persona.color}-800`}
              >
                {trait}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon, label, value, color }) {
  return (
    <div className={`p-4 rounded-xl bg-${color}-50 border border-${color}-100`}>
      <div className={`flex items-center gap-2 text-${color}-600 mb-2`}>
        {icon}
        <span className="text-xs font-medium uppercase tracking-wide">{label}</span>
      </div>
      <div className="text-xl font-bold text-gray-800">{value}</div>
    </div>
  )
}

export default ResultsDisplay