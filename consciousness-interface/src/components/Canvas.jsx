import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { X, FileText, Code, Globe, GitBranch, Play, Download, ChevronLeft, ChevronRight } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const API_URL = 'http://localhost:8099/api'

// ── Type icons ────────────────────────────────────────────────────────────────

const TYPE_META = {
  code:     { icon: Code,      label: 'Code',     color: 'text-blue-400' },
  markdown: { icon: FileText,  label: 'Markdown', color: 'text-purple-400' },
  html:     { icon: Globe,     label: 'HTML',     color: 'text-green-400' },
  react:    { icon: Code,      label: 'React',    color: 'text-cyan-400' },
  diagram:  { icon: GitBranch, label: 'Diagram',  color: 'text-yellow-400' },
  docx:     { icon: FileText,  label: 'Document', color: 'text-orange-400' },
}

// ── Renderers ─────────────────────────────────────────────────────────────────

function CodeRenderer({ content, language }) {
  return (
    <SyntaxHighlighter
      language={language || 'text'}
      style={oneDark}
      customStyle={{ margin: 0, borderRadius: '0.5rem', fontSize: '0.8rem' }}
      showLineNumbers
    >
      {content}
    </SyntaxHighlighter>
  )
}

function MarkdownRenderer({ content }) {
  return (
    <div className="prose prose-invert prose-sm max-w-none">
      <ReactMarkdown
        components={{
          code({ inline, className, children }) {
            const lang = className?.replace('language-', '') || 'text'
            if (inline) return <code className="bg-white/10 px-1 rounded text-xs">{children}</code>
            return (
              <SyntaxHighlighter language={lang} style={oneDark} customStyle={{ fontSize: '0.75rem' }}>
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            )
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}

function HtmlRenderer({ content }) {
  const csp = "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: https:;"
  return (
    <iframe
      srcDoc={content}
      sandbox="allow-scripts"
      className="w-full h-full border-0 rounded-lg bg-white"
      style={{ minHeight: '400px' }}
      title="HTML Preview"
    />
  )
}

function DiagramRenderer({ content }) {
  // Show as preformatted text — Mermaid can be added later
  return (
    <pre className="text-xs text-gray-300 bg-black/40 rounded-lg p-4 overflow-auto whitespace-pre-wrap">
      {content}
    </pre>
  )
}

function ContentRenderer({ artifact }) {
  switch (artifact.artifact_type || artifact.type) {
    case 'code':
      return <CodeRenderer content={artifact.content} language={artifact.language} />
    case 'markdown':
      return <MarkdownRenderer content={artifact.content} />
    case 'html':
    case 'react':
      return <HtmlRenderer content={artifact.content} />
    case 'diagram':
      return <DiagramRenderer content={artifact.content} />
    default:
      return (
        <pre className="text-xs text-gray-300 whitespace-pre-wrap break-words">
          {typeof artifact.content === 'string' ? artifact.content : JSON.stringify(artifact.content, null, 2)}
        </pre>
      )
  }
}

// ── Main Canvas component ─────────────────────────────────────────────────────

function Canvas({ content, onClose }) {
  const [executing, setExecuting] = useState(false)
  const [execResult, setExecResult] = useState(null)
  const [versionIndex, setVersionIndex] = useState(0)
  const [versions, setVersions] = useState(null)
  const { user } = useAuthStore()

  // content can be: null, a raw string, or an artifact-shaped object
  const artifact = !content
    ? null
    : typeof content === 'string'
    ? { artifact_type: 'markdown', content, title: 'Preview' }
    : content

  const typeMeta = artifact ? (TYPE_META[artifact.artifact_type || artifact.type] || TYPE_META.markdown) : null
  const TypeIcon = typeMeta?.icon || FileText

  const handleExecute = async () => {
    if (!artifact?.id) return
    setExecuting(true)
    setExecResult(null)
    try {
      const res = await axios.post(`${API_URL}/artifacts/${artifact.id}/execute`)
      setExecResult(res.data.result)
    } catch (err) {
      setExecResult({ error: err.response?.data?.detail || err.message })
    } finally {
      setExecuting(false)
    }
  }

  const handleDownload = () => {
    if (!artifact?.content) return
    const blob = new Blob([artifact.content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${artifact.title || 'artifact'}.${artifact.artifact_type === 'code' ? (artifact.language || 'txt') : artifact.artifact_type || 'txt'}`
    a.click()
    URL.revokeObjectURL(url)
  }

  const canExecute = artifact?.artifact_type === 'code' && artifact?.id && user?.role === 'admin'
  const canDownload = artifact?.content

  return (
    <motion.div
      initial={{ x: 400, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: 400, opacity: 0 }}
      transition={{ type: 'spring', damping: 25 }}
      className="fixed right-0 top-0 h-full w-[480px] bg-black/70 backdrop-blur-xl border-l border-white/10 z-30 flex flex-col"
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-white/10 flex-shrink-0">
        <div className="flex items-center space-x-2">
          {typeMeta && <TypeIcon className={`w-5 h-5 ${typeMeta.color}`} />}
          <span className="font-semibold truncate max-w-[200px]">
            {artifact?.title || 'Canvas'}
          </span>
          {typeMeta && (
            <span className="text-xs bg-white/10 px-2 py-0.5 rounded text-gray-400">
              {typeMeta.label}
            </span>
          )}
          {artifact?.language && (
            <span className="text-xs bg-blue-900/40 border border-blue-700/50 px-2 py-0.5 rounded text-blue-300">
              {artifact.language}
            </span>
          )}
        </div>
        <div className="flex items-center space-x-1">
          {canExecute && (
            <button
              onClick={handleExecute}
              disabled={executing}
              className="p-1.5 hover:bg-green-600/30 text-green-400 rounded-lg transition-colors disabled:opacity-50"
              title="Execute (admin)"
            >
              <Play className="w-4 h-4" />
            </button>
          )}
          {canDownload && (
            <button
              onClick={handleDownload}
              className="p-1.5 hover:bg-white/10 text-gray-400 rounded-lg transition-colors"
              title="Download"
            >
              <Download className="w-4 h-4" />
            </button>
          )}
          <button
            onClick={onClose}
            className="p-1.5 hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Version navigation */}
      {artifact?.version && (
        <div className="flex items-center justify-between px-4 py-1.5 bg-white/5 border-b border-white/5 text-xs text-gray-500 flex-shrink-0">
          <span>Version {artifact.version}</span>
          {artifact.created_at && (
            <span>{new Date(artifact.created_at).toLocaleString()}</span>
          )}
        </div>
      )}

      {/* Content */}
      <div className="flex-1 p-4 overflow-auto">
        {artifact ? (
          <ContentRenderer artifact={artifact} />
        ) : (
          <div className="text-center text-gray-500 mt-20">
            <FileText className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p>Canvas is empty</p>
            <p className="text-xs mt-1">Code, documents, and previews will appear here</p>
          </div>
        )}
      </div>

      {/* Execution result panel */}
      {execResult && (
        <div className="border-t border-white/10 p-4 flex-shrink-0 bg-black/40 max-h-48 overflow-auto">
          <div className="text-xs font-mono text-gray-400 mb-1">Output</div>
          {execResult.error ? (
            <pre className="text-xs text-red-400 whitespace-pre-wrap">{execResult.error}</pre>
          ) : (
            <pre className="text-xs text-green-300 whitespace-pre-wrap">
              {execResult.response || JSON.stringify(execResult, null, 2)}
            </pre>
          )}
        </div>
      )}
    </motion.div>
  )
}

export default Canvas
