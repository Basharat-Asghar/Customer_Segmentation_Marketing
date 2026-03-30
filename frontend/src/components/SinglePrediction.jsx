import React, { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'
import { Send, RotateCcw, MapPin, Radio } from 'lucide-react'
import ResultsDisplay from './ResultsDisplay'

const REGIONS = [
  { value: '0', label: 'US/CA/UK/AU' },
  { value: '1', label: 'W. Europe' },
  { value: '2', label: 'Rest of World' },
]

const CHANNELS = [
  { value: '1', label: 'Google' },
  { value: '2', label: 'Facebook' },
  { value: '3', label: 'YouTube' },
  { value: '4', label: 'LinkedIn' },
  { value: '5', label: 'Twitter' },
  { value: '6', label: 'Instagram' },
  { value: '7', label: 'Friend' },
  { value: '8', label: 'Other' },
]

function SinglePrediction() {
  const [formData, setFormData] = useState({
    minutes_watched: '',
    clv: '',
    region: '0',
    channel: '1',
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/predict', {
        minutes_watched: parseInt(formData.minutes_watched),
        clv: parseFloat(formData.clv),
        region: formData.region,
        channel: formData.channel,
      })

      setResult(response.data)
      toast.success('Prediction successful!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Prediction failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFormData({
      minutes_watched: '',
      clv: '',
      region: '0',
      channel: '1',
    })
    setResult(null)
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Minutes Watched */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Minutes Watched <span className="text-red-500">*</span>
            </label>
            <input
              type="number"
              min="0"
              required
              placeholder="e.g., 1500"
              value={formData.minutes_watched}
              onChange={(e) => setFormData({ ...formData, minutes_watched: e.target.value })}
              className="input-field"
            />
            <p className="text-xs text-gray-500">Total minutes watched on platform</p>
          </div>

          {/* CLV */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Customer Lifetime Value ($) <span className="text-red-500">*</span>
            </label>
            <input
              type="number"
              min="0"
              step="0.01"
              required
              placeholder="e.g., 167.50"
              value={formData.clv}
              onChange={(e) => setFormData({ ...formData, clv: e.target.value })}
              className="input-field"
            />
            <p className="text-xs text-gray-500">Total revenue from customer</p>
          </div>

          {/* Region */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
              <MapPin className="w-4 h-4" />
              Region
            </label>
            <select
              value={formData.region}
              onChange={(e) => setFormData({ ...formData, region: e.target.value })}
              className="input-field"
            >
              {REGIONS.map((r) => (
                <option key={r.value} value={r.value}>{r.label}</option>
              ))}
            </select>
          </div>

          {/* Channel */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
              <Radio className="w-4 h-4" />
              Acquisition Channel
            </label>
            <select
              value={formData.channel}
              onChange={(e) => setFormData({ ...formData, channel: e.target.value })}
              className="input-field"
            >
              {CHANNELS.map((c) => (
                <option key={c.value} value={c.value}>{c.label}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex items-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            {loading ? 'Processing...' : 'Get Prediction'}
          </button>

          <button
            type="button"
            onClick={handleReset}
            className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-all flex items-center gap-2"
          >
            <RotateCcw className="w-4 h-4" />
            Reset
          </button>
        </div>
      </form>

      {/* Results */}
      {result && <ResultsDisplay result={result} />}
    </div>
  )
}

export default SinglePrediction