import { useEffect, useState } from 'react'
import KineticGrid from '@/components/ui/kinetic-grid'
import {
  Sparkles,
  Brain,
  GraduationCap,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  Send,
  Zap,
  RotateCcw,
  BookOpen
} from 'lucide-react'
import './App.css'

const API_URL = 'https://sage-ai-of8j.onrender.com'

function App() {
  const [question, setQuestion] = useState(null)
  const [answer, setAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(false)
  const [initializing, setInitializing] = useState(true)

  const studentId = 1
  const conceptId = 1

  const getNextQuestion = async () => {
    try {
      setLoading(true)
      setFeedback(null)
      setAnswer('')

      const response = await fetch(
        `${API_URL}/api/adaptive/students/${studentId}/concepts/${conceptId}/next-question`
      )

      if (!response.ok) throw new Error('Failed to get question')

      const data = await response.json()
      setQuestion(data)
    } catch (error) {
      console.error(error)
      setFeedback({
        type: 'error',
        message: 'Could not connect to SAGE backend. Please try again.'
      })
    } finally {
      setLoading(false)
      setInitializing(false)
    }
  }

  useEffect(() => {
    getNextQuestion()
  }, [])

  const submitAnswer = async () => {
    if (!answer.trim() || !question) return

    try {
      setLoading(true)

      const response = await fetch(`${API_URL}/api/interactions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lesson_id: 1,
          concept: question.concept,
          question: question.question,
          student_answer: answer,
          correct: false,
          misconception: null,
          teacher_action: null
        })
      })

      if (!response.ok) throw new Error('Failed to submit answer')

      const data = await response.json()

      setFeedback({
        type: data.correct ? 'correct' : 'incorrect',
        message: data.correct ? 'Great job! SAGE confirmed your answer.' : 'SAGE analyzed your answer.',
        misconception: data.misconception,
        explanation: data.explanation,
        teacher_action: data.teacher_action
      })

    } catch (error) {
      console.error(error)
      setFeedback({
        type: 'error',
        message: 'Something went wrong while analyzing your answer.'
      })
    } finally {
      setLoading(false)
    }
  }

  const mastery = question?.mastery_score ?? 0

  return (
    <KineticGrid globalColor="default">
      <div className="app">

        <header className="header">
          <div className="logo">
            <div className="logo-mark">
              <Sparkles size={20} className="text-purple-300" />
            </div>
            <div>
              <h1>SAGE</h1>
              <span>AI Teacher</span>
            </div>
          </div>

          <div className="student">
            <img
              src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80"
              alt="Demo Student"
              className="avatar"
              style={{ objectFit: 'cover', borderRadius: '50%', width: '36px', height: '36px' }}
            />
            <div>
              <strong>Demo Student</strong>
              <small className="flex items-center gap-1">
                <GraduationCap size={12} /> Beginner
              </small>
            </div>
          </div>
        </header>

        <main className="main">

          <section className="welcome">
            <p className="eyebrow flex items-center justify-center gap-1.5">
              <Zap size={14} /> Adaptive Learning
            </p>
            <h2>Learn at your own pace.</h2>
            <p className="subtitle">
              SAGE understands your answers and adapts the next question to your current level.
            </p>
          </section>

          {initializing && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>SAGE is waking up...</p>
            </div>
          )}

          {!initializing && question && (
            <section className="learning-card">

              <div className="progress-row">
                <div>
                  <span className="label flex items-center gap-1">
                    <BookOpen size={12} /> Current Concept
                  </span>
                  <h3>{question.concept}</h3>
                </div>
                <div className="mastery">
                  <span>Mastery</span>
                  <strong>{question.mastery_score}%</strong>
                </div>
              </div>

              <div className="mastery-bar">
                <div className="mastery-fill" style={{ width: `${mastery}%` }}></div>
              </div>

              <div className="difficulty flex items-center gap-1">
                <Zap size={14} className="text-amber-400" /> Next Level: {question.next_difficulty.toUpperCase()}
              </div>

              <div className="question-box">
                <span className="label">Question</span>
                <h2>{question.question}</h2>
              </div>

              <div className="answer-section">
                <label htmlFor="answer">Your Answer</label>
                <textarea
                  id="answer"
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  placeholder="Type your answer here..."
                  rows="5"
                />
                <button
                  onClick={submitAnswer}
                  disabled={loading || !answer.trim()}
                  className="flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <div className="spinner" style={{ width: '16px', height: '16px' }}></div>
                      Analyzing with AI...
                    </>
                  ) : (
                    <>
                      Submit Answer <Send size={16} />
                    </>
                  )}
                </button>
              </div>

            </section>
          )}

          {feedback && (
            <section className={`feedback ${feedback.type}`}>

              <div className="feedback-title flex items-center gap-2">
                {feedback.type === 'correct' && (
                  <>
                    <CheckCircle2 size={20} className="text-emerald-400" /> Correct!
                  </>
                )}
                {feedback.type === 'incorrect' && (
                  <>
                    <RotateCcw size={20} className="text-amber-400" /> Keep Going
                  </>
                )}
                {feedback.type === 'error' && (
                  <>
                    <AlertCircle size={20} className="text-rose-400" /> Connection Problem
                  </>
                )}
              </div>

              {feedback.misconception && (
                <p>
                  <strong>🧠 What SAGE noticed:</strong> {feedback.misconception}
                </p>
              )}

              {feedback.explanation && (
                <p>
                  <strong>📖 Explanation:</strong> {feedback.explanation}
                </p>
              )}

              {feedback.teacher_action && (
                <p>
                  <strong>👨‍🏫 Next step:</strong> {feedback.teacher_action}
                </p>
              )}

              <p>{feedback.message}</p>

              {feedback.type !== 'error' && (
                <button className="next-button flex items-center justify-center gap-2" onClick={getNextQuestion}>
                  Next Question <ArrowRight size={16} />
                </button>
              )}

            </section>
          )}

        </main>

        <footer>
          <span>SAGE AI Teacher</span>
          <span>Adaptive learning powered by AI</span>
        </footer>

      </div>
    </KineticGrid>
  )
}

export default App