import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { FileText, Plus, Download } from 'lucide-react'
import { useThaleOSStore } from '../store/thaleosStore'

const docTypes = ['email', 'report', 'proposal', 'contract', 'presentation', 'social_post']

function Documents({ onCanvasOpen }) {
  const { documents, fetchDocuments, createDocument } = useThaleOSStore()
  const [creating, setCreating] = useState(false)
  const [selectedType, setSelectedType] = useState('report')

  useEffect(() => {
    fetchDocuments()
  }, [])

  const handleCreate = async () => {
    setCreating(true)
    try {
      const result = await createDocument(selectedType, '', {})
      if (onCanvasOpen) onCanvasOpen(result)
    } finally {
      setCreating(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-display font-bold">Documents</h1>
        <div className="flex items-center space-x-2">
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-quantum-500"
          >
            {docTypes.map(t => <option key={t} value={t}>{t.replace('_', ' ')}</option>)}
          </select>
          <button
            onClick={handleCreate}
            disabled={creating}
            className="flex items-center space-x-2 px-4 py-2 bg-quantum-600 hover:bg-quantum-500 rounded-lg text-sm transition-colors disabled:opacity-50"
          >
            <Plus className="w-4 h-4" />
            <span>{creating ? 'Creating...' : 'New Document'}</span>
          </button>
        </div>
      </div>

      {documents.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <FileText className="w-16 h-16 mx-auto mb-4 opacity-20" />
          <p className="text-lg">No documents yet</p>
          <p className="text-sm mt-1">Create your first document using the SCRIBE agent</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          {documents.map(doc => (
            <div key={doc.document_id} className="bg-black/30 backdrop-blur-lg rounded-xl p-4 border border-white/10">
              <FileText className="w-8 h-8 text-quantum-400 mb-2" />
              <div className="font-medium">{doc.doc_type}</div>
              <div className="text-xs text-gray-400">{doc.document_id}</div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  )
}

export default Documents
