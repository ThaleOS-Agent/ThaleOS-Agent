import React from 'react'
import { motion } from 'framer-motion'
import { X, FileText } from 'lucide-react'

function Canvas({ content, onClose }) {
  return (
    <motion.div
      initial={{ x: 400, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: 400, opacity: 0 }}
      transition={{ type: 'spring', damping: 25 }}
      className="fixed right-0 top-0 h-full w-96 bg-black/60 backdrop-blur-xl border-l border-white/10 z-30 flex flex-col"
    >
      <div className="flex items-center justify-between p-4 border-b border-white/10">
        <div className="flex items-center space-x-2">
          <FileText className="w-5 h-5 text-quantum-400" />
          <span className="font-semibold">Canvas</span>
        </div>
        <button onClick={onClose} className="p-1 hover:bg-white/10 rounded-lg transition-colors">
          <X className="w-5 h-5" />
        </button>
      </div>
      <div className="flex-1 p-4 overflow-auto">
        {content ? (
          <div className="prose prose-invert max-w-none text-sm">
            <pre className="whitespace-pre-wrap">{JSON.stringify(content, null, 2)}</pre>
          </div>
        ) : (
          <div className="text-center text-gray-500 mt-20">
            <FileText className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p>Canvas is empty</p>
            <p className="text-xs mt-1">Documents and previews will appear here</p>
          </div>
        )}
      </div>
    </motion.div>
  )
}

export default Canvas
