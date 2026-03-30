import React, { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'
import { Upload, Download, Trash2, Plus, FileSpreadsheet } from 'lucide-react'
import ResultsDisplay from './ResultsDisplay'

function BatchPrediction() {
  const [students, setStudents] = useState([
    { minutes_watched: '', clv: '', region: '0', channel: '1' },
  ])
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const addStudent = () => {
    if (students.length >= 1000) {
      toast.error('Maximum 1000 students allowed')
      return
    }
    setStudents([...students, { minutes_watched: '', clv: '', region: '0', channel: '1' }])
  }

  const removeStudent = (index) => {
    if (students.length === 1) {
      toast.error('At least one student required')
      return
    }
    setStudents(students.filter((_, i) => i !== index))
  }

  const updateStudent = (index, field, value) => {
    const updated = [...students]
    updated[index][field] = value
    setStudents(updated)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Validate all fields
    const invalid = students.some(s => !s.minutes_watched || !s.clv)
    if (invalid) {
      toast.error('Please fill in all fields')
      return
    }

    setLoading(true)

    try {
      const payload = {
        students: students.map(s => ({
          minutes_watched: parseInt(s.minutes_watched),
          clv: parseFloat(s.clv),
          region: s.region,
          channel: s.channel,
        }))
      }

      const response = await axios.post('http://localhost:8000/predict/batch', payload)
      setResults(response.data)
      toast.success(`Processed ${response.data.total} students successfully!`)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Batch prediction failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const clearAll = () => {
    setStudents([{ minutes_watched: '', clv: '', region: '0', channel: '1' }])
    setResults(null)
  }

  const exportResults = () => {
    if (!results) return

    const csv = [
      ['Minutes Watched', 'CLV', 'Region', 'Channel', 'Cluster', 'Persona'].join(','),
      ...results.predictions.map(p =>
        [p.minutes_watched, p.clv, p.region, p.channel, p.cluster, `"${p.persona}"`].join(',')
      )
    ].join('\n')

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `predictions_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-800">
          Batch Processing ({students.length} students)
        </h2>
        <div className="flex gap-2">
          <button
            onClick={clearAll}
            className="px-4 py-2 text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-all flex items-center gap-2"
          >
            <Trash2 className="w-4 h-4" />
            Clear All
          </button>
          <button
            onClick={addStudent}
            className="px-4 py-2 bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200 transition-all flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            Add Student
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="max-h-96 overflow-y-auto space-y-3 pr-2">
          {students.map((student, index) => (
            <div
              key={index}
              className="grid grid-cols-12 gap-3 items-center bg-gray-50 p-4 rounded-lg border border-gray-200"
            >
              <div className="col-span-1 text-sm font-medium text-gray-500">
                #{index + 1}
              </div>

              <div className="col-span-3">
                <input
                  type="number"
                  min="0"
                  placeholder="Minutes"
                  value={student.minutes_watched}
                  onChange={(e) => updateStudent(index, 'minutes_watched', e.target.value)}
                  className="w-full px-3 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-primary-500 outline-none"
                />
              </div>

              <div className="col-span-3">
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  placeholder="CLV ($)"
                  value={student.clv}
                  onChange={(e) => updateStudent(index, 'clv', e.target.value)}
                  className="w-full px-3 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-primary-500 outline-none"
                />
              </div>

              <div className="col-span-2">
                <select
                  value={student.region}
                  onChange={(e) => updateStudent(index, 'region', e.target.value)}
                  className="w-full px-3 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-primary-500 outline-none"
                >
                  <option value="0">US/CA/UK/AU</option>
                  <option value="1">W. Europe</option>
                  <option value="2">Rest of World</option>
                </select>
              </div>

              <div className="col-span-2">
                <select
                  value={student.channel}
                  onChange={(e) => updateStudent(index, 'channel', e.target.value)}
                  className="w-full px-3 py-2 rounded border border-gray-300 focus:ring-2 focus:ring-primary-500 outline-none"
                >
                  <option value="1">Google</option>
                  <option value="2">Facebook</option>
                  <option value="3">YouTube</option>
                  <option value="4">LinkedIn</option>
                  <option value="5">Twitter</option>
                  <option value="6">Instagram</option>
                  <option value="7">Friend</option>
                  <option value="8">Other</option>
                </select>
              </div>

              <div className="col-span-1">
                <button
                  type="button"
                  onClick={() => removeStudent(index)}
                  className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-all"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex items-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <Upload className="w-4 h-4" />
            )}
            {loading ? 'Processing...' : 'Process Batch'}
          </button>
        </div>
      </form>

      {/* Batch Results */}
      {results && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-800">Results Summary</h3>
            <button
              onClick={exportResults}
              className="px-4 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-all flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Export CSV
            </button>
          </div>

          <div className="grid grid-cols-3 gap-4 mb-4">
            {['Driven Learner', 'Passive Payer', 'Champion'].map((persona, idx) => {
              const count = results.predictions.filter(p => p.cluster === idx).length
              const percentage = ((count / results.total) * 100).toFixed(1)
              return (
                <div key={idx} className={`p-4 rounded-lg cluster-badge-${idx} border`}>
                  <div className="text-2xl font-bold">{count}</div>
                  <div className="text-sm">{persona}</div>
                  <div className="text-xs opacity-75">{percentage}%</div>
                </div>
              )
            })}
          </div>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {results.predictions.map((pred, idx) => (
              <ResultsDisplay key={idx} result={pred} compact />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default BatchPrediction